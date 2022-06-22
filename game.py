import turtle
import math
import random
import gc

FONT = ('Arial', 18, 'bold')

spaceship_image = "spaceship_2.gif"
enemy_image = "enemy.gif"
bullet_image = "bullet.gif"


wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")

wn.addshape(spaceship_image)
wn.addshape(enemy_image)
wn.addshape(bullet_image)


# screen settings
right_boundarie = 360
left_boundarie = -360
top_boundarie = 320
bottom_boundarie = -250
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()


# create player bullet
bullets = []
bulletspeed = 20
def create_bullet(x, y):
    bullet = turtle.Turtle()
    bullet.hideturtle()
    bullet.shape(bullet_image)
    bullet.penup()
    bullet.speed(0)
    bullet.setposition(x, y)
    bullet.shapesize(0.5, 0.5)
    return bullet

# create player
player = turtle.Turtle()
# player.shape(spaceship_image)
# player.penup()
# player.speed(0)
# player.setposition(0, -250)
# player.setheading(90)
playerspeed = 15

# create enemies
enemies = []
enemyspeed = 4
def create_enemies(start, stop, density):
    for i in range(start, stop, 40):
        if (random.random() < density):
            enemy = turtle.Turtle()
            enemy.shape(enemy_image)
            enemy.penup()
            enemy.speed(0)
            enemy.setposition(i, 250)
            enemies.append(enemy)
# create_enemies(-250, 250, 1)

# detect collision
def collision_detection(t1, t2):
    x_diff = t1.xcor() - t2.xcor()
    y_diff = t1.ycor() - t2.ycor()
    distance = math.sqrt(x_diff*x_diff + y_diff*y_diff)
    if (distance < 20):
        return True
    else:
        return False

# movement
def move_left(event):
    if (player.xcor() - playerspeed >= left_boundarie):
        x = player.xcor()
        x -= playerspeed
        player.setx(x)

def move_right(event):
    if (player.xcor() + playerspeed <= right_boundarie):
        x = player.xcor()
        x += playerspeed
        player.setx(x)

# fire bullet
def fire_bullet():
    x = player.xcor() + 3
    y = player.ycor() + 25 - bulletspeed
    bullet = create_bullet(x, y)
    bullet.showturtle()
    bullets.append(bullet)


# wn.getcanvas().bind("<Left>", move_left)
# wn.getcanvas().bind("<Right>", move_right)
# wn.onkey(fire_bullet, "space")
# wn.listen()


def start(x, y):
    global gameover_bool
    gameover_bool = False
    wn.clear()
    wn.bgcolor("black")
    wn.title("Space Invaders")
    wn.getcanvas().bind("<Left>", move_left)
    wn.getcanvas().bind("<Right>", move_right)
    wn.onkey(fire_bullet, "space")
    global bullets
    bullets = []
    global player
    player = turtle.Turtle()
    player.shape(spaceship_image)
    player.penup()
    player.speed(0)
    player.setposition(0, -250)
    player.setheading(90)
    global enemies
    enemies = []
    create_enemies(-250, 250, 1)
    wn.listen()
    run()

def home(x=0, y=0):
    wn.onscreenclick(None)
    wn.clear()
    wn.bgcolor("black")
    wn.title("Space Invaders")
    h = turtle.Turtle()
    h.clear()
    h.home()
    h.color('lime')
    h.write("PLAY", align="center", font=FONT)

    wn.onscreenclick(start)


def gameover():
    wn.clear()
    wn.bgcolor("black")
    wn.title("Space Invaders")
    wn.onscreenclick(None)
    go = turtle.Turtle()
    go.penup()
    go.clear()
    go.color("red")

    go.setposition(0, 150)
    go.write("Game Over", align="center", font=FONT)

    go.setposition(0, 120)
    go.write("(Click anywhere to return to the main menu)", align="center", font=FONT)
    wn.onscreenclick(home)


# main gameloop
dir = 1
gameover_bool = False
def run():
    # move enemy
    global gameover_bool
    global dir
    if (not gameover_bool):
        changeheight = False
        wn.tracer(0, 0)
        enemies.sort(key=lambda x: x.xcor())
        if (len(enemies) > 0 and (enemies[len(enemies)-1].xcor() + enemyspeed >= right_boundarie or enemies[0].xcor() - enemyspeed <= left_boundarie)):
            dir = dir * -1
            changeheight = True
        for enemy in enemies:
            enemy_x = enemy.xcor()
            enemy_y = enemy.ycor()
            if (enemy_y <= -200):
                gameover_bool = True
            if (changeheight):
                enemy_y -= 40
            enemy_x += dir*enemyspeed
            enemy.setx(enemy_x)
            enemy.sety(enemy_y)

        if (changeheight or len(enemies) == 0):
            create_enemies(-250, 250, random.random())
        wn.update()

        # move bullet
        wn.tracer(0, 0)
        delete_objects = []
        for bullet in bullets:
            if (bullet.ycor() + bulletspeed <= top_boundarie):
                for enemy in enemies:
                    if (collision_detection(bullet, enemy)):
                        delete_objects.append(bullet)
                        bullet.clear()
                        bullet.hideturtle()
                        bullets.remove(bullet)
                        delete_objects.append(bullet)
                        enemy.hideturtle()
                        enemy.clear()
                        enemies.remove(enemy)
                bullet_y = bullet.ycor()
                bullet_y += bulletspeed
                bullet.sety(bullet_y)
            else:
                delete_objects.append(bullet)
                bullet.clear()
                bullet.hideturtle()
                bullets.remove(bullet)
        wn.update()
        for o in delete_objects:
            del o
        gc.collect()
        wn.ontimer(run, 40)
    else:
        wn.ontimer(gameover, 50)

home()

# finished
turtle.done()
