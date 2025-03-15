import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3

window = pyglet.window.Window(width=1200, height=720, caption="3D Textured Cube", resizable=True)
window.set_location(400, 200)
batch = pyglet.graphics.Batch()
glEnable(GL_DEPTH_TEST)

# Load texture image
texture = pyglet.image.load('Textures/wood.jpg').get_texture()
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
view_Math = Mat4.from_translation(Vec3(x=0, y=0, z=-2))
project_Mat = Mat4.perspective_projection(aspect=1.6666, z_near=0.1, z_far=100)

# Combine view and projection matrices
vp = project_Mat @ view_Math
program['vp'] = vp

# 3D Transformations
cube_Translate = Mat4.from_translation(vector=Vec3(x=0, y=0, z=0))
cube_Rotate = Mat4.from_rotation(angle=1, vector=Vec3(x=0, y=1, z=0))
cube_Scale = Mat4.from_scale(vector=Vec3(x=1, y=1, z=1))

# Combine the transformation matrices
model_Math = cube_Translate @ cube_Rotate @ cube_Scale
program['model'] = model_Math

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

# Define the colors for each vertex (keeping your original colors)
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

# Define texture coordinates for each vertex
# For each vertex we assign UV coordinates (0-1 range)
tex_coords = (
    # Front face
    0.0, 0.0,  # 0: bottom left
    1.0, 0.0,  # 1: bottom right
    1.0, 1.0,  # 2: top right
    0.0, 1.0,  # 3: top left

    # Back face
    1.0, 0.0,  # 4: bottom left (flipped)
    0.0, 0.0,  # 5: bottom right (flipped)
    0.0, 1.0,  # 6: top right (flipped)
    1.0, 1.0,  # 7: top left (flipped)
)

# Define the indices for the cube's 12 triangles (6 faces)
indices = [
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

# Create the cube vertex list with texture coordinates
cube = program.vertex_list_indexed(8, GL_TRIANGLES,
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