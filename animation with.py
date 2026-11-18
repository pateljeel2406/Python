import turtle
import colorsys

t = turtle.Turtle()
s = turtle.Screen()

s.bgcolor("black")
t.speed(0)
t.width(2)

h = 0

for i in range(368):
    c = colorsys.hsv_to_rgb(h, 1, 1)
    t.pencolor(c)
    
    t.circle(i * 0.4)
    t.left(10)
    
    h += 1 / 368  

turtle.done()