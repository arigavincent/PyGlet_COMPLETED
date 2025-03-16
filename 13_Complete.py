import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3
from pyglet.window import key, mouse

# TODO 1: Add window configuration options (fullscreen, vsync, etc.)
window = pyglet.window.Window(width=1200, height=720, caption="3D Textured Cube", resizable=True)
window.set_location(400, 200)
batch = pyglet.graphics.Batch()
glEnable(GL_DEPTH_TEST)

# TODO 2: Implement proper texture loading error handling
texture = pyglet.image.load('Textures/t1.jpg').get_texture()

# GLSL Shaders
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

# TODO 3: Add shader compilation error checking
vertex_Shader = Shader(vertex_source, "vertex")
frag_Shader = Shader(fragment_source, "fragment")
program = ShaderProgram(vertex_Shader, frag_Shader)

# Camera setup
view_Math = Mat4.from_translation(Vec3(x=0, y=0, z=-4))
project_Mat = Mat4.perspective_projection(aspect=1.6666, z_near=0.1, z_far=100)
vp = project_Mat @ view_Math
program['vp'] = vp

# TODO 4: Create a proper camera class for better movement control
cube_x = 0
cube_y = 0
cube_z = -2
rotation_y = 0
rotation_x = 0
cube_Scale = Mat4.from_scale(vector=Vec3(x=2, y=2, z=2))

# Added zoom functionality
zoom_level = 1.0
zoom_speed = 0.1

# Cube geometry data
vertices = (
    -0.5, -0.5, 0.5,
    0.5, -0.5, 0.5,
    0.5, 0.5, 0.5,
    -0.5, 0.5, 0.5,

    -0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5, 0.5, -0.5,
    -0.5, 0.5, -0.5,

    -0.5, -0.5, -0.5,
    -0.5, -0.5, 0.5,
    -0.5, 0.5, 0.5,
    -0.5, 0.5, -0.5,

    0.5, -0.5, 0.5,
    0.5, -0.5, -0.5,
    0.5, 0.5, -0.5,
    0.5, 0.5, 0.5,

    -0.5, 0.5, 0.5,
    0.5, 0.5, 0.5,
    0.5, 0.5, -0.5,
    -0.5, 0.5, -0.5,

    -0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5, -0.5, 0.5,
    -0.5, -0.5, 0.5,
)

# Vertex colors
colors = (
    255, 0, 0, 255,
    255, 100, 0, 255,
    255, 200, 0, 255,
    255, 255, 0, 255,

    0, 0, 255, 255,
    0, 100, 255, 255,
    0, 200, 255, 255,
    0, 255, 255, 255,

    0, 255, 0, 255,
    100, 255, 0, 255,
    200, 255, 0, 255,
    255, 255, 0, 255,

    255, 0, 255, 255,
    200, 0, 255, 255,
    100, 0, 255, 255,
    0, 0, 255, 255,

    200, 200, 200, 255,
    225, 225, 225, 255,
    245, 245, 245, 255,
    255, 255, 255, 255,

    0, 0, 0, 255,
    50, 50, 50, 255,
    100, 100, 100, 255,
    150, 150, 150, 255,
)

# Texture coordinates
tex_coords = (
    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,
)

# Triangle indices
indices = [
    0, 1, 2, 2, 3, 0,
    4, 5, 6, 6, 7, 4,
    8, 9, 10, 10, 11, 8,
    12, 13, 14, 14, 15, 12,
    16, 17, 18, 18, 19, 16,
    20, 21, 22, 22, 23, 20
]

# TODO 5: Refactor mesh creation into reusable function
cube = program.vertex_list_indexed(24, GL_TRIANGLES,
                                   indices,
                                   batch=batch,
                                   vertices=('f', vertices),
                                   colors=('Bn', colors),
                                   tex_coords=('f', tex_coords))

program['tex'] = 0

# Input handling
direction = {"left": False, "right": False, "up": False, "down": False, "Auto_Rotate": False, "zoom_in": False, "zoom_out": False}
movement_speed = 5

# Handle key press events
@window.event
def on_key_press(symbol: int, modifiers: int):
    if symbol == key.LEFT or symbol == key.A:
        direction["left"] = True
    if symbol == key.RIGHT or symbol == key.D:
        direction["right"] = True
    if symbol == key.UP or symbol == key.W:
        direction["up"] = True
    if symbol == key.DOWN or symbol == key.S:
        direction["down"] = True
    if symbol == key.SPACE:
        direction["Auto_Rotate"] = True
    # Added zoom controls
    if symbol == key.PLUS or symbol == key.EQUAL:
        direction["zoom_in"] = True
    if symbol == key.MINUS or symbol == key.UNDERSCORE:
        direction["zoom_out"] = True

# Handle key release events
@window.event
def on_key_release(symbol: int, modifiers: int):
    if symbol == key.LEFT or symbol == key.A:
        direction["left"] = False
    if symbol == key.RIGHT or symbol == key.D:
        direction["right"] = False
    if symbol == key.UP or symbol == key.W:
        direction["up"] = False
    if symbol == key.DOWN or symbol == key.S:
        direction["down"] = False
    # Added zoom controls release
    if symbol == key.PLUS or symbol == key.EQUAL:
        direction["zoom_in"] = False
    if symbol == key.MINUS or symbol == key.UNDERSCORE:
        direction["zoom_out"] = False

# TODO 6: Add more mouse interaction controls (zoom, pan)
@window.event
def on_mouse_press(x: int, y: int, button: int, modifiers: int) -> None:
    if button == mouse.LEFT:
        direction["Auto_Rotate"] = False

# TODO 7: Improve physics/movement system
def update(dt):
    global cube_x, cube_y, cube_z, rotation_x, rotation_y, zoom_level

    # Process movement input
    if direction["left"]:
        cube_x -= movement_speed * dt
    if direction["right"]:
        cube_x += movement_speed * dt
    if direction["up"]:
        cube_y += movement_speed * dt
    if direction["down"]:
        cube_y -= movement_speed * dt

    # Handle zoom functionality
    if direction["zoom_in"]:
        zoom_level += zoom_speed
    if direction["zoom_out"]:
        zoom_level = max(0.1, zoom_level - zoom_speed)  # Prevent negative zoom

    # Handle auto-rotation
    if direction["Auto_Rotate"]:
        rotation_y += dt * 2
        rotation_x += dt * 2

    # Update transformation matrices
    cube_Translate = Mat4.from_translation(vector=Vec3(x=cube_x, y=cube_y, z=cube_z))
    Rotate_y = Mat4.from_rotation(angle=rotation_y, vector=Vec3(x=0, y=1, z=0))
    Rotate_x = Mat4.from_rotation(angle=rotation_x, vector=Vec3(x=1, y=0, z=0))
    # Apply zoom level to scale matrix
    cube_Scale = Mat4.from_scale(vector=Vec3(x=2*zoom_level, y=2*zoom_level, z=2*zoom_level))
    model_Math = cube_Translate @ Rotate_y @ Rotate_x @ cube_Scale
    program['model'] = model_Math

# TODO 8: Add FPS counter and performance monitoring
@window.event
def on_draw():
    window.clear()
    batch.draw()

# Game loop
pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()