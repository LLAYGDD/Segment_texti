import tkinter
import sys, random, math
from PIL import Image, ImageTk

from time import time, sleep

from random import choice, uniform, randint

from math import sin, cos, radians

# gravity, act as our constant g, you can experiment by changing it

GRAVITY = 0.05

colors = ['red', 'blue', 'yellow', 'white', 'green', 'orange', 'purple', 'seagreen', 'indigo', 'cornflowerblue']

'''
Generic class for particles
particles are emitted almost randomly on the sky, forming a round of circle (a star) before falling and getting removed
from canvas
Attributes:
    - id: identifier of a particular particle in a star
    - x, y: x,y-coordinate of a star (point of explosion)
    - vx, vy: speed of particle in x, y coordinate
    - total: total number of particle in a star
    - age: how long has the particle last on canvas
    - color: self-explantory
    - cv: canvas
    - lifespan: how long a particle will last on canvas
'''


class part:

    def __init__(self, cv, idx, total, explosion_speed, x=0., y=0., vx=0., vy=0., size=2., color='red', lifespan=2,
                 **kwargs):

        self.id = idx

        self.x = x

        self.y = y

        self.initial_speed = explosion_speed

        self.vx = vx

        self.vy = vy

        self.total = total

        self.age = 0

        self.color = color

        self.cv = cv

        self.cid = self.cv.create_oval(

            x - size, y - size, x + size,

            y + size, fill=self.color)

        self.lifespan = lifespan

    def update(self, dt):

        self.age += dt

        # particle expansions

        if self.alive() and self.expand():

            move_x = cos(radians(self.id * 360 / self.total)) * self.initial_speed

            move_y = sin(radians(self.id * 360 / self.total)) * self.initial_speed

            self.cv.move(self.cid, move_x, move_y)

            self.vx = move_x / (float(dt) * 1000)



        # falling down in projectile motion

        elif self.alive():

            move_x = cos(radians(self.id * 360 / self.total))

            # we technically don't need to update x, y because move will do the job

            self.cv.move(self.cid, self.vx + move_x, self.vy + GRAVITY * dt)

            self.vy += GRAVITY * dt



        # remove article if it is over the lifespan

        elif self.cid is not None:

            canvas.delete(self.cid)

            self.cid = None

    # define time frame for expansion

    def expand(self):

        return self.age <= 1.2

    # check if particle is still alive in lifespan

    def alive(self):

        return self.age <= self.lifespan


'''
Firework simulation loop:
Recursively call to repeatedly emit new fireworks on canvas
a list of list (list of stars, each of which is a list of particles)
is created and drawn on canvas at every call, 
via update protocol inside each 'part' object 
'''


def simulate(cv):
    t = time()

    explode_points = []

    wait_time = randint(10, 100)

    numb_explode = randint(6, 10)

    # create list of list of all particles in all simultaneous explosion

    for point in range(numb_explode):

        objects = []

        x_cordi = randint(50, 550)

        y_cordi = randint(50, 150)

        speed = uniform(0.5, 1.5)

        size = uniform(0.5, 3)

        color = choice(colors)

        explosion_speed = uniform(0.2, 1)

        total_particles = randint(10, 50)

        for i in range(1, total_particles):
            r = part(cv, idx=i, total=total_particles, explosion_speed=explosion_speed, x=x_cordi, y=y_cordi,

                     vx=speed, vy=speed, color=color, size=size, lifespan=uniform(0.6, 1.75))

            objects.append(r)

        explode_points.append(objects)

    total_time = .0

    # keeps undate within a timeframe of 1.8 second

    while total_time < 1.8:

        sleep(0.01)

        tnew = time()

        t, dt = tnew, tnew - t

        for point in explode_points:

            for item in point:
                item.update(dt)

        cv.update()

        total_time += dt

    # recursive call to continue adding new explosion on canvas

    root.after(wait_time, simulate, cv)


def close(*ignore):
    """Stops simulation loop and closes the window."""

    global root

    root.quit()


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "<Point>: (%f, %f)" % (self.x, self.y)


class Branch(object):
    def __init__(self, bottom, top, branches, level=0):
        self.bottom = bottom
        self.top = top
        self.level = level
        self.branches = branches
        self.children = []

    def __str__(self):
        s = "Top: %s, Bottom: %s, Children Count: %d" % \
            (self.top, self.bottom, len(self.children))
        return s

    def nextGen(self, n=-1, rnd=1):
        if n <= 0: n = self.branches
        if rnd == 1:
            n = random.randint(n / 2, n * 2)
            if n <= 0: n = 1
        dx = self.top.x - self.bottom.x
        dy = self.top.y - self.bottom.y
        r = 0.10 + random.random() * 0.2
        if self.top.x == self.bottom.x:
            # 如果是一条竖线
            x = self.top.x
            y = dy * r + self.bottom.y
        elif self.top.y == self.bottom.y:
            # 如果是一条横线
            x = dx * r + self.bottom.x
            y = self.top.y
        else:
            x = dx * r
            y = x * dy / dx
            x += self.bottom.x
            y += self.bottom.y
        oldTop = self.top
        self.top = Point(x, y)
        a = math.pi / (2 * n)
        for i in range(n):
            a2 = -a * (n - 1) / 2 + a * i - math.pi
            a2 *= 0.9 + random.random() * 0.2
            self.children.append(self.mkNewBranch(self.top, oldTop, a2))

    def mkNewBranch(self, bottom, top, a):
        dx1 = top.x - bottom.x
        dy1 = top.y - bottom.y
        r = 0.9 + random.random() * 0.2
        c = math.sqrt(dx1 ** 2 + dy1 ** 2) * r
        if dx1 == 0:
            a2 = math.pi / 2
        else:
            a2 = math.atan(dy1 / dx1)
            if (a2 < 0 and bottom.y > top.y) \
                    or (a2 > 0 and bottom.y < top.y) \
                    :
                a2 += math.pi
        b = a2 - a
        dx2 = c * math.cos(b)
        dy2 = c * math.sin(b)
        newTop = Point(dx2 + bottom.x, dy2 + bottom.y)
        return Branch(bottom, newTop, self.branches, self.level + 1)


class Tree(object):
    def __init__(self, root, canvas, bottom, top, branches=3, depth=3):
        self.root = root
        self.canvas = canvas
        self.bottom = bottom
        self.top = top
        self.branches = branches
        self.depth = depth
        self.new()

    def gen(self, n=1):
        for i in range(n):
            self.getLeaves()
            for node in self.leaves:
                node.nextGen()
        self.show()

    def new(self):
        self.leavesCount = 0
        self.branch = Branch(self.bottom, self.top, self.branches)
        self.gen(self.depth)
        print("leaves count: %d" % self.leavesCount)

    def chgDepth(self, d):
        self.depth += d
        if self.depth < 0: self.depth = 0
        if self.depth > 10: self.depth = 10
        self.new()

    def chgBranch(self, d):
        self.branches += d
        if self.branches < 1: self.branches = 1
        if self.branches > 10: self.branches = 10
        self.new()

    def getLeaves(self):
        self.leaves = []
        self.map(self.findLeaf)

    def findLeaf(self, node):
        if len(node.children) == 0:
            self.leaves.append(node)

    def show(self):
        for i in self.canvas.find_all():
            self.canvas.delete(i)
        self.map(self.drawNode)
        self.canvas.tag_raise("leaf")

    def exit(self, evt):
        sys.exit(0)

    def map(self, func=lambda node: node):
        # 遍历树
        children = [self.branch]
        while len(children) != 0:
            newChildren = []
            for node in children:
                func(node)
                newChildren.extend(node.children)
            children = newChildren

    def drawNode(self, node):
        self.line2(
            #		self.canvas.create_line(
            node.bottom.x,
            node.bottom.y,
            node.top.x,
            node.top.y,
            fill="#00008B",
            width=1.5 ** (self.depth - node.level),
            tags="branch level_%d" % node.level,
        )

        if len(node.children) == 0:
            # 画叶子
            self.leavesCount += 1
            self.canvas.create_oval(
                node.top.x - 3,
                node.top.y - 3,
                node.top.x + 3,
                node.top.y + 3,
                fill="#090",
                tag="leaf",
                # tag="sienna",
            )

        self.canvas.update()

    def line2(self, x0, y0, x1, y1, width=1, fill="#00008B", minDist=10, tags=""):
        dots = midDots(x0, y0, x1, y1, minDist)
        dots2 = []
        for i in range(len(dots) - 1):
            dots2.extend([dots[i].x,
                          dots[i].y,
                          dots[i + 1].x,
                          dots[i + 1].y])
        self.canvas.create_line(
            dots2,
            fill=fill,
            width=width,
            smooth=True,
            tags=tags,
        )


def midDots(x0, y0, x1, y1, d):
    dots = []
    dx, dy, r = x1 - x0, y1 - y0, 0
    if dx != 0:
        r = float(dy) / dx
    c = math.sqrt(dx ** 2 + dy ** 2)
    n = int(c / d) + 1
    for i in range(n):
        if dx != 0:
            x = dx * i / n
            y = x * r
        else:
            x = dx
            y = dy * i / n
        if i > 0:
            x += d * (0.5 - random.random()) * 0.25
            y += d * (0.5 - random.random()) * 0.25
        x += x0
        y += y0
        dots.append(Point(x, y))
    dots.append(Point(x1, y1))
    return dots


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Tree")
    gw, gh = 800, 600
    canvas = tkinter.Canvas(root,
                            width=gw,
                            height=gh,
                            )
    canvas.pack()
    tree = Tree(root, canvas, Point(gw / 2, gh - 20), Point(gw / 2, gh * 0.2), \
                branches=2, depth=8)
    root.bind("n", lambda evt: tree.new())
    root.bind("=", lambda evt: tree.chgDepth(1))
    root.bind("+", lambda evt: tree.chgDepth(1))
    root.bind("-", lambda evt: tree.chgDepth(-1))
    root.bind("b", lambda evt: tree.chgBranch(1))
    root.bind("c", lambda evt: tree.chgBranch(-1))
    root.bind("q", tree.exit)
    root.after(100, simulate, canvas)
    root.mainloop()