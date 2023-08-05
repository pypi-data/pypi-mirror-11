#ifndef ___MOTOR_CONTROL_STATE_VALIDATE___
#define ___MOTOR_CONTROL_STATE_VALIDATE___

namespace motor_control {
namespace state_validate {

template <typename NodeT>
struct OnStateMotorContinuousChanged : public ScalarFieldValidator<bool, 1> {
  typedef ScalarFieldValidator<bool, 1> base_type;

  NodeT *node_p_;
  OnStateMotorContinuousChanged() : node_p_(NULL) {
    this->tags_[0] = 7;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(bool &source, bool target) {
    if (node_p_ != NULL) { return node_p_->on_state_motor_continuous_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateMotorDelayUsChanged : public ScalarFieldValidator<uint32_t, 1> {
  typedef ScalarFieldValidator<uint32_t, 1> base_type;

  NodeT *node_p_;
  OnStateMotorDelayUsChanged() : node_p_(NULL) {
    this->tags_[0] = 6;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(uint32_t &source, uint32_t target) {
    if (node_p_ != NULL) { return node_p_->on_state_motor_delay_us_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateMotorDirectionChanged : public ScalarFieldValidator<bool, 1> {
  typedef ScalarFieldValidator<bool, 1> base_type;

  NodeT *node_p_;
  OnStateMotorDirectionChanged() : node_p_(NULL) {
    this->tags_[0] = 2;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(bool &source, bool target) {
    if (node_p_ != NULL) { return node_p_->on_state_motor_direction_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateMotorEnabledChanged : public ScalarFieldValidator<bool, 1> {
  typedef ScalarFieldValidator<bool, 1> base_type;

  NodeT *node_p_;
  OnStateMotorEnabledChanged() : node_p_(NULL) {
    this->tags_[0] = 1;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(bool &source, bool target) {
    if (node_p_ != NULL) { return node_p_->on_state_motor_enabled_changed(source); }
    return false;
  }
};

template <typename NodeT>
class Validator : public MessageValidator<4> {
public:
  OnStateMotorContinuousChanged<NodeT> motor_continuous_;
  OnStateMotorDelayUsChanged<NodeT> motor_delay_us_;
  OnStateMotorDirectionChanged<NodeT> motor_direction_;
  OnStateMotorEnabledChanged<NodeT> motor_enabled_;

  Validator() {
    register_validator(motor_continuous_);
    register_validator(motor_delay_us_);
    register_validator(motor_direction_);
    register_validator(motor_enabled_);
  }

  void set_node(NodeT &node) {
    motor_continuous_.set_node(node);
    motor_delay_us_.set_node(node);
    motor_direction_.set_node(node);
    motor_enabled_.set_node(node);
  }
};

}  // namespace state_validate
}  // namespace motor_control

#endif  // #ifndef ___MOTOR_CONTROL_STATE_VALIDATE___
    
