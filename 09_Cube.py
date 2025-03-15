import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3

window = pyglet.window.Window(width=1200, height=720, caption="3D Cube",resizable=True)
window.set_location(400, 200)
batch = pyglet.graphics.Batch()
glEnable(GL_DEPTH_TEST)

# Updated vertex shader for 3D coordinates
vertex_source = """
#version 150
in vec3 vertices;
in vec4 colors;
out vec4 newColors;
uniform mat4 vp;
uniform mat4 model;

void main() {
    gl_Position = vp * model * vec4(vertices, 1.0);
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

# Create the view and projection matrices
view_Math = Mat4.from_translation(Vec3(x=0, y=0, z=-2)) # Move camera back
# project_Mat = Mat4.orthogonal_projection(left=0,
#                                          right=1200,
#                                          bottom=0,
#                                          top=720,
#                                          z_near=0.1,
#                                          z_far=1500)
#create a perspective view
project_Mat=Mat4.perspective_projection(aspect=1.6666,z_near=0.1,z_far=100)

# Combine view and projection matrices
vp = project_Mat @ view_Math
program['vp'] = vp

# 3D Transformations (Translate, Rotate, Scale)
# Move the cube to the center of the screen and make it bigger
cube_Translate = Mat4.from_translation(vector=Vec3(x=0, y=0, z=0))
cube_Rotate = Mat4.from_rotation(angle=1, vector=Vec3(x=0, y=1, z=0))
cube_Scale = Mat4.from_scale(vector=Vec3(x=1, y=1, z=1)) # Make cube bigger

# Combine the transformation matrices
model_Math = cube_Translate @ cube_Rotate @ cube_Scale
program['model'] = model_Math

# # Enable backface culling for better rendering
# glEnable(GL_CULL_FACE)
# glCullFace(GL_BACK)

# Define the cube vertices (8 corners)
vertices = (
    # Front face
    -0.5, -0.5, 0.5,  # 0: front bottom left
    0.5, -0.5, 0.5,  # 1: front bottom right
    0.5, 0.5, 0.5,  # 2: front top right
    -0.5, 0.5, 0.5,  # 3: front top left

    # Back face
    -0.5, -0.5, -0.5,  # 4: back bottom left
    0.5, -0.5, -0.5,  # 5: back bottom right
    0.5, 0.5, -0.5,  # 6: back top right
    -0.5, 0.5, -0.5  # 7: back top left
)

# Define the colors for each vertex
colors = (
    # Front face
    255, 0, 0, 255,  # 0: Red
    0, 255, 0, 255,  # 1: Green
    0, 0, 255, 255,  # 2: Blue
    255, 255, 0, 255,  # 3: Yellow

    # Back face
    255, 0, 255, 255,  # 4: Magenta
    0, 255, 255, 255,  # 5: Cyan
    255, 255, 255, 255,  # 6: White
    0, 0, 0, 255  # 7: Black
)

# Define the indices for the cube's 12 triangles (6 faces)
indices = [  # Changed to list as Pyglet expects
    # Front face
    0, 1, 2, 2, 3, 0,
    # Back face
    5, 4, 7, 7, 6, 5,
    # Left face
    4, 0, 3, 3, 7, 4,
    # Right face
    1, 5, 6, 6, 2, 1,
    # Top face
    3, 2, 6, 6, 7, 3,
    # Bottom face
    4, 5, 1, 1, 0, 4
]

# Create the cube vertex list
cube = program.vertex_list_indexed(8, GL_TRIANGLES,
                                   indices,
                                   batch=batch,
                                   vertices=('f', vertices),
                                   colors=('Bn', colors))

# Animation variables
# rotation_speed = 1.0
# total_time = 0
angle=5


def update(dt):
    global angle
    angle+= dt

    # Update rotation
    Rotate_y = Mat4.from_rotation(angle=angle, vector=Vec3(x=0, y=1, z=0))
    Rotate_x = Mat4.from_rotation(angle=angle, vector=Vec3(x=1, y=0, z=0))
    model_Math = cube_Translate @ Rotate_y @ Rotate_x @ cube_Scale
    program['model'] = model_Math


@window.event
def on_draw():
    window.clear()
    batch.draw()


# Schedule the update function
pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()