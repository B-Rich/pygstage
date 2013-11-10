"""
Pygstage v0.1

Pygstage (pronounced "pig stage") is a Python module for Pygame that implements
a simple scene graph. A "stage" can be populated by "actor" objects, and a
"camera" delivers the pygame.Surface object to be rendered in the window.
Persistance and few other features are automatically handled by pygstage.

CURRENTLY THIS VERSION IS NOWHERE NEAR FINISHED OR EVEN RUNNABLE.


Pygstage requires Pygame to be installed. Pygame can be downloaded from http://pygame.org

Pygstage was developed by Al Sweigart (al@inventwithpython.com)
https://github.com/asweigart/pygcurse


Simplified BSD License:

Copyright 2013 Al Sweigart. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Al Sweigart ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Al Sweigart OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Al Sweigart.
"""

import pygame

# note - make this compatible with pygcurse, pyganim, and pygscratch



class Camera(object):
    def __init__(self, stage, width=None, height=None, x=0, y=0):
        self.stage = stage
        if width is None:
            width = None # TODO - need a way to get window size
        if height is None:
            height = None # TODO - need a way to get window size

        self.rect = pygame.Rect()

        self.follow = None # the Actor object that the camera follows
        self.wanderx = 0 # how far left and right from the center before the camera follows
        self.wantery = 0 # how far up and down from the center before the camera follows
        self.zoom = 1.0

    # The "wander" property is how far the followed Actor can stray from the camera before the camera follows.
    def _propgetwander(self):
        if self.wanderx == self.wandery:
            return self.wanderx
        else:
            return None # returns None if the wanderx and wandery don't match
    def _propsetwander(self, value):
        self.wanderx = value
        self.wandery = value
    wander = property(_propgetwander, _propsetwander)

    def blit(self):
        pass

    # TODO: handle special case where the followed actor is larger than the wander distance. ACTUALLY,
    # have it so that the wander distance only applies to the center of the followed actor. (Easier to implement)


class Actor(object):
    for attrname in ('top', 'left', 'bottom', 'right', 'topleft', 'bottomleft', 'topright', 'bottomright', 'midtop', 'midleft', 'midbottom', 'midright', 'center', 'centerx', 'centery', 'size', 'width', 'height', 'x', 'y', 'w', 'h'):
        exec("""def _propget%s(self): return self.rect.%s""" % (attrname, attrname))
        exec("""def _propset%s(self, value): self.rect.%s = value""" % (attrname, attrname))
        exec("""%s = property(_propget%s, _propset%s)""" % (attrname, attrname, attrname))

    def _propgetimage(self):
        return self.image
    def _propsetimage(self, value):
        if type(value) == str:
            self.image = pygame.image.load(value)
        else:
            self.image = value
        # TODO - add Pyganim compat
        self.rect = self.image.get_rect()


    def __init__(self, image, x=0, y=0):
        self.image = image
        self.visible = True
        self.x = x
        self.y = y
        #self.rotate = 0 # TODO - is this needed? What about scaling, etc.


class Stage(object):
    def _propgetbgcolor(self):
        return self.bgcolor
    def _propsetbgcolor(self, value):
        if type(value) == str:
            self.bgcolor = pygame.Color(value)
        elif type(value) in (tuple, list):
            self.bgcolor = pygame.Color(*value)
    bgcolor = property(_propgetbgcolor, _propsetbgcolor)

    def _propgetbackground(self):
        return self.background
    def _propsetbackground(self, value):
        if type(value) == str:
            self.background = pygame.image.load(value)
        else:
            self.background = value
        # TODO - handle animated backgrounds with Pyganim?
    background = property(_propgetbackground, _propsetbackground)

    def _propgetw(self):
        return self.width
    def _propsetw(self, value):
        self.width = value
    def _propgeth(self):
        return self.height
    def _propseth(self, value):
        self.height = value

    def __init__(self, width=None, height=None, bgcolor='black', background=None):
        # a width or height of None means an unlimited size in that dimension
        self.width = width
        self.height = height

        # TODO - actors needs to be special because changing it changes the z-order.
        self.actors = {} # can be either Actor objects or static images or PygAnim objects



        self.background = background # a tiled image for the background (supercedes bgcolor)

        self.layersOrder = ['foreground']
        self.layers = {'foreground': Layer()}

class Layer(object):
    def __init__(self):
        pass
