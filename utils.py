import pygame
import math
from const import *

class Utils:
    @staticmethod
    def blit_rotate_center(win, image, top_left, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(
            center=image.get_rect(topleft=top_left).center)
        win.blit(rotated_image, new_rect.topleft)
        
    @staticmethod
    def distanceBetweenTwoPoints(xPointA, yPointA, xPointB, yPointB):
        return math.sqrt((xPointA - xPointB)**2 + (yPointA - yPointB)**2)
    
    @staticmethod
    def findLinePassTwoPoints(xPointA, yPointA, xPointB, yPointB):
        # y = ax + b
        # if (xPointB - xPointA) == 0:
        #     xPointB + 0.0001
        a = (yPointB - yPointA) / (xPointB - xPointA)
        b = yPointA - a * xPointA
        return a, b

    @staticmethod
    def findSolOfEquation(a, b, c):
        # aX^2 + bX + c = 0
        delta = b**2 - 4*a*c
        # print("delta: ", delta)
        if delta < 0:
            return Equation.NO_SOLUTION, 0, 0
        if delta == 0:
            return Equation.ONE_SOLUTION, -b/(2*a), -b/(2*a)
        else:
            return Equation.TWO_SOLUTION, (-b + math.sqrt(delta))/(2*a), (-b - math.sqrt(delta))/(2*a)
    
    @staticmethod
    def getDistanceFromObstacle(xCenter, yCenter, xTarget, yTarget, xObstacle, yObstacle):
        # if abs(xTarget - xCenter) < 0.0001:
            # x = xCenter
            # (xCenter - xObstacle)^2 + (y - yObstacle)^2 = r^2
        # Pt đường thẳng lidar y = ax + b
        a, b = Utils.findLinePassTwoPoints(xCenter, yCenter, xTarget, yTarget)
        # print("42: ", Utils.verifyLine(a, b, xCenter, yCenter))
        # print("41: ", Utils.verifyLine(a, b, xTarget, yTarget))
        # print("y = {}x + {}".format(a, b))
        
        # (x - xObstacle)^2 + (y - yObstacle)^2 = r^2
        # (x - xObstacle)^2 + (a*x + b - yObstacle)^2 = r^2
        # x^2 - 2*x*xObstacle + xObstacle^2 + a^2*x^2 + 2*a*x*(b - yObstacle) + (b - yObstacle)^2 = r^2
        # Pt đường thẳng cắt hình tròn (a^2 + 1)x^2 - 2*(xObstacle - a*b + a*yObstacle)x + (b - yObstacle)**2 + xObstacle**2 - RADIUS_LIDAR**2 = 0
        a_temp = a**2 + 1
        b_temp = -2*xObstacle + 2*a*(b - yObstacle)
        c_temp = (b - yObstacle)**2 + xObstacle**2 - PlayerParam.RADIUS_OBJECT**2
        # print("a_temp = {}, b_temp = {}, c_temp = {}".format(a_temp, b_temp, c_temp))
        numberOfSolution, x1, x2 = Utils.findSolOfEquation(a_temp, b_temp, c_temp)
        
        
        if numberOfSolution == Equation.NO_SOLUTION:
            # print('NO_SOLUTION')
            return PlayerParam.INFINITY
        elif numberOfSolution == Equation.ONE_SOLUTION:
            d = Utils.distanceBetweenTwoPoints(xCenter, yCenter, x1, a*x1 + b)
            # print('ONE_SOLUTION')
            # print("---> ", x1, a*x1 + b)
            return d
        else:
            # print('TWO_SOLUTION')
            d1 = Utils.distanceBetweenTwoPoints(xCenter, yCenter, x1, a*x1 + b)
            d2 = Utils.distanceBetweenTwoPoints(xCenter, yCenter, x2, a*x2 + b)
            # print("---> ", x1, a*x1 + b)
            # print("---> ", x2, a*x2 + b)
            # print(Utils.distanceBetweenTwoPoints(x1, a*x1 + b, x2, a*x2 + b))
            # print('---check---')
            # print(Utils.verifyLine(a, b, x1, a*x1 + b))
            # print(Utils.verifyCircle(xObstacle, yObstacle, PlayerParam.RADIUS_OBJECT, x1, a*x1 + b))
            # print(Utils.verifyLine(a, b, x2, a*x2 + b))
            # print(Utils.verifyCircle(xObstacle, yObstacle, PlayerParam.RADIUS_OBJECT, x2, a*x2 + b))
            # print('---length---')
            # print(d1, d2)
            return d1 if d1 <= d2 else d2
    
    @staticmethod
    def verifyLine(a, b, x, y):
        # y = ax + b
        return a*x + b - y

    @staticmethod
    def verifyCircle(xCenter, yCenter, radius, x, y):
        return (x - xCenter)**2 + (y - yCenter)**2 - radius**2