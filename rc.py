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

    key = None
    while key != ord("q"):
        stdscr.refresh()
        key = stdscr.getch()
        if key in actions:
            label, action = actions[key]
            stdscr.addstr(1, 2, label)
            action()
        time.sleep(0.04)

finally:
    if slp is not None:
        slp.off()
    if stdscr is not None:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.endwin()
