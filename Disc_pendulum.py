# -*- coding: cp950 -*-
from visual import*
from visual.graph import*
from func import*

###############  相關參數  #####################
degree = 6.0             #每秒轉動的角度
w = vector(0, radians(degree), 0)
angle = float(raw_input("initial angle(<15 deg) : "))             #初始角度
m = 20.0             #球的重量(公斤)
kc = 500000.0             #彈力係數
Length = 25.0             #擺長
###############################################
print "\nControlings:\n ← : rotation speed down\n → : rotation speed up\n i : camera rotates with disc\n o : camera sets still\n p : print pendulum data"
print "\nclick to release the pendulum\n"
print "You can't change rotation speed after releasing the pendulum\n"
sleep(5)


gd = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation")
deviation = gdots(gdisplay = gd, pos = (0, 0), color = color.green, size = 1)
scale = gdots(gdisplay = gd, pos = [(-1, 0), (5, 0)], color = color.white, size = 0.01)

gd1 = gdisplay(x = 900, y = 350, width = 350, height = 350, title = "Trail on Disc")
gplayer = gcurve(gdisplay = gd1, color = color.white)
gplayer.plot(pos = [(8*cos(radians(angle1)), 8*sin(radians(angle1))) for angle1 in range(360)])
f1 = gdots(gdisplay = gd1, color = color.red, size = 0.01)

scene = display(width = 900, height = 700, center = (0, 2, 0), background = (0, 0, 0), title = "Pendulum on Disc",
                lights = [local_light(pos = (0, 30, 0), color = color.gray(0.8))])
floor = box(pos = (0.0, -0.75, 0.0), length = 20, width = 20, height = 0.5, material = materials.bricks)

timer = label(text = "Click to start", pos = scene.center, yoffset = scene.height/2-100, height = 50, color = color.red, box = False, line = False, opacity = 0)
rota_demo = str(int(degree*100/6.0)/100.0)
info_demo = label(text = "  Rotation Speed(< >):\n    %s  rpm\n  Initial angle:\n    %s  deg"%(rota_demo, str(angle)),
                  pos = scene.center, xoffset = -(scene.width/2-180), height = 18, color = color.gray(0.8), box = False, line = False, opacity = 0.2)

plate = frame(pos = (0, 0, 0))
disc = cylinder(frame = plate, pos = (0, -0.5, 0), radius = 8, axis = (0, 0.5, 0), color = color.white, material = materials.wood)
ceiling = cylinder(frame = plate, pos = (0, Length+2, 0), radius = 3, axis = (0, 0.2, 0), color = color.gray(0.7), material = materials.rough, opacity = 0.7)
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

scene.forward = (-plate.frame_to_world(ball_init.pos).x, -1, -plate.frame_to_world(ball_init.pos).z)
scene.autoscale = False

def update_all(dt, scene):
    update(dt, scene)
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
dt = 0.002

scene.waitfor("click")
scene.bind("keydown", key_method)
timer.color = color.yellow

while True:
    rate(1/dt)
    
    timer.text = str(int(t))
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)

    poss[0] = poss[1]*1
    poss[1] = plate.frame_to_world(ball_init.pos)*1
    
    if start:
        t += dt
        ballpos_list.append(ball.pos*1)
        trail.append(plate.world_to_frame(ball.pos))
        f1.plot(pos = (footage.z, footage.x))
        deviation.plot(pos = (t, abs(plate.world_to_frame(ball.pos) - formula_ball.pos)))
        scale.plot(pos = (-t/6, 0))
        ball.a = g + spring_f(stick.axis, kc, Length) / m
        formula_ball.a = (g
                          + spring_f(formula_stick.axis, kc, Length) / m
                          + (-2*cross(w, formula_ball.v))
                          + vector(formula_ball.pos.x, 0, formula_ball.pos.z) * dot(w, w))
        if len(ballpos_list) >= 3 and t >= dott:
            pball.append([int(t), count_v(dt, ballpos_list[-2:]), 0, count_a(dt, ballpos_list[-3:]), 0, count_v(dt, trail[-2:]), 0, count_a(dt, trail[-3:]), 0])
            pball[-1][2] = abs(pball[-1][1])
            pball[-1][4] = abs(pball[-1][3])
            pball[-1][6] = abs(pball[-1][5])
            pball[-1][8] = abs(pball[-1][7])
            dott += 1
            
    else:
        if scene.mouse.events:          #啟動
            mous = scene.mouse.getevent()
            if mous.click == "left":
                start = True
                dott = t+1
                ball.make_trail = True
                ball.retain = 20000
                footage.make_trail = True
                ball.v = count_v(dt,poss)

    plate.rotate(angle = radians(degree * dt), axis = (0, 1, 0))
    if not start:
        ball.pos = plate.frame_to_world(ball_init.pos)
        formula_ball.pos = ball_init.pos
    update_all(dt, scene)
    
    if mode == "inside":            #處理視角
        scene.forward = vector(-plate.frame_to_world(ball_init.pos).x, -1, -plate.frame_to_world(ball_init.pos).z)





