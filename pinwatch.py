from gpiozero import DigitalInputDevice, Motor, OutputDevice
from time import sleep

import config

wake = OutputDevice(config.SLEEP_PIN, initial_value=True)
motors = {"A": Motor(**config.MOTOR_A, pwm=True), "B": Motor(**config.MOTOR_B, pwm=True)}
encoders = {"A": list(config.ENCODER_A), "B": list(config.ENCODER_B)}

pins = encoders["A"] + encoders["B"]
inputs = {p: DigitalInputDevice(p) for p in pins}


def watch(label):
    motor = motors[label]
    seen = {p: set() for p in pins}
    motor.forward(0.4)
    for _ in range(50):
        for p in pins:
            seen[p].add(inputs[p].value)
        sleep(0.05)
    motor.stop()

    print(f"driving motor {label}, its encoder pins are {encoders[label]}")
    for p in pins:
        values = sorted(seen[p])
        state = "TOGGLING" if len(values) > 1 else "stuck"
        mine = "  <- this motor" if p in encoders[label] else ""
        print(f"  {p} {state} {values}{mine}")


watch("A")
sleep(1)
watch("B")
