"""
This is the main entry of your program. Almost all things you need to implement are in this file.
The main class Sketch inherits from CanvasBase. For the parts you need to implement, they are all marked with TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.1.1

Modified by Daniel Scrivener 07/2022
Modified by Ruichen (Richard) Liu 10/2024
"""

import os
import math
import copy
import random
import time

import numpy as np

from Point import Point
from CanvasBase import CanvasBase
import ColorType
from GLProgram import GLProgram
from GLBuffer import VAO, VBO, EBO, Texture
from Vivarium import Vivarium
from Quaternion import Quaternion
import GLUtility


try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")
try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError
try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class Sketch(CanvasBase):
    """
    Drawing methods and interrupt methods will be implemented in this class.
    
    Variable Instruction:
        * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging

        
    Method Instruction:
        
        
    Here are the list of functions you need to override:
        * Interrupt_MouseL: Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
        * Interrupt_MouseLeftDragging: Used to deal with mouse dragging interruption.
        * Interrupt_Keyboard: Used to deal with keyboard press interruption. Use this to add new keys or new methods
        
    Here are some public variables in parent class you might need:
        
        
    """
    context = None

    debug = 1

    last_mouse_leftPosition = None
    last_mouse_middlePosition = None
    components = None

    texture = None
    shaderProg = None
    glutility = None

    frameCount = 0

    lookAtPt = None
    upVector = None
    # use these three to control camera position, mainly used in mouse dragging
    cameraDis = None
    cameraTheta = None  # theta on horizontal sphere cut, in range [0, 2pi]
    cameraPhi = None  # in range [-pi, pi], for smooth purpose

    viewMat = None
    perspMat = None

    pauseScene = False

    # If you are having trouble rotating the camera, try increasing this parameter
    # (Windows users with trackpads may need this)
    MOUSE_ROTATE_SPEED = 1
    MOUSE_SCROLL_SPEED = 2.5

    # models
    basisAxes = None
    scene = None

    select_obj_index = -1
    select_color = [ColorType.ColorType(1, 0, 0), ColorType.ColorType(0, 1, 0), ColorType.ColorType(0, 0, 1)]


    def __init__(self, parent):
        """
        Init everything. You should set your model here.
        """
        super(Sketch, self).__init__(parent)
        # prepare OpenGL context
        # Initialize context attributes, this is needed by MacOS!
        contextAttrib = glcanvas.GLContextAttrs()
        contextAttrib.PlatformDefaults().CoreProfile().MajorVersion(3).MinorVersion(3).EndList()
        self.context = glcanvas.GLContext(self, ctxAttrs=contextAttrib)

        # Initialize Parameters
        self.last_mouse_leftPosition = [0, 0]
        self.last_mouse_middlePosition = [0, 0]
        self.components = []
        self.select_components = []

        # add components to top level
        self.resetView()

        self.glutility = GLUtility.GLUtility()
        self.backgroundColor = ColorType.BLUEGREEN

    def resetView(self):
        self.lookAtPt = [0, 0, 0]
        self.upVector = [0, 1, 0]
        self.cameraDis = 12
        self.cameraPhi = math.pi / 6
        self.cameraTheta = math.pi / 2

    def InitGL(self):
        # self.texture = Texture()

        self.shaderProg = GLProgram()
        self.shaderProg.compile()

        # instantiate models, this can only be done with a compiled GL program
        self.vivarium = Vivarium(self, self.shaderProg)
        
        self.topLevelComponent.clear()
        self.topLevelComponent.addChild(self.vivarium)
        self.topLevelComponent.initialize()

        self.components = self.vivarium.components
        self.c_dict = self.vivarium.c_dict
        self.obj_dict = self.vivarium.obj_dict

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClearDepth(1.0)
        gl.glViewport(0, 0, self.size[0], self.size[1])

        # enable depth checking
        gl.glEnable(gl.GL_DEPTH_TEST)

        # set basic viewing matrix
        self.perspMat = self.glutility.perspective(45, self.size.width, self.size.height, 0.01, 100)
        self.shaderProg.setMat4("projectionMat", self.perspMat)
        self.shaderProg.setMat4("viewMat", self.glutility.view(self.getCameraPos(), self.lookAtPt, self.upVector))
        self.shaderProg.setMat4("modelMat", np.identity(4))

    def getCameraPos(self):
        ct = math.cos(self.cameraTheta)
        st = math.sin(self.cameraTheta)
        cp = math.cos(self.cameraPhi)
        sp = math.sin(self.cameraPhi)
        result = [self.lookAtPt[0] + self.cameraDis * ct * cp,
                  self.lookAtPt[1] + self.cameraDis * sp,
                  self.lookAtPt[2] + self.cameraDis * st * cp]
        return result

    def OnResize(self, event):
        contextAttrib = glcanvas.GLContextAttrs()
        contextAttrib.PlatformDefaults().CoreProfile().MajorVersion(3).MinorVersion(3).EndList()
        self.context = glcanvas.GLContext(self, ctxAttrs=contextAttrib)

        self.size = self.GetClientSize()
        self.size[1] = max(1, self.size[1])  # avoid divided by 0
        self.SetCurrent(self.context)

        self.init = False
        self.Refresh(eraseBackground=True)
        self.Update()

    def OnPaint(self, event=None):
        """
        This will be called at every frame
        """
        self.SetCurrent(self.context)
        if not self.init:
            # Init the OpenGL environment if not initialized
            self.InitGL()
            self.init = True
        # the draw method
        self.OnDraw()

    def OnDraw(self):
        gl.glClearColor(*self.backgroundColor, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # These are per-frame updates to the shader! Update the viewing matrix and the joint transforms
        self.viewMat = self.glutility.view(self.getCameraPos(), self.lookAtPt, self.upVector)
        self.shaderProg.setMat4("viewMat", self.viewMat)

        self.topLevelComponent.update(np.identity(4))
        self.topLevelComponent.draw(self.shaderProg)

        # perform the next step of the animation
        self.vivarium.animationUpdate()

        self.SwapBuffers()

    def _adjust_size(self, event):
        keycode = event.GetUnicodeKey()
        angle = 10
        pos = 0.02
        scale = 0.1
        q_size = 30
        if keycode == ord('U') or keycode == ord('u') or keycode == ord('V') or keycode == ord('v') or keycode == ord(
                'W') or keycode == ord('w'):
            size = angle
        elif keycode == ord('X') or keycode == ord('x') or keycode == ord('Y') or keycode == ord('y') or keycode == ord(
                'Z') or keycode == ord('z'):
            size = pos
        elif keycode == ord('L') or keycode == ord('l') or keycode == ord('K') or keycode == ord('k') or keycode == ord(
                'G') or keycode == ord('g'):
            size = scale
        elif keycode == ord('S') or keycode == ord('s') or keycode == ord('A') or keycode == ord('a') or keycode == ord('B') or keycode == ord('b') or keycode == ord('C') or keycode == ord('c'):
            size = q_size
        else:
            return None
        if event.ShiftDown():
            pass
        else:
            size = -size
        if event.ControlDown():
            size = size / 10
        return size

    def _adjust_angle(self, target, keycode, size, mirror=False):
        if keycode == ord('u') or keycode == ord('U'):
            target.setDefaultAngle(target.uAngle + size, target.uAxis)
        elif keycode == ord('v') or keycode == ord('V'):
            if mirror:
                target.setDefaultAngle(target.vAngle - size, target.vAxis)
                return
            target.setDefaultAngle(target.vAngle + size, target.vAxis)
        elif keycode == ord('w') or keycode == ord('W'):
            if mirror:
                target.setDefaultAngle(target.wAngle - size, target.wAxis)
                return
            target.setDefaultAngle(target.wAngle + size, target.wAxis)
        else:
            return

    def _adjust_pos(self, target, keycode, size, mirror=False):
        if keycode == ord('x') or keycode == ord('X'):
            j = 0
            if mirror:
                size = -size
        elif keycode == ord('y') or keycode == ord('Y'):
            j = 1
        elif keycode == ord('z') or keycode == ord('Z'):
            j = 2
        else:
            return
        p = Point(tuple(c + size if i == j else c for i, c in enumerate(target.currentPos)))
        target.setDefaultPosition(p)

    def _adjust_scale(self, target, keycode, size):
        if keycode == ord('l') or keycode == ord('L'):
            i = 0
        elif keycode == ord('k') or keycode == ord('K'):
            i = 1
        elif keycode == ord('g') or keycode == ord('G'):
            i = 2
        else:
            return
        sc = copy.deepcopy(target.currentScaling)
        sc[i] = sc[i] + size if sc[i] + size > 0 else 0.001
        target.setDefaultScale(sc)

    def _select_target(self, event):
        keycode = event.GetKeyCode()
        select_components = self.vivarium.obj_dict['prey'].components
        if keycode in [wx.WXK_LEFT]:
            if len(select_components) > 0:
                select_components[self.select_obj_index].reset("color")
                self.select_obj_index = (self.select_obj_index - 1) % len(select_components)
                select_components[self.select_obj_index].setCurrentColor(self.select_color[0])
            self.update()
        elif keycode in [wx.WXK_RIGHT]:
            if len(select_components) > 0:
                select_components[self.select_obj_index].reset("color")
                self.select_obj_index = (self.select_obj_index + 1) % len(select_components)
                select_components[self.select_obj_index].setCurrentColor(self.select_color[0])
            self.update()
        target = select_components[self.select_obj_index]
        return target

    def _get_mirror(self, target):
        for name, c in self.c_dict.items():
            if c is target:
                if len(name.split('_', 1)) == 2:
                    pre, suf = name.split('_', 1)
                    if pre == 'left':
                        mirror_name = 'right_' + suf
                        print(f'target {name}, mirror {mirror_name}')
                        return self.c_dict[mirror_name]
                    elif pre == 'right':
                        mirror_name = 'left_' + suf
                        print(f'target {name}, mirror {mirror_name}')
                        return self.c_dict[mirror_name]
        return None

    def adjust(self, event):
        target = self._select_target(event)
        keycode = event.GetUnicodeKey()
        if self.select_obj_index < 0 or target is None:
            return
        size = self._adjust_size(event)
        if size is None:
            return

        self._adjust_angle(target, keycode, size)
        self._adjust_pos(target, keycode, size)
        self._adjust_scale(target, keycode, size)
        print(
            f"current u: {target.uAngle} v: {target.vAngle} w: {target.wAngle}  pos: {target.currentPos}, scale: {target.currentScaling}")
        mirror = self._get_mirror(target)
        if mirror is not None:
            self._adjust_angle(mirror, keycode, size, mirror=True)
            self._adjust_pos(mirror, keycode, size, mirror=True)
            self._adjust_scale(mirror, keycode, size)


    def OnDestroy(self, event):
        """
        Window destroy event binding

        :param event: Window destroy event
        :return: None
        """
        if self.shaderProg is not None:
            del self.shaderProg
        super(Sketch, self).OnDestroy(event)

    def Interrupt_Scroll(self, wheelRotation):
        """
        When mouse wheel rotating detected, do following things

        :param wheelRotation: mouse wheel changes, normally +120 or -120
        :return: None
        """
        if wheelRotation == 0:
            return
        wheelChange = wheelRotation / abs(wheelRotation)
        self.cameraDis = max(self.cameraDis - wheelChange * 0.1, 0.01)
        self.update()

    def unprojectCanvas(self, x, y, u=0.5):
        """
        unproject a canvas point to world coordiantes. 2D -> 3D
        you need give an extra parameter u, to tell the method how far are you from znear
        u is the proportion of distance to znear / zfar-znear
        in the gluUnProject, the distribution of z is not linear when using perspective projection,
        so z=0.5 is not in the middle,
        that's why we compute out the ray and use linear interpolation and u to get the point

        :param u: u is the proportion to the znear/, in range [0, 1]
        :type u: float
        """
        result1 = self._unproject(x, y, 0.0)
        result2 = self._unproject(x, y, 1.0)
        result = Point([(1 - u) * r1 + u * r2 for r1, r2 in zip(result1, result2)])
        return result

    def _unproject(self, x, y, z):
        model_matrix = np.identity(4)
        proj_matrix = self.viewMat @ self.perspMat
        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        model_view_proj_matrix = proj_matrix @ model_matrix
        inv_model_view_proj_matrix = np.linalg.inv(model_view_proj_matrix)

        x_ndc = (x - viewport[0]) / viewport[2] * 2.0 - 1.0
        y_ndc = (y - viewport[1]) / viewport[3] * 2.0 - 1.0
        z_ndc = 2.0 * z - 1.0
        
        ndc_coords = np.array([x_ndc, y_ndc, z_ndc, 1.0])
        world_coords = inv_model_view_proj_matrix.T @ ndc_coords # transpose because they are row-major
        if world_coords[3] != 0:
            world_coords /= world_coords[3]
        return world_coords[:3]

    def Interrupt_MouseL(self, x, y):
        """
        When mouse click detected, store current position in last_mouse_leftPosition

        :param x: Mouse click's x coordinate
        :type x: int
        :param y: Mouse click's y coordinate
        :type y: int
        :return: None
        """
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def Interrupt_MouseMiddleDragging(self, x, y):
        """
        When mouse drag motion with middle key detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """

        if self.new_dragging_event:
            self.last_mouse_middlePosition[0] = x
            self.last_mouse_middlePosition[1] = y
            return

        originalMidPt = self.unprojectCanvas(*self.last_mouse_middlePosition, 0.5)

        self.last_mouse_middlePosition[0] = x
        self.last_mouse_middlePosition[1] = y

        currentMidPt = self.unprojectCanvas(x, y, 0.5)
        changes = currentMidPt - originalMidPt
        moveSpeed = 0.185 * self.cameraDis / 6
        self.lookAtPt = [self.lookAtPt[0] - changes[0] * moveSpeed,
                         self.lookAtPt[1] - changes[1] * moveSpeed,
                         self.lookAtPt[2] - changes[2] * moveSpeed]

    def Interrupt_MouseLeftDragging(self, x, y):
        """
        When mouse drag motion detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """

        if self.new_dragging_event:
            self.last_mouse_leftPosition[0] = x
            self.last_mouse_leftPosition[1] = y
            return

        # Change viewing angle when dragging happened
        dx = x - self.last_mouse_leftPosition[0]
        dy = y - self.last_mouse_leftPosition[1]

        # restrict phi movement range, stop cameraphi changes at pole points
        self.cameraPhi = min(math.pi / 2, max(-math.pi / 2, self.cameraPhi - dy / 50))
        self.cameraTheta += dx / 100 * (self.MOUSE_ROTATE_SPEED)

        self.cameraTheta = self.cameraTheta % (2 * math.pi)

        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def update(self):
        """
        Update current canvas
        :return: None
        """
        self.topLevelComponent.update(np.identity(4))

    def Interrupt_Keyboard(self, keycode):
        """
        Keyboard interrupt bindings

        :param keycode: wxpython keyboard event's keycode
        :return: None
        """
        # Default Scene
        if chr(keycode) in "rR":
            # reset viewing angle
            self.viewing_quaternion = Quaternion()
            self.update()
        
        # A test scene with only one (1) predator and one (1) prey
        if chr(keycode) in "tT":
            # reset viewing angle
            self.viewing_quaternion = Quaternion()
            self.update()
        if keycode in [wx.WXK_ESCAPE]:
            # exit component editing mode
            self.select_components[self.select_obj_index].reset("color")
            self.select_obj_index = -1
            self.update()

if __name__ == "__main__":
    print("This is the main entry! ")
    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame, here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test",
                     style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)  # Disable Resize: ^ wx.RESIZE_BORDER
    canvas = Sketch(frame)

    frame.Show()
    app.MainLoop()
