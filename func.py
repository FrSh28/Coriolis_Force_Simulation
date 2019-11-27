'''
 Copyright (C) 2019 Yi-Fan Shyu, Yueh-Feng Ku
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is furnished
 to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from visual import*

g = vector(0.0, -9.8, 0.0)

def count_v(dt, pos):
    if len(pos) == 2:
        return (pos[1] - pos[0]) / dt
    elif len(pos) == 3:
        return (pos[2] - pos[0]) / (2 * dt)
    else:
        return None

def count_a(dt, pos):
    if len(pos) == 3:
        return (pos[2] + pos[0] - 2 * pos[1]) / dt**2
    else:
        return None

def get_g(mass, G = g):
    return mass * G

def spring_f(length, k, initlen = 0.0):
    return -norm(length) * k * (mag(length) - mag(initlen))

def update(dt, scene):
    for i in scene.objects:
        last_v = None
        if hasattr(i, 'a') and hasattr(i, 'v'):
            last_v = i.v
            i.v += i.a * dt
        if hasattr(i, 'v') and hasattr(i, 'pos'):
            if last_v:
                i.pos += (last_v+i.v)/2 * dt
            else:
                i.pos += i.v * dt
        if hasattr(i, 'v') and hasattr(i, 'S'):
            if last_v:
                i.S += mag((last_v+i.v)/2 * dt)
            else:
                i.S += mag(i.v * dt)

