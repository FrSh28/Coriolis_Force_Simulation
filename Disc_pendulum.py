# -*- coding: cp950 -*-
from visual import*
from visual.graph import*
from func import*

###############  相關參數  #####################
degree = 6.0             #每秒轉動的角度
w = (0,radians(degree),0)
angle = float(raw_input("initial angle(<15 deg) : "))             #初始角度
m = 20.0             #球的重量(公斤)
kc = 500000.0             #彈力係數
Length = 25.0             #擺長
###############################################
print "\nControlings:\n ← : rotation speed down\n → : rotation speed up\n i : camera rotates with disc\n o : camera sets still\n p : print pendulum data"
print "\nclick to release the pendulum\n"
print "You can't change rotation speed after releasing the pendulum\n"
sleep(5)


gd = gdisplay(x = 900 , y = 0 , width = 350 , height = 350 , title = "Deviation")
deviation = gdots(pos = (0, 0), gdisplay = gd , color = color.green , size = 1)
scale = gdots(pos = [(5, 0), (-1, 0)], gdisplay = gd , color = color.white, visible = False, size = 0.01)

gd1 = gdisplay(x = 900 , y = 350 , width = 350 , height = 350 , title = "Trail on Disc")
gplayer = gcurve(sdisplay = gd1, color = color.white)
gplayer.plot(pos = [(8 * cos(radians(angle1)), 8 * sin(radians(angle1))) for angle1 in range(360)])
f1 = gcurve(color=color.blue)

scene = display(width = 900, height = 700, center =(0 ,2 ,0), background = (0, 0, 0), title = "Pendulum on Disc", lights = [local_light(pos = (0, 30, 0), color = color.gray(0.8))])
floor = box(pos = (0.0, -0.75, 0.0), length = 20, width = 20, height = 0.5, material = materials.bricks)

timer = label(text = "Click to start", pos = scene.center, opacity = 0,box = False ,  line = False, yoffset = scene.height/2-100, height = 50, color = color.red)
rota_demo = str(int(degree*100/6.0)/100.0)
info_demo = label(text = "  Rotation Speed(< >):\n    %s  rpm\n  Initial angle:\n    %s  deg"%(rota_demo, str(angle)), pos = scene.center, xoffset = -(scene.width/2-180), height = 18, color = (0.8,0.8,0.8), box = False, line = False, opacity = 0.2)


plate = frame(pos = (0.0, 0.0, 0.0))
disc = cylinder(frame = plate, pos = (0.0, -0.5, 0.0), radius = 8, color = (1, 1, 1), axis = (0, 0.5, 0), material = materials.wood)
ceiling = cylinder(frame = plate, pos = (0.0, Length + 2.0, 0.0), radius = 3, color = color.gray(0.7), axis = (0, 0.2, 0), opacity = 0.7, material = materials.rough)
sphere(frame = plate, pos = ceiling.pos,  color = ceiling.color, radius = 0.2, opacity = 0.7)
ball_init = sphere(frame = plate, pos = (Length * -sin(radians(angle)), ceiling.pos.y - Length * cos(radians(angle)), 0.0), visible = False)

ball = sphere(pos = plate.frame_to_world(ball_init.pos), radius = 0.5, opacity = 0.5, v = vector(0.0, 0.0, 0.0),
              a = vector(0.0, 0.0, 0.0), make_trail = False, color = color.red, material = materials.rough)
stick = cylinder(pos = ceiling.pos, radius = 0.1, opacity = 0.5, color = ball.color, axis = ball.pos - ceiling.pos, length = Length, material = materials.rough)
footage = cylinder(frame = plate, pos = (ball.pos.x, 0.02, ball.pos.z), radius = ball.radius, color = ball.color,
                   axis = (0.0, 0.02, 0.0), opacity = 0.5, material = materials.rough, make_trail = False)

formula_ball = sphere(frame = plate , pos = ball_init.pos, radius = 0.5, opacity = 0.5, v = vector(0.0, 0.0, 0.0),
                      a = vector(0.0, 0.0, 0.0), make_trail = False, color = color.blue, material = materials.rough)
formula_stick = cylinder(frame = plate , pos = ceiling.pos, radius = 0.1, opacity = 0.5, color = formula_ball.color, axis = formula_ball.pos - ceiling.pos, length = Length, material = materials.rough)
formula_footage = cylinder(frame = plate, pos = (formula_ball.pos.x, 0.02, formula_ball.pos.z), radius = formula_ball.radius, color = formula_ball.color,
                           axis = (0.0, 0.02, 0.0), opacity = 0.5, material = materials.rough, make_trail = False)

def update_all(dt, scene):
    update(dt, scene)
    stick.axis = ball.pos - plate.frame_to_world(ceiling.pos)
    footage.pos.x = plate.world_to_frame(ball.pos).x
    footage.pos.z = plate.world_to_frame(ball.pos).z
    formula_stick.axis = formula_ball.pos - ceiling.pos
    formula_footage.pos.x = formula_ball.pos.x
    formula_footage.pos.z = formula_ball.pos.z
    f1.plot(pos = (footage.z , footage.x))

poss = [ball_init.pos, ball_init.pos]
ballpos_list = []
pball = []
pn = 0
start = False

def key_method(evt):
    global mode, pn, degree, w, rota_demo
    key = evt.key
    if key == "i":
        mode = "inside"
    elif key == "o":
        mode = "outside"
    elif key == "p":
        for i in range(pn):
            print "t = %d   v: %s %.5f   a: %s %.3f   observer_a: %s %.5f\n"%(pball[i][0], pball[i][1], pball[i][2], pball[i][3], pball[i][4], pball[i][5], pball[i][6])
    elif start == False:
        if key == "left":
            degree -= 1
            w = (0,radians(degree),0)
            rota_demo = str(int(degree*100/6.0)/100.0)
        elif key == "right":
            degree += 1
            w = (0,radians(degree),0)
            rota_demo = str(int(degree*100/6.0)/100.0)
        info_demo.text = "  Rotation Speed(< >):\n    %s  rpm\n  Initial angle:\n    %s  deg"%(rota_demo, str(angle))

scene.autoscale = False
scene.forward = (-plate.frame_to_world(ball_init.pos).x, -1, -plate.frame_to_world(ball_init.pos).z)
mode = "outside"

scene.waitfor("click")
scene.bind("keydown", key_method)

t = 0.0
dt = 0.001

timer.color = color.yellow
timer.text = str(int(t))

while True:
    rate(1/dt)
    
    timer.text = str(int(t))
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-180)

    poss[0] = poss[1] * 1
    poss[1] = plate.frame_to_world(ball_init.pos) * 1
    
    if start:
        t += dt
        ballpos_list.append(ball.pos * 1)
        trail.append(pos = plate.world_to_frame(ball.pos))
        ball.a = g + spring_f(stick.axis, kc, Length) / m
        formula_ball.a = g + spring_f(formula_stick.axis, kc, Length) / m - 2*cross(w , formula_ball.v) + vector(formula_ball.pos.x , 0 ,formula_ball.pos.z) * dot(w , w)
        deviation.plot(pos = (t , abs(plate.world_to_frame(ball.pos) - formula_ball.pos)))
        scale.plot(pos = (-t/6 , 0), visible = False)
        if len(ballpos_list) >= 3 and t >= dott:
            pball.append([int(t), count_v(dt, ballpos_list[-2:]), 0, count_a(dt, ballpos_list[-3:]), 0, count_a(dt, [vector(trail.pos[-3]), vector(trail.pos[-2]), vector(trail.pos[-1])]), 0])
            pball[pn][2] = abs(pball[pn][1])
            pball[pn][4] = abs(pball[pn][3])
            pball[pn][6] = abs(pball[pn][5])
            pn += 1
            dott += 1
            
    else:
        if scene.mouse.events:          #啟動
            mous = scene.mouse.getevent()
            if mous.click == 'left':
                start = True
                dott = t+1
                ball.make_trail = True
                footage.make_trail = True
                formula_ball.make_trail = True
                formula_footage.make_trail = True
                trail = curve(frame = plate, pos = [plate.world_to_frame(ball.pos)], color = (0.3,0.3,0.3))
                ball.v = count_v(dt,poss)

    plate.rotate(angle = radians(degree * dt), axis = (0, 1, 0))
    if not start:
        ball.pos = plate.frame_to_world(ball_init.pos)
        formula_ball.pos = ball_init.pos
    update_all(dt, scene)
    
    if mode == "inside":            #處理視角
        scene.forward = vector(-plate.frame_to_world(ball_init.pos).x, -1, -plate.frame_to_world(ball_init.pos).z)





