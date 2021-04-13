public enum WaveMode {
  START,
  UP_1, UP_2, UP_3, UP_4, UP_5, UP_6,
  DOWN_1, DOWN_2, DOWN_3, DOWN_4, DOWN_5, DOWN_6,
  END;
  
  static WaveMode nextState(WaveMode prevMode) {
    switch (prevMode) {
      case START:
        return UP_1;
      case UP_1:
        return UP_2;
      case UP_2:
        return UP_3;
      case UP_3:
        return UP_4;
      case UP_4:
        return UP_5;
      case UP_5:
        return UP_6;
      case UP_6:
        return DOWN_6;
      case DOWN_6:
        return DOWN_5;
      case DOWN_5:
        return DOWN_4;
      case DOWN_4:
        return DOWN_3;
      case DOWN_3:
        return DOWN_2;
      case DOWN_2:
        return DOWN_1;
      case DOWN_1:
        return END;
      case END:
        return START;
      default:
        return prevMode;
    }
  }
  
  static WaveMode begin() {
    return START;
  }
}
