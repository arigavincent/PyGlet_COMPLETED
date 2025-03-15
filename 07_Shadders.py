import pyglet
from pyglet.gl import GL_TRIANGLES
from pyglet.graphics.shader import Shader, ShaderProgram


window = pyglet.window.Window(width=800, height=800, caption="My Window")
window.set_location(400, 200)
batch = pyglet.graphics.Batch()

# Version 150 with no layout qualifiers
vertex_source = """
#version 150
in vec2 vertices;
in vec4 colors;
out vec4 newColors;

void main() {
    gl_Position = vec4(vertices, 0.0, 1.0);
    newColors = colors;
}
"""

fragment_source = """
#version 150
in vec4 newColors;
out vec4 outColors;

void main() {
    outColors = newColors;
}
"""

vertex_Shader = Shader(vertex_source, "vertex")
frag_Shader = Shader(fragment_source, "fragment")
program = ShaderProgram(vertex_Shader, frag_Shader)

# Create the vertex list
triangle = program.vertex_list(3, GL_TRIANGLES,
                    batch=batch,
                    vertices=('f', (-0.5, -0.5, 0.5, -0.5, 0.0, 0.5)),
                    colors=('Bn', (255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255)))

@window.event
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()