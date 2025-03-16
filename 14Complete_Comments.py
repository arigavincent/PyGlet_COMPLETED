import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import Mat4, Vec3
from pyglet.window import key, mouse

# Window initialization
# Creates a resizable window with a specific title, dimensions, and position
# TODO 1: Add window configuration options (fullscreen, vsync, etc.)
window = pyglet.window.Window(width=1200, height=720, caption="3D Textured Cube", resizable=True)
window.set_location(400, 200)  # Position the window on the screen
batch = pyglet.graphics.Batch()  # Create a batch for efficient rendering of multiple objects
glEnable(GL_DEPTH_TEST)  # Enable depth testing so closer objects render on top of further ones

# Load texture for the cube
# TODO 2: Implement proper texture loading error handling
texture = pyglet.image.load('Textures/t1.jpg').get_texture()  # Load image and convert to OpenGL texture

# GLSL Shaders define how vertices are processed (vertex shader) and pixels are colored (fragment shader)
# Vertex Shader: Transforms 3D coordinates to 2D screen coordinates and passes color and texture data
vertex_source = """
#version 150
in vec3 vertices;      // Input vertex positions
in vec4 colors;        // Input vertex colors
in vec2 tex_coords;    // Input texture coordinates
out vec4 newColors;    // Output color data to fragment shader
out vec2 newTexCoords; // Output texture coordinates to fragment shader
uniform mat4 vp;       // View-projection matrix (camera + projection)
uniform mat4 model;    // Model matrix (position, rotation, scale of object)

void main() {
    // Calculate final vertex position by applying transformations
    gl_Position = vp * model * vec4(vertices, 1.0);
    newColors = colors;        // Pass vertex colors to fragment shader
    newTexCoords = tex_coords; // Pass texture coordinates to fragment shader
}
"""

# Fragment Shader: Determines the final color of each pixel
fragment_source = """
#version 150
in vec4 newColors;      // Input colors from vertex shader
in vec2 newTexCoords;   // Input texture coordinates from vertex shader
out vec4 outColors;     // Final output color
uniform sampler2D tex;  // Texture sampler

void main() {
    // Sample the texture at the specified coordinates
    vec4 texColor = texture(tex, newTexCoords);
    // Multiply texture color by vertex color for final output
    outColors = texColor * newColors;
}
"""

# Compile shaders and create shader program
# TODO 3: Add shader compilation error checking
vertex_Shader = Shader(vertex_source, "vertex")
frag_Shader = Shader(fragment_source, "fragment")
program = ShaderProgram(vertex_Shader, frag_Shader)  # Combine shaders into a program

# Camera setup
# Create view matrix (camera position and orientation)
view_Math = Mat4.from_translation(Vec3(x=0, y=0, z=-4))  # Move camera back 4 units
# Create projection matrix (perspective transformation)
project_Mat = Mat4.perspective_projection(aspect=1.6666, z_near=0.1, z_far=100)  # Define viewing frustum
vp = project_Mat @ view_Math  # Combine into view-projection matrix
program['vp'] = vp  # Send to shader as uniform

# Object position and orientation variables
# TODO 4: Create a proper camera class for better movement control
cube_x = 0  # Cube x position
cube_y = 0  # Cube y position
cube_z = -2  # Cube z position (2 units into the screen)
rotation_y = 0  # Rotation around y-axis (in radians)
rotation_x = 0  # Rotation around x-axis (in radians)
cube_Scale = Mat4.from_scale(vector=Vec3(x=2, y=2, z=2))  # Scale cube to twice its original size

# Added zoom functionality
zoom_level = 1.0  # Initial zoom level (1.0 = normal size)
zoom_speed = 0.1  # How quickly zoom changes with key presses

# Cube geometry data
# Vertices for each of the 6 faces of the cube (4 vertices per face)
# Each triplet represents x, y, z coordinates of a vertex
vertices = (
    # Front face vertices (z = 0.5)
    -0.5, -0.5, 0.5,  # Bottom left
    0.5, -0.5, 0.5,  # Bottom right
    0.5, 0.5, 0.5,  # Top right
    -0.5, 0.5, 0.5,  # Top left

    # Back face vertices (z = -0.5)
    -0.5, -0.5, -0.5,  # Bottom left
    0.5, -0.5, -0.5,  # Bottom right
    0.5, 0.5, -0.5,  # Top right
    -0.5, 0.5, -0.5,  # Top left

    # Left face vertices (x = -0.5)
    -0.5, -0.5, -0.5,  # Bottom back
    -0.5, -0.5, 0.5,  # Bottom front
    -0.5, 0.5, 0.5,  # Top front
    -0.5, 0.5, -0.5,  # Top back

    # Right face vertices (x = 0.5)
    0.5, -0.5, 0.5,  # Bottom front
    0.5, -0.5, -0.5,  # Bottom back
    0.5, 0.5, -0.5,  # Top back
    0.5, 0.5, 0.5,  # Top front

    # Top face vertices (y = 0.5)
    -0.5, 0.5, 0.5,  # Front left
    0.5, 0.5, 0.5,  # Front right
    0.5, 0.5, -0.5,  # Back right
    -0.5, 0.5, -0.5,  # Back left

    # Bottom face vertices (y = -0.5)
    -0.5, -0.5, -0.5,  # Back left
    0.5, -0.5, -0.5,  # Back right
    0.5, -0.5, 0.5,  # Front right
    -0.5, -0.5, 0.5,  # Front left
)

# Vertex colors
# Each face has 4 vertices, each with RGBA color values (R,G,B,A)
colors = (
    # Front face colors (reddish)
    255, 0, 0, 255,  # Pure red
    255, 100, 0, 255,  # Orange-red
    255, 200, 0, 255,  # Yellow-orange
    255, 255, 0, 255,  # Yellow

    # Back face colors (bluish)
    0, 0, 255, 255,  # Pure blue
    0, 100, 255, 255,  # Light blue
    0, 200, 255, 255,  # Cyan-blue
    0, 255, 255, 255,  # Cyan

    # Left face colors (greenish)
    0, 255, 0, 255,  # Pure green
    100, 255, 0, 255,  # Yellow-green
    200, 255, 0, 255,  # Yellow
    255, 255, 0, 255,  # Yellow

    # Right face colors (purplish)
    255, 0, 255, 255,  # Magenta
    200, 0, 255, 255,  # Purple
    100, 0, 255, 255,  # Blue-purple
    0, 0, 255, 255,  # Blue

    # Top face colors (white shades)
    200, 200, 200, 255,  # Light gray
    225, 225, 225, 255,  # Lighter gray
    245, 245, 245, 255,  # Almost white
    255, 255, 255, 255,  # Pure white

    # Bottom face colors (black/gray shades)
    0, 0, 0, 255,  # Black
    50, 50, 50, 255,  # Dark gray
    100, 100, 100, 255,  # Medium gray
    150, 150, 150, 255,  # Light gray
)

# Texture coordinates
# Maps 2D texture onto each face of the cube (u,v coordinates)
# Range is 0.0 to 1.0, where (0,0) is bottom-left and (1,1) is top-right of texture
tex_coords = (
    # Front face texture mapping
    0.0, 0.0,  # Bottom left
    1.0, 0.0,  # Bottom right
    1.0, 1.0,  # Top right
    0.0, 1.0,  # Top left

    # Back face texture mapping
    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    # Left face texture mapping
    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    # Right face texture mapping
    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    # Top face texture mapping
    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,

    # Bottom face texture mapping
    0.0, 0.0,
    1.0, 0.0,
    1.0, 1.0,
    0.0, 1.0,
)

# Triangle indices
# Define how vertices are connected to form triangles
# Each face consists of 2 triangles (6 indices per face)
indices = [
    0, 1, 2, 2, 3, 0,  # Front face (vertices 0,1,2 and 2,3,0)
    4, 5, 6, 6, 7, 4,  # Back face
    8, 9, 10, 10, 11, 8,  # Left face
    12, 13, 14, 14, 15, 12,  # Right face
    16, 17, 18, 18, 19, 16,  # Top face
    20, 21, 22, 22, 23, 20  # Bottom face
]

# Create the cube mesh by sending vertex data to GPU
# TODO 5: Refactor mesh creation into reusable function
cube = program.vertex_list_indexed(24, GL_TRIANGLES,  # 24 vertices, drawing triangles
                                   indices,  # How vertices connect
                                   batch=batch,  # Add to rendering batch
                                   vertices=('f', vertices),  # Vertex positions (format: float)
                                   colors=('Bn', colors),  # Vertex colors (format: Byte, normalized)
                                   tex_coords=('f', tex_coords))  # Texture coordinates (format: float)

# Set the texture unit for the shader
program['tex'] = 0  # Use texture unit 0

# Input handling
# Dictionary to track which direction keys are being pressed
direction = {"left": False, "right": False, "up": False, "down": False, "Auto_Rotate": False, "zoom_in": False,
             "zoom_out": False}
movement_speed = 5  # Movement speed factor


# Handle key press events
@window.event
def on_key_press(symbol: int, modifiers: int):
    """
    Process key press events and update direction states

    Args:
        symbol (int): Key symbol constant
        modifiers (int): Modifier key flags
    """
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
    """
    Process key release events and update direction states

    Args:
        symbol (int): Key symbol constant
        modifiers (int): Modifier key flags
    """
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


# Mouse input handling
# TODO 6: Add more mouse interaction controls (zoom, pan)
@window.event
def on_mouse_press(x: int, y: int, button: int, modifiers: int) -> None:
    if button == mouse.LEFT:
        direction["Auto_Rotate"] = False  # Stop auto-rotation when mouse is clicked


# Update function called every frame to handle animation and movement
# TODO 7: Improve movement
def update(dt):

        #dt (float): Time elapsed since last update in seconds

    global cube_x, cube_y, cube_z, rotation_x, rotation_y, zoom_level

    # Process movement input - adjust cube position based on key presses
    if direction["left"]:
        cube_x -= movement_speed * dt  # Move cube left
    if direction["right"]:
        cube_x += movement_speed * dt  # Move cube right
    if direction["up"]:
        cube_y += movement_speed * dt  # Move cube up
    if direction["down"]:
        cube_y -= movement_speed * dt  # Move cube down

    # Handle zoom functionality
    if direction["zoom_in"]:
        zoom_level += zoom_speed  # Increase zoom (make cube bigger)
    if direction["zoom_out"]:
        zoom_level = max(0.1, zoom_level - zoom_speed)  # Decrease zoom (make cube smaller), but not below 0.1

    # Handle auto-rotation
    if direction["Auto_Rotate"]:
        rotation_y += dt * 2  # Rotate around y-axis (horizontal)
        rotation_x += dt * 2  # Rotate around x-axis (vertical)

    # Update transformation matrices
    # These matrices define how the cube is transformed in 3D space
    cube_Translate = Mat4.from_translation(vector=Vec3(x=cube_x, y=cube_y, z=cube_z))
    Rotate_y = Mat4.from_rotation(angle=rotation_y, vector=Vec3(x=0, y=1, z=0))
    Rotate_x = Mat4.from_rotation(angle=rotation_x, vector=Vec3(x=1, y=0, z=0))
    # Apply zoom level to scale matrix
    cube_Scale = Mat4.from_scale(vector=Vec3(x=2 * zoom_level, y=2 * zoom_level, z=2 * zoom_level))
    model_Math = cube_Translate @ Rotate_y @ Rotate_x @ cube_Scale
    program['model'] = model_Math


@window.event
def on_draw():
    window.clear()
    batch.draw()


# The Main Loop
pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()