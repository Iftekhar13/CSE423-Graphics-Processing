from OpenGL.GL import *
from OpenGL.GLUT import *

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60

# Circle class
class GrowingCircle: #representation of a circle with its center coordinates, radius, and a growth rate
    def __init__(self, center_x, center_y, radius, growth_rate):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.growth_rate = growth_rate

    def update(self): #responsible for updating the circle's radius based on its growth rate
        self.radius += self.growth_rate #increments the current radius

    def is_outside_window(self): 

        return (
            self.center_x - self.radius < 0 #Checks if the left edge of the circle is to the left of the window's left boundary.
            or self.center_x + self.radius > WINDOW_WIDTH #Checks if the right edge of the circle is to the right of the window's right boundary
            or self.center_y - self.radius < 0 #Checks if the bottom edge of the circle is below the window's bottom boundary.
            or self.center_y + self.radius > WINDOW_HEIGHT #Checks if the top edge of the circle is above the window's top boundary
        ) 

# Variables
growing_circles = [] #It will keep track of all the circles that are currently on the screen.
is_paused = False #It will be used to determine whether the animation is currently paused or not
growth_rate = 1 #represents the rate at which the circles will grow

# Initialize GLUT
glutInit() #Initializes the GLUT library
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) #Sets the display mode for the window. 
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT) #Sets the initial size of the window
glutCreateWindow(b"Lab3_20201120") #Creates a window with the given title. The title is specified as a bytes object 

# Initialize OpenGL
glClearColor(0, 0, 0, 0) #Sets the clear color for the color buffer
glMatrixMode(GL_PROJECTION) 
glLoadIdentity() #Loads the identity matrix into the current matrix 
glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1) 
glMatrixMode(GL_MODELVIEW) #Specifies that subsequent matrix operations will affect the model-view matrix.
glLoadIdentity()
# Function to draw a circle using midpoint circle drawing algorithm with 8-way symmetry
def circ_point(x, y, cx, cy): 
    glVertex2f(cx + x, cy + y) 
    glVertex2f(cx + y, cy + x) 
    glVertex2f(cx + y, cy - x) 
    glVertex2f(cx + x, cy - y) 
    glVertex2f(cx - x, cy - y) 
    glVertex2f(cx - y, cy - x) 
    glVertex2f(cx - y, cy + x) 
    glVertex2f(cx - x, cy + y) 

def mid_circle(cx, cy, radius): #implementng midpoint circle algorithm
    d = 1 - radius #initial decision parameter
    x = 0
    y = radius

    glBegin(GL_POINTS) #for drawing points for the circle
    circ_point(x, y, cx, cy)

    while x < y:
        if d < 0: #if initial decision parameter is negative then east pixel is chosen
            d = d + 2 * x + 3 #updating decision parameter accordingly
        else: #if decision parameter is positive southeast pixel is chosen
            d = d + 2 * x - 2 * y + 5 #updating decision parameter accordingly
            y = y - 1 #value of y is decremented by 1

        x = x + 1 #in both cases value of x will increment by 1
        circ_point(x, y, cx, cy)

    glEnd()

# Display function
def display(): #for clearing the screen, drawing each growing circle, and swapping the buffers to display the rendered image
    glClear(GL_COLOR_BUFFER_BIT) #clears the color buffer

    for circle in growing_circles: #This loop iterates through the list of growing_circles
        mid_circle(circle.center_x, circle.center_y, int(circle.radius)) #For each circle in growing_circles,
                                                    # it calls the mid_circle function to draw the circle using the midpoint circle drawing algorithm.
    glutSwapBuffers() #swaps the front and back buffers for smooth animation and to prevent flickering.

# Update function
def update(value): #for updating the state of the growing circles and triggering the display function to redraw the scene
    global is_paused, growth_rate, growing_circles

    if not is_paused: #checks whether the animation is not paused
        for circle in growing_circles: #iterates through each circle in the growing_circles list 
            circle.update() #calls the update method of each circle.

        growing_circles = [circle for circle in growing_circles if not circle.is_outside_window()] #filters out circles that are outside the window boundaries 
                                                                                       #using the is_outside_window method of the GrowingCircle class.
    glutPostRedisplay()
    glutTimerFunc(int(1000 / FPS), update, 0) #sets up the next update callback. 
                                              #creates a continuous loop for updating and redrawing the scene

# Keyboard function
def keyboard(key, x, y):
    global is_paused, growth_rate

    if key == b' ': #checks if the pressed key is the spacebar
        is_paused = not is_paused

# Special keyboard function for handling arrow keys
def special_key(key, x, y):
    global growth_rate

    if key == GLUT_KEY_LEFT: #checks if the pressed special key is the left arrow key.
        growth_rate += 1 #If the left arrow key is pressed, this line increments the growth_rate variable by 1.
        for circle in growing_circles: # iterates over each circle in the growing_circles list.
            circle.growth_rate = growth_rate # this line sets its growth rate to the updated value of growth_rate

    elif key == GLUT_KEY_RIGHT: #checks if the pressed special key is the right arrow key.
        growth_rate = max(1, growth_rate - 1) #If the right arrow key is pressed, this line decrements the growth_rate variable by 1 
        for circle in growing_circles: #to update the growth rates of all existing circles   
            circle.growth_rate = growth_rate

# Mouse function
def mouse(button, state, x, y): #to handle mouse events
    global growing_circles

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not is_paused: #checks if the right mouse button is pressed and if the animation is not paused.
        y = WINDOW_HEIGHT - y  # Invert y coordinate
        growing_circles.append(GrowingCircle(x, y, 5, growth_rate)) #This line creates a new instance of the GrowingCircle class
                                              #and appends it to the growing_circles list.
                                              #The parameters for the new circle are the x and y coordinates of the mouse click, an initial radius of 5
                                              #and the current growth rate.

# Register functions
glutDisplayFunc(display) #sets the display callback function
glutTimerFunc(int(1000 / FPS), update, 0) #sets the timer callback function. The update function will be called repeatedly at a fixed interval determined by FPS
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_key)  # Register special function for arrow keys
glutMouseFunc(mouse)

# Start main loop
glutMainLoop()
