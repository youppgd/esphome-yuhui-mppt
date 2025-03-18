import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
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
)

from . import yuhui_mppt_ns, YuhuiMPPT, CONF_YUHUI_MPPT_ID, YUHUI_MPPT_COMPONENT_SCHEMA

DEPENDENCIES = ['yuhui_mppt']

YuhuiMPPTBinarySensor = yuhui_mppt_ns.class_('YuhuiMPPTBinarySensor', binary_sensor.BinarySensor, cg.Component)

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

ICON_CHARGING_STATUS = "mdi:battery-charging-50"
ICON_EQUALIZING_CHARGE = "mdi:battery-charging-100"
ICON_TRACKING = "mdi:solar-power"
ICON_FLOATING_CHARGE = "mdi:battery-charging-100"
ICON_CHARGING_CURRENT_LIMIT = "mdi:arrow-down-bold-circle-outline"
ICON_CHARGING_DERATING = "mdi:arrow-down-bold-circle-outline"
ICON_REMOTE_CONTROL_DISABLE_CHARGING = "mdi:power-plug-off"
ICON_PV_OVERVOLTAGE = "mdi:flash-alert"
ICON_CHARGING_RELAY = "mdi:power-plug-battery"
ICON_LOAD_OUTPUT = "mdi:power-plug"
ICON_FAN_CONTROL = "mdi:fan"
ICON_OVERCHARGE_PROTECTION = "mdi:flash-alert"
ICON_OVERVOLTAGE_PROTECTION = "mdi:flash-alert"

CONFIG_SCHEMA = YUHUI_MPPT_COMPONENT_SCHEMA.extend({
    cv.GenerateID(CONF_YUHUI_MPPT_ID): cv.use_id(YuhuiMPPT),
    cv.Optional(CONF_CHARGING_STATUS): binary_sensor.binary_sensor_schema(
        icon=ICON_CHARGING_STATUS
    ),
    cv.Optional(CONF_EQUALIZING_CHARGE): binary_sensor.binary_sensor_schema(
        icon=ICON_EQUALIZING_CHARGE
    ),
    cv.Optional(CONF_TRACKING): binary_sensor.binary_sensor_schema(
        icon=ICON_TRACKING
    ),
    cv.Optional(CONF_FLOATING_CHARGE): binary_sensor.binary_sensor_schema(
        icon=ICON_FLOATING_CHARGE
    ),
    cv.Optional(CONF_CHARGING_CURRENT_LIMIT): binary_sensor.binary_sensor_schema(
        icon=ICON_CHARGING_CURRENT_LIMIT
    ),
    cv.Optional(CONF_CHARGING_DERATING): binary_sensor.binary_sensor_schema(
        icon=ICON_CHARGING_DERATING
    ),
    cv.Optional(CONF_REMOTE_CONTROL_DISABLE_CHARGING): binary_sensor.binary_sensor_schema(
        icon=ICON_REMOTE_CONTROL_DISABLE_CHARGING
    ),
    cv.Optional(CONF_PV_OVERVOLTAGE): binary_sensor.binary_sensor_schema(
        icon=ICON_PV_OVERVOLTAGE
    ),
    cv.Optional(CONF_CHARGING_RELAY): binary_sensor.binary_sensor_schema(
        icon=ICON_CHARGING_RELAY
    ),
    cv.Optional(CONF_LOAD_OUTPUT): binary_sensor.binary_sensor_schema(
        icon=ICON_LOAD_OUTPUT
    ),
    cv.Optional(CONF_FAN_CONTROL): binary_sensor.binary_sensor_schema(
        icon=ICON_FAN_CONTROL
    ),
    cv.Optional(CONF_OVERCHARGE_PROTECTION): binary_sensor.binary_sensor_schema(
        icon=ICON_OVERCHARGE_PROTECTION
    ),
    cv.Optional(CONF_OVERVOLTAGE_PROTECTION): binary_sensor.binary_sensor_schema(
        icon=ICON_OVERVOLTAGE_PROTECTION
    ),
})


async def to_code(config):
    var = await cg.get_variable(config[CONF_YUHUI_MPPT_ID])


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
