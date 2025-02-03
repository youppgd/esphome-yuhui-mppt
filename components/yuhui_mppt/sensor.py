import esphome.codegen as cg
import esphome.config_validation as cv
import esphome.components.button as button
from esphome.components import sensor, binary_sensor, text_sensor
from esphome.const import(
    CONF_CURRENT,
    CONF_POWER,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ICON_EMPTY,
    STATE_CLASS_MEASUREMENT,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_EMPTY,
    UNIT_PERCENT,
    UNIT_VOLT,
    UNIT_WATT,
    ICON_FLASH,
    UNIT_KILOWATT_HOURS
)

from . import CONF_YUHUI_MPPT_ID, YuhuiMPPT

CODEOWNERS = ["@Depressboy"]

CONF_RUNNING_STATUS = 'running_status'
CONF_BATTERY_STATUS = 'battery_status'
CONF_FAN_STATUS = 'fan_status'
CONF_TEMPERATURE_STATUS = 'temperature_status'
CONF_DC_OUTPUT_STATUS = 'dc_output_status'
CONF_INTERNAL_TEMPERATURE1_STATUS = 'internal_temperature1_status'
CONF_INTERNAL_TEMPERATURE2_STATUS = 'internal_temperature2_status'
CONF_EXTERNAL_TEMPERATURE1_STATUS = 'external_temperature1_status'
CONF_CHARGING_STATUS = 'charging_status'
CONF_EQUALIZING_CHARGE = 'equalizing_charge'
CONF_TRACKING = 'tracking'
CONF_FLOATING_CHARGE = 'floating_charge'
CONF_CHARGING_CURRENT_LIMIT = 'charging_current_limit'
CONF_CHARGING_DERATING = 'charging_derating'
CONF_REMOTE_CONTROL_DISABLE_CHARGING = 'remote_control_disable_charging'
CONF_PV_OVERVOLTAGE = 'pv_overvoltage'
CONF_CHARGING_RELAY = 'charging_relay'
CONF_LOAD_OUTPUT = 'load_output'
CONF_FAN_CONTROL = 'fan_control'
CONF_OVERCHARGE_PROTECTION = 'overcharge_protection'
CONF_OVERVOLTAGE_PROTECTION = 'overvoltage_protection'
CONF_PV_VOLTAGE = 'pv_voltage'
CONF_BATTERY_VOLTAGE = 'battery_voltage'
CONF_CHARGING_CURRENT = 'charging_current'
CONF_INTERNAL_TEMPERATURE = 'internal_temperature'
CONF_DAILY_ENERGY = 'daily_energy'
CONF_TOTAL_ENERGY = 'total_energy'
CONF_POWER = 'power'

CONF_ALLOW_CHARGING = 'allow_charging'
CONF_DISABLE_CHARGING = 'disable_charging'
CONF_ENABLE_DC_OUTPUT = 'enable_dc_output'
CONF_DISABLE_DC_OUTPUT = 'disable_dc_output'
CONF_SILENCE_ALARM = 'silence_alarm'
CONF_ENABLE_BACKLIGHT = 'enable_backlight'

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_YUHUI_MPPT_ID): cv.use_id(YuhuiMPPT),
    cv.Optional(CONF_RUNNING_STATUS): text_sensor.text_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_BATTERY_STATUS): text_sensor.text_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_FAN_STATUS): text_sensor.text_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_TEMPERATURE_STATUS): text_sensor.text_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_DC_OUTPUT_STATUS): text_sensor.text_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_INTERNAL_TEMPERATURE1_STATUS): text_sensor.text_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_INTERNAL_TEMPERATURE2_STATUS): text_sensor.text_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_EXTERNAL_TEMPERATURE1_STATUS): text_sensor.text_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_CHARGING_STATUS): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_EQUALIZING_CHARGE): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_TRACKING): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_FLOATING_CHARGE): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_CHARGING_CURRENT_LIMIT): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_CHARGING_DERATING): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_REMOTE_CONTROL_DISABLE_CHARGING): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_PV_OVERVOLTAGE): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_CHARGING_RELAY): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_LOAD_OUTPUT): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_FAN_CONTROL): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_OVERCHARGE_PROTECTION): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_OVERVOLTAGE_PROTECTION): binary_sensor.binary_sensor_schema(icon=ICON_FLASH),
    cv.Optional(CONF_PV_VOLTAGE): sensor.sensor_schema(unit_of_measurement=UNIT_VOLT, icon=ICON_FLASH, accuracy_decimals=1),
    cv.Optional(CONF_BATTERY_VOLTAGE): sensor.sensor_schema(unit_of_measurement=UNIT_VOLT, icon=ICON_FLASH, accuracy_decimals=2),
    cv.Optional(CONF_CHARGING_CURRENT): sensor.sensor_schema(unit_of_measurement=UNIT_AMPERE, icon=ICON_FLASH, accuracy_decimals=2),
    cv.Optional(CONF_INTERNAL_TEMPERATURE): sensor.sensor_schema(unit_of_measurement=UNIT_CELSIUS, icon=ICON_FLASH, accuracy_decimals=1),
    cv.Optional(CONF_DAILY_ENERGY): sensor.sensor_schema(unit_of_measurement=UNIT_KILOWATT_HOURS, icon=ICON_FLASH, accuracy_decimals=2),
    cv.Optional(CONF_TOTAL_ENERGY): sensor.sensor_schema(unit_of_measurement=UNIT_KILOWATT_HOURS, icon=ICON_FLASH, accuracy_decimals=2),
    cv.Optional(CONF_POWER): sensor.sensor_schema(unit_of_measurement=UNIT_WATT, icon=ICON_FLASH, accuracy_decimals=2),
    cv.Optional(CONF_ALLOW_CHARGING): button.BUTTON_SCHEMA,
    cv.Optional(CONF_DISABLE_CHARGING): button.BUTTON_SCHEMA,
    cv.Optional(CONF_ENABLE_DC_OUTPUT): button.BUTTON_SCHEMA,
    cv.Optional(CONF_DISABLE_DC_OUTPUT): button.BUTTON_SCHEMA,
    cv.Optional(CONF_SILENCE_ALARM): button.BUTTON_SCHEMA,
    cv.Optional(CONF_ENABLE_BACKLIGHT): button.BUTTON_SCHEMA,
})

async def to_code(config):
    var = await cg.get_variable(config[CONF_YUHUI_MPPT_ID])

    if CONF_RUNNING_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_RUNNING_STATUS])
        cg.add(var.set_running_status_text_sensor(sens))
    if CONF_BATTERY_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_BATTERY_STATUS])
        cg.add(var.set_battery_status_text_sensor(sens))
    if CONF_FAN_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_FAN_STATUS])
        cg.add(var.set_fan_status_text_sensor(sens))
    if CONF_TEMPERATURE_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_TEMPERATURE_STATUS])
        cg.add(var.set_temperature_status_text_sensor(sens))
    if CONF_DC_OUTPUT_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_DC_OUTPUT_STATUS])
        cg.add(var.set_dc_output_status_text_sensor(sens))
    if CONF_INTERNAL_TEMPERATURE1_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_INTERNAL_TEMPERATURE1_STATUS])
        cg.add(var.set_internal_temperature1_status_text_sensor(sens))
    if CONF_INTERNAL_TEMPERATURE2_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_INTERNAL_TEMPERATURE2_STATUS])
        cg.add(var.set_internal_temperature2_status_text_sensor(sens))
    if CONF_EXTERNAL_TEMPERATURE1_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_EXTERNAL_TEMPERATURE1_STATUS])
        cg.add(var.set_external_temperature1_status_text_sensor(sens))
    if CONF_CHARGING_STATUS in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CHARGING_STATUS])
        cg.add(var.set_charging_status_sensor(sens))
    if CONF_EQUALIZING_CHARGE in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_EQUALIZING_CHARGE])
        cg.add(var.set_equalizing_charge_sensor(sens))
    if CONF_TRACKING in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_TRACKING])
        cg.add(var.set_tracking_sensor(sens))
    if CONF_FLOATING_CHARGE in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_FLOATING_CHARGE])
        cg.add(var.set_floating_charge_sensor(sens))
    if CONF_CHARGING_CURRENT_LIMIT in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CHARGING_CURRENT_LIMIT])
        cg.add(var.set_charging_current_limit_sensor(sens))
    if CONF_CHARGING_DERATING in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CHARGING_DERATING])
        cg.add(var.set_charging_derating_sensor(sens))
    if CONF_REMOTE_CONTROL_DISABLE_CHARGING in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_REMOTE_CONTROL_DISABLE_CHARGING])
        cg.add(var.set_remote_control_disable_charging_sensor(sens))
    if CONF_PV_OVERVOLTAGE in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_PV_OVERVOLTAGE])
        cg.add(var.set_pv_overvoltage_sensor(sens))
    if CONF_CHARGING_RELAY in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_CHARGING_RELAY])
        cg.add(var.set_charging_relay_sensor(sens))
    if CONF_LOAD_OUTPUT in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_LOAD_OUTPUT])
        cg.add(var.set_load_output_sensor(sens))
    if CONF_FAN_CONTROL in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_FAN_CONTROL])
        cg.add(var.set_fan_control_sensor(sens))
    if CONF_OVERCHARGE_PROTECTION in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_OVERCHARGE_PROTECTION])
        cg.add(var.set_overcharge_protection_sensor(sens))
    if CONF_OVERVOLTAGE_PROTECTION in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_OVERVOLTAGE_PROTECTION])
        cg.add(var.set_overvoltage_protection_sensor(sens))
    if CONF_PV_VOLTAGE in config:
        sens = await sensor.new_sensor(config[CONF_PV_VOLTAGE])
        cg.add(var.set_pv_voltage_sensor(sens))
    if CONF_BATTERY_VOLTAGE in config:
        sens = await sensor.new_sensor(config[CONF_BATTERY_VOLTAGE])
        cg.add(var.set_battery_voltage_sensor(sens))
    if CONF_CHARGING_CURRENT in config:
        sens = await sensor.new_sensor(config[CONF_CHARGING_CURRENT])
        cg.add(var.set_charging_current_sensor(sens))
    if CONF_INTERNAL_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_INTERNAL_TEMPERATURE])
        cg.add(var.set_internal_temperature_sensor(sens))
    if CONF_DAILY_ENERGY in config:
        sens = await sensor.new_sensor(config[CONF_DAILY_ENERGY])
        cg.add(var.set_daily_energy_sensor(sens))
    if CONF_TOTAL_ENERGY in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_ENERGY])
        cg.add(var.set_total_energy_sensor(sens))
    if CONF_POWER in config:
        sens = await sensor.new_sensor(config[CONF_POWER])
        cg.add(var.set_power_sensor(sens))

    if CONF_ALLOW_CHARGING in config:
        btn = await button.new_button(config[CONF_ALLOW_CHARGING])
        cg.add(var.set_allow_charging_button(btn))
    if CONF_DISABLE_CHARGING in config:
        btn = await button.new_button(config[CONF_DISABLE_CHARGING])
        cg.add(var.set_disable_charging_button(btn))
    if CONF_ENABLE_DC_OUTPUT in config:
        btn = await button.new_button(config[CONF_ENABLE_DC_OUTPUT])
        cg.add(var.set_enable_dc_output_button(btn))
    if CONF_DISABLE_DC_OUTPUT in config:
        btn = await button.new_button(config[CONF_DISABLE_DC_OUTPUT])
        cg.add(var.set_disable_dc_output_button(btn))
    if CONF_SILENCE_ALARM in config:
        btn = await button.new_button(config[CONF_SILENCE_ALARM])
        cg.add(var.set_silence_alarm_button(btn))
    if CONF_ENABLE_BACKLIGHT in config:
        btn = await button.new_button(config[CONF_ENABLE_BACKLIGHT])
        cg.add(var.set_enable_backlight_button(btn))
