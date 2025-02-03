import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, CONF_ICON

from .. import yuhui_mppt_ns, YuhuiMPPT, CONF_YUHUI_MPPT_ID, YUHUI_MPPT_COMPONENT_SCHEMA  # 修改导入路径

DEPENDENCIES = ['yuhui_mppt']

CONF_CHARGE_SWITCH = 'charge_switch'
CONF_DC_OUTPUT_SWITCH = 'dc_output_switch'

ICON_CHARGING = "mdi:battery-charging-50"
ICON_DC_OUTPUT = "mdi:power-plug"

TYPES = {
    CONF_CHARGE_SWITCH: (0x01, 0x02),
    CONF_DC_OUTPUT_SWITCH: (0x03, 0x04),
}

YuhuiMPPTSwitch = yuhui_mppt_ns.class_('YuhuiMPPTSwitch', switch.Switch, cg.Component)

YUHUISWITCH_SCHEMA = switch.switch_schema(
    YuhuiMPPTSwitch, icon=ICON_CHARGING, block_inverted=True
).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = YUHUI_MPPT_COMPONENT_SCHEMA.extend({
  cv.Optional(type): YUHUISWITCH_SCHEMA for type in TYPES
})


async def to_code(config):
    parent = await cg.get_variable(config[CONF_YUHUI_MPPT_ID])

    for type, (on, off) in TYPES.items():
        if type in config:
            conf = config[type]
            var = await switch.new_switch(conf)
            await cg.register_component(var, conf)
            cg.add(getattr(parent, f"set_{type}")(var))
            cg.add(var.set_parent(parent))
            cg.add(var.set_on_command(on))
            if off is not None:
                cg.add(var.set_off_command(off))
