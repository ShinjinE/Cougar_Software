public enum ControlMode {
  EXACT_POS,
  STEP_POS,
  ROVE_MACRO_UP,
  ROVE_MACRO_DOWN,
  PERFORM_MACRO,
  WAVE_MACRO;
  
  static ControlMode nextState(ControlMode prevMode) {
    switch (prevMode) {
      case EXACT_POS:
        return ControlMode.STEP_POS;
      case STEP_POS:
        return ControlMode.EXACT_POS;
      case ROVE_MACRO_UP:
        return ROVE_MACRO_DOWN;
      case ROVE_MACRO_DOWN:
        return ROVE_MACRO_UP;
      default:
        return prevMode;
    }
  }
  
  public String toString() {
    switch (this) {
      case EXACT_POS:
        return "EXACT_POS";
      case STEP_POS:
        return "STEP_POS";
      case ROVE_MACRO_UP:
      case ROVE_MACRO_DOWN:
        return "ROVE_MACRO";
      case PERFORM_MACRO:
        return "PERFORM_MACRO";
      case WAVE_MACRO:
        return "WAVE_MACRO";
      default:
        return "ERROR - No state set";
    }
  }
}
