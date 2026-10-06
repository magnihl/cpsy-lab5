from gpiozero import DigitalInputDevice, Motor, OutputDevice
from time import sleep

import config

wake = OutputDevice(config.SLEEP_PIN, initial_value=True)
a = Motor(**config.MOTOR_A, pwm=True)

pins = list(config.ENCODER_A) + list(config.ENCODER_B)
inputs = [DigitalInputDevice(p) for p in pins]

print("pins", pins)
print("driving motor A, watching all four encoder lines")

a.forward(0.4)
seen = {p: set() for p in pins}

for _ in range(50):
    for p, d in zip(pins, inputs):
        seen[p].add(d.value)
    sleep(0.05)

a.stop()

for p in pins:
    values = sorted(seen[p])
    state = "TOGGLING" if len(values) > 1 else "stuck"
    print(f"{p} {state} {values}")
