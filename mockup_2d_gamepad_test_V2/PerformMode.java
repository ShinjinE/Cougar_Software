public enum PerformMode {
  START(0),
  ANGRY_1(500),
  MID(500),
  SAD_1(500),
  WAIT_1(250),
  MAD_TO_SAD(0),
  WAIT_2(100),
  SAD_TO_MAD(0),
  WAIT_3(100),
  SAD_2(500),
  ANGRY_2(500),
  END(250);
  
  final private int duration;
  
  private PerformMode(int duration) {
    this.duration = duration;
  }
  
  public int getDuration() { return duration; }
  
  static PerformMode nextState(PerformMode prevMode) {
    switch (prevMode) {
      case START:
        return ANGRY_1;
      case ANGRY_1:
        return MID;
      case MID:
        return SAD_1;
      case SAD_1:
        return WAIT_1;
      case WAIT_1:
        return MAD_TO_SAD;
      case MAD_TO_SAD:
        return WAIT_2;
      case WAIT_2:
        return SAD_TO_MAD;
      case SAD_TO_MAD:
        return WAIT_3;
      case WAIT_3:
        return SAD_2;
      case SAD_2:
        return ANGRY_2;
      case ANGRY_2:
        return END;
      case END:
        return START;
      default:
        return prevMode;
    }
  }
  
  static PerformMode begin() {
    return START;
  }
}
