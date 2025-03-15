from math import sin,cos

import pyglet
from pyglet import shapes
window = pyglet.window.Window(width=1280, height=720, caption="Shapes in Pyglet")
window.set_location(400,200)

batch = pyglet.graphics.Batch()

circle = shapes.Circle(x=250, y=300, radius=100, color=(50, 225, 30), batch=batch)

square = shapes.Rectangle(x=550, y=300, width=200, height=200, color=(255, 22, 20), batch=batch)
square.anchor_position=(100,100)

star = shapes.Star(x=1000, y=300, outer_radius=60, inner_radius=40, num_spikes=8, color=(255, 255, 0), batch=batch)



@window.event
def on_draw():
    window.clear()
    batch.draw()
value=0
def update(dt):
    global value
    value +=0.07
    circle.radius +=sin(value)
    square.rotation +=1
    star.rotation +=2
    star.x +=sin(value)*8
    star.y +=cos(value)*6
    circle.x +=cos(value)*5
    square.x += cos(value) * 5
    square.x += sin(value) * 8
    circle.x += sin(value) * 8

pyglet.clock.schedule_interval(update,1/60)
pyglet.app.run()
