from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
POINT_RADIUS = 0.03
MIN_SPEED, MAX_SPEED = 0.005, 0.1
SPEED_INCREMENT = 0.005

# Initialize variables
points = []
frozen = False

class Point:
    def __init__(self, x, y, color, speed):
        self.x, self.y = x, y
        self.color = color
        self.speed = speed
        self.velocity = [random.uniform(-speed, speed), random.uniform(-speed, speed)]
        self.blinking = False
        self.blink_counter = 0
        self.original_color = color

    def toggle_blinking(self):
        self.blinking = not self.blinking

    def update_blinking(self):
        if self.blinking:
            self.blink_counter += 1
            if self.blink_counter % 30 == 0:
                self.color = (0.0, 0.0, 0.0) if self.color == self.original_color else self.original_color

def draw_point(x, y, color):
    glColor3f(*color)
    num_segments = 100
    glBegin(GL_POLYGON)
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        xi = x + POINT_RADIUS * math.cos(theta)
        yi = y + POINT_RADIUS * math.sin(theta)
        glVertex2f(xi, yi)
    glEnd()

def display():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    for point in points:
        point.update_blinking()
        draw_point(point.x, point.y, point.color)

    glutSwapBuffers()

def mouse_click(button, state, x, y):
    global points
    if not frozen and button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        x, y = x / WINDOW_WIDTH * 2 - 1, 1 - y / WINDOW_HEIGHT * 2
        color = (random.random(), random.random(), random.random())
        speed = random.uniform(MIN_SPEED, MAX_SPEED)
        points.append(Point(x, y, color, speed))
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for point in points:
            point.toggle_blinking()
    glutPostRedisplay()

def toggle_freeze():
    global frozen
    frozen = not frozen

def keyboard(key, x, y):
    if key == b' ':
        toggle_freeze()
        for point in points:
            point.blink_counter = 0
    elif key == GLUT_KEY_DOWN and not frozen:
        for point in points:
            point.speed = max(point.speed - SPEED_INCREMENT, MIN_SPEED)
    elif key == GLUT_KEY_UP and not frozen:
        for point in points:
            point.speed = min(point.speed + SPEED_INCREMENT, MAX_SPEED)

def idle():
    if not frozen:
        for point in points:
            if point.x + POINT_RADIUS >= 1.0 or point.x - POINT_RADIUS <= -1.0:
                point.velocity[0] *= -1
            if point.y + POINT_RADIUS >= 1.0 or point.y - POINT_RADIUS <= -1.0:
                point.velocity[1] *= -1
            point.x += point.velocity[0] * point.speed
            point.y += point.velocity[1] * point.speed

    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b'The Amazing Box')

    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)
    glutSpecialFunc(keyboard)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
