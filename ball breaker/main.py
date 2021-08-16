from ursina import *

app = Ursina()

dx = 0.05
dy = 0.05
score = 0
dead = False

def update():
    global dx,dy,score,dead
    if not(dead):
        if held_keys['right arrow']:
            board.x += 0.07
        if held_keys['left arrow']:
            board.x -= 0.07
        ball.x += dx
        ball.y += dy
        if ball.x >= 7 or ball.x <= -7:
            dx *= -1
        hit_info = ball.intersects()
        if hit_info.hit:
            dy *= -1
            if hit_info.entity in boxes:
                destroy(hit_info.entity)
                score += 1
        print_on_screen("SCORE:" + str(score), position=(-0.8, 0.45))
        if ball.y <= -3:
            dead = True
    if dead:
        destroy(board)
        destroy(ball)
        for i in boxes:
            destroy(i)
        print_on_screen("GAME OVER!",position=(-0.07,0.20))
        print_on_screen("FINAL SCORE:" + str(score), position=(-0.07, 0.15))
box_1 = Entity(model="cube",color=color.cyan,texture="brick",scale=(1,0.5,0.5),position=(-10,3,0),collider="box")
boxes = []
for i in range(6,-7,-1):
    for j in range(1,6):
        boxes.append(duplicate(box_1,x=i,y=j/2+0.5))
board = Entity(model="cube",color=color.orange,texture="brick",scale=(4,0.5,0.5),position=(0,-3,0),collider="box")
ball = Entity(model="sphere",color=color.orange,scale=0.5,position=(0,-1,0),collider = "box")
app.run()