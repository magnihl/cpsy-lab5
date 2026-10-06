from gpiozero import Motor, OutputDevice, RotaryEncoder
from time import sleep

import config

wake = OutputDevice(config.SLEEP_PIN, initial_value=True)
a = Motor(**config.MOTOR_A, pwm=True)
b = Motor(**config.MOTOR_B, pwm=True)
ea = RotaryEncoder(*config.ENCODER_A, max_steps=0)
eb = RotaryEncoder(*config.ENCODER_B, max_steps=0)

RUN = 2

for speed in (0.4, 0.6, 0.8):
    start_a, start_b = ea.steps, eb.steps
    a.forward(speed)
    b.forward(speed)
    sleep(RUN)
    a.stop()
    b.stop()
    sleep(1)

    moved_a = abs(ea.steps - start_a)
    moved_b = abs(eb.steps - start_b)
    ratio = moved_a / moved_b if moved_b else 0
    print(f"speed {speed}  A {moved_a}  B {moved_b}  ratio {ratio:.2f}")
