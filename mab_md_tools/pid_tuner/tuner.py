import pyCandle
import time
import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum

@dataclass
class PID_params:
    KP: float
    KI: float
    KD: float
    I_MAX: float
class Mode(Enum):
    VELOCITY = 1
    POSITION = 2

CAN_ID = 316
TARGET = 10
TEST_DURATION = 5
SAMPLING_TIME = 0.001

velocityPID_params = PID_params(5, 10, 0.0, 0.25)
positionPID_params = PID_params(6, 0.02, 0.0, 1.0)

def run_pid_test(mode: Mode):
    candle = pyCandle.attachCandle(pyCandle.CAN_DATARATE_1M, pyCandle.USB)

    md = pyCandle.MD(CAN_ID, candle)
    if md.init() != pyCandle.MD_Error_t.OK:
        print(f"Błąd: Nie znaleziono sterownika o ID {CAN_ID}")
        return

    print("Inicjalizacja pomyślna. Ustawianie parametrów...")
    
    match mode:
        case Mode.VELOCITY:
            md.setMotionMode(pyCandle.VELOCITY_PID)
        case Mode.POSITION:
            md.setMotionMode(pyCandle.POSITION_PID)

    md.setVelocityPIDparam(velocityPID_params.KP,
                           velocityPID_params.KI,
                           velocityPID_params.KD,
                           velocityPID_params.I_MAX
    )

    md.setPositionPIDparam(positionPID_params.KP,
                           positionPID_params.KI,
                           positionPID_params.KD,
                           positionPID_params.I_MAX
    )
    
    
    md.zero()
    time.sleep(0.1)

    timestamps = []
    actual_positions = []
    target_positions = []

    try:
        md.enable()
        
        start_time = time.time()
        while (time.time() - start_time) < TEST_DURATION:
            current_elapsed = time.time() - start_time
            
            match mode:
                case Mode.POSITION:
                    md.setTargetPosition(TARGET)
                    out, err = md.getPosition()
                case Mode.VELOCITY:
                    md.setTargetVelocity(TARGET)
                    out, err = md.getVelocity()

            if err == pyCandle.MD_Error_t.OK:
                timestamps.append(current_elapsed)
                actual_positions.append(out)
                target_positions.append(TARGET)
            
            time.sleep(SAMPLING_TIME)

    except KeyboardInterrupt:
        print("\nPrzerwano ręcznie!")
    
    finally:
        md.disable()
        print("Silnik wyłączony.")

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, target_positions, 'r--', label='Zadana (Target)')
    plt.plot(timestamps, actual_positions, 'b-', label='Aktualna (Actual)')
    # plt.title(f"Test PID (Kp={KP}, Ki={KI}, Kd={KD})")
    plt.xlabel("Czas [s]")
    plt.ylabel("Wartość")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_pid_test(Mode.POSITION)