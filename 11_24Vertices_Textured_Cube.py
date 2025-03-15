import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3

window = pyglet.window.Window(width=1200, height=720, caption="3D Textured Cube", resizable=True)
window.set_location(400, 200)
batch = pyglet.graphics.Batch()
glEnable(GL_DEPTH_TEST)

# Load texture image
texture = pyglet.image.load('Textures/t1.jpg').get_texture()
# Enable texture repeat if needed
glBindTexture(GL_TEXTURE_2D, texture.id)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glBindTexture(GL_TEXTURE_2D, 0)

# Updated vertex shader for texture coordinates
vertex_source = """
#version 150
in vec3 vertices;
in vec4 colors;
in vec2 tex_coords;
out vec4 newColors;
out vec2 newTexCoords;
uniform mat4 vp;
uniform mat4 model;

void main() {
    gl_Position = vp * model * vec4(vertices, 1.0);
    newColors = colors;
    newTexCoords = tex_coords;
}
"""

fragment_source = """
#version 150
in vec4 newColors;
in vec2 newTexCoords;
out vec4 outColors;
uniform sampler2D tex;

void main() {
    vec4 texColor = texture(tex, newTexCoords);
    outColors = texColor * newColors;
}
"""

vertex_Shader = Shader(vertex_source, "vertex")
frag_Shader = Shader(fragment_source, "fragment")
program = ShaderProgram(vertex_Shader, frag_Shader)

# Create the view and projection matrices
view_Math = Mat4.from_translation(Vec3(x=0, y=0, z=-4))
project_Mat = Mat4.perspective_projection(aspect=1.6666, z_near=0.1, z_far=100)

# Combine view and projection matrices
vp = project_Mat @ view_Math
program['vp'] = vp

# 3D Transformations
cube_Translate = Mat4.from_translation(vector=Vec3(x=0, y=0, z=-2))
cube_Rotate = Mat4.from_rotation(angle=1, vector=Vec3(x=0, y=1, z=0))
cube_Scale = Mat4.from_scale(vector=Vec3(x=2, y=2, z=2))

# Combine the transformation matrices
model_Math = cube_Translate @ cube_Rotate @ cube_Scale
program['model'] = model_Math

# Define the cube vertices (24 vertices - 4 per face)
vertices = (
    # Front face (0-3)
    -0.5, -0.5, 0.5,  # 0: front bottom left
    0.5, -0.5, 0.5,  # 1: front bottom right
    0.5, 0.5, 0.5,  # 2: front top right
    -0.5, 0.5, 0.5,  # 3: front top left

    # Back face (4-7)
    -0.5, -0.5, -0.5,  # 4: back bottom left
    0.5, -0.5, -0.5,  # 5: back bottom right
    0.5, 0.5, -0.5,  # 6: back top right
    -0.5, 0.5, -0.5,  # 7: back top left

    # Left face (8-11)
    -0.5, -0.5, -0.5,  # 8: back bottom left
    -0.5, -0.5, 0.5,  # 9: front bottom left
    -0.5, 0.5, 0.5,  # 10: front top left
    -0.5, 0.5, -0.5,  # 11: back top left

    # Right face (12-15)
    0.5, -0.5, 0.5,  # 12: front bottom right
    0.5, -0.5, -0.5,  # 13: back bottom right
    0.5, 0.5, -0.5,  # 14: back top right
    0.5, 0.5, 0.5,  # 15: front top right

    # Top face (16-19)
    -0.5, 0.5, 0.5,  # 16: front top left
    0.5, 0.5, 0.5,  # 17: front top right
    0.5, 0.5, -0.5,  # 18: back top right
    -0.5, 0.5, -0.5,  # 19: back top left

    # Bottom face (20-23)
    -0.5, -0.5, -0.5,  # 20: back bottom left
    0.5, -0.5, -0.5,  # 21: back bottom right
    0.5, -0.5, 0.5,  # 22: front bottom right
    -0.5, -0.5, 0.5,  # 23: front bottom left
)

# Define the colors for each vertex (24 vertices - 4 per face)
colors = (
    # Front face - red gradient
    255, 0, 0, 255,  # 0: red
    255, 100, 0, 255,  # 1: orange-red
    255, 200, 0, 255,  # 2: yellow-red
    255, 255, 0, 255,  # 3: yellow

    # Back face - blue gradient
    0, 0, 255, 255,  # 4: blue
    0, 100, 255, 255,  # 5: light blue
    0, 200, 255, 255,  # 6: cyan-blue
    0, 255, 255, 255,  # 7: cyan

    # Left face - green gradient
    0, 255, 0, 255,  # 8: green
    100, 255, 0, 255,  # 9: yellow-green
    200, 255, 0, 255,  # 10: yellow
    255, 255, 0, 255,  # 11: yellow

    # Right face - purple gradient
    255, 0, 255, 255,  # 12: magenta
    200, 0, 255, 255,  # 13: purple
    100, 0, 255, 255,  # 14: blue-purple
    0, 0, 255, 255,  # 15: blue

    # Top face - white gradient
    200, 200, 200, 255,  # 16: light gray
    225, 225, 225, 255,  # 17: lighter gray
    245, 245, 245, 255,  # 18: almost white
    255, 255, 255, 255,  # 19: white

    # Bottom face - black gradient
    0, 0, 0, 255,  # 20: black
    50, 50, 50, 255,  # 21: dark gray
    100, 100, 100, 255,  # 22: gray
    150, 150, 150, 255,  # 23: light gray
)


tex_coords = (
    # Front face
    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    # Back face
    0.0, 0.0,  # 4: bottom left
    1.0, 0.0,  # 5: bottom right
    1.0, 1.0,  # 6: top right
    0.0, 1.0,  # 7: top left

    # Left face
    0.0, 0.0,  # 8: bottom left
    1.0, 0.0,  # 9: bottom right
    1.0, 1.0,  # 10: top right
    0.0, 1.0,  # 11: top left

    # Right face
    0.0, 0.0,  # 12: bottom left
    1.0, 0.0,  # 13: bottom right
    1.0, 1.0,  # 14: top right
    0.0, 1.0,  # 15: top left

    # Top face
    0.0, 0.0,  # 16: bottom left
    1.0, 0.0,  # 17: bottom right
    1.0, 1.0,  # 18: top right
    0.0, 1.0,  # 19: top left

    # Bottom face
    0.0, 0.0,  # 20: bottom left
    1.0, 0.0,  # 21: bottom right
    1.0, 1.0,  # 22: top right
    0.0, 1.0,  # 23: top left
)

# Define the indices for the cube's 12 triangles (6 faces)
# Each face uses its own set of 4 vertices
indices = [
    # Front face (0-3)
    0, 1, 2, 2, 3, 0,

    # Back face (4-7)
    4, 5, 6, 6, 7, 4,

    # Left face (8-11)
    8, 9, 10, 10, 11, 8,

    # Right face (12-15)
    12, 13, 14, 14, 15, 12,

    # Top face (16-19)
    16, 17, 18, 18, 19, 16,

    # Bottom face (20-23)
    20, 21, 22, 22, 23, 20
]

# Create the cube vertex list with texture coordinates
cube = program.vertex_list_indexed(24, GL_TRIANGLES,
                                   indices,
                                   batch=batch,
                                   vertices=('f', vertices),
                                   colors=('Bn', colors),
                                   tex_coords=('f', tex_coords))

# Set the texture in the shader
program['tex'] = 0  # Texture unit 0

# Animation variables
angle = 5


def update(dt):
    global angle
    angle += dt

    # Update rotation
    Rotate_y = Mat4.from_rotation(angle=angle, vector=Vec3(x=0, y=1, z=0))
    Rotate_x = Mat4.from_rotation(angle=angle * 0.7, vector=Vec3(x=1, y=0, z=0))
    model_Math = cube_Translate @ Rotate_y @ Rotate_x @ cube_Scale
    program['model'] = model_Math


@window.event
def on_draw():
    window.clear()
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture.id)
    batch.draw()
    glBindTexture(GL_TEXTURE_2D, 0)


# Schedule the update function
pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()