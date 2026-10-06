from gpiozero import Motor, OutputDevice, RotaryEncoder
from time import sleep

import config

# DRV8833 ignores all input while SLP is low
wake = OutputDevice(config.SLEEP_PIN, initial_value=True)

a = Motor(**config.MOTOR_A, pwm=True)
b = Motor(**config.MOTOR_B, pwm=True)
ea = RotaryEncoder(*config.ENCODER_A, max_steps=0)
eb = RotaryEncoder(*config.ENCODER_B, max_steps=0)

SPEED = 0.3
RUN = 1


def run(motor, encoder, label, direction):
    print(f"{label} {direction}")
    before = encoder.steps
    getattr(motor, direction)(SPEED)
    sleep(RUN)
    motor.stop()
    print(f"  steps {before} to {encoder.steps}")


print("start, wheels should be off the ground")

run(a, ea, "motor A", "forward")
run(a, ea, "motor A", "backward")
run(b, eb, "motor B", "forward")
run(b, eb, "motor B", "backward")

print("done")
