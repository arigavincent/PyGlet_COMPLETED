import pyglet
from pyglet import shapes
from pyglet.window import mouse

window = pyglet.window.Window(width=1280, height=720, caption="MouseEvents in PyGlet")
window.set_location(400, 200)
window.set_mouse_visible(False)

batch = pyglet.graphics.Batch()

# Circles
circle = shapes.Circle(x=250, y=300, radius=10, color=(252, 40, 3), batch=batch)
circle1 = shapes.Circle(x=400, y=300, radius=5, color=(50, 225, 30), batch=batch)

@window.event
def on_draw() -> None:
    window.clear()
    batch.draw()

@window.event
def on_mouse_motion(x: int, y: int, dx: int, dy: int) -> None:
     circle1.x = x
     circle1.y = y
    #circle1.position=(x,y)

@window.event
def on_mouse_press(x: int, y: int, button: int, modifiers: int) -> None:
    if button == mouse.LEFT:
        # circle.x = x
        # circle.y = y
        circle.position=(x,y)

def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        circle.position = (x, y)




pyglet.app.run()
