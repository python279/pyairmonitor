# -*- coding: utf-8 -*-
#
# lhq@python279.org


import RPi.GPIO as GPIO


class Switch:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(37, GPIO.OUT)
        GPIO.output(37, False)

    def on(self):
        GPIO.output(37, True)

    def off(self):
        GPIO.output(37, False)

    def state(self):
        return GPIO.input(37)
