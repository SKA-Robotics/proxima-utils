import pyCandle
import time
import matplotlib.pyplot as plt

CAN_ID = 316
TARGET_POSITION = 10.0
TEST_DURATION = 2.0
SAMPLING_TIME = 0.01

KP = 1.5
KI = 0.1
KD = 0.05
I_MAX = 10.0

def run_pid_test():
    candle = pyCandle.attachCandle(pyCandle.CAN_DATARATE_1M, pyCandle.USB)

    md = pyCandle.MD(CAN_ID, candle)
    if md.init() != pyCandle.OK:
        print(f"Błąd: Nie znaleziono sterownika o ID {CAN_ID}")
        return

    print("Inicjalizacja pomyślna. Ustawianie parametrów...")
    
    md.setMotionMode(pyCandle.POSITION_PID)
    md.setPositionPIDparam(KP, KI, KD, I_MAX)
    
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
            
            pos, err = md.getPosition()
            
            if err == pyCandle.OK:
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
    plt.title(f"Test PID (Kp={KP}, Ki={KI}, Kd={KD})")
    plt.xlabel("Czas [s]")
    plt.ylabel("Pozycja")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_pid_test()