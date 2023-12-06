from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


m0, n0, m1, n1 = 5500, 9000, 5800, 9400  # For Diamond (initial coordinates)
x0, y0, x1, y1 = 1000, 500, 3250, 500  # For Catcher (initial coordinates)
speed = 100  #the speed at which the diamond falls
Left = 0         #for controlling the movement in left direction
Right = 0        #for controlling the movement in right direction


def catcher(x0, y0, x1, y1):  #for drawing catcher
    glColor3f(0.7, 0.7, 0.7)  #sets the color to grey  
    midpointline(x0 - Left + Right, y0, x1 - Left + Right, y1) #Upper Side:   
    midpointline(x0 + 150 - Left + Right, y0 - 400, x1 - 150 - Left + Right, y1 - 400) #Lower Side:  
    midpointline(x0 - Left + Right, y0, x0 + 150 - Left + Right, y0 - 400) #Left Side: 
    midpointline(x1 - 150 - Left + Right, y1 - 400, x1 - Left + Right, y1) #Right Side:


def draw_diamond(a, b, size): #x and y coordinate of the center of diamond, size is the half 0f the side length)
    glBegin(GL_POLYGON)
    glVertex2f(a, b) #(top vertex)
    glVertex2f(a + size, b + size)  #(right vertex)
    glVertex2f(a, b + 2 * size) #(bottom vertex)
    glVertex2f(a - size, b + size) #(left vertex)
    glEnd()

def diamond(m0, n0, m1, n1):  # for drawing diamond
    glColor3f(1.0, 1.0, 1.0)  # setting the color to white
    draw_diamond(m0 + 300, n0 - 400, 150)


def arrow():  #for drawing arrow facing left
    glColor3f(0, 1.0, 0)  #color set to cyan
    midpointline(350, 9100, 1350, 9100) #horizontal line of the arrow
    midpointline(350, 9100, 850, 9450) #upper right diagonal
    midpointline(350, 9100, 850, 8750) #lower right diagonal


def pause():  #drawing pause, unpause button
    glColor3f(0, 0, 1.0)
    midpointline(4500, 9300, 4500, 8600)
    midpointline(4900, 9300, 4900, 8600)


def cross(): #drawing cross
    glColor3f(1.0, 0.0, 0.0) 
    midpointline(8500, 9300, 9200, 8600)
    midpointline(8500, 8600, 9200, 9300)


def pixel(x0, y0):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x0, y0)
    glEnd()


def midpointline(x0, y0, x1, y1): #midpoint line algorithm
    zone = zoneFinder(x0, y0, x1, y1)
    x0, y0 = zone0converter(zone, x0, y0) #call the zone0converter function used to convert the coordinates based on the determined zone.
    x1, y1 = zone0converter(zone, x1, y1)
    dx = x1 - x0  #change in x
    dy = y1 - y0  #change in y
    dinit = 2 * dy - dx  #initial decision
    dne = 2 * dy - 2 * dx  #for updating d if northeast is chosen
    de = 2 * dy  #for updating d if east is chosen 

    for i in range(x0, x1):
        a, b = zerotoOriginal(zone, x0, y0)
        if dinit >= 0:
            dinit = dinit + dne #if dinit greater than or equal to zero then d is updated by adding dinit and dne
            pixel(a, b)  #calls the draw_points function with the converted coordinates 
            x0 += 1 #move the iteration to the next pixel in the northeast direction
            y0 += 1 #move the iteration to the next pixel in the northeast direction
        else:
            dinit = dinit + de  #if dinit less than zero then d is updated by adding dinit and de
            pixel(a, b)  #calls the draw_points function with the converted coordinates
            x0 += 1  #move the iteration to the next pixel in the east direction


def zoneFinder(x0, y0, x1, y1): #determines the zone of a line based on the signs of the differences in x and y coordinates between its two endpoints
    dx = x1 - x0  #change in x
    dy = y1 - y0  #change in y
    if abs(dx) > abs(dy):  # For Zone 0, 3, 4 and 7
        if dx > 0 and dy > 0:
            return 0 #zone zero
        elif dx < 0 and dy > 0:
            return 3 #zone three
        elif dx < 0 and dy < 0:
            return 4 #zone 4
        else:
            return 7 #zone seven
    else:  # For zone 1, 2, 5 and 6
        if dx > 0 and dy > 0:
            return 1 #zone one
        elif dx < 0 and dy > 0:
            return 2 #zone two
        elif dx < 0 and dy < 0:
            return 5 #zone five
        else:
            return 6 #zone six


def zone0converter(zone, x0, y0): #for converting to zone zero coordinates
    if zone == 0:
        return x0, y0
    elif zone == 1:
        return y0, x0
    elif zone == 2:
        return -y0, x0
    elif zone == 3:
        return -x0, y0
    elif zone == 4:
        return -x0, -y0
    elif zone == 5:
        return -y0, -x0
    elif zone == 6:
        return -y0, x0
    elif zone == 7:
        return x0, -y0


def zerotoOriginal(zone, x0, y0): #for converting coordinates from Zone 0 to their original zone
    if zone == 0:
        return x0, y0
    if zone == 1:
        return y0, x0
    if zone == 2:
        return -y0, -x0
    if zone == 3:
        return -x0, y0
    if zone == 4:
        return -x0, -y0
    if zone == 5:
        return -y0, -x0
    if zone == 6:
        return y0, -x0
    if zone == 7:
        return x0, -y0


def specialKeyListener(key, L, R): #setting right and left arrow key for moving the catcher
    glutPostRedisplay()
    global Left, Right
    if key == GLUT_KEY_LEFT:

        Left += 300  #increments the left variable by 300
    elif key == GLUT_KEY_RIGHT:

        Right += 300  #increments the right variable by 300
    glutPostRedisplay()


def animate():
    global n0, n1
    n0 -= speed
    n1 -= speed
    if n1 - 800 == 0:
        n0 = 7800
        n1 = 8200
    glutPostRedisplay()
    glutTimerFunc(15, animate, 0)


def iterate(): #for setting up the OpenGL context
    glViewport(0, 0, 500, 500) #to make a square viewport of 500x500 pixels
    glMatrixMode(GL_PROJECTION) #to set up the camera and viewing volume
    glLoadIdentity()
    glOrtho(0.0, 10000, 0.0, 10000, 0.0, 1.0) #coordinate system that will be used for rendering
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity() #resets the current matrix


def showScreen():  #for rendering the scene
    global x0, y0, x1, y1
    global m0, n0, m1, n1
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    animate() #updates the position of the diamond
    glColor3f(1.0, 0.0, 0.0)
    arrow()
    pause()
    cross()
    catcher(x0, y0, x1, y1)
    diamond(m0, n0, m1, n1)
    glutTimerFunc(0, animate, 0)
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Diamond Catcher")  
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutMainLoop()