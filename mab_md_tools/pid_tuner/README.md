# Proxima - MAB Drive Tuner


Due to the lack of a graphical interface for examining PID parameters, we decided to create a Python script. The script's task is to connect to the MD controller, set parameters, and perform a step response of the control system.

>[!note]
>Remember to set proper `CAN_ID` of MD driver. ID is the last 3 digits from manufacture sticker on driver.

# Usage

```
pip install -r requirements.txt
python3 tuner.py
```

>[!info]
>Make sure that python script has permissions to access usb device 
>[See more](https://askubuntu.com/questions/1048870/permission-denied-to-non-root-user-for-usb-device/1187646#1187646)

# Configuration

```python

# Configuratuon

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
SAMPLING_TIME = 0.01

velocityPID_params = PID_params(5, 10, 0.0, 0.25) 
positionPID_params = PID_params(6, 0.02, 0.0, 1.0)

...

if __name__ == "__main__":
    run_pid_test(Mode.POSITION) # or Mode.VELOCITY

```

![[Projects/Proxima/Software/proxima-utils/mab_md_tools/attachments/PID tuner - plots.png]]