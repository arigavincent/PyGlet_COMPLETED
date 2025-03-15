import pyglet
from pyglet import shapes
from pyglet.window import *


class MyClass(pyglet.window.Window):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_location(600,600)
        self.batch=pyglet.graphics.Batch()
        self.circle=shapes.Circle(x=400,y=200,radius=100,color=(50, 168, 88),batch=self.batch)
        self.direction={"left":False,"right":False,"up":False,"down":False}
        self.speed=20


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol ==key.LEFT:
            self.direction["left"]=True
        if symbol ==key.RIGHT:
            self.direction["right"]=True
        if symbol ==key.UP:
            self.direction["up"]=True
        if symbol ==key.DOWN:
            self.direction["down"]=True

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol == key.LEFT:
            self.direction["left"] = False
        if symbol == key.RIGHT:
            self.direction["right"] = False
        if symbol == key.UP:
            self.direction["up"] = False
        if symbol == key.DOWN:
            self.direction["down"] = False

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()

    def update(self,dt) ->None:
        if self.direction["left"]:
            self.circle.x -=self.speed
        if self.direction["right"]:
            self.circle.x +=self.speed
        if self.direction["up"]:
            self.circle.y +=self.speed
        if self.direction["down"]:
            self.circle.y -=self.speed

if __name__ =="__main__":
    Window = MyClass(width=800, height=800, caption="My Window", resizable=True)
    pyglet.clock.schedule_interval(Window.update, 1 / 60)
    pyglet.app.run()


