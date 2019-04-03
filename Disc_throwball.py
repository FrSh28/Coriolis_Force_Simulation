#-*- coding: cp950 -*-
'''
 Copyright (C) 2018 Yi-Fan Shyu, Yueh-Feng Ku
 
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
from visual.graph import*
from random import*
from func import*

#Units: cm, s, radian
rpm10 = 0       #rpm times 10
w = vector(0, 2*pi*rpm10/600.0, 0)
throw_dir = 0   #in degrees
balls_v = 5.0
balls_duration = 5.0

print "\nUnits: cm, s\n"
print "Controlings:\n left , right : change rotation speed\n a : throwing direction turns left\n d : throwing direction turns right"
print " i : camera rotates with disc\n o : camera sets still\n p : print balls data"
print "\nclick to throw the ball\n\n*You can't change rotation speed while any ball exists."
sleep(5)


g_dev = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation", xtitle = "t", ytitle = "%")
gdots(gdisplay = g_dev, pos = [(-0.5, 0), (balls_duration+0.5, 0), (0, 0.01)], color = color.white, size = 0.01)

g_trail = gdisplay(x = 900, y = 350, width = 350, height = 350, xmax = 10, xmin = -10, ymax = 10, ymin = -10, title = "Trail on Disc")
gcurve(gdisplay = g_trail, pos = [(10*cos(radians(angle)), 10*sin(radians(angle))) for angle in range(380)], color = color.white)
gdots(gdisplay = g_trail, pos = (0, -9), color = color.green, size = 8, shape = "square")
gdots(gdisplay = g_trail, pos = (0, 9), color = color.yellow, size = 8, shape = "square")

scene = display(width = 900, height = 700, center = vector(0, 2, 0), background = color.black, title = "Throw Ball on Disc", autoscale = False,
                lights = [local_light(pos = vector(0, 20, 0), color = color.gray(0.7))])

timer = label(text = "Click To Start", pos = scene.center, yoffset = scene.height/2-100, height = 50, color = color.red, box = False, line = False, opacity = 0)
rota_demo = str(rpm10/10.0)
throwdir_demo = str(throw_dir)
info_demo = label(text = "  Rotation Speed(< >):\n    %s  rpm\n  Throw Direction(a d):\n    %s  deg" % (rota_demo, throwdir_demo),
                  pos = scene.center, xoffset = -(scene.width/2-200), height = 18, color = color.white, background = color.black, box = False, line = False, opacity = 0.5)

floor = box(pos = vector(0, -0.75, 0), length = 25, width = 25, height = 0.5, material = materials.bricks)
plate = frame(pos = vector(0, 0, 0))
disc = cylinder(frame = plate, pos = vector(0, -0.5, 0), radius = 10, axis = vector(0, 0.5, 0), color = color.gray(0.7), material = materials.wood)
pyramid(frame = plate, pos = vector(9, 0, 0), size = (0.6, 0.6, 0.6), axis = vector(0, 1, 0), color = color.yellow, material = materials.rough)
player = pyramid(frame = plate, pos = vector(-9, 0, 0), size = (0.3, 0.6, 0.6), axis = vector(0, 1, 0), color = color.green, material = materials.rough)
throw = arrow(frame = plate, pos = vector(-9, 0, 0), shaftwidth = 0.1, color = color.green, material = materials.rough)
throw.axis = rotate(vector(-player.pos.x, 0, -player.pos.z), angle = radians(throw_dir), axis = vector(0, -1, 0)) * 0.3

scene.forward = vector(-plate.frame_to_world(player.pos).x, -3, -plate.frame_to_world(player.pos).z) * 1.5
scene.autoscale = False

poss = [player.pos, player.pos]
balls = []
formula_balls = []
balln = -1
trails = []
pball = []
arrows = []
formula_arrows = []

def mouse_method(evt):
    global balln
    if evt.click == "left":
        balln += 1
        graph_color = (uniform(0.3, 0.8), uniform(0.3, 0.8), uniform(0.3, 0.8))
        balls.append(sphere(pos = vector(plate.frame_to_world(player.pos).x, 0.3, plate.frame_to_world(player.pos).z), radius = 0.3, make_trail = True, color = color.red, material = materials.rough, opacity = 0.5,
                            time = 0.0, num = balln, v = count_v(dt, poss) + balls_v * norm(plate.frame_to_world(throw.axis)), a = vector(0, 0, 0), S = 0.0,
                            graph_trail = gcurve(gdisplay = g_trail, color = graph_color, dot = True, size = 5, dot_color = graph_color), deviation = gcurve(gdisplay = g_dev, color = graph_color, dot = True, size = 5, dot_color = graph_color)))
        formula_balls.append(sphere(frame = plate, pos = vector(player.pos.x, 0.3, player.pos.z), radius = 0.3, make_trail = False, color = color.blue, material = materials.rough, opacity = 0.5,
                                    v = balls_v * norm(throw.axis), a = vector(0, 0, 0)))
        arrows.append(arrow(frame = plate, pos = balls[-1].pos, shaftwidth = 0.2, axis = vector(0, 0, 0), color = color.red, material = materials.rough, opacity = 0.5))
        formula_arrows.append(arrow(frame = plate, pos = balls[-1].pos, shaftwidth = 0.2, axis = vector(0, 0, 0), color = color.blue, material = materials.rough, opacity = 0.5))
        trails.append(curve(frame = plate, pos = [plate.world_to_frame(balls[-1].pos) for i in range(3)], color = graph_color))
        pball.append([balln+1, vector(0, 0, 0), 0, vector(0, 0, 0), 0, vector(0, 0, 0), 0, vector(0, 0, 0), 0])

def key_method(evt):
    global mode, rpm10, rota_demo, w, throw_dir, throwdir_demo
    k = scene.kb.getkey()
    if k == "i":
        mode = "inside"
    elif k == "o":
        mode = "outside"
    elif k == "p":
        for pb in pball:
            print("\nball %d:\ninertial:\n  v: %s  %.5f\n  a: %s  %.5f\nnon-inertial:\n  v: %s  %.5f\n  a: %s  %.5f"
                    % (pb[0], pb[1], pb[2], pb[3], pb[4], pb[5], pb[6], pb[7], pb[8]))
    elif k == "left" and len(balls) == 0:
        rpm10 -= 2
        rota_demo = str(rpm10/10.0)
        w = vector(0, 2*pi*rpm10/600.0, 0)
    elif k == "right" and len(balls) == 0:
        rpm10 += 2
        rota_demo = str(rpm10/10.0)
        w = vector(0, 2*pi*rpm10/600.0, 0)
    elif k == "a" or k == "d":
        if k == "a":
            throw_dir -= 1
        else:
            throw_dir +=1
        throw_dir %= 360
        if throw_dir > 180:
            throw_dir -= 360
        throwdir_demo = str(throw_dir)
        throw.axis = rotate(vector(-player.pos.x, 0, -player.pos.z), angle = radians(throw_dir), axis = vector(0, -1, 0)) * 0.3
    info_demo.text = "  Rotation Speed(< >):\n    %s  rpm\n  Throw Direction(a d):\n    %s  deg" % (rota_demo, throwdir_demo)

mode = "outside"
t = 0
dt = 0.001

scene.waitfor("click")
scene.bind("click", mouse_method)
scene.bind("keydown", key_method)
timer.color = color.yellow

while True:
    rate(1/dt)
    
    t += dt
    timer.text = str(int(t))
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-200)
    
    poss[0] = poss[1]*1
    poss[1] = plate.frame_to_world(player.pos)*1
    
    for b in balls:
        ballpos = plate.world_to_frame(b.pos)
        b.graph_trail.plot(pos = (ballpos.z, ballpos.x))
        if b.S:
            b.deviation.plot(pos = (b.time, mag(ballpos - formula_balls[balls.index(b)].pos)*100.0 / b.S))
        
        if b.time >= balls_duration:
            b.trail_object.visible = False
            b.visible = False
            formula_balls[balls.index(b)].visible = False
            arrows[balls.index(b)].visible = False
            formula_arrows[balls.index(b)].visible = False
            del b.deviation, b.graph_trail, trails[balls.index(b)], formula_arrows[balls.index(b)], formula_balls[balls.index(b)], arrows[balls.index(b)], balls[balls.index(b)]
        
        else:
            b.time += dt
            trails[balls.index(b)].append(pos = ballpos)
            pball[b.num][1] = b.v
            pball[b.num][2] = mag(pball[b.num][1])
            pball[b.num][3] = b.a
            pball[b.num][4] = mag(pball[b.num][3])
            pball[b.num][5] = vector(count_v(dt, trails[balls.index(b)].pos[-2:]))
            pball[b.num][6] = mag(pball[b.num][5])
            pball[b.num][7] = vector(count_a(dt, trails[balls.index(b)].pos[-3:]))
            pball[b.num][8] = mag(pball[b.num][7])
            arrows[balls.index(b)].pos = ballpos
            arrows[balls.index(b)].axis = pball[b.num][7] * 0.5
    
    for fb in formula_balls:
        fb.a = -2*cross(w, fb.v) - cross(w, cross(w, fb.pos))
        formula_arrows[formula_balls.index(fb)].pos = fb.pos
        formula_arrows[formula_balls.index(fb)].axis = fb.a * 0.5
    
    plate.rotate(angle = mag(w) * dt, axis = norm(w))
    update(dt, scene)
    
    if mode == "inside":
        scene.forward = vector(-plate.frame_to_world(player.pos).x, -3, -plate.frame_to_world(player.pos).z) * 1.5

