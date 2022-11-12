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

isSackgasse = False
isMiddleRight = True
isMiddleLeft = True
isEmptyLeft = False

isTurning = False
count = 0
while robot.step(timeStep) != -1:
    # always drive forward
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)
    
    print(outerLeftSensor.getValue(), centralLeftSensor.getValue(), centralSensor.getValue(), centralRightSensor.getValue(), outerRightSensor.getValue())
    
    if centralSensor.getValue() > 0:
        leftMotor.setVelocity(-velocity*2)
        rightMotor.setVelocity(velocity)
    elif outerRightSensor.getValue() > 2500:
        leftMotor.setVelocity(-velocity*2)
        rightMotor.setVelocity(velocity)
    
    if outerLeftSensor.getValue() == 0 and centralLeftSensor.getValue() == 0 and centralSensor.getValue() == 0:
        count += 1
    
    if count > 50:
        isTurning = True

    if isTurning == True:
        print("TUUURNING")
        leftMotor.setVelocity(-velocity*2)
        rightMotor.setVelocity(velocity)
        if outerLeftSensor.getValue() > 0 and centralLeftSensor.getValue() == 0 and centralSensor.getValue() == 0 and centralRightSensor.getValue() == 0 and outerRightSensor.getValue() == 0:
            print("FINSIIICHED")
            isTurning = False
            count = 0
    print(count)
      
    """
    if centralLeftSensor.getValue() > 1000 and outerLeftSensor.getValue() > 0:
        print("SACKGASSE")
        isSackgasse = True

    if isSackgasse == True:
        leftMotor.setVelocity(velocity)
        rightMotor.setVelocity(-velocity*2)
        isSackgasse = False
    # turn left if to narrow to right wall
    if outerRightSensor.getValue() > 2500 and isSackgasse == False:
        print("RECHTS FAHREN")
        isMiddleRight = False
    
    if isMiddleRight == False:
        leftMotor.setVelocity(velocity)
        rightMotor.setVelocity(velocity*2)
        isMiddleRight = True
    
    if outerLeftSensor.getValue() > 4000 and isEmptyLeft == False:
        print("ZU NAH LINKS", isEmptyLeft)
        leftMotor.setVelocity(velocity)
        rightMotor.setVelocity(-velocity*2)
        continue
    # turn for Sackgasse
    

    # turn left if wall ends
    if outerLeftSensor.getValue() == 0 and centralLeftSensor.getValue() == 0:
        print("ABBIEGEN")
        isEmptyLeft = True
    
    if isEmptyLeft == True:
        leftMotor.setVelocity(-velocity/2)
        rightMotor.setVelocity(velocity*2)

    if outerLeftSensor.getValue() > 0 or centralLeftSensor.getValue() > 0:
        isEmptyLeft = False
    
    """