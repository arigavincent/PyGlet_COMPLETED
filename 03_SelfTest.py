import pyglet
from math import sin,cos

from pyglet import shapes
#creates a window
window=pyglet.window.Window(width=1020,height=1020,caption="Ariga_Testing_Himself")
# sets the location of the window
window.set_location(400,200)
#creates a batch object
batch=pyglet.graphics.Batch()
#creates a circle shape
circle=shapes.Circle(x=150,y=400,radius=100,color=(50, 168, 90),batch=batch)
# creates a square object or shape
sq=shapes.Rectangle(x=500,y=400,width=200,height=200,color=(50, 168, 90),batch=batch)
# sets the anchor or rotation position for the square object during rotation
#sq.anchor_position=(100,100)
#creates a star object or shape in other wards
star=shapes.Star(x=800,y=400,inner_radius=100,outer_radius=150,num_spikes=8,color=(168, 156, 50),batch=batch)
# Handles events in pyglet and makes sure that the on_draw() fxn is always invoked automatically when pyglet needs to draw
@window.event
#This fxn does the drawing of the shapes that are in the batch
def on_draw():
    #this one avoids overlapping redrawing
    window.clear()
    #draws the shapes in batch
    batch.draw()

value=0
#this fxn adds the animation effect to the sgapes
def update(dt):
    # makes value variable global due to scope accessibility
    global value
    value += 0.07
    # adds the rotation effect to the square shape
    sq.rotation += 1
    #star.rotation +=3
    #circle.radius +=cos(value)
    # Adds oscillation to the circle
    circle.radius = 100 + cos(value) * 10
    star.x += cos(value)
    star.y += sin(value)

#This schedules the fxn update() to be called 60 times in every sec
pyglet.clock.schedule_interval(update,1/60)
#This starts the pyglet event and keeps the program running
pyglet.app.run()