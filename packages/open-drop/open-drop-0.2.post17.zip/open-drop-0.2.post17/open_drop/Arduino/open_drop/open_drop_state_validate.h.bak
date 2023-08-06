#ifndef ___OPEN_DROP_STATE_VALIDATE___
#define ___OPEN_DROP_STATE_VALIDATE___

namespace open_drop {
namespace state_validate {

template <typename NodeT>
struct OnStateFrequencyChanged : public ScalarFieldValidator<float, 1> {
  typedef ScalarFieldValidator<float, 1> base_type;

  NodeT *node_p_;
  OnStateFrequencyChanged() : node_p_(NULL) {
    this->tags_[0] = 2;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(float &source, float target) {
    if (node_p_ != NULL) { return node_p_->on_state_frequency_changed(source); }
    return false;
  }
};

template <typename NodeT>
struct OnStateVoltageChanged : public ScalarFieldValidator<float, 1> {
  typedef ScalarFieldValidator<float, 1> base_type;

  NodeT *node_p_;
  OnStateVoltageChanged() : node_p_(NULL) {
    this->tags_[0] = 1;
  }

  void set_node(NodeT &node) { node_p_ = &node; }
  virtual bool operator()(float &source, float target) {
    if (node_p_ != NULL) { return node_p_->on_state_voltage_changed(target, source); }
    return false;
  }
};

template <typename NodeT>
class Validator : public MessageValidator<2> {
public:
  OnStateFrequencyChanged<NodeT> frequency_;
  OnStateVoltageChanged<NodeT> voltage_;

  Validator() {
    register_validator(frequency_);
    register_validator(voltage_);
  }

  void set_node(NodeT &node) {
    frequency_.set_node(node);
    voltage_.set_node(node);
  }
};

}  // namespace state_validate
}  // namespace open_drop

#endif  // #ifndef ___OPEN_DROP_STATE_VALIDATE___
    
