import pyglet
from pyglet import shapes

window=pyglet.window.Window(height=700,width=800,caption="Anita")
window.set_location(400,200)
batch=pyglet.graphics.Batch()
star=shapes.Star(x=400,y=400,inner_radius=100,outer_radius=150,num_spikes=8,color=(55,55,150),batch=batch)
star1=shapes.Star(x=300,y=600,inner_radius=100,outer_radius=150,num_spikes=8,color=(55,115,150),batch=batch)
circle=shapes.Circle(x=200,y=500,radius=50,color=(70,115,10),batch=batch)
rectangle=shapes.Rectangle(x=200,y=500,height=200,width=300,color=(60,115,70),batch=batch)
@window.event
def on_draw()->None:
    window.clear()
    batch.draw()



pyglet.app.run()