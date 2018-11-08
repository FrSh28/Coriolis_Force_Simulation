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

#Units: sec, cm, degree
degree = 6.0
w = vector(0, radians(degree), 0)
angle = float(raw_input("initial angle(<15 deg) : "))
m = 20.0
kc = 500000.0
Length = 50.0

print "\nControlings:\n ← : rotation speed down\n → : rotation speed up\n i : camera rotates with disc\n o : camera sets still\n p : print pendulum data"
print "\nclick to release the pendulum\n"
print "You can't change rotation speed after releasing the pendulum\n"
subprocess.Popen([str(os.path.dirname(os.path.realpath(__file__)))+"\\vector_calculate.exe"])
sleep(5)
connect()
write("init %f %f %f %f\0"%(m, kc, Length, Length+2))   #stick.pos = (0,Length+2,0)


gd = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation")
deviation = gdots(gdisplay = gd, pos = (0, 0), color = color.green, size = 1)
scale = gdots(gdisplay = gd, pos = [(-1, 0), (5, 0)], color = color.white, size = 0.01)

gd1 = gdisplay(x = 900, y = 350, width = 350, height = 350, title = "Trail on Disc")
gplayer = gcurve(gdisplay = gd1, color = color.white)
gplayer.plot(pos = [(20*cos(radians(angle1)), 20*sin(radians(angle1))) for angle1 in range(360)])
f1 = gdots(gdisplay = gd1, color = color.red, size = 0.01)

scene = display(width = 900, height = 700, center = (0, 2, 0), background = (0, 0, 0), title = "Pendulum on Disc",
                lights = [local_light(pos = (0, 30, 0), color = color.gray(0.8))])
floor = box(pos = (0.0, -0.75, 0.0), length = 40, width = 40, height = 0.5, material = materials.bricks)

timer = label(text = "Click to start", pos = scene.center, yoffset = scene.height/2-100, height = 50, color = color.red, box = False, line = False, opacity = 0)
rota_demo = str(int(degree*100/6.0)/100.0)
info_demo = label(text = "  Rotation Speed(< >):\n    %s  rpm\n  Initial angle:\n    %s  deg"%(rota_demo, str(angle)),
                  pos = scene.center, xoffset = -(scene.width/2-180), height = 18, color = color.gray(0.8), box = False, line = False, opacity = 0.2)

plate = frame(pos = (0, 0, 0))
disc = cylinder(frame = plate, pos = (0, -0.5, 0), radius = 20, axis = (0, 0.5, 0), color = color.white, material = materials.wood)
ceiling = cylinder(frame = plate, pos = (0, Length+2, 0), radius = 8, axis = (0, 0.2, 0), color = color.gray(0.7), material = materials.rough, opacity = 0.7)
sphere(frame = plate, pos = ceiling.pos, radius = 0.2, color = ceiling.color, opacity = 0.7)
ball_init = sphere(frame = plate, pos = (Length * -sin(radians(angle)), ceiling.pos.y - Length * cos(radians(angle)), 0.0), visible = False)

ball = sphere(pos = plate.frame_to_world(ball_init.pos), radius = 0.5, v = vector(0.0, 0.0, 0.0), a = vector(0.0, 0.0, 0.0),
              make_trail = False, color = color.red, material = materials.rough, opacity = 0.5)
stick = cylinder(pos = ceiling.pos, radius = 0.1, length = Length, axis = ball.pos - ceiling.pos, color = ball.color, material = materials.rough, opacity = 0.5)
footage = cylinder(frame = plate, pos = (ball.pos.x, 0.02, ball.pos.z), radius = ball.radius, axis = (0, 0.02, 0), make_trail = False,
                   color = ball.color, material = materials.rough, opacity = 0.5)

formula_ball = sphere(frame = plate, pos = ball_init.pos, radius = 0.5, v = vector(0.0, 0.0, 0.0), a = vector(0.0, 0.0, 0.0),
                      make_trail = False, color = color.blue, material = materials.rough, opacity = 0.5)
formula_stick = cylinder(frame = plate, pos = ceiling.pos, radius = 0.1, length = Length, axis = formula_ball.pos - ceiling.pos, color = formula_ball.color, material = materials.rough, opacity = 0.5)
formula_footage = cylinder(frame = plate, pos = (formula_ball.pos.x, 0.02, formula_ball.pos.z), radius = formula_ball.radius, axis = (0, 0.02, 0), make_trail = False,
                           color = formula_ball.color, material = materials.rough, opacity = 0.5)

scene.forward = (-plate.frame_to_world(ball_init.pos).x, -3, -plate.frame_to_world(ball_init.pos).z)
scene.autoscale = False

def update_all(dt, scene):
    stick.axis = ball.pos - plate.frame_to_world(ceiling.pos)
    footage.pos.x = plate.world_to_frame(ball.pos).x
    footage.pos.z = plate.world_to_frame(ball.pos).z

    formula_stick.axis = formula_ball.pos - ceiling.pos
    formula_footage.pos.x = formula_ball.pos.x
    formula_footage.pos.z = formula_ball.pos.z

poss = [ball_init.pos, ball_init.pos]
ballpos_list = []
trail = []
pball = []
start = False

def key_method(evt):
    global mode, degree, w, rota_demo
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
            degree -= 1
            w = vector(0, radians(degree), 0)
            rota_demo = str(int(degree*100/6.0)/100.0)
        elif key == "right":
            degree += 1
            w = vector(0, radians(degree), 0)
            rota_demo = str(int(degree*100/6.0)/100.0)
        info_demo.text = "  Rotation Speed(< >):\n    %s  rpm\n  Initial angle:\n    %s  deg"%(rota_demo, str(angle))

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

    plate.rotate(angle = radians(degree * dt), axis = (0, 1, 0))
    ball.pos = plate.frame_to_world(ball_init.pos)
    formula_ball.pos = ball_init.pos
    update_all(dt, scene)

    poss[0] = poss[1]*1
    poss[1] = ball.pos*1

    if scene.mouse.events:
        mous = scene.mouse.getevent()
        if mous.click == "left":
            break

    if mode == "inside":
        scene.forward = vector(-plate.frame_to_world(ball_init.pos).x, -3, -plate.frame_to_world(ball_init.pos).z)

start = True
dott = t+1
ball.make_trail = True
ball.retain = 500
footage.make_trail = True
footage.retain = 500
ball.v = count_v(dt,poss)
write("start %.18E %f %.18E %.18E %.18E %.18E %.18E %.18E\0"%(w.y, dt, poss[0][0], poss[0][1], poss[0][2], poss[1][0], poss[1][1], poss[1][2]))
write("c %d %.18E %.18E %.18E %.18E %.18E %.18E\0"
    %(count, ball.pos.x, ball.pos.y, ball.pos.z, formula_ball.pos.x, formula_ball.pos.y, formula_ball.pos.z))

dt = 0.01

while True:
    rate(1/dt)
    
    timer.text = str(int(t))
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)
    
    t += dt
    count += 1

    while True:
        mess = read().split('$')
        if mess[0] == "c":
            break
    ball.pos = vector(float(mess[2]), float(mess[3]), float(mess[4]))
    formula_ball.pos = vector(float(mess[5]), float(mess[6]), float(mess[7]))
    plate.rotate(angle = radians(degree * dt), axis = (0, 1, 0))
    update_all(dt, scene)
    write("c %d %.18E %.18E %.18E %.18E %.18E %.18E\0"
        %(count, ball.pos.x, ball.pos.y, ball.pos.z, formula_ball.pos.x, formula_ball.pos.y, formula_ball.pos.z))

    ballpos_list.append(ball.pos*1)
    trail.append(plate.world_to_frame(ball.pos))
    f1.plot(pos = (footage.z, footage.x))
    deviation.plot(pos = (t, abs(plate.world_to_frame(ball.pos) - formula_ball.pos)))
    scale.plot(pos = (-t/6, 0))

    if len(ballpos_list) >= 3 and t >= dott:
        pball.append([int(t), count_v(dt, ballpos_list[-2:]), 0, count_a(dt, ballpos_list[-3:]), 0, count_v(dt, trail[-2:]), 0, count_a(dt, trail[-3:]), 0])
        pball[-1][2] = abs(pball[-1][1])
        pball[-1][4] = abs(pball[-1][3])
        pball[-1][6] = abs(pball[-1][5])
        pball[-1][8] = abs(pball[-1][7])
        dott += 1
    
    if mode == "inside":
        scene.forward = vector(-plate.frame_to_world(ball_init.pos).x, -3, -plate.frame_to_world(ball_init.pos).z)





