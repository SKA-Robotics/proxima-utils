import pyCandle
import time
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class PID_params:
    KP: float
    KI: float
    KD: float
    I_MAX: float

CAN_ID = 316
TARGET_POSITION = 10.0
TEST_DURATION = 3.0
SAMPLING_TIME = 0.01

positionPID_params = PID_params(100.5, 1.5, 0.0, 1.0)
velocityPID_params = PID_params(10.100000, 1.000500, 0.0, 0.25)

def run_pid_test():
    candle = pyCandle.attachCandle(pyCandle.CAN_DATARATE_1M, pyCandle.USB)

    md = pyCandle.MD(CAN_ID, candle)
    if md.init() != pyCandle.MD_Error_t.OK:
        print(f"Błąd: Nie znaleziono sterownika o ID {CAN_ID}")
        return

    print("Inicjalizacja pomyślna. Ustawianie parametrów...")
    
    md.setMotionMode(pyCandle.VELOCITY_PID)
    
    md.setPositionPIDparam(positionPID_params.KP,
                           positionPID_params.KI,
                           positionPID_params.KD,
                           positionPID_params.I_MAX
    )
    
    md.setVelocityPIDparam(velocityPID_params.KP,
                           velocityPID_params.KI,
                           velocityPID_params.KD,
                           velocityPID_params.I_MAX
    )
    
    md.zero()
    time.sleep(0.1)

    timestamps = []
    actual_positions = []
    target_positions = []

    try:
        print(f"Start testu! Przejazd na pozycję: {TARGET_POSITION}")
        md.enable()
        
        start_time = time.time()
        while (time.time() - start_time) < TEST_DURATION:
            current_elapsed = time.time() - start_time
            
            md.setTargetPosition(TARGET_POSITION)
            # md.setTargetVelocity(10)
            
            pos, err = md.getPosition()
            # print(err)
            
            if err == pyCandle.MD_Error_t.OK:
                timestamps.append(current_elapsed)
                actual_positions.append(pos)
                target_positions.append(TARGET_POSITION)
            
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
    plt.ylabel("Pozycja")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_pid_test()