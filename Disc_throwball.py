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
from output import*

#Units: cm, s, radian
rpm10 = 0       #rpm times 10
w = vector(0, 2*pi*rpm10/600.0, 0)
throw_dir = 0   #in degrees
balls_v = 5.0
balls_duration = 5.0

print "\nUnits: cm, s\n"
print "Controlings:\n left , right : change rotation speed\n a : throwing direction turns left\n d : throwing direction turns right"
print " i : camera rotates with disc\n o : camera sets still\n r : save balls data"
print "\nclick to throw the ball\n\n*You can't change rotation speed while any ball exists."
sleep(5)


g_dev = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation", xtitle = "t", ytitle = "%")
gdots(gdisplay = g_dev, pos = [(-1, 0), (balls_duration+0.5, 0), (0, 0.01)], color = color.white, size = 0.01)

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
                  pos = scene.center, xoffset = -(scene.width/2-200), height = 18, color = color.white, background = color.black, box = False, line = False, opacity = 0.7)

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
balln = -1
balls = []
arrows = []
balls_pos = []
trails = []
formula_balls = []
formula_arrows = []
balls_data = [[None], ["t"]]+[[i/50.0] for i in range(251)]

def mouse_method(evt):
    global balln, balls_data
    if evt.click == "left":
        balln += 1
        graph_color = vector(uniform(0.3, 0.8), uniform(0.3, 0.8), uniform(0.3, 0.8))
        balls.append(sphere(pos = vector(plate.frame_to_world(player.pos).x, 0.3, plate.frame_to_world(player.pos).z), radius = 0.3, make_trail = True, color = color.red, material = materials.rough, opacity = 0.5,
                            time = 0.0, num = balln, v = count_v(dt, poss) + balls_v * norm(plate.frame_to_world(throw.axis)), a = vector(0, 0, 0), S = 0.0,
                            graph_trail = gcurve(gdisplay = g_trail, color = graph_color, dot = True, size = 5, dot_color = graph_color), deviation = gcurve(gdisplay = g_dev, color = graph_color, dot = True, size = 5, dot_color = graph_color),
                            data = [], dotn = 0))
        arrows.append(arrow(frame = plate, pos = balls[-1].pos, shaftwidth = 0.2, axis = vector(0, 0, 0), color = color.red, material = materials.rough, opacity = 0.5))
        balls_pos.append([balls[-1].pos*1, balls[-1].pos*1])
        trails.append(curve(frame = plate, pos = [plate.world_to_frame(balls[-1].pos) for i in range(3)], color = graph_color))

        formula_balls.append(sphere(frame = plate, pos = vector(player.pos.x, 0.3, player.pos.z), radius = 0.3, make_trail = False, color = color.blue, material = materials.rough, opacity = 0.5,
                                    v = balls_v * norm(throw.axis), a = vector(0, 0, 0)))
        formula_balls[-1].a = -2*cross(w, formula_balls[-1].v) - cross(w, cross(w, formula_balls[-1].pos))
        formula_arrows.append(arrow(frame = plate, pos = formula_balls[-1].pos, shaftwidth = 0.2, axis = vector(0, 0, 0), color = color.blue, material = materials.rough, opacity = 0.5))

        balls[-1].data.append([balls[-1].v, balls[-1].a, "NO_DATA", "NO_DATA"])
        balls_data[0] += ["ball "+str(balln+1), "", "", ""]
        balls_data[1] += ["iner_v", "iner_a", "non-iner_v", "non-iner_a"]
        for i in range(251):
            balls_data[i+2] += [None, None, None, None]

def key_method(evt):
    global mode, balls_data, rpm10, w, rota_demo, throw_dir, throwdir_demo
    k = scene.kb.getkey()
    if k == "i":
        mode = "inside"
    elif k == "o":
        mode = "outside"
    elif k == "r":
        save_csv("Disc_throwball.csv", balls_data)
    elif k == "left" and len(balls) == 0:
        rpm10 -= 2
        w = vector(0, 2*pi*rpm10/600.0, 0)
        rota_demo = str(rpm10/10.0)
    elif k == "right" and len(balls) == 0:
        rpm10 += 2
        w = vector(0, 2*pi*rpm10/600.0, 0)
        rota_demo = str(rpm10/10.0)
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
    
    plate.rotate(angle = mag(w) * dt, axis = norm(w))
    update(dt, scene)
    
    for b in balls:
        ballpos = plate.world_to_frame(b.pos)
        b.graph_trail.plot(pos = (ballpos.z, ballpos.x))
        if b.S:
            b.deviation.plot(pos = (b.time, mag(ballpos - formula_balls[balls.index(b)].pos)*100.0 / b.S))
        
        if b.time >= balls_duration:
            for i in range(len(b.data)):
                for j in range(4):
                    balls_data[i+2][j+b.num*4+1] = b.data[i][j]
            b.trail_object.visible = False
            b.visible = False
            formula_balls[balls.index(b)].visible = False
            arrows[balls.index(b)].visible = False
            formula_arrows[balls.index(b)].visible = False
            del b.deviation, b.graph_trail, balls_pos[balls.index(b)], trails[balls.index(b)], formula_arrows[balls.index(b)], formula_balls[balls.index(b)], arrows[balls.index(b)], balls[balls.index(b)]
        
        else:
            b.time += dt
            b.dotn += 1
            balls_pos[balls.index(b)].append(b.pos*1)
            trails[balls.index(b)].append(pos = ballpos)
            if not(b.dotn % 20):
                b.data.append([count_v(dt, balls_pos[balls.index(b)][-2:]),
                               count_a(dt, balls_pos[balls.index(b)][-3:]),
                               vector(count_v(dt, trails[balls.index(b)].pos[-2:])),
                               vector(count_a(dt, trails[balls.index(b)].pos[-3:]))])
            arrows[balls.index(b)].pos = ballpos
            arrows[balls.index(b)].axis = vector(count_a(dt, trails[balls.index(b)].pos[-3:])) * 0.5
    
    for fb in formula_balls:
        fb.a = -2*cross(w, fb.v) - cross(w, cross(w, fb.pos))
        formula_arrows[formula_balls.index(fb)].pos = fb.pos
        formula_arrows[formula_balls.index(fb)].axis = fb.a * 0.5
    
    if mode == "inside":
        scene.forward = vector(-plate.frame_to_world(player.pos).x, -3, -plate.frame_to_world(player.pos).z) * 1.5

