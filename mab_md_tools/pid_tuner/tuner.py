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

# Konfiguracja
CAN_ID = 316
TARGET = 10
TEST_DURATION = 5
SAMPLING_TIME = 0.01

velocityPID_params = PID_params(5, 10, 0.0, 0.25)
positionPID_params = PID_params(6, 0.02, 0.0, 1.0)

def run_pid_test(mode: Mode):
    candle = pyCandle.attachCandle(pyCandle.CAN_DATARATE_1M, pyCandle.USB)
    md = pyCandle.MD(CAN_ID, candle)
    
    if md.init() != pyCandle.MD_Error_t.OK:
        print(f"Błąd: Nie znaleziono sterownika o ID {CAN_ID}")
        return

    print(f"Inicjalizacja pomyślna. Tryb: {mode.name}. Start testu...")
    
    if mode == Mode.POSITION:
        md.setMotionMode(pyCandle.POSITION_PID)
    else:
        md.setMotionMode(pyCandle.VELOCITY_PID)

    md.setVelocityPIDparam(velocityPID_params.KP, velocityPID_params.KI, 
                           velocityPID_params.KD, velocityPID_params.I_MAX)
    md.setPositionPIDparam(positionPID_params.KP, positionPID_params.KI, 
                           positionPID_params.KD, positionPID_params.I_MAX)
    
    md.zero()
    time.sleep(0.2)

    timestamps = []
    hist_pos = []
    hist_vel = []
    hist_trq = []
    target_vals = []

    try:
        md.enable()
        start_time = time.time()
        
        while (time.time() - start_time) < TEST_DURATION:
            t_now = time.time() - start_time
            
            if mode == Mode.POSITION:
                md.setTargetPosition(TARGET)
            else:
                md.setTargetVelocity(TARGET)

            pos, err_p = md.getPosition()
            vel, err_v = md.getVelocity()
            trq, err_t = md.getTorque()

            if all(err == pyCandle.MD_Error_t.OK for err in [err_p, err_v, err_t]):
                timestamps.append(t_now)
                hist_pos.append(pos)
                hist_vel.append(vel)
                hist_trq.append(trq)
                target_vals.append(TARGET)
            
            time.sleep(SAMPLING_TIME)

    except KeyboardInterrupt:
        print("\nPrzerwano ręcznie!")
    finally:
        md.disable()
        print("Silnik wyłączony. Generowanie wykresów...")

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    fig.suptitle(f"Test Regulacji PID - Tryb {mode.name}", fontsize=16)

    # Wykres 1: Pozycja
    ax1.plot(timestamps, hist_pos, 'b-', label='Aktualna Pozycja')
    if mode == Mode.POSITION:
        ax1.plot(timestamps, target_vals, 'r--', label='Zadana Pozycja')
    ax1.set_ylabel("Pozycja")
    ax1.legend(loc='upper right')
    ax1.grid(True)

    # Wykres 2: Prędkość
    ax2.plot(timestamps, hist_vel, 'g-', label='Aktualna Prędkość')
    if mode == Mode.VELOCITY:
        ax2.plot(timestamps, target_vals, 'r--', label='Zadana Prędkość')
    ax2.set_ylabel("Prędkość")
    ax2.legend(loc='upper right')
    ax2.grid(True)

    # Wykres 3: Moment (Torque)
    ax3.plot(timestamps, hist_trq, 'm-', label='Moment (Torque)')
    ax3.set_ylabel("Moment [Nm / %]")
    ax3.set_xlabel("Czas [s]")
    ax3.legend(loc='upper right')
    ax3.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    run_pid_test(Mode.POSITION)