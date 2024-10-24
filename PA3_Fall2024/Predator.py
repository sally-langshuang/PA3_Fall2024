from Shapes import *
from Point import Point
import ColorType as Ct
from EnvironmentObject import EnvironmentObject
from util import AddMirror

class Predator(Component, EnvironmentObject):
    def __init__(self, position, shaderProg, size=1):
        super(Predator, self).__init__(position)
        bound = Cube(Point((0, 0, 0)), shaderProg, [0.35 * size, 0.9 * size, 0.9 * size], Ct.WHITE)
        # self.addChild(bound)
        body = Body(self, Point((0, -0.04 * size, 0 * size)), shaderProg, size=size)
        tail = Tail(body.c_dict['body'], Point((0 * size, -0.02 * size, -0.02 * size)), shaderProg, size=size)
        neck = Neck(body.c_dict['body'], Point((0 * size, 0.04 * size, 0.12 * size)), shaderProg, size=size)
        head = Head(neck.c_dict['neck1'], Point((0 * size, 0.04 * size, 0.14 * size)), shaderProg, size=size)
        pre_l_leg = Leg(body.c_dict['body'], Point((0.04*size, 0*size, 0.12*size)), shaderProg, pre="pre", size=size)
        pre_r_leg = Leg(body.c_dict['body'], Point((-0.04*size, 0*size, 0.12*size)), shaderProg, pre = "pre",mirror=True, size=size)
        suf_l_leg = Leg(body.c_dict['body'], Point((0.04 * size, 0 * size, -0.06 * size)), shaderProg, pre="suf", size=size)
        suf_r_leg = Leg(body.c_dict['body'], Point((-0.04 * size, 0 * size, -0.06 * size)), shaderProg, pre="suf", mirror=True,
                        size=size)
        self.components = ([bound] + body.components +
                           head.components +
                           tail.components +
                           neck.components +
                           pre_l_leg.components + pre_r_leg.components +
                           suf_l_leg.components + suf_r_leg.components)
        self.c_dict = {
            'bound': bound,
            **body.c_dict,
            **tail.c_dict,
            **neck.c_dict,
            **head.c_dict,
            **pre_l_leg.c_dict, **pre_r_leg.c_dict,
            **suf_l_leg.c_dict, **suf_r_leg.c_dict}
        for limb1 in [self.c_dict['left_pre_leg_limb1'],self.c_dict['right_pre_leg_limb1'],self.c_dict['left_suf_leg_limb1'],self.c_dict['right_suf_leg_limb1']]:
            limb1.setRotateExtent(limb1.uAxis, 0, -20)
            limb1.setRotateExtent(limb1.vAxis, -90, 90)
            limb1.setRotateExtent(limb1.wAxis, -60, 60)

        for limb0 in [self.c_dict['left_pre_leg_limb0'],self.c_dict['right_pre_leg_limb0'],self.c_dict['left_suf_leg_limb0'],self.c_dict['right_suf_leg_limb0']]:
            limb0.setRotateExtent(limb1.uAxis, 40, -40)
            limb0.setRotateExtent(limb1.vAxis, -90, 90)
            limb0.setRotateExtent(limb1.wAxis, -60, 60)

        s0, s1 = 2, 1
        self.rotation_speed = [
            [s0, 0, 0], [-s1, 0, 0],
            [-s0, 0, 0], [-s1, 0, 0],
            [-s0, 0, 0], [-s1, 0, 0],
            [s0, 0, 0], [-s1, 0, 0],
        ]

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
        # print(f'before {comp.uAngle}, {comp.vAngle}, {comp.wAngle}, {comp.uRange}, {comp.vRange}, {comp.wRange}')
        limbs = [
            self.c_dict['left_pre_leg_limb0'], self.c_dict['left_pre_leg_limb1'],
            self.c_dict['right_pre_leg_limb0'], self.c_dict['right_pre_leg_limb1'],
            self.c_dict['left_suf_leg_limb0'], self.c_dict['left_suf_leg_limb1'],
            self.c_dict['right_suf_leg_limb0'], self.c_dict['right_suf_leg_limb1'],
                 ]
        for i,comp in enumerate(limbs):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if comp.uAngle + self.rotation_speed[i][0] >= comp.uRange[1] or comp.uAngle + self.rotation_speed[i][0] <= \
                    comp.uRange[0]:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle + self.rotation_speed[i][1] >= comp.vRange[1] + self.rotation_speed[i][1] or comp.vAngle <= \
                    comp.vRange[0]:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle + self.rotation_speed[i][2] >= comp.wRange[1] or comp.wAngle + self.rotation_speed[i][2] <= \
                    comp.wRange[0]:
                self.rotation_speed[i][2] *= -1
            # print(f'{comp.uAngle}, {comp.vAngle}, {comp.wAngle}, {comp.uRange}, {comp.vRange}, {comp.wRange}')
        self.vAngle = (self.vAngle + 3) % 360

        pass
        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.


class Body(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None, size=1):
        super().__init__(position, display_obj)
        body = Sphere(position, shaderProg, [0.16 *size, 0.16 *size, 0.25 *size],
                      Ct.SEAGREEN, lowPoly=False)
        white_body = Sphere(Point((0*size, -0.04*size, 0.02*size)), shaderProg, [0.14 *size, 0.14 *size, 0.23 *size],
                      Ct.WHITE, lowPoly=False)


        parent.addChild(self)
        self.addChild(body)
        body.addChild(white_body)


        self.components = [body, white_body]
        self.c_dict = {'body': body, 'white_body': white_body}

        stub_size=[0.033, 0.034,0.033, 0.032]
        stub_z =[0.05 ,-0.03,-0.12,-0.18]
        stub_y = [0.14, 0.138, 0.105, 0.04]
        stub_u = [-90, -100,-120,-150]
        for i in range(4):

            stub = Cone(Point((0 * size, stub_y[i] * size, stub_z[i]* size)), shaderProg,
                        [0.01 * size, stub_size[i] * size, stub_size[i] * size], Ct.GREENYELLOW, lowPoly=False)
            stub.setCurrentAngle(stub_u[i], stub.uAxis)
            body.addChild(stub)
            self.components.append(stub)
            self.c_dict[f'body_stub{i}'] =stub

class Neck(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None, size=1):
        super().__init__(position)
        neck0 = Cone(position, shaderProg, [0.09 * size, 0.1 * size, 0.10 * size],
                     Ct.SEAGREEN, lowPoly=False)
        neck0.setCurrentAngle(-60, neck0.uAxis)
        stub3 = Cone(Point((0 * size, 0.07 * size, (0) * size)), shaderProg,
                    [0.01 * size, 0.032 * size, 0.032 * size], Ct.GREENYELLOW, lowPoly=False)
        stub3.setCurrentAngle(-70, stub3.uAxis)
        neck1 = Cylinder(Point((0 * size, 0 * size, 0.1 * size)), shaderProg, [0.04 * size, 0.04 * size, 0.18 * size],
                         Ct.SEAGREEN, lowPoly=False)
        parent.addChild(self)
        self.addChild(neck0)
        neck0.addChild(neck1)
        neck0.addChild(stub3)
        self.components = [neck0, neck1, stub3]
        self.c_dict = {'neck0': neck0, 'neck1': neck1, 'stub3': stub3}
        for i in range(3):
            stub = Cone(Point((0*size, 0.035*size, (0.16 - 0.08*i)*size)), shaderProg, [0.01 * size, (0.026 + 0.002*i) * size, (0.026 + 0.002*i) * size],Ct.GREENYELLOW, lowPoly=False)
            stub.setCurrentAngle(-90, stub.uAxis)
            neck1.addChild(stub)
            self.components.append(stub)
            self.c_dict[f'stub{i}'] = stub


class Tail(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None, size=1):
        super().__init__(position)
        tail0 = Cone(position, shaderProg, [0.08 * size, 0.08 * size, 0.10 * size],
                     Ct.SEAGREEN, lowPoly=False)
        tail0.setCurrentAngle(-200, tail0.uAxis)
        white_tail0 = Cone(Point((0*size,0.02*size,0*size)), shaderProg, [0.06 * size, 0.06 * size, 0.08 * size],
                     Ct.WHITE, lowPoly=False)
        tail1 = Cone(Point((0, 0, 0.18 * size)), shaderProg, [0.05 * size, 0.05 * size, 0.22 * size], Ct.SEAGREEN,
                     lowPoly=False)
        tail1.setCurrentAngle(10, tail1.uAxis)

        parent.addChild(self)
        self.addChild(tail0)
        tail0.addChild(tail1)
        tail0.addChild(white_tail0)

        self.components = [tail0, tail1, white_tail0]
        self.c_dict = {'tail0': tail0, 'tail1': tail1, 'white_tail0': white_tail0}
        stub_size = [0.030, 0.028, 0.025, 0.020]
        stub_z = [-0.1, -0.02, 0.06, 0.14]
        stub_y = [-0.04, -0.03, -0.02, -0.01]
        stub_u = [90, 90, 90, 90]
        for i in range(4):
            stub = Cone(Point((0 * size, stub_y[i] * size, stub_z[i] * size)), shaderProg,
                        [0.01 * size, stub_size[i] * size, stub_size[i] * size], Ct.GREENYELLOW, lowPoly=False)
            stub.setCurrentAngle(stub_u[i], stub.uAxis)
            tail1.addChild(stub)
            self.components.append(stub)
            self.c_dict[f'tail_stub{i}'] = stub


class Head(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None, size=1):
        super().__init__(position)
        head = Sphere(position, shaderProg, [0.08 * size, 0.072 * size, 0.10 * size],
                      Ct.SEAGREEN, lowPoly=False)
        head.setDefaultAngle(60, head.uAxis)
        mouth = Sphere(Point((0*size,-0.02*size, 0.018*size)), shaderProg, [0.081 * size, 0.001 * size, 0.08 * size],
                      Ct.DARKGREEN, lowPoly=False)

        head_stub0 = Cone(Point((0 * size, 0.06 * size, 0 * size)), shaderProg,
                          [0.01 * size, 0.020 * size, 0.020 * size], Ct.GREENYELLOW, lowPoly=False)
        head_stub0.setCurrentAngle(-110, head_stub0.uAxis)

        head_stub1 = Cone(Point((0 * size, 0.02*size, -0.05 * size)), shaderProg,
                    [0.01 * size, 0.025 * size, 0.025 * size], Ct.GREENYELLOW, lowPoly=False)
        head_stub1.setCurrentAngle(-160, head_stub1.uAxis)


        parent.addChild(self)
        self.addChild(head)
        head.addChild(mouth)
        head.addChild(head_stub0)
        head.addChild(head_stub1)

        self.components = [head, mouth, head_stub0, head_stub1]
        self.c_dict = {'head': head, 'mouth': mouth, 'head_stub0': head_stub0, 'head_stub1': head_stub1}

        l_eyeball, r_eyeball = AddMirror(self, [head, head], Sphere, (0.06 * size, -0.02 * size, 0.02 * size), shaderProg,
                                         [0.04* size, 0.04 * size, 0.04 * size], Ct.WHITE, "eyeball", [-80, -30, 90])
        AddMirror(self, [l_eyeball, r_eyeball], Sphere, (0 * size, -0.02 * size, 0 * size), shaderProg,
                  [0.02 * size, 0.02 * size, 0.02 * size], Ct.BLACK, "pupil", [0, 0, 0])


class Leg(Component):
    def __init__(self, parent, position, shaderProg, display_obj=None, mirror=False, pre="pre", size= 1):
        super().__init__(position, display_obj)
        limb_len = 0.06 * size
        limb_width = 0.06 * size

        joint0 = Sphere(position, shaderProg, [limb_width, limb_width, limb_width], Ct.SEAGREEN)
        if not mirror:
            joint0.setDefaultAngle(180, joint0.vAxis)
        else:
            joint0.setDefaultAngle(-180, joint0.vAxis)
        joint0.setDefaultAngle(-90, joint0.uAxis)

        limb0 = Cylinder(Point((0, 0, limb_len)), shaderProg, [limb_width, limb_width, limb_len], Ct.SEAGREEN)

        joint1 = Sphere(Point((0, 0, limb_len)), shaderProg, [limb_width, limb_width, limb_width], Ct.SEAGREEN)

        limb1 = Cylinder(Point((0, 0, limb_len)), shaderProg, [limb_width, limb_width, limb_len], Ct.SEAGREEN)

        nail1 = Cone(Point((0 * size,-0.06 * size, 0.08 * size)), shaderProg,
             [0.015 * size, 0.020 * size, 0.020 * size], Ct.WHITE, lowPoly=False)
        nail1.setDefaultAngle(-170, nail1.uAxis)

        nail0 = Cone(Point((0.04 * size, -0.05 * size, 0.08 * size)), shaderProg,
                     [0.015 * size, 0.020 * size, 0.020 * size], Ct.WHITE, lowPoly=False)
        nail0.setDefaultAngle(-170, nail0.uAxis)

        nail2 = Cone(Point((-0.04 * size, -0.05 * size, 0.08 * size)), shaderProg,
                     [0.015 * size, 0.020 * size, 0.020 * size], Ct.WHITE, lowPoly=False)
        nail2.setDefaultAngle(-170, nail2.uAxis)


        parent.addChild(self)
        self.addChild(joint0)
        joint0.addChild(limb0)
        limb0.addChild(joint1)
        joint1.addChild(limb1)
        limb1.addChild(nail0)
        limb1.addChild(nail1)
        limb1.addChild(nail2)
        self.components = [joint0, limb0, joint1, limb1, nail1]
        self.c_dict = dict()
        for k, v in {'leg_joint0': joint0, 'leg_limb0': limb0, 'leg_joint1': joint1, 'leg_limb1': limb1, 'leg_nail0': nail0, 'leg_nail1': nail1, 'leg_nail2': nail2}.items():
            k = pre +"_" + k
            if not mirror:
                k = 'left_' + k
            else:
                k = 'right_' + k
            self.c_dict[k] = v