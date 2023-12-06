from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

raindrops = []  # List to store raindrop positions
rain_tilt = 0.0  # Initial rain tilt
background_color = (0.529, 0.808, 0.922, 1.0)  # Initial background color (sky blue)
window_color = (0.8, 0.898, 1.0)  # Initial window color (light blue)

def display():
    glClearColor(*background_color)  # Set the background color
    glClear(GL_COLOR_BUFFER_BIT)  # Clear the color buffer

    glColor3f(0.0, 0.0, 0.0)  # Set the outline color to black

    line_thickness = 20  # Line thickness for drawing
    glLineWidth(line_thickness)  # Set the line thickness

    # Draw the outline of a hollow triangle (roof)
    glColor3f(0.376, 0.376, 0.376)  # Set the roof color to grey
    glBegin(GL_TRIANGLES)  # Start drawing a triangle
    glVertex2f(0, 0.8)  # Vertex 1 (top)
    glVertex2f(-0.4, 0.3)  # Vertex 2 (bottom-left)
    glVertex2f(0.4, 0.3)  # Vertex 3 (bottom-right)
    glEnd()  # End drawing the triangle

    # Draw the body of the house as ash grey
    glColor3f(0.75, 0.75, 0.75)  # Set the house color to ash grey
    glBegin(GL_POLYGON)  # Start drawing a polygon
    glVertex2f(-0.35, 0.3)
    glVertex2f(-0.35, -0.4)
    glVertex2f(0.35, -0.4)
    glVertex2f(0.35, 0.3)
    glEnd()  # End drawing the polygon

    glColor3f(0.545, 0.271, 0.075)  # Set the door color to brown

    # Draw the door
    glBegin(GL_POLYGON)
    glVertex2f(-0.25, -0.05)
    glVertex2f(-0.25, -0.4)
    glVertex2f(-0.1, -0.4)
    glVertex2f(-0.1, -0.05)
    glEnd()

    glColor3f(*window_color)  # Set the window color

    # Draw the window
    glBegin(GL_POLYGON)
    glVertex2f(0.1, 0.1)
    glVertex2f(0.3, 0.1)
    glVertex2f(0.3, -0.1)
    glVertex2f(0.1, -0.1)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)  # Set the color for the remaining lines

    # Draw the rest of the house
    glBegin(GL_LINES)  # Start drawing lines
    glVertex2f(-0.4, 0.3)  # Vertex 1 (bottom)
    glVertex2f(0.4, 0.3)  # Vertex 2 (top-left)

    glVertex2f(-0.4, 0.3)  # Vertex 2 (top-left)
    glVertex2f(0, 0.8)  # Vertex 3 (top-right)

    glVertex2f(0.4, 0.3)  # Vertex 3 (top-right)
    glVertex2f(0, 0.8)  # Vertex 1 (bottom)

    glVertex2f(-0.35, 0.3)
    glVertex2f(-0.35, -0.4)

    glVertex2f(0.35, 0.3)
    glVertex2f(0.35, -0.4)

    glVertex2f(-0.35, -0.4)
    glVertex2f(0.35, -0.4)
    glEnd()

    door_window()  # Call the door and window drawing function

    draw_rain()  # Call the raindrop drawing function

    glutSwapBuffers()  # Swap the front and back buffers for double buffering

def door_window():
    line_thickness = 1.5  # Set the line thickness for the door and window outlines
    glLineWidth(line_thickness)  # Set the line thickness for drawing outlines

    glBegin(GL_LINES)  # Start drawing lines
    # Draw the door outline
    glVertex2f(-0.25, -0.4)
    glVertex2f(-0.25, -0.05)

    glVertex2f(-0.25, -0.05)
    glVertex2f(-0.1, -0.05)

    glVertex2f(-0.1, -0.05)
    glVertex2f(-0.1, -0.4)

    # Draw the window outline
    glVertex2f(0.3, -0.1)
    glVertex2f(0.1, -0.1)

    glVertex2f(0.1, -0.1)
    glVertex2f(0.1, 0.1)

    glVertex2f(0.3, -0.1)
    glVertex2f(0.3, 0.1)

    glVertex2f(0.1, 0.1)
    glVertex2f(0.3, 0.1)

    # Draw window crossbars
    glVertex2f(0.2, 0.1)
    glVertex2f(0.2, -0.1)

    glVertex2f(0.1, 0)
    glVertex2f(0.3, 0)
    glEnd()

    glPointSize(4.0)  # Set the point size (adjust for desired size)

    glBegin(GL_POINTS)  # Start drawing points
    glVertex2f(-0.12, -0.225)  # Coordinates of the point
    glEnd()

def draw_rain():
    glLineWidth(2.0)  # Set the line thickness for raindrops
    glColor3f(0.0, 139, 139)  # Set the color to cyan

    glBegin(GL_LINES)  # Start drawing lines
    for x, y in raindrops:
        glVertex2f(x, y)
        glVertex2f(x + rain_tilt, y - 0.05)  # Adjust this value to control the length and direction of raindrops
    glEnd()

def mouse_click(button, state, x, y):
    global rain_tilt
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rain_tilt = -0.02  # Tilt rain left when left-clicked
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        rain_tilt = 0.02  # Tilt rain right when right-clicked

def change_background_color(new_color):
    global background_color, window_color
    background_color = new_color
    if new_color == (0.0, 0.0, 0.2, 1.0):
        window_color = (1.0, 1.0, 0.0)  # Change the window color to yellow
    else:
        window_color = (0.8, 0.898, 1.0)  # Revert the window color to sky blue
    glutPostRedisplay()  # Trigger a display update

def keyboard(key, x, y):
    if key == b'n':
        change_background_color((0.0, 0.0, 0.2, 1.0))  # Change the background color to dark blue
    elif key == b'd':
        change_background_color((0.529, 0.808, 0.922, 1.0))  # Change the background color to sky blue

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)  # Set display mode for double buffering and RGB color
    glutInitWindowSize(1200, 800)  # Set the initial window size
    glutCreateWindow(b'Task1')  # Create a window with a title
    glutDisplayFunc(display)  # Register the display callback function

    glutMouseFunc(mouse_click)  # Register the mouse click callback
    glutKeyboardFunc(keyboard)  # Register the keyboard callback

    # Initialize raindrop positions
    for _ in range(200):
        x = random.uniform(-1, 1)  # Random x positions within the house
        y = random.uniform(-0.2, 1)  # Random y positions above the house
        raindrops.append((x, y))

    glutMainLoop()  # Enter the main event loop

if __name__ == "__main__":
    main()

