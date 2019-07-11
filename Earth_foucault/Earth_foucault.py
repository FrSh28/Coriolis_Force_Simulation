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
from visual.graph import*
import subprocess
from communicate import*
from func import*
from output import*

#Units: km, hr, radian
degree = 0.26251614     #Earth's rotation speed
rotate_ratio10 = 0     #rotate ratio times 10
w = vector(0, degree * rotate_ratio10/10.0, 0)
Er = 6371
latitude = abs(float(raw_input("latitude : ")))  #in degrees
init_angle = 0
while init_angle <= 0:
    init_angle = float(raw_input("initial angle(<20 deg) : "))  #in degrees
angle = radians(init_angle)
m = 30.0
kc = 500000000.0
Length = 10
amplitude = Length * sin(angle)
gn = 9.80665*(Er**2)*(3600**2)*(10**-3)
def gravity(r):
    return -gn/(mag(r)**2) * norm(r)

print "\nUnits: km, hr\n"
print "Controlings:\n left , right : change rotation speed\n i : camera rotates with Earth\n o : camera sets still\n r : save pendulum data"
print "\nclick to release the pendulum\n\n*You can't change rotation speed after releasing the pendulum."
#exe cpp
subprocess.Popen([str(os.path.dirname(os.path.realpath(__file__)))+"\\vector_calculate.exe"])
sleep(5)
connect()
write("init %f %f %f\0"%(m, kc, Length))


g_dev = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation", xtitle = "t", ytitle = "%")
scale = gdots(gdisplay = g_dev, pos = [(-1, 0), (5, 0), (0, 0.0001)], color = color.white, size = 0.01)
deviation = gcurve(gdisplay = g_dev, color = color.green)

g_trail = gdisplay(x = 900, y = 350, width = 350, height = 350, xmax = amplitude, xmin = -amplitude, ymax = amplitude, ymin = -amplitude, title = "Trail on Ground")
gdots(gdisplay = g_trail, pos = (0 , 0), size = 1)
graph_trail = gcurve(gdisplay = g_trail, color = color.red)

scene = display(width = 900, height = 700, center = vector(0, 0, 0), background = color.black, title = "Foucault Pendulum",
                lights = [distant_light(direction = vector(0, 1, 0), color = color.gray(0.7)), distant_light(direction = vector(0, -1, 0), color = color.gray(0.7)),
                          distant_light(direction = vector(1, 0, 0), color = color.gray(0.7)), distant_light(direction = vector(-1, 0, 0), color = color.gray(0.7)),
                          distant_light(direction = vector(0, 0, 1), color = color.gray(0.7)), distant_light(direction = vector(0, 0, -1), color = color.gray(0.7))])

timer = label(text = "Click To Start", pos = scene.center, yoffset = scene.height/2-100, height = 50, color = color.red, box = False, line = False, opacity = 0)
rota_demo = str(rotate_ratio10/10.0)
latitude_str = str(latitude) + " N"
info_demo = label(text = "  Rotation Speed(< >):\n    %sx\n  Latitude:\n    %s\n  Init Angle:\n    %s  deg\n  Earth Radius:\n    %s  km"
                            % (rota_demo, str(latitude), str(init_angle), Er), pos = scene.center, xoffset = -(scene.width/2-180), height = 16, color = color.white, background = color.black, box = False, line = False, opacity = 0.7)

earth = frame(pos = vector(0, 0, 0))
ground = frame(frame = earth, pos = vector(0, Er * sin(radians(latitude)), Er * cos(radians(latitude))))
floor = box(frame = ground, pos = vector(0, 0, 0), length = Length, width = Length, height = 0.2, material = materials.wood)
ceiling = sphere(frame = ground, pos = vector(0, Length+0.3, 0), color = color.gray(0.3), radius = 0.1, material = materials.rough)
ball_init_pos = vector(0, ceiling.pos.y - Length * cos(angle), Length * sin(angle))
ground.rotate(angle = radians(90-latitude), axis = vector(1, 0, 0))

ball = sphere(pos = earth.frame_to_world(ground.frame_to_world(ball_init_pos)), radius = 0.15, make_trail = False, color = color.red, material = materials.rough, opacity = 0.5,
              v = vector(0, 0, 0), a = vector(0, 0, 0))
stick = cylinder(pos = earth.frame_to_world(ground.frame_to_world(ceiling.pos)), length = Length, radius = 0.05, color = ball.color, material = materials.rough, opacity = 0.5)
stick.axis = ball.pos - stick.pos
footage = cylinder(frame = ground, pos = vector(earth.world_to_frame(ground.world_to_frame(ball.pos)).x, 0.1, earth.world_to_frame(ground.world_to_frame(ball.pos)).z),
                   radius = ball.radius, axis =   vector(0, 0.001, 0), make_trail = False, color = ball.color, material = materials.rough, opacity = 0.5)

formula_ball = sphere(frame = earth, pos = ground.frame_to_world(ball_init_pos), radius = 0.15, make_trail = False, color = color.blue, material = materials.rough, opacity = 0.5,
                      v = vector(0, 0, 0), a = vector(0, 0, 0))
formula_stick = cylinder(frame = earth, pos = ground.frame_to_world(ceiling.pos), length = Length, radius = 0.05, color = formula_ball.color, material = materials.rough, opacity = 0.5)
formula_stick.axis = formula_ball.pos - formula_stick.pos
formula_footage = cylinder(frame = ground, pos = vector(ground.world_to_frame(formula_ball.pos).x, 0.1, ground.world_to_frame(formula_ball.pos).z),
                           radius = formula_ball.radius, axis = vector(0, 0.001, 0), make_trail = False, color = formula_ball.color, material = materials.rough, opacity = 0.5)

scene.forward = -earth.frame_to_world(ground.pos)
scene.autoscale = False

def update_line(dt, scene):
    stick.pos = earth.frame_to_world(ground.frame_to_world(ceiling.pos))
    stick.axis = ball.pos - stick.pos
    footage.pos.x = ground.world_to_frame(earth.world_to_frame(ball.pos)).x
    footage.pos.z = ground.world_to_frame(earth.world_to_frame(ball.pos)).z

    formula_stick.pos = ground.frame_to_world(ceiling.pos)
    print formula_stick.pos
    formula_stick.axis = formula_ball.pos - formula_stick.pos
    formula_footage.pos.x = ground.world_to_frame(formula_ball.pos).x
    formula_footage.pos.z = ground.world_to_frame(formula_ball.pos).z

ball_pos = []
trail = []
data = [["t", "iner_pos", "iner_v", "iner_a", "non-iner_pos", "non-iner_v", "non-iner_a"]]
start = False

def key_method(evt):
    global mode, degree, rotate_ratio10, w, rota_demo
    key = evt.key
    if key == "i":
        mode = "inside"
        scene.range = vector(200, 200, 200)
    elif key == "o":
        mode = "outside"
        scene.center = timer.pos = info_demo.pos = vector(0, 0, 0)
        scene.forward = -earth.frame_to_world(ground.pos)
        scene.range = vector(3900, 3900, 3900)
    elif key == "r":
        save_csv("Earth_foucault.csv", data)
    elif start == False:
        if key == "left":
            rotate_ratio10 -= 1
            w = vector(0, degree * (rotate_ratio10/10.0), 0)
            rota_demo = str(rotate_ratio10/10.0)
        elif key == "right":
            rotate_ratio10 += 1
            w = vector(0, degree * (rotate_ratio10/10.0), 0)
            rota_demo = str(rotate_ratio10/10.0)
        info_demo.text = "  Rotation Speed(< >):\n    %sx\n  Latitude:\n    %s N\n  Init Angle:\n    %s  deg\n  Earth Radius:\n    %s  km"%(rota_demo, str(latitude), str(degrees(angle)), Er)

sphere(frame = earth, radius = Er, material = materials.earth)
[curve(pos = [vector(4000, -Er*1.2, z*400), vector(-4000, -Er*1.2, z*400)], color = color.gray(0.5)) for z in range(-10, 11)]
[curve(pos = [vector(x*400, -Er*1.2, 4000), vector(x*400, -Er*1.2, -4000)], color = color.gray(0.5)) for x in range(-10, 11)]

mode = "outside"
t = 0.0
dt = 0.0001
count = 0

scene.waitfor("click")
while scene.mouse.events:
    scene.mouse.getevent()
while scene.kb.keys:
    scene.kb.getkey()
scene.bind("keydown", key_method)
timer.color = color.yellow
timer.text = str(int(t*10)/10.0) + " hr"

while True:
    rate(0.1/dt)
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)

    earth.rotate(angle = mag(w) * dt, axis = norm(w))
    ball.pos = earth.frame_to_world(ground.frame_to_world(ball_init_pos))
    formula_ball.pos = ground.frame_to_world(ball_init_pos)
    update_line(dt, scene)

    if scene.mouse.events:
        mous = scene.mouse.getevent()
        if mous.click == "left":
            break

    if mode == "inside":
        scene.center = timer.pos = info_demo.pos = earth.frame_to_world(ground.pos)
        scene.forward = rotate(-stick.pos, angle = radians(60), axis = cross(-stick.pos, scene.up))

start = True
footage.make_trail = True
footage.retain = 1000
ball.v = cross(w, ball.pos)
ball.a = gravity(ball.pos)
ball_pos += [ball.pos*1]
trail += [ground.world_to_frame(earth.world_to_frame(ball.pos)), ground.world_to_frame(earth.world_to_frame(ball.pos))]
data.append([count/100.0, ball.pos, ball.v, ball.a, vector(trail[-1]), "NO_DATA", "NO_DATA"])
write("start %.18E %f %.18E %.18E %.18E %.18E %.18E %.18E\0" % (w.y, dt, ball.pos.x, ball.pos.y, ball.pos.z, formula_stick.pos.x, formula_stick.pos.y, formula_stick.pos.z))
write("c %d %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E\0"
        % (count, ball.pos.x, ball.pos.y, ball.pos.z, stick.pos.x, stick.pos.y, stick.pos.z,
            formula_ball.pos.x, formula_ball.pos.y, formula_ball.pos.z))

dt = 0.001

while True:
    rate(0.1/dt)
    
    t += dt
    count += 1
    timer.text = str(int(t*10)/10.0) + " hr"
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)

    while True:
        mess = read().split('$')
        if mess[0] == "c":
            break
    ball.pos = vector(float(mess[2]), float(mess[3]), float(mess[4]))
    formula_ball.pos = vector(float(mess[5]), float(mess[6]), float(mess[7]))
    earth.rotate(angle = mag(w) * dt, axis = norm(w))
    update_line(dt, scene)
    write("c %d %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E %.18E\0"
            % (count, ball.pos.x, ball.pos.y, ball.pos.z, stick.pos.x, stick.pos.y, stick.pos.z,
                formula_ball.pos.x, formula_ball.pos.y, formula_ball.pos.z))
    
    ball_pos.append(ball.pos*1)
    trail.append(ground.world_to_frame(earth.world_to_frame(ball.pos)))
    graph_trail.plot(pos = (trail[-1][0], -trail[-1][2]))
    deviation.plot(pos = (t, mag(earth.world_to_frame(ball.pos) - formula_ball.pos)*100.0 / amplitude))
    scale.plot(pos = (-t/6, 0))

    if not(count % 900):
        graph_trail = gcurve(gdisplay = g_trail, pos = (trail[-1][0], -trail[-1][2]), color = color.red)
        deviation = gcurve(gdisplay = g_dev, pos = (t, mag(earth.world_to_frame(ball.pos) - formula_ball.pos)*100.0 / amplitude), color = color.green)
    
    if count > 1 and not((count-1) % 5):
        data.append([count/1000.0, ball_pos[-1], count_v(dt, ball_pos[-3:]), count_a(dt, ball_pos[-3:]), count_v(dt, trail[-3:]), count_a(dt, trail[-3:])])
    
    if mode == "inside":
        scene.center = timer.pos = info_demo.pos = earth.frame_to_world(ground.pos+vector(0,0.3,0))
        scene.forward = rotate(-stick.pos, angle = radians(60), axis = cross(-stick.pos, scene.up))

