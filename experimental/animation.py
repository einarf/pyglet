#!/usr/bin/env python

'''
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import sys

from pyglet import clock
from pyglet import image
from pyglet import window

w = window.Window()

class AnimationPlayer(object):
    expected_delay = 0

    def __init__(self, animation):
        self.animation = animation
        self.index = -1
        self.next_frame(0)

    def next_frame(self, dt):
        self.index = (self.index + 1) % len(self.animation.frames)
        frame = self.animation.frames[self.index]
        if frame.delay is not None:
            delay = frame.delay - (self.expected_delay - dt)
            delay = min(max(0, delay), frame.delay)
            clock.schedule_once(self.next_frame, delay)
            self.expected_delay = delay

    def blit(self, x, y):
        self.animation.frames[self.index].image.blit(x, y)

animation = image.load_animation(sys.argv[1])
clock.tick()
player = AnimationPlayer(animation)

while not w.has_exit:
    clock.tick()

    w.dispatch_events()
    w.clear()
    player.blit(w.width//2, w.height//2)
    w.flip()
