
# Particle Simulator

Simulate the effects of particles on each other in a scientific test environment.

![v1](https://github.com/user-attachments/assets/f68613f8-4ca7-4d4e-bf0f-c50a2e906173)

```python
HeavyParticle(radius=10, mass=1e6, pos=Vector.screenPos(0.5))
HeavyParticle(radius=2, mass=1e3, pos=Vector.screenPos(0.75, 0.5), initV=Vector(0,50))
```
A planet orbiting a star, simulated using two simple commands.

---

![v2](https://github.com/user-attachments/assets/0f4bda4c-ef47-4461-8e45-b8661f274bed)

```python
CohesiveParticle(radius=2, mass=10, pos=Vector.screenPos(1/3))
CohesiveParticle(radius=2, mass=10, pos=Vector.screenPos(2/3, 1/3))
CohesiveParticle(radius=2, mass=10, pos=Vector.screenPos(1/2, 2/3))
```
A special case of the three body problem when they are arranged in a triangle, simulated with three simple commands.

### Installation Guide
1. No libraries need to be installed. Only the standard library is used.
2. Run `python -i main.py` in a terminal.
3. Run commands here. Some example commands are given at the end of the file to help you.
4. Functions like `clear()` and `Vector.screenPos()` are provided for your convinience.

