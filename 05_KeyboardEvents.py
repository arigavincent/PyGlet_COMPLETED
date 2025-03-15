import pyglet
from pyglet import shapes
from pyglet.window import key

window = pyglet.window.Window(width=1280, height=720, caption="KeyBoard Events in PyGlet")
window.set_location(400, 200)
#window.set_mouse_visible(False)

batch = pyglet.graphics.Batch()

# Circles
circle = shapes.Circle(x=250, y=300, radius=10, color=(252, 40, 3), batch=batch)
#circle1 = shapes.Circle(x=400, y=300, radius=5, color=(50, 225, 30), batch=batch)

@window.event
def on_draw() -> None:
    window.clear()
    batch.draw()

direction={"left":False,"right":False,"up":False,"down":False}

@window.event
def on_key_press(symbol:int, modifiers:int):
    if symbol == key.LEFT:
        #circle.x -=20
        direction["left"]=True
    if symbol == key.RIGHT:
        #circle.x +=20
        direction["right"] = True
    if symbol == key.UP:
        #circle.y +=20
        direction["up"] = True
    if symbol == key.DOWN:
        #circle.y -=20
        direction["down"] = True

@window.event
def on_key_release(symbol:int,modifiers:int):
    if symbol == key.LEFT:
        # circle.x -=20
        direction["left"] = False
    if symbol == key.RIGHT:
        # circle.x +=20
        direction["right"] = False
    if symbol == key.UP:
        # circle.y +=20
        direction["up"] = False
    if symbol == key.DOWN:
        # circle.y -=20
        direction["down"] = False

@window.event
def update(dt):
   if direction["left"]:
       circle.x -= 20
   if direction["right"]:
       circle.x += 20
   if direction["up"]:
       circle.y += 20
   if direction["down"]:
       circle.y -= 20

pyglet.clock.schedule_interval(update,1/60)
pyglet.app.run()

