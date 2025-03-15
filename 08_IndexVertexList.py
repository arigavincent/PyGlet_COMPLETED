import pyglet
from pyglet.gl import GL_TRIANGLES
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3

window = pyglet.window.Window(width=800, height=800, caption="My Window")
window.set_location(400, 200)
batch = pyglet.graphics.Batch()

# Version 150 with no layout qualifiers
vertex_source = """
#version 150
in vec2 vertices;
in vec4 colors;
out vec4 newColors;
uniform mat4 vp;
uniform mat4 model;

void main() {
    gl_Position = vp * model * vec4(vertices, 0.0f, 1.0f);
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
# TODO create the view and (orthogonal/orthographic) proj matrices
view_Math = Mat4.from_translation(Vec3(x=0, y=0, z=-1))
project_Mat = Mat4.orthogonal_projection(left=0,
                                         right=800,
                                         bottom=0,
                                         top=800,
                                         z_near=0.1,
                                         z_far=100)
#TODO Combine view and projec matrices into one
vp = project_Mat @ view_Math
#TODO upload the combined vp matrix to the vertex shadder vp uniform
program['vp'] = vp
#TODO 3D Transformations(Translate,Rotate,Scale)
sq_Translate=Mat4.from_translation(vector=Vec3(x=400,y=400,z=0))
sq_Rotate=Mat4.from_rotation(angle=1,vector=Vec3(x=0,y=0,z=-1))
sq_Scale=Mat4.from_scale(vector=Vec3(x=2,y=2,z=0))
#TODO Combine the Transformation matrices into a single matrix - order: T * R * S
model_Math=sq_Translate @ sq_Rotate @ sq_Scale
#TODO create the model matrix and upload it to the model uniform
# model_Math=Mat4.from_translation(Vec3(x=400,y=400,z=0))
program['model']=model_Math

# TODO Create the vertex list
# triangle = program.vertex_list(3, GL_TRIANGLES,
#                     batch=batch,
#                     vertices=('f', vertices),
#                     colors=('Bn', (255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255)))

# TODO Create an indexed vertex  list
vertices = [x * 100 for x in (-0.5, -0.5, 0.5, -0.5, 0.5, 0.5, -0.5, 0.5)]

rectangle = program.vertex_list_indexed(4, GL_TRIANGLES,
                                        indices=(0, 1, 2, 2, 3, 0),
                                        batch=batch,
                                        vertices=('f', vertices),
                                        colors=(
                                        'Bn', (255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 255, 255, 0, 255)))


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.app.run()
