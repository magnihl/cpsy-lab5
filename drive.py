from gpiozero import Motor, OutputDevice
from time import sleep

import config

wake = OutputDevice(config.SLEEP_PIN, initial_value=True)
a = Motor(**config.MOTOR_A, pwm=True)
b = Motor(**config.MOTOR_B, pwm=True)

SPEED = 0.4
RUN = 2

print("both forward")
a.forward(SPEED)
b.forward(SPEED)
sleep(RUN)
a.stop()
b.stop()

sleep(1)

print("both backward")
a.backward(SPEED)
b.backward(SPEED)
sleep(RUN)
a.stop()
b.stop()

print("done")
