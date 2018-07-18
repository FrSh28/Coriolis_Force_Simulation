# -*- coding: cp950 -*-
from visual import*
from visual.graph import*
from func import*

###############  相關參數  ###############
#hr, km
degree = 15.0             #每hr.自轉的角度
w = vector(0, radians(degree), 0)
Er = 6371               #地半徑
latitude = abs(float(raw_input("latitude : ")))             #緯度
init_angle = float(raw_input("initial angle(<20 deg) : "))             #初始角度
angle = radians(init_angle)
m = 28.0                  #球的重量
kc = 500000000.0              #彈力係數
Length = 6.7             #擺長
gn = 9.80665*(Er**2)*(3600**2)*(10**-3)
def gravity(r):
    return -gn/(abs(r)**2)
########################################
print "\nUnits: hr , km\n"
print "Controlings:\n ← : rotation speed down\n → : rotation speed up\n i : camera rotates with disc\n o : camera sets still"
print "\nclick to realse the pendulum\n"
print "You can't change rotation speed after releasing the pendulum\n"
sleep(5)


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
    update(dt, scene)
    stick.pos = earth.frame_to_world(ground.frame_to_world(ceiling.pos))
    stick.axis = ball.pos - stick.pos
    footage.pos.x = ground.world_to_frame(earth.world_to_frame(ball.pos)).x
    footage.pos.z = ground.world_to_frame(earth.world_to_frame(ball.pos)).z

    formula_stick.pos = ground.frame_to_world(ceiling.pos)
    formula_stick.axis = formula_ball.pos - formula_stick.pos
    formula_footage.pos.x = ground.world_to_frame(formula_ball.pos).x
    formula_footage.pos.z = ground.world_to_frame(formula_ball.pos).z

poss = [ball.pos, ball.pos]
ballpos_list = []
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

scene.waitfor("click")
scene.bind("keydown", key_method)
timer.color = color.yellow

while True:
    rate(0.03/dt)
    
    timer.text = str(int(t*10)/10.0) + " hr."
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)
    
    poss[0] = poss[1]*1
    poss[1] = ball.pos*1
    
    if start:
        t += dt
        ballpos_list.append(ball.pos*1)
        trail.append(pos = ground.world_to_frame(earth.world_to_frame(ball.pos)))
        f1.plot(pos = (trail.pos[-1][2], trail.pos[-1][0]))
        deviation.plot(pos = (t, abs(earth.world_to_frame(ball.pos) - formula_ball.pos)))
        scale.plot(pos = (-t/6, 0))
        ball.a = gravity(ball.pos) * norm(ball.pos) + spring_f(stick.axis, kc, Length) / m
        formula_ball.a = (gravity(formula_ball.pos) * norm(formula_ball.pos)
                          + spring_f(formula_stick.axis, kc, Length) / m
                          + (-2*cross(w, formula_ball.v))
                          + vector(formula_ball.pos.x, 0, formula_ball.pos.z) * dot(w, w))
            
    else:
        if scene.mouse.events:          #啟動
            mous = scene.mouse.getevent()
            if mous.click == "left":
                start = True
                ball.make_trail = True
                ball.retain = 500
                footage.make_trail = True
                footage.retain = 500
                trail = points(frame = ground, pos = [ground.world_to_frame(earth.world_to_frame(ball.pos))], color = color.red, size = 1)
                ball.v = count_v(dt, poss)
    
    earth.rotate(angle = radians(degree * dt), axis = (0, 1, 0))
    if not start:
        ball.pos = earth.frame_to_world(ground.frame_to_world(ball_init.pos))
        formula_ball.pos = ground.frame_to_world(ball_init.pos)
    update_all(dt, scene)
    
    if mode == "inside":                #處理模式(視角)
        scene.center = timer.pos = info_demo.pos = earth.frame_to_world(ground.pos)
        scene.forward = rotate(-stick.pos, angle = radians(60), axis = cross(-stick.pos, scene.up))
    




