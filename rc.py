#!/usr/bin/env python3
"""Keyboard remote control. w a s d to drive, e stop, r re-arm, q quit."""

import curses
import time

from gpiozero import Button, DigitalOutputDevice, Motor, Robot

import config

SPEED = 0.5
STOP_PIN = "GPIO4"

# the terminal waits before it starts repeating a held key, so the first
# press gets a long grace period and the rest get a short one
STOP_AFTER = 0.1
FIRST_HOLD = 0.7
REPEAT_GAP = 0.25

stdscr = None
slp = None

try:
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)
    stdscr.addstr(0, 2, "w a s d drive, e stop, r re-arm, q quit")

    slp = DigitalOutputDevice(config.SLEEP_PIN)
    slp.on()

    robot = Robot(
        left=Motor(**config.MOTOR_A),
        right=Motor(**config.MOTOR_B),
    )

    estop = Button(STOP_PIN, pull_up=True, bounce_time=0.05)
    latched = False

    def trip():
        global latched
        latched = True
        robot.stop()
        slp.off()

    estop.when_pressed = trip

    actions = {
        ord("w"): ("forward ", lambda: robot.forward(SPEED)),
        ord("s"): ("backward", lambda: robot.backward(SPEED)),
        ord("a"): ("left    ", lambda: robot.left(SPEED)),
        ord("d"): ("right   ", lambda: robot.right(SPEED)),
        ord("e"): ("stop    ", robot.stop),
    }

    last_press = 0.0
    prev_press = 0.0
    moving = False
    shown = None

    while True:
        stdscr.refresh()
        key = stdscr.getch()
        now = time.monotonic()

        if key == ord("q"):
            break

        state = "E-STOP TRIPPED, press r" if latched else "armed            "
        if state != shown:
            stdscr.addstr(2, 2, state)
            shown = state

        if latched:
            if key == ord("r"):
                latched = False
                slp.on()
                moving = False
            time.sleep(0.02)
            continue

        if key in actions:
            label, action = actions[key]
            stdscr.addstr(1, 2, label)
            action()
            prev_press = last_press
            last_press = now
            moving = True
        elif moving:
            repeating = (last_press - prev_press) < REPEAT_GAP
            timeout = STOP_AFTER if repeating else FIRST_HOLD
            if now - last_press > timeout:
                robot.stop()
                stdscr.addstr(1, 2, "idle    ")
                moving = False

        time.sleep(0.02)

finally:
    if slp is not None:
        slp.off()
    if stdscr is not None:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.endwin()
