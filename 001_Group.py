import pyglet
from pyglet import shapes

window=pyglet.window.Window(height=700,width=700,caption="Group")
window.set_location(400,200)
batch=pyglet.graphics.Batch()
circle=shapes.Circle(x=400,y=350,radius=100,color=(245, 66, 182),batch=batch)
rct= shapes.Rectangle(x=200,y=300,width=200,height=300,color=(60,35,40),batch=batch)

sqr= shapes.Rectangle(x=100,y=200,width=200,height=200,color=(50,80,90),batch=batch)
sqr anchor
@window.event
def on_draw()->None:
    window.clear()
    batch.draw()

def update(dt, rotation=None):
        sqr.rotation +=3

pyglet.clock.schedule_interval(update,1/60)
pyglet.app.run()