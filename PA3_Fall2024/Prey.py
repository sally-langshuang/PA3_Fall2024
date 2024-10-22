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
    name = "George"

    def __init__(self, postion, shaderProg, size=1):
        super(Prey, self).__init__(postion)
        bound = Cube(Point((0,0,0)), shaderProg, [0.30, 0.45, 0.25], Ct.WHITE)
        bound = Cube(Point((0,0,0)), shaderProg, [0.30/2, 0.45/2, 0.25/2], Ct.WHITE)
        # self.addChild(bound)
        body = Body(self, Point((0, 0.3*size, -0.2 * size)), shaderProg, size=size)
        head = Head(body.c_dict['body'], Point((0, 0, 0)), shaderProg, size=size)
        self.components = body.components + head.components + [bound]
        self.c_dict = {**body.c_dict, **head.c_dict, 'bound': bound}
        self.rotation_speed = []
        for comp in self.components:
            comp.setRotateExtent(comp.uAxis, 0, 35)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)

        self.rotation_speed.append([0.5, 0, 0])
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 4
        self.species_id = 1

        left_leg = self.c_dict['left_leg_joint0']
        right_leg = self.c_dict['right_leg_joint0']
        self.rotation_speed = []
        speed = 5
        for i, leg in enumerate([left_leg, right_leg]):
            leg.setRotateExtent(leg.uAxis, leg.default_uAngle - 35, leg.default_uAngle + 35)
            leg.setRotateExtent(leg.vAxis, leg.default_vAngle - 45, leg.default_vAngle + 45)
            leg.setRotateExtent(leg.wAxis, leg.default_wAngle - 45, leg.default_wAngle + 45)
            self.rotation_speed.append([0.5 *speed if i %2 == 0 else -0.5*speed,0, 0])

        left_arm = self.c_dict['left_arm_joint0']
        right_arm = self.c_dict['right_arm_joint0']
        for i, arm in enumerate([left_arm, right_arm]):
            arm.setRotateExtent(leg.uAxis, arm.default_uAngle - 35, arm.default_uAngle + 35)
            arm.setRotateExtent(leg.vAxis, arm.default_vAngle - 45, arm.default_vAngle + 45)
            arm.setRotateExtent(leg.wAxis, arm.default_wAngle - 45, arm.default_wAngle + 45)
            self.rotation_speed.append([-0.5 *speed if i %2 ==0 else 0.5* speed, 0, 0])


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
        pass
        # left_leg = self.c_dict['left_leg_joint0']
        # right_leg = self.c_dict['right_leg_joint0']
        # left_arm = self.c_dict['left_arm_joint0']
        # right_arm = self.c_dict['right_arm_joint0']
        # for i, comp in enumerate([left_leg, right_leg, left_arm, right_arm]):
        #     # print(f'before {comp.uAngle}, {comp.vAngle}, {comp.wAngle}, {comp.uRange}, {comp.vRange}, {comp.wRange}')
        #     comp.rotate(self.rotation_speed[i][0], comp.uAxis)
        #     comp.rotate(self.rotation_speed[i][1], comp.vAxis)
        #     comp.rotate(self.rotation_speed[i][2], comp.wAxis)
        #     if comp.uAngle + self.rotation_speed[i][0] >= comp.uRange[1] or comp.uAngle + self.rotation_speed[i][0] <= comp.uRange[0]:  # rotation reached the limit
        #         self.rotation_speed[i][0] *= -1
        #     if comp.vAngle + self.rotation_speed[i][1] >= comp.vRange[1] + self.rotation_speed[i][1] or comp.vAngle <= comp.vRange[0]:
        #         self.rotation_speed[i][1] *= -1
        #     if comp.wAngle + self.rotation_speed[i][2] >= comp.wRange[1] or comp.wAngle + self.rotation_speed[i][2] <= comp.wRange[0]:
        #         self.rotation_speed[i][2] *= -1
        #     # print(f'{comp.uAngle}, {comp.vAngle}, {comp.wAngle}, {comp.uRange}, {comp.vRange}, {comp.wRange}')

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
        self.name = "head"
        head = Sphere(Point((0 *size, 0.14 *size, 0.2 *size)), shaderProg, [0.2 *size, 0.2 *size, 0.2 *size],
                      Ct.PINK)
        head.setDefaultAngle(-90, head.uAxis)
        head.setDefaultAngle(0, head.wAxis)
        head.setRotateExtent(head.uAxis, -45, 45)
        head.setRotateExtent(head.vAxis, -45, 45)
        head.setRotateExtent(head.wAxis, -45, 45)

        nose = Cylinder(Point((0 *size, -0.08 *size, 0.16 *size)), shaderProg, [0.06 *size, 0.05 *size, 0.075 *size], Ct.PINK)
        nose.setDefaultAngle(90, nose.uAxis)

        parent.addChild(self)
        self.addChild(head)
        head.addChild(nose)
        self.components = [head, nose]
        self.c_dict = {"head": head, "nose": nose}
        AddMirror(self, [nose, nose], Cylinder, (0.03 *size, 0 *size, 0 *size), shaderProg, [0.02 *size, 0.02 *size, 0.076 *size], Ct.SOFTRED, "nostril")
        l_eyeball, r_eyeball = AddMirror(self, [head, head], Sphere, (0.12 *size, -0.1 *size, 0.1 *size), shaderProg, [0.045 *size, 0.045 *size, 0.045 *size], Ct.WHITE, "eyeball", [-20, 0, 20])
        AddMirror(self, [l_eyeball, r_eyeball], Sphere, (0 *size, -0.02 *size, 0 *size), shaderProg, [0.03 *size, 0.03 *size, 0.03 *size], Ct.BLACK, "pupil", [0, 0, 0])

        AddMirror(self, [head, head], Sphere, (0.10 *size, -0.02 *size, 0.18 *size), shaderProg,
                                         [0.04 *size, 0.008 *size, 0.08 *size], Ct.PINK, "ear", [0, 0, 0])


def AddMirror(self, parents, shape, pos, shaderProg, size, color, name, angle=[0, 0, 0]):
    l = shape(Point(pos), shaderProg, size, color)
    r = shape(Point(tuple(x if i != 0 else -x for i, x in enumerate(pos))), shaderProg, size, color)
    for i, prefix, c, parent in zip(range(2), ['left', 'right'], [l, r], parents):
        for j, a in enumerate(angle):
            a = a % 360
            if a  == 0: continue

            x = None
            if j == 0:
                x = c.uAxis
            elif j == 1:
                x = c.vAxis
                if i % 2 == 1:
                  a = -a
            elif j == 2:
                x = c.wAxis
                if i % 2 == 1:
                  a = -a

            if x is not None:
                c.setDefaultAngle(a, x)

        self.components.append(c)
        self.c_dict[prefix +"_"+ name] = c
        parent.addChild(c)
    return l, r



class Body(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None, size=1):
        super().__init__(position, display_obj)
        body = Sphere(Point((0, 0, 0)), shaderProg, [0.20 *size, 0.20 *size, 0.18 *size],
                      Ct.BLUE, lowPoly=True)

        left_arm = Arm(body, Point((0.08 *size, 0.08 *size, 0*size)), shaderProg, size=size)
        right_arm = Arm(body, Point((-0.08 *size, 0.08 *size, 0 *size)), shaderProg, mirror=True, size=size)

        left_leg = Leg(body, Point((0.06 *size, -0.09 *size, 0 *size)), shaderProg, size=size)
        right_leg = Leg(body, Point((-0.06 *size, -0.09 *size, 0 *size)), shaderProg, mirror=True, size=size)

        parent.addChild(self)
        self.addChild(body)
        body.addChild(left_arm)
        body.addChild(right_arm)
        body.addChild(left_leg)
        body.addChild(right_leg)

        self.components = [body] + left_arm.components + right_arm.components + left_leg.components + right_leg.components
        self.c_dict = {'body': body, **left_arm.c_dict, **right_arm.c_dict, **left_leg.c_dict, **right_leg.c_dict}

class Arm(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None, mirror=False, size=1):
        super().__init__(position, display_obj)
        limb_len = 0.08 * size
        limb_width = 0.01 * size

        joint0 = Sphere(position, shaderProg, [limb_width, limb_width, limb_width], Ct.PINK)
        if not mirror:
            joint0.setDefaultAngle(45, joint0.vAxis)
        else:
            joint0.setDefaultAngle(-45, joint0.vAxis)
        joint0.setDefaultAngle(90, joint0.uAxis)

        limb0 = Cylinder(Point((0, 0, limb_len)), shaderProg, [limb_width, limb_width, limb_len], Ct.PINK)

        joint1 = Sphere(Point((0, 0, limb_len)), shaderProg, [limb_width, limb_width, limb_width], Ct.PINK)


        finger_lenth = 0.025 *size
        figer_width = 0.008 *size
        finger_angle = 55
        finger0 = Cylinder(Point((0, 0, finger_lenth)), shaderProg, [figer_width, figer_width, finger_lenth], Ct.PINK)
        finger0.setDefaultAngle(finger_angle, finger0.uAxis)

        finger1 = Cylinder(Point((0, 0, finger_lenth)), shaderProg, [figer_width, figer_width, finger_lenth], Ct.PINK)


        finger2 = Cylinder(Point((0, 0, finger_lenth)), shaderProg, [figer_width, figer_width, finger_lenth], Ct.PINK)
        finger2.setDefaultAngle(-finger_angle, finger0.uAxis)


        parent.addChild(self)
        self.addChild(joint0)
        joint0.addChild(limb0)
        limb0.addChild(joint1)
        joint1.addChild(finger0)
        joint1.addChild(finger1)
        joint1.addChild(finger2)
        self.components = [joint0, limb0, joint1, finger0, finger1, finger2]
        if not mirror:
            self.c_dict = {'left_arm_joint0': joint0, 'left_arm_limb0': limb0, 'left_arm_joint1': joint1,  'left_arm_finger0': finger0, 'left_arm_finger1': finger1, 'left_arm_finger2': finger2}
        else:
            self.c_dict = {'right_arm_joint0': joint0, 'right_arm_limb0': limb0, 'right_arm_joint1': joint1,
                           'right_arm_finger0': finger0, 'right_arm_finger1': finger1, 'right_arm_finger2': finger2}

class Leg(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None, mirror=False, size= 1):
        super().__init__(position, display_obj)
        limb_len = 0.09 * size
        limb_width = 0.01 * size

        joint0 = Sphere(position, shaderProg, [limb_width, limb_width, limb_width], Ct.PINK)
        if not mirror:
            joint0.setDefaultAngle(180, joint0.vAxis)
        else:
            joint0.setDefaultAngle(-180, joint0.vAxis)
        joint0.setDefaultAngle(-90, joint0.uAxis)

        limb0 = Cylinder(Point((0, 0, limb_len)), shaderProg, [limb_width, limb_width, limb_len], Ct.PINK)

        joint1 = Sphere(Point((0, 0, limb_len)), shaderProg, [limb_width, limb_width, limb_width], Ct.PINK)

        shoe_board = Cylinder(Point((0, -0.02 * size, 0)), shaderProg, [0.025 * size, 0.05*size, 0.015*size], Ct.BLACK)
        shoe_head = Sphere(Point((0, -0.025*size, -0.01*size)), shaderProg, [0.032*size, 0.032*size, 0.025*size], Ct.BLACK)

        parent.addChild(self)
        self.addChild(joint0)
        joint0.addChild(limb0)
        limb0.addChild(joint1)
        joint1.addChild(shoe_board)
        shoe_board.addChild(shoe_head)
        self.components = [joint0, limb0, joint1, shoe_board, shoe_head]
        if not mirror:
            self.c_dict = {'left_leg_joint0': joint0, 'left_leg_limb0': limb0, 'left_leg_joint1': joint1, 'left_leg_shoe_board': shoe_board, 'left_leg_shoe_head': shoe_head}
        else:
            self.c_dict = {'right_leg_joint0': joint0, 'right_leg_limb0': limb0, 'right_leg_joint1': joint1, 'right_leg_shoe_board': shoe_board, 'right_leg_shoe_head': shoe_head}