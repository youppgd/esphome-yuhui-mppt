#include "switch.h"
#include "esphome/core/log.h"

namespace esphome {
namespace yuhui {

static const char *TAG = "yuhui_mppt.switch";

void YuhuiMPPTSwitch::write_state(bool state) {
  if (state) {
    this->parent_->send_control_command(this->on_command_);
  } else {
    this->parent_->send_control_command(this->off_command_);
  }
}

}  // namespace yuhui
}  // namespace esphome
