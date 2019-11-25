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
from random import*
from func import*
from output import*

#Units: km, hr, radian
degree = 0.26251614     #Earth's rotation speed
rotate_ratio10 = 10     #rotate ratio times 10
w = vector(0, degree * rotate_ratio10/10.0, 0)
Er = 6371
latitude = float(raw_input("latitude : "))  #in degrees
if latitude >= 0:
    str_latitude = str(latitude) + " N"
else:
    str_latitude = str(-latitude) + " S"
fire_angle = 15     #in degrees
fire_dir = 30       #in degrees
balls_v = 25000.0
balls_duration = 2.5001
gn = 9.80665*(Er**2)*(3600**2)*(10**-3)
def gravity(r):
    return -gn/(mag(r)**2) * norm(r)

print "\nUnits: km, hr\n"
print "Controlings:\n left , right : change rotation speed\n w : raise throwing angle\n s : lower throwing angle\n a : throwing direction turns left\n d : throwing direction turns right"
print " i : camera rotates with Earth\n o : camera sets still\n b : camera follows flying balls\n r : save balls data"
print "\nclick to throw the ball\n\n*You can't change rotation speed while any ball exists."
sleep(5)


g_dev = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation", xtitle = "t", ytitle = "%")
gdots(gdisplay = g_dev, pos = [(-0.25, 0), (balls_duration-1, 0), (0, 0.005)], color = color.white, size = 0.01)

g_trail = display(x = 900, y = 350, width = 350, height = 350, center = vector(0, 0, 0), background = color.black, title = "Map", userspin = False,
                    lights = [distant_light(direction = vector(0, 0, 1)), distant_light(direction = vector(0, 0, -1))])
def project(lat, lon, z):
    return vector(Er*lon, Er*lat, z)

curve(display = g_trail, pos = [project(-pi/2, -pi, 0), project(pi/2, -pi, 0), project(pi/2, pi, 0),
                            project(-pi/2, pi, 0), project(-pi/2, -pi, 0)], color = color.gray(0.8), size = 3)
for lat in range(-90, 91, 30):
    curve(display = g_trail, pos = [project(radians(lat), -pi, 0), project(radians(lat), pi, 0)], color = color.gray(0.8), size = 1.5)
    label(display = g_trail, text = str(lat), pos = project(radians(lat), -pi*0.9, 0), box = False, line = False, opacity = 0)
for lon in range(-180, 181, 30):
    curve(display = g_trail, pos = [project(pi/2, radians(lon), 0), project(-pi/2, radians(lon), 0)], color = color.gray(0.8), size = 1.5)

label(display = g_trail, text = "latitude", pos = project(pi/2, -pi, 0) + vector(3500, 3000, 0), box = False, line = False, opacity = 0)
[label(display = g_trail, text = str(lat), pos = project(radians(lat), -pi*0.9, 0), box = False, line = False, opacity = 0) for lat in range(-90, 91, 30)]

updater = sphere(display = g_trail, radius = 1, color = color.white, make_trail = True, retain = 1050, trail_type = "points")
updater.trail_object.size = 1

scene = display(width = 900, height = 700, center = vector(0, 0, 0), background = color.black, title = "Throw Ball on Earth",
                lights = [distant_light(direction = vector(0, 1, 0), color = color.gray(0.7)), distant_light(direction = vector(0, -1, 0), color = color.gray(0.7)),
                          distant_light(direction = vector(1, 0, 0), color = color.gray(0.7)), distant_light(direction = vector(-1, 0, 0), color = color.gray(0.7)),
                          distant_light(direction = vector(0, 0, 1), color = color.gray(0.7)), distant_light(direction = vector(0, 0, -1), color = color.gray(0.7))])

[curve(pos = [vector(4000, -Er*1.2, z*400), vector(-4000, -Er*1.2, z*400)], color = color.gray(0.5)) for z in range(-10, 11)]
[curve(pos = [vector(x*400, -Er*1.2, 4000), vector(x*400, -Er*1.2, -4000)], color = color.gray(0.5)) for x in range(-10, 11)]

timer = label(text = "Click To Start", pos = scene.center, yoffset = scene.height/2-100, height = 50, color = color.red, box = False, line = False, opacity = 0)
rota_demo = str(rotate_ratio10/10.0)
info_demo = label(text = "  Rotation Speed(< >):\n    %sx\n  Latitude:\n    %s\n  Fire Angle(w s):\n    %s  deg\n  Fire Direction(a d):\n    %s  deg\n  Earth Radius:\n    %s  km"
                    % (rota_demo, str_latitude, str(fire_angle), str(fire_dir), str(Er)), pos = scene.center, xoffset = -(scene.width/2-180), height = 16, color = color.white, background = color.black, box = False, line = False, opacity = 0.7)

earth = frame(pos = vector(0, 0, 0))
sphere(frame = earth, radius = Er, material = materials.earth, opacity = 0.7)
player = pyramid(frame = earth, pos = vector(0, Er * sin(radians(latitude)), Er * cos(radians(latitude))), color = color.green, size = vector(100, 100, 100), material = materials.rough)
player.axis = norm(player.pos)
fireaxis = arrow(frame = earth, pos = player.pos, length = 300, color = color.green, material = materials.rough)
fireaxis.axis = rotate(rotate(rotate(vector(1, 0, 0), angle = radians(fire_angle), axis =  vector(0, -1, 0)), angle = radians(fire_dir), axis = vector(0, 0, 1)), angle = radians(latitude), axis = vector(-1, 0, 0)) * 300
track = cylinder(frame = earth, pos = vector(0, 0, 0), radius = 1.5*Er, length = 1, axis = norm(cross(player.axis, fireaxis.axis)), color = color.gray(0.7), opacity = 0.1)
update_frame = frame(frame = earth, axis = track.axis)

scene.forward = -earth.frame_to_world(player.pos)
scene.autoscale = False

poss = [player.pos, player.pos]
balln = -1
balls = []
arrows = []
trails = []
formula_balls = []
formula_arrows = []
balls_data = [[None], ["t"]]+[[i/200.0] for i in range(501)]

def new_ball():
    global balln, balls_data
    balln += 1
    graph_color = vector(uniform(0.3, 0.8), uniform(0.0, 0.5), uniform(0.3, 0.8))
    balls.append(sphere(pos = earth.frame_to_world(player.pos), radius = 40, make_trail = True, color = color.red, material = materials.rough, opacity = 0.5,
                        time = 0.0, num = balln, v = cross(w, earth.frame_to_world(player.pos)) + balls_v * norm(earth.frame_to_world(fireaxis.axis)), a = vector(0, 0, 0), S = 0.0,
                        graph_trail = sphere(display = g_trail, radius = 300, color = graph_color, make_trail = True, trail_type = "points", material = materials.rough),
                        deviation = gcurve(gdisplay = g_dev, color = graph_color, dot = True, size = 5, dot_color = graph_color), dev_count = 0,
                        data = [], dotn = 0, last_pos = earth.frame_to_world(player.pos)))
    balls[-1].a = gravity(balls[-1].pos)
    balls[-1].graph_trail.trail_object.display = g_trail
    balls[-1].graph_trail.trail_object.size = 2
    arrows.append(arrow(frame = earth, pos = balls[-1].pos, shaftwidth = 20, axis = vector(0, 0, 0), color = color.red, material = materials.rough, opacity = 0.5))
    trails.append(curve(frame = earth, pos = [earth.world_to_frame(balls[-1].pos), earth.world_to_frame(balls[-1].pos)], color = graph_color))
    
    formula_balls.append(sphere(frame = earth, pos = player.pos, radius = 40, make_trail = False, color = color.blue, material = materials.rough, opacity = 0.5,
                                v = balls_v * norm(fireaxis.axis), a = vector(0, 0, 0)))
    formula_balls[-1].a = gravity(formula_balls[-1].pos) - 2 * cross(w, formula_balls[-1].v) - cross(w, cross(w, formula_balls[-1].pos))
    formula_arrows.append(arrow(frame = earth, pos = formula_balls[-1].pos, shaftwidth = 20, axis = vector(0, 0, 0), color = color.blue, material = materials.rough, opacity = 0.5))
    
    balls[-1].data.append([balls[-1].pos, balls[-1].v, balls[-1].a, vector(trails[balls.index(balls[-1])].pos[-1]), "NO_DATA", "NO_DATA"])
    balls_data[0] += ["ball "+str(balln+1), "", "", "", "", ""]
    balls_data[1] += ["iner_pos", "iner_v", "iner_a(no gravity)", "non-iner_pos", "non-iner_v", "non-iner_a(no gravity)"]
    for i in range(501):
        balls_data[i+2] += [None, None, None, None, None, None]

def key_method(evt):
    global mode, balls_data, degree, rotate_ratio10, w, rota_demo, fire_angle, fire_dir
    k = evt.key
    if k == "i":
        mode = "inside"
        scene.center = timer.pos = info_demo.pos = vector(0, 0, 0)
    elif k == "o":
        mode = "outside"
        scene.center = timer.pos = info_demo.pos = vector(0, 0, 0)
        scene.forward = -earth.frame_to_world(player.pos)
    elif k == "b":
        mode = "ball"
    elif k == "r":
        save_csv("Earth_throwball.csv", balls_data)
    elif k == "left" and len(balls) == 0:
        rotate_ratio10 -= 1
        w = vector(0, degree * (rotate_ratio10/10.0), 0)
        rota_demo = str(rotate_ratio10/10.0)
    elif k == "right" and len(balls) == 0:
        rotate_ratio10 += 1
        w = vector(0, degree * (rotate_ratio10/10.0), 0)
        rota_demo = str(rotate_ratio10/10.0)
    elif k == "w" or k == "s" or k == "a" or k == "d":
        if k == "w" and fire_angle < 90:
            fire_angle += 1
        elif k == "s" and fire_angle > 0:
            fire_angle -= 1
        elif k == "a":
            fire_dir += 1
            fire_dir %= 360
        elif k == "d":
            fire_dir -=1
            fire_dir %= 360
        fireaxis.axis = rotate(rotate(rotate(vector(1, 0, 0), angle = radians(fire_angle), axis = vector(0, -1, 0)), angle = radians(fire_dir), axis = vector(0, 0, 1)), angle = radians(latitude), axis = vector(-1, 0, 0)) * 300
        if not fire_angle == 90:
            update_frame.axis = track.axis = norm(cross(player.axis, fireaxis.axis))
    info_demo.text = ("  Rotation Speed(< >):\n    %sx\n  Latitude:\n    %s\n  Fire Angle(w s):\n    %s  deg\n  Fire Direction(s d):\n    %s  deg\n  Earth Radius:\n    %s  km"
                        % (rota_demo, str_latitude, str(fire_angle), str(fire_dir), Er))

mode = "outside"
t = 0
dt = 0.0001

scene.waitfor("click")
while scene.mouse.clicked:
    scene.mouse.getclick()
while scene.kb.keys:
    scene.kb.getkey()
scene.bind("keydown", key_method)
timer.color = color.yellow

while True:
    rate(0.1/dt)
    
    t += dt
    timer.text = str(int(t*10)/10.0)+" hr"
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)

    earth.rotate(angle = mag(w) * dt, axis = norm(w))
    update(dt, scene)

    if scene.mouse.clicked:
        scene.mouse.getclick()
        new_ball()
    
    tmp_pos = update_frame.frame_to_world(vector(0, sin(-t*60)*Er, cos(-t*60)*Er))
    updater_lat = asin(tmp_pos.y/Er)
    if tmp_pos.z > 0:
        updater_lon = atan(tmp_pos.x/tmp_pos.z)
    else:
        if tmp_pos.x > 0:
            updater_lon = pi + atan(tmp_pos.x/tmp_pos.z)
        else:
            updater_lon = -pi + atan(tmp_pos.x/tmp_pos.z)
    updater.pos = project(updater_lat, updater_lon, 1)

    poss[0] = poss[1]*1
    poss[1] = earth.frame_to_world(player.pos)*1
    
    for b in balls:
        if b.time > balls_duration or mag(b.pos) - Er <= -0.01 or mag(b.pos) >= 5 * Er:
            for i in range(len(b.data)):
                for j in range(6):
                    balls_data[i+2][j+b.num*6+1] = b.data[i][j]
            b.trail_object.visible = False
            b.visible = False
            b.graph_trail.visible = False
            formula_balls[balls.index(b)].visible = False
            arrows[balls.index(b)].visible = False
            formula_arrows[balls.index(b)].visible = False
            del b.deviation, b.graph_trail, trails[balls.index(b)], formula_arrows[balls.index(b)], formula_balls[balls.index(b)], arrows[balls.index(b)], balls[balls.index(b)]
        
        else:
            b.time += dt
            b.dotn += 1
            ballpos = earth.world_to_frame(b.pos)
            b.a = gravity(b.pos)
            trails[balls.index(b)].append(pos = ballpos)
            
            if b.S:
                b.deviation.plot(pos = (b.time, mag(ballpos - formula_balls[balls.index(b)].pos)*100 / b.S))
            
            updater_lat = asin(ballpos.y/mag(ballpos))
            if ballpos.z > 0:
                updater_lon = atan(ballpos.x/ballpos.z)
            else:
                if ballpos.x > 0:
                    updater_lon = pi + atan(ballpos.x/ballpos.z)
                else:
                    updater_lon = -pi + atan(ballpos.x/ballpos.z)
            b.graph_trail.pos = project(updater_lat, updater_lon, 1)

            if b.dotn > 1 and not((b.dotn-1) % 50):
                b.data.append([b.pos, b.v, b.a - gravity(b.last_pos),
                               vector(trails[balls.index(b)].pos[-2]),
                               vector(count_v(dt, trails[balls.index(b)].pos[-3:])),
                               vector(count_a(dt, trails[balls.index(b)].pos[-3:])) - gravity(vector(trails[balls.index(b)].pos[-2]))])
                b.last_pos = b.pos*1
            arrows[balls.index(b)].pos = ballpos
            arrows[balls.index(b)].axis = (vector(count_a(dt, trails[balls.index(b)].pos[-3:]))
                                            - gravity(vector(trails[balls.index(b)].pos[-2]))) * 0.03
    
    for fb in formula_balls:
        fb.a = gravity(fb.pos) - 2 * cross(w, fb.v) - cross(w, cross(w, fb.pos))
        formula_arrows[formula_balls.index(fb)].pos = fb.pos
        formula_arrows[formula_balls.index(fb)].axis = (fb.a - gravity(fb.pos)) * 0.03
    
    if mode == "inside":
        scene.forward = -earth.frame_to_world(player.pos)
    elif mode == "ball" and len(balls):
        scene.center = timer.pos = info_demo.pos = balls[-1].pos
        scene.forward = -balls[-1].pos

