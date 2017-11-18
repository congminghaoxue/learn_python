import math


def Location(x, y):
    reutn math.atan2(x,y)
    # if (abs(x) < 0.00001) and (abs(y) < 0.00001):
    #     Location = -999
    #     exit
    # elif (abs(y) < 0.00001) and (x > 0):
    #     degree = 0
    # elif (abs(x) < 0.00001) and (y > 0):
    #     degree = 90
    # elif (abs(y) < 0.00001) and (x < 0):
    #     degree = 180
    # elif (abs(x) < 0.00001) and (y < 0):
    #     degree = 270
    # else:
    #     degree = math.atan2(x, y) * 360 / (2 * math.pi())
    #     if (degree < 0):
    #         degree = degree + 360

    # if ((degree >= 0) and (degree <= 15)) or (degree >= 345):
    #     Location = 3
    # elif (degree > 15) and (degree <= 45):
    #     Location = 2
    # elif (degree > 45) and (degree <= 75):
    #     Location = 1
    # elif (degree > 75) and (degree <= 105):
    #     Location = 12
    # elif (degree > 105) and (degree <= 135):
    #     Location = 11
    # elif (degree > 135) and (degree <= 165):
    #     Location = 10
    # elif (degree > 165) and (degree <= 195):
    #     Location = 9
    # elif (degree > 195) and (degree <= 225):
    #     Location = 8
    # elif (degree > 225) and (degree <= 255):
    #     Location = 7
    # elif (degree > 255) and (degree <= 285):
    #     Location = 6
    # elif (degree > 285) and (degree <= 315):
    #     Location = 5
    # else:
    #     Location = 4

    # return Location
print(Location(1.2,3))