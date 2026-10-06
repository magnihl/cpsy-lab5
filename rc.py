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
    STOP_AFTER = 0.4
    last_press = 0.0
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
            last_press = now
            moving = True
        elif moving and now - last_press > STOP_AFTER:
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
