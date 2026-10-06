from gpiozero import Button
from time import sleep

PIN = "GPIO4"

switch = Button(PIN, pull_up=True, bounce_time=0.05)

print(f"watching {PIN}, press or flip the switch, ctrl c to quit")

last = None
while True:
    now = switch.is_pressed
    if now != last:
        print("closed" if now else "open")
        last = now
    sleep(0.05)
