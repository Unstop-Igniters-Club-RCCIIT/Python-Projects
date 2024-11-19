import math

from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    i: float
    j: float

    def fromPolar(mag, dir):
        return Vector(mag * math.cos(dir), mag * math.sin(dir))

    def __repr__(self):
        r = abs(self)
        s = f'{(self.i)} î + {(self.j)} ĵ;\t r = {r}'
        if r != 0:
            s += f'\tθ = {math.degrees(self.direction())}°'
        return s

    def __abs__(self):
        return math.hypot(self.i, self.j)

    # r0: value to return for 0 Vector
    def direction(self, r0=None):
        return math.atan2(self.j, self.i)

    def isSmall(self):
        return abs(self.i) < 5 and abs(self.j) < 5

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.dotProduct(other)
        else:
            return Vector(self.i * other, self.j * other)

    def __add__(self, vec):
        return Vector(self.i + vec.i, self.j + vec.j)

    def __sub__(self, vec):
        return Vector(self.i - vec.i, self.j - vec.j)

    def __neg__(self):
        return Vector(-self.i, -self.j)

    def __truediv__(self, v):
        return Vector(self.i / v, self.j / v)

    def screenPos(x_frac, y_frac=None):
        if not y_frac:
            y_frac = x_frac
        return Vector(can.winfo_width() * x_frac, can.winfo_height() * y_frac)


import time
from abc import ABC, abstractmethod  # Abstract Base Classes


class Particle(ABC):

    particles = []

    def __init__(self, color=None, radius=1, pos=None, initV=Vector(0, 0), fixed=False):
        if not color:
            import colorsys
            import random
            hsv = random.random(), random.betavariate(3, 1), random.betavariate(8, 1)
            # Betavariate: https://www.desmos.com/calculator/xufebk8ftc, HSV: https://www.desmos.com/calculator/ibnrin2j2i
            color = '#%02x%02x%02x' % tuple(round(i * 255) for i in colorsys.hsv_to_rgb(*hsv))

        self.color = color
        self.radius = radius
        self.pos = pos or Vector.screenPos(0.5)
        self.v = initV
        self._fixed = fixed

        Particle.particles.append(self)

        if not fixed:
            Updater.addTask(self.updatePosition0, self.updatePosition1)

    @abstractmethod
    def updatePosition0(self):
        pass

    def updatePosition1(self, lastUpdated):
        now = time.time_ns()
        self.pos += self.v * (now - lastUpdated) * 1e-9
        return now

    def delete(self):
        Particle.particles.remove(self)
        if not self._fixed:
            Updater.removeTask(self.updatePosition1)


class VelocitiedParticle(Particle):

    @abstractmethod
    def updatePosition0(self):
        # set self.v to whatever
        pass

    def updatePosition1(self, lastUpdated):
        now = time.time_ns()
        self.pos += self.v * (now - lastUpdated) * 1e-9 * timeFactor
        return now


class PointerFollowingParticle(VelocitiedParticle):

    def __init__(self, speed=1, **particleOptions):
        self.speed = speed
        super().__init__(**particleOptions)

    def updatePosition0(self):
        self.v = (Vector(can.winfo_pointerx() - can.winfo_rootx(), can.winfo_pointery() - can.winfo_rooty()) - self.pos) * self.speed
        # absolute position of pointer - position of top of canvas - current pos. use local variable for v if you dont care abt the arrow


class AccelaratedParticle(Particle):

    @abstractmethod
    def updatePosition0(self):
        # set self.a to whatever
        pass

    def updatePosition1(self, lastUpdated):
        # print('Did this run?')
        now = time.time_ns()
        dt = (now - lastUpdated) * 1e-9 * timeFactor
        self.pos += self.v * dt + self.a * dt**2 / 2  # s += ut + at²/2
        self.v += self.a * dt
        #self.pos += self.v * dt
        return now


class PointerAttractedParticle(AccelaratedParticle):
    def __init__(self, speed=1, **particleOptions):
        self.speed = speed
        super().__init__(**particleOptions)

    def updatePosition0(self):
        self.a = (Vector(can.winfo_pointerx() - can.winfo_rootx(), can.winfo_pointery() - can.winfo_rooty()) - self.pos) * self.speed
        # absolute position of pointer - position of top of canvas - current pos


class CohesiveParticle(AccelaratedParticle):
    cohesiveParticles = []

    def __init__(self, mass=1, **particleOptions):
        self.mass = mass
        super().__init__(**particleOptions)
        CohesiveParticle.cohesiveParticles.append(self)

    def updatePosition0(self):
        F = Vector(0, 0)
        for i in CohesiveParticle.cohesiveParticles:
            if i is not self:
                F += i.pos - self.pos
        self.a = F / self.mass  # accelaration

    def delete(self):
        super().delete()
        CohesiveParticle.cohesiveParticles.remove(self)


# experienes gravity
class HeavyParticle(AccelaratedParticle):
    heavyParticles = []

    def __init__(self, mass=1, **particleOptions):
        self.mass = mass
        super().__init__(**particleOptions)
        HeavyParticle.heavyParticles.append(self)

    def updatePosition0(self):
        a = Vector(0, 0)
        for i in HeavyParticle.heavyParticles:
            if i is not self:
                r = i.pos - self.pos
                a += Vector.fromPolar(i.mass * abs(r)**-2, r.direction())
        # self.a = a
        if a:
            self.a = a
        # print('This ran:', a)

    def delete(self):
        super().delete()
        HeavyParticle.heavyParticles.remove(self)


class ChargedParticle(Particle):
    chargedParticles = []

    def __init__(self, charge, mass=1, **particleOptions):
        self.charge = charge
        self.mass = mass
        super().__init__(**particleOptions)
        ChargedParticle.chargedParticles.append(self)

    def updatePosition0(self):
        E = Vector(0, 0)  # electric field
        for i in ChargedParticle.chargedParticles:
            if i is not self:
                r = i.pos - self.pos
                mag = i.charge * abs(r)**-2  # q/r^2
                E += Vector.fromPolar(mag, r.direction())
        # print(abs(E))
        self.a = E * self.charge / self.mass  # accelaration
        # self.pos = self.a

    def delete(self):
        super().delete()
        ChargedParticle.chargedParticles.remove(self)


class Updater:
    tasks0 = []
    tasks1 = []
    lastUpdateds = []
    lenTasks = 0

    def addTask(cb0, cb1):
        Updater.tasks0.append(cb0)
        Updater.tasks1.append(cb1)
        Updater.lastUpdateds.append(time.time_ns())
        Updater.lenTasks += 1

    def runUpdater():
        for i in Updater.tasks0:
            i()
        for i in range(Updater.lenTasks):
            Updater.lastUpdateds[i] = Updater.tasks1[i](Updater.lastUpdateds[i])
        root.after(Updater.tasksFpsInverse, Updater.runUpdater)

    def removeTask(cb1):
        idx = Updater.tasks1.index(cb1)
        Updater.lenTasks -= 1
        del Updater.tasks0[idx], Updater.tasks1[idx], Updater.lastUpdateds[idx]


def renderer():
    import tkinter as tk

    global root, can
    root = tk.Tk()
    can = tk.Canvas(root, background='#121212', width=1080, height=608)

    fpsInverse = round(1000 / fps)
    Updater.tasksFpsInverse = round(1000 / tasksFps)

    def drawCanvas():
        can.delete('all')
        for p in Particle.particles:
            can.create_oval(
                p.pos.i - p.radius, p.pos.j - p.radius,
                p.pos.i + p.radius, p.pos.j + p.radius,
                fill=p.color, outline=p.color)
            # circle centered at p.pos of radius p.radius
            if showVelocity and not p.v.isSmall():
                vRel2p = p.pos + p.v
                can.create_line(p.pos.i, p.pos.j, vRel2p.i, vRel2p.j, arrow=tk.LAST, fill=velocityColor or p.color)
            if showAcceleration and hasattr(p, 'a'):
                aRel2p = p.pos + p.a
                can.create_line(p.pos.i, p.pos.j, aRel2p.i, aRel2p.j, arrow=tk.LAST, fill=accelerationColor or p.color)

        root.after(fpsInverse, drawCanvas)

    root.after_idle(Updater.runUpdater)
    root.after_idle(drawCanvas)

    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    can.grid(row=0, column=0, sticky="nsew")

    root.mainloop()
    print()
    import os
    import signal
    os.kill(os.getpid(), signal.SIGINT)


# settings:
fps = 25
tasksFps = 100

timeFactor = 1
showVelocity = True
velocityColor = None  # that of the particle
showAcceleration = False  # when possible
accelerationColor = None  # that of the particle


def clear():
    for i in Particle.particles:
        i.delete()


def clearOffScreen():
    for p in Particle.particles:
        if (p.pos.i < 0 or p.pos.i > can.winfo_width()) and (p.pos.j < 0 or p.pos.j > can.winfo_height()):
            p.delete()


if __name__ == '__main__':
    renderer = __import__('threading').Thread(target=renderer)
    renderer.start()


'''
p = PointerFollowingParticle(radius=5, speed=1.3)

p = PointerAttractedParticle(radius=2, speed=0.01)


p1 = ChargedParticle(-1, radius=5, pos=Vector.screenPos(1/3))
p2 = ChargedParticle(+1, radius=5, pos=Vector.screenPos(2/3))

p1 = HeavyParticle(radius=10, mass=1e6, pos=Vector.screenPos(0.5))
p2 = HeavyParticle(radius=2, mass=1e3, pos=Vector.screenPos(0.75, 0.5), initV=Vector(0,50))


p1 = CohesiveParticle(radius=2, mass=10, pos=Vector.screenPos(1/3))
p2 = CohesiveParticle(radius=2, mass=10, pos=Vector.screenPos(2/3, 1/3))
p3 = CohesiveParticle(radius=2, mass=10, pos=Vector.screenPos(1/2, 2/3))
'''
