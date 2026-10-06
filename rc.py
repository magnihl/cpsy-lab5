#!/usr/bin/env python3
"""Keyboard remote control. w a s d to drive, e to stop, q to quit."""

import curses
import time

from gpiozero import DigitalOutputDevice, Motor, Robot

import config

SPEED = 0.5

stdscr = None
slp = None

try:
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.nodelay(1)
    stdscr.addstr(0, 2, "w a s d to drive, e stop, q quit")

    slp = DigitalOutputDevice(config.SLEEP_PIN)
    slp.on()

    robot = Robot(
        left=Motor(**config.MOTOR_A),
        right=Motor(**config.MOTOR_B),
    )

    actions = {
        ord("w"): ("forward ", lambda: robot.forward(SPEED)),
        ord("s"): ("backward", lambda: robot.backward(SPEED)),
        ord("a"): ("left    ", lambda: robot.left(SPEED)),
        ord("d"): ("right   ", lambda: robot.right(SPEED)),
        ord("e"): ("stop    ", robot.stop),
    }

    # curses reports presses but never releases, so a key held down arrives
    # as repeats and letting go just means the repeats stop
    # the terminal waits before it starts repeating a held key, so the first
    # press gets a long grace period and the rest get a short one
    STOP_AFTER = 0.1
    FIRST_HOLD = 0.7
    REPEAT_GAP = 0.25

    last_press = 0.0
    prev_press = 0.0
    moving = False

    while True:
        stdscr.refresh()
        key = stdscr.getch()
        now = time.monotonic()

        if key == ord("q"):
            break

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
