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
isLeft = False
isTurning = False
isEnd = False
isStandardMaze = False
count = 0
count_black_dots = 0
t0 = time.time()
while robot.step(timeStep) != -1:
    # always drive forward
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)
    running_time = time.time() - t0
    print(groundLeftSensor.getValue())
    print(outerLeftSensor.getValue(), centralLeftSensor.getValue(), centralSensor.getValue(), centralRightSensor.getValue(), outerRightSensor.getValue())
    if centralSensor.getValue() > 0 or outerLeftSensor.getValue() > 0 or centralLeftSensor.getValue() > 0:
        isLeft = True
    print("isLeft", isLeft)
    print("Is Maze: ", isStandardMaze)
   
    if isLeft == True and isTurning == False:        
        leftMotor.setVelocity(velocity)
        rightMotor.setVelocity(-velocity*2)
        isLeft = False

    elif outerRightSensor.getValue() > 3100:
        print("RIGHT")
        leftMotor.setVelocity(-velocity*2)
        rightMotor.setVelocity(velocity)
    
    if groundLeftSensor.getValue() < 200:
        isStandardMaze = True
    
    if outerLeftSensor.getValue() == 0 and centralLeftSensor.getValue() == 0 and centralSensor.getValue() == 0:
        count += 1

    if count > 45:
        isTurning = True
    
    print("isTurning", isTurning)

    if isTurning == True:
        leftMotor.setVelocity(-velocity*2)
        rightMotor.setVelocity(velocity)
        if outerLeftSensor.getValue() > 0 and centralLeftSensor.getValue() == 0 and centralSensor.getValue() == 0 and centralRightSensor.getValue() == 0 and outerRightSensor.getValue() == 0:
            isTurning = False
            count = 0
    
    if isStandardMaze == True and groundRightSensor.getValue() < 200:
        count_black_dots += 1
        
    if count_black_dots > 239:
        isEnd = True
    
    if groundLeftSensor.getValue() < 500 and groundRightSensor.getValue() < 500 and centralSensor.getValue() > 0:
        isEnd = True
    
    if isEnd == True:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
    print(count_black_dots)

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