from gpiozero import OutputDevice
from time import sleep

import config

# plain on/off, no PWM, so a multimeter reads a steady level
wake = OutputDevice(config.SLEEP_PIN, initial_value=True)

pins = {
    "AIN1 (J5 #1)": config.MOTOR_A["forward"],
    "AIN2 (J5 #2)": config.MOTOR_A["backward"],
    "BIN1 (J8 #1)": config.MOTOR_B["forward"],
    "BIN2 (J8 #2)": config.MOTOR_B["backward"],
}

devices = {label: OutputDevice(pin) for label, pin in pins.items()}

for label, dev in devices.items():
    print(f"{label} on {pins[label]} HIGH for 10 s, measure it now")
    dev.on()
    sleep(10)
    dev.off()
    print(f"{label} back to low")

print("done")
