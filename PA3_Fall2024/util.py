from Point import Point

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
