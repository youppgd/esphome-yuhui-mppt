import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import(
    CONF_CURRENT,
    CONF_POWER,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_ENERGY,
    ICON_EMPTY,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
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

CONF_PV_VOLTAGE = 'pv_voltage'
CONF_BATTERY_VOLTAGE = 'battery_voltage'
CONF_CHARGING_CURRENT = 'charging_current'
CONF_INTERNAL_TEMPERATURE = 'internal_temperature'
CONF_DAILY_ENERGY = 'daily_energy'
CONF_TOTAL_ENERGY = 'total_energy'
CONF_CHARGING_POWER = 'charging_power'

ICON_PV_VOLTAGE = "mdi:solar-power"
ICON_BATTERY_VOLTAGE = "mdi:battery"
ICON_CHARGING_CURRENT = "mdi:current-dc"
ICON_INTERNAL_TEMPERATURE = "mdi:thermometer"
ICON_DAILY_ENERGY = "mdi:lightning-bolt-outline"
ICON_TOTAL_ENERGY = "mdi:lightning-bolt-outline"
ICON_CHARGING_POWER = "mdi:flash"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_YUHUI_MPPT_ID): cv.use_id(YuhuiMPPT),
    cv.Optional(CONF_PV_VOLTAGE): sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT,
        icon=ICON_PV_VOLTAGE,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_BATTERY_VOLTAGE): sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT,
        icon=ICON_BATTERY_VOLTAGE,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_CHARGING_CURRENT): sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE,
        icon=ICON_CHARGING_CURRENT,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_INTERNAL_TEMPERATURE): sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        icon=ICON_INTERNAL_TEMPERATURE,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    cv.Optional(CONF_DAILY_ENERGY): sensor.sensor_schema(
        unit_of_measurement=UNIT_KILOWATT_HOURS,
        icon=ICON_DAILY_ENERGY,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    cv.Optional(CONF_TOTAL_ENERGY): sensor.sensor_schema(
        unit_of_measurement=UNIT_KILOWATT_HOURS,
        icon=ICON_TOTAL_ENERGY,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_ENERGY,
        state_class=STATE_CLASS_TOTAL_INCREASING,
    ),
    cv.Optional(CONF_CHARGING_POWER): sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        icon=ICON_CHARGING_POWER,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
})

async def to_code(config):
    var = await cg.get_variable(config[CONF_YUHUI_MPPT_ID])

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
    if CONF_CHARGING_POWER in config:
        sens = await sensor.new_sensor(config[CONF_CHARGING_POWER])
        cg.add(var.set_charging_power_sensor(sens))
