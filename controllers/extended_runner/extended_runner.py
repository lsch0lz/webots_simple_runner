"""Naive maze runner controller."""

from controller import Robot
import time

robot = Robot()

# Get simulation step length.
timeStep = int(robot.getBasicTimeStep())

maxMotorVelocity = 6

# motors
leftMotor = robot.getDevice("motor.left")
rightMotor = robot.getDevice("motor.right")

# front sensors
outerLeftSensor = robot.getDevice("prox.horizontal.0")
centralLeftSensor = robot.getDevice("prox.horizontal.1")
centralSensor = robot.getDevice("prox.horizontal.2")
centralRightSensor = robot.getDevice("prox.horizontal.3")
outerRightSensor = robot.getDevice("prox.horizontal.4")
leftSensor = robot.getDevice("prox.horizontal.5")
rightSensor = robot.getDevice("prox.horizontal.6")

outerLeftSensor.enable(timeStep)
centralLeftSensor.enable(timeStep)
centralSensor.enable(timeStep)
centralRightSensor.enable(timeStep)
outerRightSensor.enable(timeStep)
leftSensor.enable(timeStep)
rightSensor.enable(timeStep)

# ground sensors
groundLeftSensor = robot.getDevice("prox.ground.0")
groundRightSensor = robot.getDevice("prox.ground.1")

groundLeftSensor.enable(timeStep)
groundRightSensor.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

# states of the robot
is_middle_right = True
is_middle_left = True
is_empty_left = False
is_left = False
is_turning = False
is_end = False
is_standard_maze = False

# counting variables
count = 0
count_black_dots = 0
while robot.step(timeStep) != -1:
    # always drive forward
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)

    # condition for left wall
    if centralSensor.getValue() > 0 or outerLeftSensor.getValue() > 0 or centralLeftSensor.getValue() > 0:
        is_left = True

    # action for left wall
    if is_left and not is_turning:
        leftMotor.setVelocity(velocity)
        rightMotor.setVelocity(-velocity * 2)
        is_left = False
    # action for right wall
    elif outerRightSensor.getValue() > 3100:
        leftMotor.setVelocity(-velocity * 2)
        rightMotor.setVelocity(velocity)

    # detect the type of maze
    if groundLeftSensor.getValue() < 200:
        is_standard_maze = True

    # look for open paths on the left
    if outerLeftSensor.getValue() == 0 and centralLeftSensor.getValue() == 0 and centralSensor.getValue() == 0:
        count += 1

    # condition to turn left, if there's an open path
    if count > 45:
        is_turning = True

    # action for turning into open path
    if is_turning:
        leftMotor.setVelocity(-velocity * 2)
        rightMotor.setVelocity(velocity)
        # drive forward if there is something on the left
        if outerLeftSensor.getValue() > 0 and centralLeftSensor.getValue() == 0 and centralSensor.getValue() == 0 and centralRightSensor.getValue() == 0 and outerRightSensor.getValue() == 0:
            is_turning = False
            count = 0

    # action for standard maze --> Dots are Black not Brown
    if is_standard_maze and groundRightSensor.getValue() < 200:
        count_black_dots += 1

    # condition for stopping in standard maze
    if count_black_dots > 239:
        is_end = True

    # condition for stopping in own maze
    if groundLeftSensor.getValue() < 500 and groundRightSensor.getValue() < 500 and centralSensor.getValue() > 0:
        is_end = True

    # action for stopping
    if is_end:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)