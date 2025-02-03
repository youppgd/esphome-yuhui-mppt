import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID
from esphome.components import custom_modbus

DEPENDENCIES = ['custom_modbus']
AUTO_LOAD = ["binary_sensor", "sensor", "switch", "text_sensor", "button"]
MULTI_CONF = True

CONF_YUHUI_MPPT_ID = "yuhui_mppt_id"
CONF_RX_TIMEOUT = "rx_timeout"
CONF_DEVICE_ADDRESS = "device_address"

yuhui_mppt_ns = cg.esphome_ns.namespace('yuhui')
YuhuiMPPT = yuhui_mppt_ns.class_('YuhuiMPPT', cg.PollingComponent, custom_modbus.ModbusDevice)

YUHUI_MPPT_COMPONENT_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_YUHUI_MPPT_ID): cv.use_id(YuhuiMPPT),
    }
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(YuhuiMPPT),
            cv.Optional(
                CONF_RX_TIMEOUT, default="150ms",
            ): cv.positive_time_period_milliseconds,
            cv.Optional(
                CONF_DEVICE_ADDRESS, default=0x01,
            ): cv.hex_uint8_t,
        }
    )
    .extend(cv.polling_component_schema("2s"))
    .extend(custom_modbus.modbus_device_schema(0x01))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await custom_modbus.register_modbus_device(var, config)

    cg.add(var.set_device_address(config[CONF_DEVICE_ADDRESS]))