# -*- coding: cp950 -*-
from visual import*
from visual.graph import*
from random import*
from func import*

###############  相關參數  ###############
degree = 0.0             #每秒轉動的角度
w = vector(0,radians(degree),0)
throw_dir = 0          #發射方向(右為正)
balls_v = 7.0             #球速度
########################################
print "Controlings:\n ← : rotation speed down\n → : rotation speed up\n i : camera rotates with disc\n o : camera sets still\n p : print balls data"
print "\nclick to throw the ball\n\nYou can't change rotation speed while any ball exists "
sleep(5)


gd = gdisplay(x = 900, y = 0, width = 350, height = 350, title = "Deviation")
gdots(gdisplay = gd, pos = [(3.5, 0), (-0.5, 0)], size = 1 )

gd1 = gdisplay(x = 900 , y = 350, width = 350, height = 350, xmax = 10, xmin = -10, ymax = 10, ymin = -10, title = "Trail on Disc")
gplayer = gcurve(gdisplay = gd1 , color = color.white)
gplayer.plot(pos = [(7 * cos(radians(angle)), 7 * sin(radians(angle))) for angle in range(360)])

scene = display(width = 900, height = 700, autoscale = False, center =(0, 2, 0), background = (0, 0, 0),
                title = "Throw Ball on Disc", lights = [local_light(pos = (0, 20, 0), color = color.gray(0.7))])

floor = box(pos = (0.0, -0.75, 0.0), length = 20, width = 20, height = 0.5, material = materials.wood)
timer = label(text = "Click To Start", pos = scene.center, yoffset = scene.height/2-100, height = 50,
              color = color.red, box = False, line = False, opacity = 0)
rota_demo = str(int(degree*100/6.0)/100.0)
throwdir_demo = str(throw_dir)
info_demo = label(text = "  Rotation Speed(< >):\n    %s  rpm\n  Throw Direction(A D):\n    %s  deg"%(rota_demo, throwdir_demo),
                  pos = scene.center, xoffset = -(scene.width/2-200), height = 18, color = (0.8,0.8,0.8), box = False, line = False, opacity = 0.2)

plate = frame(pos = (0,0,0))
disc = cylinder(frame = plate, pos = (0, -0.5, 0), radius = 7, color = (0.7, 0.7, 0.7), axis = (0,0.5,0), material = materials.rough)
sphere(frame = plate, pos = (7, 0, 0), radius = 0.3, color = (0, 0, 1), material = materials.rough)
player = sphere(frame = plate, pos = (-7, 0, 0), radius = 0.3, color = (1, 0, 0), material = materials.rough)
throw = arrow(frame = plate, pos = player.pos, shaftwidth = 0.1, color = color.green, material = materials.rough)
throw.axis = rotate((-player.pos.x, 0, -player.pos.z), angle = radians(throw_dir), axis = (0, -1, 0)) * 0.3

poss = [player.pos, player.pos]
balls = []
formula_balls = []
balln = -1
ballpos_list = []
trails = []
pball = []
arrows = []
formula_arrows = []

def mouse_method(evt):
    global balln
    if evt.click == "left":
        balln += 1
        bcollor = (uniform(0.3, 0.6) , uniform(0.3, 0.6) , uniform(0.3, 0.6))
        balls.append(sphere(pos = (plate.frame_to_world(player.pos).x, 0, plate.frame_to_world(player.pos).z), v = count_v(dt, poss)*1 + balls_v * norm(plate.frame_to_world(throw.axis)),
                            radius = 0.3, color = color.red, material = materials.rough, make_trail = True, opacity = 0.5, tleft = 3.0, num = balln, graph = gcurve(gdisplay = gd1, color = bcollor),
                            deviation = gdots(gdisplay = gd, color = bcollor, size = 1)))
        formula_balls.append(sphere(frame = plate, pos = (player.pos.x, 0, player.pos.z), v = balls_v * norm(throw.axis), radius = 0.3, color = color.blue, material = materials.rough,
                                    make_trail = False, tleft = 3.0, opacity = 0.5, graph = gcurve(gdisplay = gd1, color = bcollor)))
        arrows.append(arrow(frame = plate, pos = balls[-1].pos, axis = (0, 0, 0), shaftwidth = 0.2, color = color.red, opacity = 0.5, material = materials.rough))
        formula_arrows.append(arrow(frame = plate, pos = balls[-1].pos, axis = (0, 0, 0), shaftwidth = 0.2, color = color.blue, opacity = 0.5, material = materials.rough))            
        ballpos_list.append([])
        trails.append(curve(frame = plate, pos = [plate.world_to_frame(balls[-1].pos)], color = balls[-1].graph.color))                                             
        pball.append([vector(0, 0, 0), 0, vector(0, 0, 0), 0, vector(0, 0, 0), 0 , vector(0,0,0) , vector(0,0,0) , vector(0,0,0)])                                                                              

def key_method(evt):
    global mode, balln, degree, rota_demo, w, throw_dir, throwdir_demo
    k = scene.kb.getkey()
    if k == "i":
        mode = "inside"
    elif k == "o":
        mode = "outside"
    elif k == "p":
        for i in range(balln+1):
            print("\n"+str(i+1)+"\nv: %s    %.5f\na: %s    %.5f\nobserver_a: %s    %.5f"
                    %(pball[i][0], pball[i][1], pball[i][2], pball[i][3], pball[i][4], pball[i][5]))
    elif k == "left" and len(balls) == 0:
        degree -= 1
        rota_demo = str(int(degree*100/6.0)/100.0)
        w = vector(0,radians(degree), 0)
    elif k == "right" and len(balls) == 0:
        degree += 1
        rota_demo = str(int(degree*100/6.0)/100.0)
        w = vector(0,radians(degree), 0)
    elif k == "a" or k == "d":
        if k == "a":
            throw_dir -= 1
        else:
            throw_dir +=1
        throw_dir %= 360
        if throw_dir > 180:
            throw_dir -= 360
        throwdir_demo = str(throw_dir)
        throw.axis = rotate((-player.pos.x, 0, -player.pos.z), angle = radians(throw_dir), axis = (0, -1, 0)) * 0.3
    info_demo.text = "  Rotation Speed(< >):\n    %s  rpm\n  Throw Direction(A D):\n    %s  deg"%(rota_demo, throwdir_demo)

mode = "outside"
t = 0
dt = 0.001

scene.forward = (-plate.frame_to_world(player.pos).x, -2, -plate.frame_to_world(player.pos).z)
scene.waitfor("click")
scene.bind("click", mouse_method)
scene.bind("keydown", key_method)

timer.color = color.yellow
timer.text = str(int(t))

while True:
    rate(1/dt)
    
    t += dt
    timer.text = str(int(t))
    timer.yoffset = scene.height/2-100
    info_demo.xoffset = -(scene.width/2-200)
    
    poss[0] = poss[1] * 1
    poss[1] = plate.frame_to_world(player.pos) * 1
    
    for b in balls:
        ballpos = plate.world_to_frame(b.pos)
        b.graph.plot(pos = (ballpos.z,ballpos.x))
        b.deviation.plot(pos = (3.0-b.tleft , abs(ballpos - formula_balls[balls.index(b)].pos)))
        if b.tleft <= 0:
            b.trail_object.visible = False
            b.visible = False
            formula_balls[balls.index(b)].visible = False
            del arrows[balls.index(b)] , formula_arrows[balls.index(b)] , trails[balls.index(b)], formula_balls[balls.index(b)], balls[balls.index(b)]
        else:
            b.tleft -= dt
            ballpos_list[balls.index(b)].append(b.pos * 1)
            if abs(ballpos) - disc.radius < 0.01 :
                trails[balls.index(b)].append(pos = ballpos)
                if len(trails[balls.index(b)].pos) >= 3:
                    arrows[balls.index(b)].pos = ballpos
                    pball[b.num][4] = vector(count_a(dt, trails[balls.index(b)].pos[-3:]))
                    pball[b.num][5] = abs(pball[b.num][4])
                    pball[b.num][6] = vector(count_v(dt, trails[balls.index(b)].pos[-2:]))
                    arrows[balls.index(b)].axis = pball[b.num][4]
            else:
                arrows[balls.index(b)].visible = False
                formula_arrows[balls.index(b)].visible = False
                trails[balls.index(b)].visible = False
            
            if len(ballpos_list[balls.index(b)]) >= 3:
                pball[b.num][0] = count_v(dt, ballpos_list[balls.index(b)][-2:])
                pball[b.num][1] = abs(pball[balls.index(b)][0])
                pball[b.num][2] = count_a(dt, ballpos_list[balls.index(b)][-3:])
                pball[b.num][3] = abs(pball[b.num][2])

    for fb in formula_balls:
        fb.tleft -= dt
        fballpos = fb.pos
        fb.graph.plot(pos = (fballpos.z,fballpos.x))
        fb.a = -2*cross(w , fb.v) + (fb.pos) * dot(w , w) 
        formula_arrows[formula_balls.index(fb)].pos = fballpos
        formula_arrows[formula_balls.index(fb)].axis = fb.a
    
    plate.rotate(angle = radians(degree * dt), axis = (0, 1, 0))
    update(dt, scene)
    
    if mode == "inside":            #處理視角
        scene.forward = vector(-plate.frame_to_world(player.pos).x, -2, -plate.frame_to_world(player.pos).z)



