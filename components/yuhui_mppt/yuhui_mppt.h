#pragma once

#include "esphome/core/component.h"
#include "esphome/components/custom_modbus/modbus.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/button/button.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/switch/switch.h"
#include <queue>

namespace esphome {
namespace yuhui {

enum YuhuiMPPTState {
  IDLE,
  SENDING_QUERY,
  WAITING_RESPONSE
};

class YuhuiMPPT : public PollingComponent, public custom_modbus::ModbusDevice {
 public:
  void set_device_address(uint8_t address) { this->device_address_ = address; }
  void set_rx_timeout(uint32_t timeout) { this->rx_timeout_ = timeout; }

  void setup() override;
  void loop() override;
  void update() override;

  void send_query_command();
  void send_control_command(uint8_t control_code);
  void send_parameter_command(uint8_t parameter_code, uint32_t parameter_value, uint8_t data_length);
  void send_clock_calibration_command();
  void on_modbus_raw_data(const std::vector<uint8_t> &data) override;
  void on_modbus_data(const std::vector<uint8_t> &data) override { this->on_modbus_raw_data(data); }

  void set_running_status_text_sensor(text_sensor::TextSensor *sensor) { running_status_text_sensor_ = sensor; }
  void set_battery_status_text_sensor(text_sensor::TextSensor *sensor) { battery_status_text_sensor_ = sensor; }
  void set_fan_status_text_sensor(text_sensor::TextSensor *sensor) { fan_status_text_sensor_ = sensor; }
  void set_temperature_status_text_sensor(text_sensor::TextSensor *sensor) { temperature_status_text_sensor_ = sensor; }
  void set_dc_output_status_text_sensor(text_sensor::TextSensor *sensor) { dc_output_status_text_sensor_ = sensor; }
  void set_internal_temperature1_status_text_sensor(text_sensor::TextSensor *sensor) { internal_temperature1_status_text_sensor_ = sensor; }
  void set_internal_temperature2_status_text_sensor(text_sensor::TextSensor *sensor) { internal_temperature2_status_text_sensor_ = sensor; }
  void set_external_temperature1_status_text_sensor(text_sensor::TextSensor *sensor) { external_temperature1_status_text_sensor_ = sensor; }
  void set_charging_status_sensor(binary_sensor::BinarySensor *sensor) { charging_status_sensor_ = sensor; }
  void set_equalizing_charge_sensor(binary_sensor::BinarySensor *sensor) { equalizing_charge_sensor_ = sensor; }
  void set_tracking_sensor(binary_sensor::BinarySensor *sensor) { tracking_sensor_ = sensor; }
  void set_floating_charge_sensor(binary_sensor::BinarySensor *sensor) { floating_charge_sensor_ = sensor; }
  void set_charging_current_limit_sensor(binary_sensor::BinarySensor *sensor) { charging_current_limit_sensor_ = sensor; }
  void set_charging_derating_sensor(binary_sensor::BinarySensor *sensor) { charging_derating_sensor_ = sensor; }
  void set_remote_control_disable_charging_sensor(binary_sensor::BinarySensor *sensor) { remote_control_disable_charging_sensor_ = sensor; }
  void set_pv_overvoltage_sensor(binary_sensor::BinarySensor *sensor) { pv_overvoltage_sensor_ = sensor; }
  void set_charging_relay_sensor(binary_sensor::BinarySensor *sensor) { charging_relay_sensor_ = sensor; }
  void set_load_output_sensor(binary_sensor::BinarySensor *sensor) { load_output_sensor_ = sensor; }
  void set_fan_control_sensor(binary_sensor::BinarySensor *sensor) { fan_control_sensor_ = sensor; }
  void set_overcharge_protection_sensor(binary_sensor::BinarySensor *sensor) { overcharge_protection_sensor_ = sensor; }
  void set_overvoltage_protection_sensor(binary_sensor::BinarySensor *sensor) { overvoltage_protection_sensor_ = sensor; }
  void set_pv_voltage_sensor(sensor::Sensor *sensor) { pv_voltage_sensor_ = sensor; }
  void set_battery_voltage_sensor(sensor::Sensor *sensor) { battery_voltage_sensor_ = sensor; }
  void set_charging_current_sensor(sensor::Sensor *sensor) { charging_current_sensor_ = sensor; }
  void set_internal_temperature_sensor(sensor::Sensor *sensor) { internal_temperature_sensor_ = sensor; }
  void set_daily_energy_sensor(sensor::Sensor *sensor) { daily_energy_sensor_ = sensor; }
  void set_total_energy_sensor(sensor::Sensor *sensor) { total_energy_sensor_ = sensor; }
  void set_charging_power_sensor(sensor::Sensor *sensor) { charging_power_sensor_ = sensor; }

  void set_silence_alarm_button(button::Button *button) { silence_alarm_button_ = button; }
  void set_enable_backlight_button(button::Button *button) { enable_backlight_button_ = button; }
  void set_clock_calibration_button(button::Button *button) { clock_calibration_button_ = button; }

  void set_disable_charge_switch(esphome::switch_::Switch *disable_charge_switch) { disable_charge_switch_ = disable_charge_switch; }
  void set_dc_output_switch(esphome::switch_::Switch *dc_output_switch) { dc_output_switch_ = dc_output_switch; }

 protected:
  text_sensor::TextSensor *running_status_text_sensor_ = nullptr;
  text_sensor::TextSensor *battery_status_text_sensor_ = nullptr;
  text_sensor::TextSensor *fan_status_text_sensor_ = nullptr;
  text_sensor::TextSensor *temperature_status_text_sensor_ = nullptr;
  text_sensor::TextSensor *dc_output_status_text_sensor_ = nullptr;
  text_sensor::TextSensor *internal_temperature1_status_text_sensor_ = nullptr;
  text_sensor::TextSensor *internal_temperature2_status_text_sensor_ = nullptr;
  text_sensor::TextSensor *external_temperature1_status_text_sensor_ = nullptr;
  binary_sensor::BinarySensor *charging_status_sensor_ = nullptr;
  binary_sensor::BinarySensor *equalizing_charge_sensor_ = nullptr;
  binary_sensor::BinarySensor *tracking_sensor_ = nullptr;
  binary_sensor::BinarySensor *floating_charge_sensor_ = nullptr;
  binary_sensor::BinarySensor *charging_current_limit_sensor_ = nullptr;
  binary_sensor::BinarySensor *charging_derating_sensor_ = nullptr;
  binary_sensor::BinarySensor *remote_control_disable_charging_sensor_ = nullptr;
  binary_sensor::BinarySensor *pv_overvoltage_sensor_ = nullptr;
  binary_sensor::BinarySensor *charging_relay_sensor_ = nullptr;
  binary_sensor::BinarySensor *load_output_sensor_ = nullptr;
  binary_sensor::BinarySensor *fan_control_sensor_ = nullptr;
  binary_sensor::BinarySensor *overcharge_protection_sensor_ = nullptr;
  binary_sensor::BinarySensor *overvoltage_protection_sensor_ = nullptr;
  sensor::Sensor *pv_voltage_sensor_ = nullptr;
  sensor::Sensor *battery_voltage_sensor_ = nullptr;
  sensor::Sensor *charging_current_sensor_ = nullptr;
  sensor::Sensor *internal_temperature_sensor_ = nullptr;
  sensor::Sensor *daily_energy_sensor_ = nullptr;
  sensor::Sensor *total_energy_sensor_ = nullptr;
  sensor::Sensor *charging_power_sensor_ = nullptr;

  button::Button *silence_alarm_button_ = nullptr;
  button::Button *enable_backlight_button_ = nullptr;
  button::Button *clock_calibration_button_ = nullptr;

  esphome::switch_::Switch *disable_charge_switch_ = nullptr;
  esphome::switch_::Switch *dc_output_switch_ = nullptr;

  int baud_rate_ = 9600;
  uint8_t device_address_ = 0x01;
  std::string id_;

  YuhuiMPPTState state_ = IDLE;
  unsigned long last_query_time_ = 0;
  uint8_t buffer_[37];
  size_t buffer_index_ = 0;
  unsigned long last_receive_time_ = 0;
  bool awaiting_response_ = false;
  std::queue<std::vector<uint8_t>> send_queue_;
  unsigned long last_send_time_ = 0;
  uint32_t rx_timeout_ = 1000;  // 默认1秒超时

  void handle_command(uint8_t *data);
  void process_state_();
  void process_send_queue_();
};

}  // namespace yuhui
}  // namespace esphome
