import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button
from esphome.const import CONF_ID

from .. import yuhui_mppt_ns, YuhuiMPPT, CONF_YUHUI_MPPT_ID, YUHUI_MPPT_COMPONENT_SCHEMA

DEPENDENCIES = ['yuhui_mppt']

YuhuiMPPTButton = yuhui_mppt_ns.class_('YuhuiMPPTButton', button.Button, cg.Component)
YuhuiMPPTClockCalibrationButton = yuhui_mppt_ns.class_('YuhuiMPPTClockCalibrationButton', button.Button, cg.Component)

CONF_SILENCE_ALARM = 'silence_alarm'
CONF_ENABLE_BACKLIGHT = 'enable_backlight'
CONF_CLOCK_CALIBRATION = 'clock_calibration'

ICON_SILENCE_ALARM = "mdi:bell"
ICON_ENABLE_BACKLIGHT = "mdi:lightbulb-on"
ICON_CLOCK_CALIBRATION = "mdi:clock"

TYPES = {
    CONF_SILENCE_ALARM: (0x05),
    CONF_ENABLE_BACKLIGHT: (0x06),
}

YuhuiMPPTButtonSchema = button.button_schema(
    YuhuiMPPTButton, icon=ICON_SILENCE_ALARM
).extend(cv.COMPONENT_SCHEMA)

YuhuiMPPTClockCalibrationButtonSchema = button.button_schema(
    YuhuiMPPTClockCalibrationButton, icon=ICON_CLOCK_CALIBRATION
).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = YUHUI_MPPT_COMPONENT_SCHEMA.extend({
    cv.Optional(type): YuhuiMPPTButtonSchema for type in TYPES
}).extend({
    cv.Optional(CONF_CLOCK_CALIBRATION): YuhuiMPPTClockCalibrationButtonSchema,
})


async def to_code(config):
    parent = await cg.get_variable(config[CONF_YUHUI_MPPT_ID])

    for type, (value) in TYPES.items():
        if type in config:
            conf = config[type]
            var = await button.new_button(conf)
            await cg.register_component(var, conf)
            cg.add(getattr(parent, f"set_{type}_button")(var))
            cg.add(var.set_parent(parent))
            cg.add(var.set_command(value))

    if CONF_CLOCK_CALIBRATION in config:
        conf = config[CONF_CLOCK_CALIBRATION]
        var = await button.new_button(conf)
        await cg.register_component(var, conf)
        cg.add(parent.set_clock_calibration_button(var))
        cg.add(var.set_parent(parent))
