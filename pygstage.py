"""
Pygstage v0.1

Pygstage (pronounced "pig stage") is a Python module for Pygame that implements
a simple scene graph. A "stage" can be populated by "actor" objects, and a
"camera" delivers the pygame.Surface object to be rendered in the window.
Persistance, layers, and few other features are automatically handled by pygstage.

CURRENTLY THIS VERSION IS NOWHERE NEAR FINISHED OR EVEN RUNNABLE.


Pygstage requires Pygame to be installed. Pygame can be downloaded from http://pygame.org

Pygstage was developed by Al Sweigart (al@inventwithpython.com)
https://github.com/asweigart/pygstage


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
    """TODO docstring"""

    def __init__(self, stage, rect=None, width=None, height=None, x=0, y=0, follow=None, wander=None, wanderx=0, wandery=0, zoom=1.0):
        """TODO docstring"""
        self.follow = follow
        self.zoom = zoom

        # If rect is set, then it overrides width, height, x, and y.
        if rect is None:
            if width is None or height is None:
                raise TypeError('Arguments for width and height are required if no rect argument is given')

            self._rect = pygame.Rect(0, 0, width, height)
            self._rect.centerx = x
            self._rect.centery = y
        else:
            self._rect = pygame.Rect(rect)

        # If wander is set, then it overrides wanderx and wandery.
        if wander is not None:
            self.wander = wander
        else:
            self.wanderx = wanderx
            self.wandery = wandery

        # Attach this camera to the stage
        self.stage = stage
        self.stage.cameras.append(self) # TODO - note, stage has to implement list stuff

    # stage property
    def _propgetstage(self):
        return self._stage

    def _propsetstage(self, value):
        # stage can only be a pygstage Stage object.
        if value.__class__.__name__ != 'Stage':
            raise TypeError('Camera stage must be a Stage object')
        self._stage = value

    stage = property(_propgetstage, _propsetstage)


    # wander property
    def _propgetwander(self):
        if self._wanderx == self._wandery:
            return self._wanderx
        else:
            return None # returns None if the wanderx and wandery don't match

    def _propsetwander(self, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError('Camera wander must be positive: %.200s' % (value))
            self._wanderx = value
            self._wandery = value
        except (ValueError, TypeError):
            raise TypeError('Camera wander must be castable to int: %.200s' % (value))

    wander = property(_propgetwander, _propsetwander)


    # wanderx property
    def _propgetwanderx(self):
        return self._wanderx

    def _propsetwanderx(self, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError('Camera wanderx must be positive: %.200s' % (value))
            self._wanderx = value
        except (ValueError, TypeError):
            raise TypeError('Camera wanderx must be castable to int: %.200s' % (value))

    wanderx = property(_propgetwanderx, _propsetwanderx)


    # wandery property
    def _propgetwandery(self):
        return self._wandery

    def _propsetwandery(self, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError('Camera wandery must be positive: %.200s' % (value))
            self._wandery = value
        except (ValueError, TypeError):
            raise TypeError('Camera wandery must be castable to int: %.200s' % (value))

    wandery = property(_propgetwandery, _propsetwandery)


    # rect property
    def _propgetrect(self):
        return self._rect

    def _propsetrect(self, value):
        try:
            self._rect = pygame.Rect(value)
            self._surface = pygame.Surface((self._rect.width, self._rect.height))
        except TypeError:
            raise TypeError('Camera rect must be rect style object')

    rect = property(_propgetrect, _propsetrect)


    # Setting up properties so the user only needs to type camObj.left, instead of camObj.rect.left.
    for attrname in ('top', 'left', 'bottom', 'right', 'topleft', 'bottomleft', 'topright', 'bottomright', 'midtop', 'midleft', 'midbottom', 'midright', 'center', 'centerx', 'centery', 'x', 'y', 'w', 'h'):
        exec("""def _propget%s(self): return self._rect.%s""" % (attrname, attrname))
        exec("""def _propset%s(self, value):
            oldWidth = self._rect.width
            oldHeight = self._rect.height
            self._rect.%s = value
            if oldWidth != self._rect.width or oldHeight != self._rect.height:
                self._surface = pygame.Surface((self._rect.width, self._rect.height))
            if self._stage.width is not None:
                if self._rect.left < 0:
                    self._rect.left = 0
                elif self._rect.right > self._stage.width:
                    self._rect.right = self._stage.width
            if self._stage.height is not None:
                if self._rect.top < -self.0:
                    self._rect.top = -self.0
                if self._rect.bottom > self._stage.height:
                    self._rect.bottom = self._stage.height
            """ % (attrname, attrname))
        exec("""%s = property(_propget%s, _propset%s)""" % (attrname, attrname, attrname))

    # Setting up properties that change the size of the camera's Surface object.
    for attrname in ('size', 'width', 'height'):
        exec("""def _propget%s(self): return self._rect.%s""" % (attrname, attrname))
        exec("""def _propset%s(self, value):
            self._rect.%s = value
            self._surface = pygame.Surface((self._rect.width, self._rect.height))""" % (attrname, attrname))
        exec("""%s = property(_propget%s, _propset%s)""" % (attrname, attrname, attrname))

    # follow property
    def _propgetfollow(self):
        return self._follow

    def _propsetfollow(self, value):
        if value is not None:
            if value.__class__.__name__ != 'Actor':
                raise TypeError('Camera follow argument must be an Actor object')
        self._follow = value

    follow = property(_propgetfollow, _propsetfollow)


    # zoom property
    def _propgetzoom(self):
        return self._zoom

    def _propsetzoom(self, value):
        try:
            self.zoom = float(value)
        except (ValueError, TypeError):
            raise TypeError('Camera zoom argument must be castable to float: %.200s' % (value))

    zoom = property(_propgetzoom, _propsetzoom)


    def blit(self, destSurface, dest):
        """TODO docstring"""
        pass
        # Get the stage's actors
        self._stage._actors

        # Determine the position if this camera is following an actor
        self.center = self._follow.center

        # Draw the bgcolor and position the background
        self._surface.fill(self._stage.bgcolor) # TODO

        # Determine the collision rectangle if this camera is zoomed at all

        # Find the actors that intersect with this camera

        # Order the actors by their zorders

        # Draw all the actors

        # Blit the Camera's Surface object to destSurface








class Actor(object):
    def __init__(self, image, stage=None, x=0, y=0, zorder=0):
        """TODO docstring"""
        self._stage = stage
        self._stage._actors.append(self) # TODO - fix this when actors is set up for real
        self._zorder = zorder # TODO - eventually make this a property that updates the stage's idea of what the actors' zorders are. For now, the stage will just poll.

    # Setting up properties so the user only needs to type actorObj.left, instead of actorObj.rect.left.
    # NOTE - size, width, and height cannot be set since these are dependent on the image
    # TODO - wait, shouldn't this be modifying the image's rect?
    for attrname in ('top', 'left', 'bottom', 'right', 'topleft', 'bottomleft', 'topright', 'bottomright', 'midtop', 'midleft', 'midbottom', 'midright', 'center', 'centerx', 'centery', 'x', 'y', 'w', 'h'):
        exec("""def _propget%s(self): return self._rect.%s""" % (attrname, attrname))
        exec("""def _propset%s(self, value): self._rect.%s = value""" % (attrname, attrname))
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












class Stage(object):
    """TODO docstring"""


    def __init__(self, width=None, height=None, bgcolor='black', background=None):
        """TODO docstring"""
        # a width or height of None means an unlimited size in that dimension
        self.width = width
        self.height = height
        self.background = background # a tiled image for the background (supercedes bgcolor)
        self.bgcolor = bgcolor

        # TODO - eventually I'd like to subclass these so that these aren't just plain lists or dictionaries.
        self._actors = {} # keys are strings of actor names, values are Actor objects.
        self._cameras = {} # keys are strings of camera names, values are Camera objects.

    def _propgetbgcolor(self):
        return self._bgcolor
    def _propsetbgcolor(self, value):
        if type(value) == str:
            self._bgcolor = pygame.Color(value)
        elif type(value) in (tuple, list):
            self._bgcolor = pygame.Color(*value)
    bgcolor = property(_propgetbgcolor, _propsetbgcolor)


    def _propgetbackground(self):
        return self._background
    def _propsetbackground(self, value):
        if type(value) == str:
            self._background = pygame.image.load(value)
        else:
            self._background = value
        # TODO - handle animated backgrounds with Pyganim?
    background = property(_propgetbackground, _propsetbackground)


    def _propgetw(self):
        return self._width

    def _propsetw(self, value):
        self._width = int(value)

    width = property(_propgetw, _propsetw)
    w = width


    def _propgeth(self):
        return self._height

    def _propseth(self, value):
        self._height = int(value)

    height = property(_propgeth, _propseth)
    h = height

