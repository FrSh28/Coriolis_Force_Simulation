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
from communicate import*
import subprocess

#Units: hr, km, degree
degree = 15.0
w = vector(0, radians(degree), 0)
Er = 6371
latitude = abs(float(raw_input("latitude : ")))
init_angle = float(raw_input("initial angle(<20 deg) : "))
angle = radians(init_angle)
m = 32.0
kc = 500000000.0
Length = 6.7

print "\nUnits: hr , km\n"
print "Controlings:\n ← : rotation speed down\n → : rotation speed up\n i : camera rotates with disc\n o : camera sets still"
print "\nclick to release the pendulum\n"
print "You can't change rotation speed after releasing the pendulum\n"
#execpp
subprocess.Popen([str(os.path.dirname(os.path.realpath(__file__)))+"\\vector_calculate.exe"])
sleep(5)
connect()
write("init %f %f %f\0"%(m, kc, Length))


gd = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation")
deviation = gdots(pos = (0, 0), gdisplay = gd, color = color.green, size = 1)
scale = gdots(gdisplay = gd, pos = [(-1, 0), (5, 0)], color = color.white, visible = False, size = 0.01)

gsize = Length * sin(angle)
gd1 = gdisplay(x = 900, y = 350, width = 350, height = 350, xmax = gsize, xmin = -gsize, ymax = gsize, ymin = -gsize, title = "Trail on Ground: X vs Z")
f1 = gdots(gdisplay = gd1, color = color.red, size = 1)
gdots(gdisplay = gd1, pos = (0 , 0),size = 1 )

scene = display(width = 900, height = 700, center = (0, 0, 0), background = (0, 0, 0), title = "Foucault Pendulum",
                lights = [distant_light(direction = (0, 1, 0), color = color.gray(0.7)), distant_light(direction = (0, -1, 0), color = color.gray(0.7)),
                          distant_light(direction = (1, 0, 0), color = color.gray(0.7)), distant_light(direction = (-1, 0, 0), color = color.gray(0.7)),
                          distant_light(direction = (0, 0, 1), color = color.gray(0.7)), distant_light(direction = (0, 0, -1), color = color.gray(0.7))])

timer = label(text = "Click To Start", pos = scene.center, yoffset = scene.height/2-100, height = 50, color = color.red, box = False, line = False, opacity = 0)
rota_demo = str(int(degree*100/15.0)/100.0)
info_demo = label(text = "  Rotation Speed(< >):\n    %sx\n  Latitude:\n    %s N\n  Angle:\n    %s  deg\n  Earth Radius:\n    %s  km"%(rota_demo, str(latitude), str(degrees(angle)), Er),
                   pos = scene.center, xoffset = -(scene.width/2-180), height = 16, color = color.gray(0.8), box = False, line = False, opacity = 0.2)

earth = frame(pos = (0, 0, 0))
ground = frame(frame = earth, pos = (Er * -cos(radians(latitude)), Er * sin(radians(latitude)), 0))
floor = box(frame = ground, pos = (0, 0, 0), length = Length, width = Length, height = 0.2, material = materials.wood)
ceiling = sphere(frame = ground, pos = (0, Length+0.3, 0), color = color.gray(0.3), radius = 0.1, material = materials.rough)
ball_init = sphere(frame = ground, pos = (Length * -sin(angle), ceiling.pos.y - Length * cos(angle), 0), visible = False)
ground.rotate(angle = radians(90-latitude), axis = (0, 0, 1))

ball = sphere(pos = earth.frame_to_world(ground.frame_to_world(ball_init.pos)), radius = 0.15,
              v = vector(0.0, 0.0, 0.0), a = vector(0.0, 0.0, 0.0), make_trail = False, color = color.red, material = materials.rough, opacity = 0.5)
stick = cylinder(pos = earth.frame_to_world(ground.frame_to_world(ceiling.pos)), length = Length, radius = 0.05, color = ball.color, material = materials.rough, opacity = 0.5)
stick.axis = ball.pos - stick.pos
footage = cylinder(frame = ground, pos = (earth.world_to_frame(ground.world_to_frame(ball.pos)).x, 0.1, earth.world_to_frame(ground.world_to_frame(ball.pos)).z),
                   radius = ball.radius, axis = (0, 0.001, 0), make_trail = False, color = ball.color, material = materials.rough, opacity = 0.5)

formula_ball = sphere(frame = earth, pos = ground.frame_to_world(ball_init.pos), radius = 0.15,
                      v = vector(0.0,0.0,0.0), a = vector(0.0, 0.0, 0.0), make_trail = False, color = color.blue, material = materials.rough, opacity = 0.5)
formula_stick = cylinder(frame = earth, pos = ground.frame_to_world(ceiling.pos), length = Length, radius = 0.05, color = formula_ball.color, material = materials.rough, opacity = 0.5)
formula_stick.axis = formula_ball.pos - formula_stick.pos
formula_footage = cylinder(frame = ground, pos = (ground.world_to_frame(formula_ball.pos).x, 0.1, ground.world_to_frame(formula_ball.pos).z),
                           radius = formula_ball.radius, axis = (0, 0.001, 0), make_trail = False, color = formula_ball.color, material = materials.rough, opacity = 0.5)

scene.forward = -earth.frame_to_world(ground.pos)
scene.autoscale = False

def update_all(dt, scene):
    stick.pos = earth.frame_to_world(ground.frame_to_world(ceiling.pos))
    stick.axis = ball.pos - stick.pos
    footage.pos.x = ground.world_to_frame(earth.world_to_frame(ball.pos)).x
    footage.pos.z = ground.world_to_frame(earth.world_to_frame(ball.pos)).z

    formula_stick.pos = ground.frame_to_world(ceiling.pos)
    formula_stick.axis = formula_ball.pos - formula_stick.pos
    formula_footage.pos.x = ground.world_to_frame(formula_ball.pos).x
    formula_footage.pos.z = ground.world_to_frame(formula_ball.pos).z

poss = [ball.pos, ball.pos]
start = False

def key_method(evt):
    global mode, degree, w, rota_demo
    key = evt.key
    if key == "i":
        mode = "inside"
        scene.range = (250, 250, 250)
    elif key == "o":
        mode = "outside"
        scene.center = timer.pos = info_demo.pos = vector(0, 0, 0)
        scene.forward = -earth.frame_to_world(ground.pos)
        scene.range = (3900, 3900, 3900)
    elif start == False:
        if key == "left":
            degree -= 1
            w = vector(0, radians(degree), 0)
            rota_demo = str(int(degree*100/15.0)/100.0)
        elif key == "right":
            degree += 1
            w = vector(0, radians(degree), 0)
            rota_demo = str(int(degree*100/15.0)/100.0)
        info_demo.text = "  Rotation Speed(< >):\n    %sx\n  Latitude:\n    %s N\n  Angle:\n    %s  deg\n  Earth Radius:\n    %s  km"%(rota_demo, str(latitude), str(degrees(angle)), Er)

cylinder(frame = earth, pos = (0, -Er*1.2, 0), radius = 20, axis = (0, 3*Er, 0), color = color.green)
sphere(frame = earth, radius = Er, material = materials.earth, opacity = 0.4)
[curve(pos = [(4000, -Er*1.2, z*400), (-4000, -Er*1.2, z*400)], color = color.gray(0.5))for z in range(-10, 11)]
[curve(pos = [(x*400, -Er*1.2, 4000), (x*400, -Er*1.2, -4000)], color = color.gray(0.5))for x in range(-10, 11)]

mode = "outside"
t = 0.0
dt = 0.0001
count = 0

scene.waitfor("click")
scene.bind("keydown", key_method)
timer.color = color.yellow
timer.text = str(int(t*10)/10.0) + " hr."

while True:
    rate(0.1/dt)
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)

    earth.rotate(angle = radians(degree * dt), axis = (0, 1, 0))
    ball.pos = earth.frame_to_world(ground.frame_to_world(ball_init.pos))
    formula_ball.pos = ground.frame_to_world(ball_init.pos)
    update_all(dt, scene)

    poss[0] = poss[1]*1
    poss[1] = ball.pos*1

    if scene.mouse.events:
        mous = scene.mouse.getevent()
        if mous.click == "left":
            break

    if mode == "inside":
        scene.center = timer.pos = info_demo.pos = earth.frame_to_world(ground.pos)
        scene.forward = rotate(-stick.pos, angle = radians(60), axis = cross(-stick.pos, scene.up))

start = True
ball.make_trail = True
ball.retain = 500
footage.make_trail = True
footage.retain = 500
trail = points(frame = ground, pos = [ground.world_to_frame(earth.world_to_frame(ball.pos))], color = color.red, size = 1)
write("start %.18E %f %.18E %.18E %.18E %.18E %.18E %.18E\0"%(w.y, dt, poss[0][0], poss[0][1], poss[0][2], poss[1][0], poss[1][1], poss[1][2]))
write("c %d %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E\0"
    %(count, ball.pos.x, ball.pos.y, ball.pos.z, stick.pos.x, stick.pos.y, stick.pos.z, 
        formula_ball.pos.x, formula_ball.pos.y, formula_ball.pos.z, formula_stick.pos.x, formula_stick.pos.y, formula_stick.pos.z))

dt = 0.001

while True:
    rate(0.1/dt)
    
    timer.text = str(int(t*10)/10.0) + " hr."
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
    earth.rotate(angle = radians(degree * dt), axis = (0, 1, 0))
    update_all(dt, scene)
    write("c %d %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E\0"
        %(count, ball.pos.x, ball.pos.y, ball.pos.z, stick.pos.x, stick.pos.y, stick.pos.z, 
            formula_ball.pos.x, formula_ball.pos.y, formula_ball.pos.z, formula_stick.pos.x, formula_stick.pos.y, formula_stick.pos.z))

    trail.append(pos = ground.world_to_frame(earth.world_to_frame(ball.pos)))
    f1.plot(pos = (trail.pos[-1][2], trail.pos[-1][0]))
    deviation.plot(pos = (t, abs(earth.world_to_frame(ball.pos) - formula_ball.pos)))
    scale.plot(pos = (-t/6, 0))    
    
    if mode == "inside":
        scene.center = timer.pos = info_demo.pos = earth.frame_to_world(ground.pos)
        scene.forward = rotate(-stick.pos, angle = radians(60), axis = cross(-stick.pos, scene.up))
    




