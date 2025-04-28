#include "yuhui_mppt.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"
#include "esphome/components/sensor/sensor.h"

namespace esphome {
namespace yuhui {

static const char *TAG = "yuhui_mppt";

void YuhuiMPPT::setup() {
  // 初始化Modbus
  this->baud_rate_ = 9600;
}

void YuhuiMPPT::loop() {
  if (this->awaiting_response_ && (millis() - this->last_send_time_ > this->rx_timeout_)) {
    ESP_LOGW(TAG, "Response timeout, sending next command");
    this->awaiting_response_ = false;
    this->process_send_queue_();
  }
}

void YuhuiMPPT::update() {
  // 在 update 方法中调用 send_query_command
  this->send_query_command();
}

uint8_t calculate_checksum(const uint8_t *data, size_t len) {
  uint16_t sum = 0;
  for (size_t i = 0; i < len; i++) {
    sum += data[i];
  }
  return sum & 0xFF;  // 取低字节
}

void YuhuiMPPT::send_query_command() {
  std::vector<uint8_t> data = {this->device_address_, 0xB3, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00};
  data[7] = calculate_checksum(data.data(), 7);

  this->send_queue_.push(data);
  this->process_send_queue_();
}

void YuhuiMPPT::send_control_command(uint8_t control_code) {
  std::vector<uint8_t> data = {this->device_address_, 0xC0, control_code, 0x00, 0x00, 0x00, 0x00, 0x00};
  data[7] = calculate_checksum(data.data(), 7);

  this->send_queue_.push(data);
  this->process_send_queue_();
}

void YuhuiMPPT::send_parameter_command(uint8_t parameter_code, uint32_t parameter_value, uint8_t data_length) {
  std::vector<uint8_t> data = {this->device_address_, 0xD0, parameter_code, 0x00, 0x00, 0x00, 0x00, 0x00};
  
  if (data_length == 1) {
    data[6] = (parameter_value & 0xFF);
  } else if (data_length == 2) {
    data[5] = (parameter_value >> 8) & 0xFF;
    data[6] = (parameter_value & 0xFF);
  } else if (data_length == 4) {
    data[3] = (parameter_value >> 24) & 0xFF;
    data[4] = (parameter_value >> 16) & 0xFF;
    data[5] = (parameter_value >> 8) & 0xFF;
    data[6] = (parameter_value & 0xFF);
  }

  data[7] = calculate_checksum(data.data(), 7);

  this->send_queue_.push(data);
  this->process_send_queue_();
}

void YuhuiMPPT::send_clock_calibration_command() {
  time_t now = time(nullptr);
  struct tm *timeinfo = localtime(&now);

  uint8_t year = (timeinfo->tm_year + 1900) % 100;
  uint8_t month = timeinfo->tm_mon + 1;
  uint8_t day = timeinfo->tm_mday;
  uint8_t hour = timeinfo->tm_hour;
  uint8_t minute = timeinfo->tm_min;

  std::vector<uint8_t> data = {this->device_address_, 0xDF, year, month, day, hour, minute};
  uint8_t checksum = calculate_checksum(data.data(), 7);
  data.push_back(checksum);

  this->send_queue_.push(data);
  this->process_send_queue_();
}

void YuhuiMPPT::process_send_queue_() {
  if (this->awaiting_response_ || this->send_queue_.empty()) {
    return;
  }

  std::vector<uint8_t> data = this->send_queue_.front();
  this->send_queue_.pop();

  this->send_raw_no_crc(data);
  this->awaiting_response_ = true;
  this->last_send_time_ = millis();
  ESP_LOGD(TAG, "Sent command: %s", format_hex_pretty(&data.front(), data.size()).c_str());
}

void YuhuiMPPT::on_modbus_raw_data(const std::vector<uint8_t> &data) {
  this->awaiting_response_ = false;
  this->process_send_queue_();

  if (data.size() < 37) {
    //ESP_LOGW(TAG, "Received data size is too small, expected at least 37 bytes, got %d", data.size());
    return;
  }

  uint8_t address = data[0];
  uint8_t command = data[1];
  uint8_t control_code = data[2];
  uint8_t status = data[3];
  uint8_t charging_status_value = data[4];
  uint8_t control_status = data[5];
  uint16_t pv_voltage = (data[6] << 8) | data[7];
  uint16_t battery_voltage = (data[8] << 8) | data[9];
  uint16_t charging_current = (data[10] << 8) | data[11];
  uint16_t internal_temperature = (data[12] << 8) | data[13];
  uint16_t external_temperature = (data[16] << 8) | data[17];
  uint32_t daily_energy = (data[20] << 24) | (data[21] << 16) | (data[22] << 8) | data[23];
  uint32_t total_energy = (data[24] << 24) | (data[25] << 16) | (data[26] << 8) | data[27];
  uint8_t checksum = data[36];

  // 计算校验和
  uint8_t calculated_checksum = calculate_checksum(data.data(), 36);

  if (calculated_checksum != checksum) {
    ESP_LOGW(TAG, "Checksum mismatch: expected 0x%02X, got 0x%02X", calculated_checksum, checksum);
    return;
  }

  // 校验设备地址
  if (address != this->device_address_) {
    ESP_LOGW(TAG, "Received data from unexpected device address: 0x%02X", address);
    return;
  }

  // 忽略控制命令的返回数据
  if (command == 0xC0) {
    ESP_LOGD(TAG, "Received control command response, ignoring");
    return;
  }

  if (command == 0xB3 && control_code == 0x01) {
    ESP_LOGD(TAG, "Received command 0xB3: Query real-time data");

    // 解析运行状态
    bool running_status = status & 0x01;
    std::string running_status_str = running_status ? "Error" : "Normal";
    std::string battery_status = (status & 0x02) ? "Over-discharge protection" : "Normal";
    bool fan_status = status & 0x04;
    std::string fan_status_str = fan_status ? "Fan fault" : "Normal";
    bool temperature_status = status & 0x08;
    std::string temperature_status_str = temperature_status ? "Over-temperature protection" : "Normal";
    bool dc_output_status = status & 0x10;
    std::string dc_output_status_str = dc_output_status ? "DC output short-circuit protection" : "Normal";
    bool internal_temperature1_status = status & 0x20;
    std::string internal_temperature1_status_str = internal_temperature1_status ? "Fault" : "Normal";
    bool internal_temperature2_status = status & 0x40;
    std::string internal_temperature2_status_str = internal_temperature2_status ? "Fault" : "Normal";
    bool external_temperature1_status = status & 0x80;
    std::string external_temperature1_status_str = external_temperature1_status ? "Fault" : "Normal";
    
    ESP_LOGD(TAG, "Running status: %s", running_status_str.c_str());
    ESP_LOGD(TAG, "Battery status: %s", battery_status.c_str());
    ESP_LOGD(TAG, "Fan status: %s", fan_status_str.c_str());
    ESP_LOGD(TAG, "Temperature status: %s", temperature_status_str.c_str());
    ESP_LOGD(TAG, "DC output status: %s", dc_output_status_str.c_str());
    ESP_LOGD(TAG, "Internal temperature 1 status: %s", internal_temperature1_status_str.c_str());
    ESP_LOGD(TAG, "Internal temperature 2 status: %s", internal_temperature2_status_str.c_str());
    ESP_LOGD(TAG, "External temperature 1 status: %s", external_temperature1_status_str.c_str());

    // 更新传感器状态
    if (this->running_status_text_sensor_ != nullptr)
      this->running_status_text_sensor_->publish_state(running_status_str);
    if (this->battery_status_text_sensor_ != nullptr)
      this->battery_status_text_sensor_->publish_state(battery_status);
    if (this->fan_status_text_sensor_ != nullptr)
      this->fan_status_text_sensor_->publish_state(fan_status_str);
    if (this->temperature_status_text_sensor_ != nullptr)
      this->temperature_status_text_sensor_->publish_state(temperature_status_str);
    if (this->dc_output_status_text_sensor_ != nullptr)
      this->dc_output_status_text_sensor_->publish_state(dc_output_status_str);
    if (this->internal_temperature1_status_text_sensor_ != nullptr)
      this->internal_temperature1_status_text_sensor_->publish_state(internal_temperature1_status_str);
    if (this->internal_temperature2_status_text_sensor_ != nullptr)
      this->internal_temperature2_status_text_sensor_->publish_state(internal_temperature2_status_str);
    if (this->external_temperature1_status_text_sensor_ != nullptr)
      this->external_temperature1_status_text_sensor_->publish_state(external_temperature1_status_str);

    // 解析充电状态
    bool charging_status = charging_status_value & 0x01;
    bool equalizing_charge = charging_status_value & 0x02;
    bool tracking = charging_status_value & 0x04;
    bool floating_charge = charging_status_value & 0x08;
    bool charging_current_limit = charging_status_value & 0x10;
    bool charging_derating = charging_status_value & 0x20;
    bool remote_control_disable_charging = charging_status_value & 0x40;
    bool pv_overvoltage = charging_status_value & 0x80;

    ESP_LOGD(TAG, "Charging status: %s", charging_status ? "Charging" : "Not charging");
    ESP_LOGD(TAG, "Equalizing charge: %s", equalizing_charge ? "Active" : "Inactive");
    ESP_LOGD(TAG, "Tracking: %s", tracking ? "Active" : "Inactive");
    ESP_LOGD(TAG, "Floating charge: %s", floating_charge ? "Active" : "Inactive");
    ESP_LOGD(TAG, "Charging current limit: %s", charging_current_limit ? "Active" : "Inactive");
    ESP_LOGD(TAG, "Charging derating: %s", charging_derating ? "Active" : "Inactive");
    ESP_LOGD(TAG, "Remote control disable charging: %s", remote_control_disable_charging ? "Active" : "Inactive");
    ESP_LOGD(TAG, "PV overvoltage: %s", pv_overvoltage ? "Active" : "Inactive");

    // 更新充电状态传感器
    if (this->charging_status_sensor_ != nullptr)
      this->charging_status_sensor_->publish_state(charging_status);
    if (this->equalizing_charge_sensor_ != nullptr)
      this->equalizing_charge_sensor_->publish_state(equalizing_charge);
    if (this->tracking_sensor_ != nullptr)
      this->tracking_sensor_->publish_state(tracking);
    if (this->floating_charge_sensor_ != nullptr)
      this->floating_charge_sensor_->publish_state(floating_charge);
    if (this->charging_current_limit_sensor_ != nullptr)
      this->charging_current_limit_sensor_->publish_state(charging_current_limit);
    if (this->charging_derating_sensor_ != nullptr)
      this->charging_derating_sensor_->publish_state(charging_derating);
    if (this->remote_control_disable_charging_sensor_ != nullptr) 
      this->remote_control_disable_charging_sensor_->publish_state(remote_control_disable_charging);
    if (this->disable_charge_switch_ != nullptr)
      this->disable_charge_switch_->publish_state(remote_control_disable_charging);
    if (this->pv_overvoltage_sensor_ != nullptr)
      this->pv_overvoltage_sensor_->publish_state(pv_overvoltage);

    // 解析控制状态
    bool charging_relay = control_status & 0x01;
    bool load_output = control_status & 0x02;
    bool fan_control = control_status & 0x04;
    bool overcharge_protection = control_status & 0x10;
    bool overvoltage_protection = control_status & 0x20;

    ESP_LOGD(TAG, "Charging relay: %s", charging_relay ? "On" : "Off");
    ESP_LOGD(TAG, "Load output: %s", load_output ? "On" : "Off");
    ESP_LOGD(TAG, "Fan control: %s", fan_control ? "On" : "Off");
    ESP_LOGD(TAG, "Overcharge protection: %s", overcharge_protection ? "Active" : "Inactive");
    ESP_LOGD(TAG, "Overvoltage protection: %s", overvoltage_protection ? "Active" : "Inactive");

    // 更新控制状态传感器
    if (this->charging_relay_sensor_ != nullptr)
      this->charging_relay_sensor_->publish_state(charging_relay);
    if (this->load_output_sensor_ != nullptr)
      this->load_output_sensor_->publish_state(load_output);
    if (this->dc_output_switch_ != nullptr)
      this->dc_output_switch_->publish_state(load_output);
    if (this->fan_control_sensor_ != nullptr)
      this->fan_control_sensor_->publish_state(fan_control);
    if (this->overcharge_protection_sensor_ != nullptr)
      this->overcharge_protection_sensor_->publish_state(overcharge_protection);
    if (this->overvoltage_protection_sensor_ != nullptr)
      this->overvoltage_protection_sensor_->publish_state(overvoltage_protection);

    // 解析 PV 电压
    float pv_voltage_value = pv_voltage / 10.0;
    ESP_LOGD(TAG, "PV voltage: %.1f V", pv_voltage_value);

    // 更新 PV 电压传感器
    if (this->pv_voltage_sensor_ != nullptr)
      this->pv_voltage_sensor_->publish_state(pv_voltage_value);

    // 解析电池电压
    float battery_voltage_value = battery_voltage / 100.0;
    ESP_LOGD(TAG, "Battery voltage: %.2f V", battery_voltage_value);

    // 更新电池电压传感器
    if (this->battery_voltage_sensor_ != nullptr)
      this->battery_voltage_sensor_->publish_state(battery_voltage_value);

    // 解析充电电流
    float charging_current_value = charging_current / 100.0;
    ESP_LOGD(TAG, "Charging current: %.2f A", charging_current_value);

    // 更新充电电流传感器
    if (this->charging_current_sensor_ != nullptr)
      this->charging_current_sensor_->publish_state(charging_current_value);

    // 计算功率
    float power_value = battery_voltage_value * charging_current_value;
    ESP_LOGD(TAG, "Power: %.2f W", power_value);

    // 更新功率传感器
    if (this->charging_power_sensor_ != nullptr)
      this->charging_power_sensor_->publish_state(power_value);

    // 解析内部温度
    float internal_temperature_value = internal_temperature / 10.0;
    ESP_LOGD(TAG, "Internal temperature: %.1f °C", internal_temperature_value);

    // 更新内部温度传感器
    if (this->internal_temperature_sensor_ != nullptr)
      this->internal_temperature_sensor_->publish_state(internal_temperature_value);
      
    // 解析外部温度
    float external_temperature_value = external_temperature / 10.0;
    ESP_LOGD(TAG, "External temperature: %.1f °C", external_temperature_value);

    // 更新外部温度传感器
    if (this->external_temperature_sensor_ != nullptr)
      this->external_temperature_sensor_->publish_state(external_temperature_value);

    // 解析日发电量
    float daily_energy_value = daily_energy / 1000.0;
    ESP_LOGD(TAG, "Daily energy: %.3f kWh", daily_energy_value);

    // 更新日发电量传感器
    if (this->daily_energy_sensor_ != nullptr)
      this->daily_energy_sensor_->publish_state(daily_energy_value);

    // 解析总电量
    float total_energy_value = total_energy / 1000.0;
    ESP_LOGD(TAG, "Total energy: %.3f kWh", total_energy_value);

    // 更新总电量传感器
    if (this->total_energy_sensor_ != nullptr)
      this->total_energy_sensor_->publish_state(total_energy_value);

    // 处理查询实时数据的逻辑
    // ...existing code...
  }
  // ...existing code...
}

}  // namespace yuhui
}  // namespace esphome
