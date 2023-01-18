import math
import turtle

def inputData():
    velocity = float(input("Input a velocity (m/s): "))
    angle = float(input("Input an angle (degrees): "))
    angle = math.radians(angle)
    distance = float(input("Input the horizontal distance to the wall (m): "))
    height = float(input("Input the height of the wall (m): "))
    return velocity, angle, distance, height


def calcProjectileMotion(velocity, angle, distance, height):
    Time = round(((2*velocity*math.sin(angle))/9.8), 2)
    targetArea = distance + round(height*2, 2)
    DistanceTraveled = round((velocity**2 *math.sin(2*angle))/9.8, 2)
    maxHeight = round((velocity**2 * math.sin(angle)**2)/(2*9.8), 2)

    if (DistanceTraveled > distance) and (maxHeight > height) and (DistanceTraveled < targetArea):
        HitTarget = 0
    if (DistanceTraveled < distance) or (maxHeight < height):
        HitTarget = -1
    elif (DistanceTraveled > targetArea):
        HitTarget = 1

    results = {"Time": Time, "DistanceTraveled": DistanceTraveled, "HitTarget": HitTarget}
    return results


def outputResults(results):
    print("The total flight time of the projectile was " + str(results["Time"]) + " seconds")
    print("The total distance the projectile traveled was " + str(results["DistanceTraveled"]) + " meters")
    if str(results["HitTarget"]) == "0":
        print("The projectile hit the target area!")
    if str(results["HitTarget"]) == "-1":
        print("The projectile fell short of the target area!")
    if str(results["HitTarget"]) == "1":
        print("The projectile flew past the target area!")


def drawProjectile(velocity, angle, distance, height):
    wn = turtle.Screen()
    wn.bgcolor("white")
    wn.title("Catapult Simulation")

    #Drawing the ground
    ground = turtle.Turtle()
    ground.speed(100)
    ground.hideturtle()
    ground.penup()
    ground.goto(-600, -300)
    ground.showturtle()
    ground.pendown()
    ground.color("Green")
    ground.fillcolor("Green")
    ground.pensize(1)
    ground.begin_fill()
    for i in range(4):
        ground.forward(1500)
        ground.right(90)
    ground.end_fill()

    #Drawing the structure
    structure = turtle.Turtle()
    structure.pensize(5)
    structure.penup()
    structure.speed(100)
    structure.hideturtle()
    structure.goto((-100 + distance*5), -300)
    structure.pendown()
    structure.color("Grey")
    structure.left(90)
    structure.forward(height*5)
    structure.right(90)
    structure.forward(5)
    structure.right(90)
    structure.forward(height*5)

    #Drawing the target area
    target = turtle.Turtle()
    target.pensize(1)
    target.penup()
    target.speed(100)
    target.hideturtle()
    target.goto((-100 + distance*5 + 5), -300)
    target.pendown()
    target.color("Red")
    target.fillcolor("Red")
    target.begin_fill()
    for i in range(4):
        target.forward(height*2*5 - 5)
        target.right(90)
    target.end_fill()

    #Drawing the path of the projectile
    path = turtle.Turtle()
    path.hideturtle()
    path.penup()
    path.pensize(5)
    path.goto(-100, -300)
    path.pendown()
    path.speed(70)
    path.color("Black")
    t = 0
    tinterval = .01
    g = 9.8
    Time = round(((2*velocity*math.sin(angle))/9.8), 2)
    timeAtWall = round(distance/(velocity*math.cos(angle)), 2)
    heightAtWall = round(((velocity*math.sin(angle)*timeAtWall) - (0.5*g*timeAtWall**2)), 2)
    maxHeight = round((velocity**2 * math.sin(angle)**2)/(2*9.8), 2)
    while t<(Time-0.03):
        t = round(t+tinterval, 2)
        x = -100 + (velocity*t*math.cos(angle)*5)
        y = -300 + ((velocity*math.sin(angle)*t) - (0.5*g*t**2))*5
        if t == timeAtWall:
            if y < (height*5-300):
                break
        path.goto(x,y)

    wn.mainloop()



if __name__ == "__main__":
    velocity, angle, distance, height = inputData()
    results = calcProjectileMotion(velocity, angle, distance, height)
    outputResults(results)
    drawProjectile(velocity, angle, distance, height)

