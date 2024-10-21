import random

from Component import Component
from Shapes import *
from Point import Point
import ColorType as Ct
from EnvironmentObject import EnvironmentObject

class Prey(Component, EnvironmentObject):
    components = None
    rotation_speed = None
    translation_speed = None

    def __init__(self, parent, postion, shaderProg):
        super(Prey, self).__init__(postion)
        body = Body(parent, Point((0, 0, 0)), shaderProg)
        head = Head(body, Point((0, 0, 0)), shaderProg)

        self.components = head.components + body.components
        self.addChild(body)
        body.addChild(head)

        self.rotation_speed = []
        for comp in self.components:
            comp.setRotateExtent(comp.uAxis, 0, 35)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)

        self.rotation_speed.append([0.5, 0, 0])
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 4
        self.species_id = 1

    def stepForward(self, components, tank_dimensions, vivarium):
        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.
        pass

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.
        # create periodic animation for creature joints

        pass
        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.


class Head(Component):
    def __init__(self, parent, position, shaderProg, size=1, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        head = Sphere(Point((0, 0, 0)), shaderProg, [0.15, 0.15, 0.15],
                      Ct.PINK)

        head.setRotateExtent(head.uAxis, -45, 45)
        head.setRotateExtent(head.vAxis, -45, 45)
        head.setRotateExtent(head.wAxis, -45, 45)

        self.addChild(head)
        self.components = [head]


class Body(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        body = Sphere(Point((0, 0, 0)), shaderProg, [0.2, 0.2, 0.2],
                      Ct.BLUE)

        body.setDefaultAngle(-90, body.uAxis)

        self.addChild(body)
        self.components = [body]
