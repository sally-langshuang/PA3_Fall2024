"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener
"""

import numpy as np

from PA3_Fall2024.Predator import Predator
from Point import Point
from Component import Component
from ModelTank import Tank
from EnvironmentObject import EnvironmentObject
from ModelLinkage import Linkage
from Prey import Prey


class Vivarium(Component):
    """
    The Vivarium for our animation
    """
    components = None  # List
    c_dict = None
    obj_dict = None
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent, shaderProg):
        self.parent = parent
        self.shaderProg = shaderProg

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(Point((0, 0, 0)), shaderProg, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]
        self.k_c_dict = dict()
        self.c_k_dict = dict()
        self.obj_dict = dict()
        # self.addNewObjInTank(Linkage(parent, Point((0, 0, 0)), shaderProg))
        self.addNewObjInTank(Prey(Point((1, 1, 1)), shaderProg), "prey0")
        self.addNewObjInTank(Prey(Point((-1, 1, 1)), shaderProg), "prey1")
        self.addNewObjInTank(Predator(Point((0, 0, 0)), shaderProg), "predator0")

    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """

        for c in self.components[::-1]:
            if isinstance(c, EnvironmentObject):
                c.animationUpdate()
                c.stepForward(self.components, self.tank_dimensions, self)

        self.update()

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            self.tank.children.remove(obj)
            self.components.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent, name=""):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
            if name != "":
                self.obj_dict[name] = newComponent
                for k, v in newComponent.c_dict.items():
                    k = k + "_" + name
                    self.k_c_dict[k] = v
                    self.c_k_dict[v] = k
        if isinstance(newComponent, EnvironmentObject):
            # add environment components list reference to this new object's
            newComponent.env_obj_list = self.components
