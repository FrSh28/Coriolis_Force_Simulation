from visual import*


g = vector(0.0, -9.8, 0.0)

def count_v(dt, pos):
    if len(pos) == 2:
        return (pos[1] - pos[0]) / dt

def count_a(dt, pos):
    if len(pos) == 3:
        return (pos[2] + pos[0] - 2 * pos[1]) / dt**2

def get_g(mass, G = g):
    return mass * G

def spring_f(length, k, initlen = 0.0):
    return -norm(length) * k * (abs(length) - abs(initlen))

def update(dt, scene):
    for i in scene.objects:
        if hasattr(i, 'a'):
            i.v += i.a * dt
        if hasattr(i, 'v'):
            i.pos += i.v *dt
