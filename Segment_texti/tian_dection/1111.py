import turtle as T
import random
import time
from random import random





def Tree(branch, t):
    time.sleep(0.005)
    if branch > 4:
        if 8 <= branch <= 15:
            if random.randint(0, 2) == 0:
                t.color('snow')  # 白
            else:
                t.color('lightcoral')  # 淡珊瑚色
            t.pensize(branch / 4)
        elif branch < 10:
            if random.randint(0, 1) == 0:
                t.color('snow')
            else:
                t.color('lightcoral')  # 淡珊瑚色
            t.pensize(branch / 2)
        else:
            t.color('sienna')  # 赭(zhě)色
            t.pensize(branch / 10)  # 6
        t.forward(branch)

        a = 2 * random.random()
        t.right(20 * a)
        b = 2 * random.random()
        Tree(branch - 10 * b, t)
        t.left(40 * a)
        Tree(branch - 10 * b, t)
        t.right(20 * a)
        t.up()
        t.backward(branch)
        t.down()

# 掉落的花瓣
def Petal(m, t):
    for i in range(m):
        a = 200 - 400 * random.random()
        b = 10 - 20 * random.random()
        t.up()
        t.forward(b)
        t.left(90)
        t.forward(a)
        t.down()
        t.color('lightcoral')  # 淡珊瑚色
        t.circle(1)
        t.up()
        t.backward(a)
        t.right(90)
        t.backward(b)

# 绘图区域
t = T.Turtle(visible=False,shape='circle')
# 画布大小


w = T.Screen()
width ,height = 800,600
w.setup(width,height)
t.hideturtle()  # 隐藏画笔
t.getscreen().tracer(5, 0)
w.screensize(bg='black')  # wheat小麦

t.left(90)
t.up()
t.backward(150)
t.down()
t.color('sienna')

# 画樱花的躯干
Tree(60, t)
# 掉落的花瓣
Petal(200, t)
w.exitonclick()

