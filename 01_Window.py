import pyglet
from pyglet import shapes

window=pyglet.window.Window(width=720,height=720,caption="MyFirstWindow")
window.set_location(600,200)
batch=pyglet.graphics.Batch()
circle=shapes.Circle(x=400,y=160,radius=100,color=(150,150,150),batch=batch)
rect=shapes.Rectangle(x=250,y=260,height=200,width=300,color=(55,55,150),batch=batch)
triangle = shapes.Triangle(x=250, y=460,
                           x2=400, y2=660,
                           x3=550, y3=460,
                           color=(200, 100, 50),batch=batch)
line1=shapes.Line(x=100, y=100, x2=400, y2=300, color=(60, 60, 160),batch=batch)
line1.rotation=33
line1.opacity=255
star=shapes.Star(x=600,y=600,inner_radius=100,outer_radius=150,num_spikes=9,color=(25,150,240),batch=batch)
@window.event
def on_draw()->None:
    window.clear()
    batch.draw()
    # circle.draw()
    # rect.draw()
    # triangle.draw()
    # line1.draw()
    # star.draw()

pyglet.app.run()