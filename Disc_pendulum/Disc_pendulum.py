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
from func import*
from communicate import*
import subprocess

#Units: cm, s, radian
rpm10 = 0       #rpm times 10
w = vector(0, 2*pi*rpm10/600.0, 0)
init_angle = 0
while init_angle <= 0:
    init_angle = float(raw_input("initial angle(<20 deg) : "))   #in degrees
angle = radians(init_angle)
m = 20.0
kc = 500000.0
Length = 50.0
amplitude = Length * sin(angle)

print "\nControlings:\n left , right : change rotation speed\n i : camera rotates with disc\n o : camera sets still\n p : print pendulum data"
print "\nclick to release the pendulum\n\n*You can't change rotation speed after releasing the pendulum."
#exe cpp
subprocess.Popen([str(os.path.dirname(os.path.realpath(__file__)))+"\\vector_calculate.exe"])
sleep(5)
connect()
write("init %f %f %f %f\0"%(m, kc, Length, Length+2))   #stick.pos = (0,Length+2,0)


g_dev = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation", xtitle = "t", ytitle = "%")
scale = gdots(gdisplay = g_dev, pos = [(-1, 0), (5, 0), (0, 0.0001)], color = color.white, size = 0.01)
deviation = gcurve(gdisplay = g_dev, color = color.green)

g_trail = gdisplay(x = 900, y = 350, width = 350, height = 350, xmax = amplitude, xmin = -amplitude, ymax = amplitude, ymin = -amplitude, title = "Trail on Disc")
gdots(gdisplay = g_trail, pos = (0 , 0), size = 1)
graph_trail = gcurve(gdisplay = g_trail, color = color.red)

scene = display(width = 900, height = 700, center = vector(0, 2, 0), background = color.black, title = "Pendulum on Disc",
                lights = [local_light(pos = vector(0, 30, 0), color = color.gray(0.8))])

timer = label(text = "Click to start", pos = scene.center, yoffset = scene.height/2-100, height = 50, color = color.red, box = False, line = False, opacity = 0)
rota_demo = str(rpm10/10.0)
info_demo = label(text = "  Rotation Speed(< >):\n    %s  rpm\n  Initial angle:\n    %s  deg" % (rota_demo, str(init_angle)),
                  pos = scene.center, xoffset = -(scene.width/2-180), height = 18, color = color.white, background = color.black, box = False, line = False, opacity = 0.5)

floor = box(pos = vector(0.0, -0.75, 0.0), length = Length+5, width = Length+5, height = 0.5, material = materials.bricks)
plate = frame(pos = vector(0, 0, 0))
disc = cylinder(frame = plate, pos = vector(0, -0.5, 0), radius = Length / 2, axis = vector(0, 0.5, 0), color = color.gray(0.7), material = materials.wood)
ceiling = cylinder(frame = plate, pos = vector(0, Length+2, 0), radius = Length / 4, axis = vector(0, 0.2, 0), color = color.gray(0.7), material = materials.rough, opacity = 0.7)
sphere(frame = plate, pos = ceiling.pos, radius = Length / 20, color = ceiling.color, opacity = 0.7)
ball_init_pos = vector(Length * sin(angle), ceiling.pos.y - Length * cos(angle), 0)

ball = sphere(pos = plate.frame_to_world(ball_init_pos), radius = 1, make_trail = False, color = color.red, material = materials.rough, opacity = 0.5,
                v = vector(0, 0, 0), a = vector(0, 0, 0))
stick = cylinder(pos = ceiling.pos, radius = 0.2, length = Length, axis = ball.pos - ceiling.pos, color = ball.color, material = materials.rough, opacity = 0.5)
footage = cylinder(frame = plate, pos = vector(ball.pos.x, 0.02, ball.pos.z), radius = ball.radius, axis = vector(0, 0.02, 0),
                    make_trail = False, color = ball.color, material = materials.rough, opacity = 0.5)

formula_ball = sphere(frame = plate, pos = ball_init_pos, radius = 1, make_trail = False, color = color.blue, material = materials.rough, opacity = 0.5,
                        v = vector(0, 0, 0), a = vector(0, 0, 0))
formula_stick = cylinder(frame = plate, pos = ceiling.pos, radius = 0.2, length = Length, axis = formula_ball.pos - ceiling.pos, color = formula_ball.color, material = materials.rough, opacity = 0.5)
formula_footage = cylinder(frame = plate, pos = vector(formula_ball.pos.x, 0.02, formula_ball.pos.z), radius = formula_ball.radius, axis = vector(0, 0.02, 0),
                            make_trail = False, color = formula_ball.color, material = materials.rough, opacity = 0.5)

forward = vector(Length / 4, 5, 0)
scene.forward = -plate.frame_to_world(forward)
scene.autoscale = False

def update_all(dt, scene):
    stick.axis = ball.pos - plate.frame_to_world(ceiling.pos)
    footage.pos.x = plate.world_to_frame(ball.pos).x
    footage.pos.z = plate.world_to_frame(ball.pos).z

    formula_stick.axis = formula_ball.pos - ceiling.pos
    formula_footage.pos.x = formula_ball.pos.x
    formula_footage.pos.z = formula_ball.pos.z

poss = [ball.pos, ball.pos]
trail = []
pball = []
start = False

def key_method(evt):
    global mode, rpm10, w, rota_demo
    key = evt.key
    if key == "i":
        mode = "inside"
    elif key == "o":
        mode = "outside"
    elif key == "p":
        for pb in pball:
            print("\nt = %d\nv: %s    %.5f   \na: %s    %.5f   \nobserver_a: %s    %.5f\nobserver_a: %s    %.5f"
                  %(pb[0], pb[1], pb[2], pb[3], pb[4], pb[5], pb[6], pb[7], pb[8]))
    elif start == False:
        if key == "left":
            rpm10 -= 1
            w = vector(0, 2*pi*rpm10/600.0, 0)
            rota_demo = str(rpm10/10.0)
        elif key == "right":
            rpm10 += 1
            w = vector(0, 2*pi*rpm10/600.0, 0)
            rota_demo = str(rpm10/10.0)
        info_demo.text = "  Rotation Speed(< >):\n    %s  rpm\n  Initial angle:\n    %s  deg" % (rota_demo, str(init_angle))

mode = "outside"
t = 0.0
dt = 0.001
count = 0

scene.waitfor("click")
scene.bind("keydown", key_method)
timer.color = color.yellow
timer.text = str(int(t))

while True:
    rate(1/dt)
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)

    plate.rotate(angle = mag(w) * dt, axis = norm(w))
    ball.pos = plate.frame_to_world(ball_init_pos)
    formula_ball.pos = ball_init_pos
    update_all(dt, scene)

    poss[0] = poss[1]*1
    poss[1] = ball.pos*1

    if scene.mouse.events:
        mous = scene.mouse.getevent()
        if mous.click == "left":
            break

    if mode == "inside":
        scene.forward = -plate.frame_to_world(forward)

start = True
dott = t+1
ball.make_trail = True
ball.retain = 500
footage.make_trail = True
footage.retain = 500
ball.v = count_v(dt,poss)
write("start %.18E %f %.18E %.18E %.18E %.18E %.18E %.18E\0" % (w.y, dt, poss[0][0], poss[0][1], poss[0][2], poss[1][0], poss[1][1], poss[1][2]))
write("c %d %.18E %.18E %.18E %.18E %.18E %.18E\0"
        % (count, ball.pos.x, ball.pos.y, ball.pos.z, formula_ball.pos.x, formula_ball.pos.y, formula_ball.pos.z))

dt = 0.01
n = 0

while True:
    rate(1/dt)
    
    timer.text = str(int(t))
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)
    
    t += dt
    count += 1
    n += 1

    while True:
        mess = read().split('$')
        if mess[0] == "c":
            break
    ball.pos = vector(float(mess[2]), float(mess[3]), float(mess[4]))
    formula_ball.pos = vector(float(mess[5]), float(mess[6]), float(mess[7]))
    plate.rotate(angle = mag(w) * dt, axis = norm(w))
    update_all(dt, scene)
    write("c %d %.18E %.18E %.18E %.18E %.18E %.18E\0"
            % (count, ball.pos.x, ball.pos.y, ball.pos.z, formula_ball.pos.x, formula_ball.pos.y, formula_ball.pos.z))

    trail.append(plate.world_to_frame(ball.pos))
    graph_trail.plot(pos = (footage.z, footage.x))
    deviation.plot(pos = (t, mag(plate.world_to_frame(ball.pos) - formula_ball.pos) / amplitude))
    scale.plot(pos = (-t/6, 0))

    if not(n % 900):
        graph_trail = gcurve(gdisplay = g_trail, pos = (footage.z, footage.x), color = color.red)
        deviation = gcurve(gdisplay = g_dev, pos = (t, mag(plate.world_to_frame(ball.pos) - formula_ball.pos) / amplitude), color = color.green)

    if t >= dott:
        pball.append([int(t), ball.v, 0, ball.a, 0, count_v(dt, trail[-2:]), 0, count_a(dt, trail[-3:]), 0])
        pball[-1][2] = mag(pball[-1][1])
        pball[-1][4] = mag(pball[-1][3])
        pball[-1][6] = mag(pball[-1][5])
        pball[-1][8] = mag(pball[-1][7])
        dott += 1
    
    if mode == "inside":
        scene.forward = -plate.frame_to_world(forward)

