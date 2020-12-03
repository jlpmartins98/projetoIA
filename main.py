#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


class Pastor:
    def __init__(self,posicao,direcao): 
        self.posicao = posicao
        self.direcao = direcao

paredes = [] #array com as paredes 
ovelhas=0
ev3=EV3Brick()
encontrou_parede = 0
motor_esquerdo = Motor(Port.B)
motor_direito = Motor(Port.C)

obstacle_sensor = UltrasonicSensor(Port.S2)
sensor_toque = TouchSensor(Port.S1)
sensor_cor = ColorSensor(Port.S4)

robot = DriveBase(motor_esquerdo, motor_direito, wheel_diameter = 55.5, axle_track= 104)

informacao = Pastor(1,0)  #Informação sobre o robot

def adiciona_parede():
    x_parede = informacao.posicao
    if(informacao.direcao==0): # Virado para cima
        y_parede = x_parede + 6
    elif(informacao.direcao==90): # Virado para a direita
        y_parede = x_parede + 1
    elif(informacao.direcao==180): # Virado para baixo
        y_parede = x_parede - 6
    elif(informacao.direcao==270): # Virado para a esquerda
        y_parede = x_parede -1

    if(len(paredes)<6):
        paredes.append([x_parede,y_parede])

def ovelhas():    
    while obstacle_sensor.distance() < 300:
        ev3.speaker.beep()
        ovelhas += 1



def andar():
    while(sensor_cor.color()== Color.WHITE):
        robot.drive(100,-1)
    robot.stop()
    
    #ev3.speaker.beep()
    if(sensor_cor.color()==Color.BLACK): #Encontra limite do cacifo
        ev3.speaker.beep()
        robot.straight(150) #Anda até o centro do cacifo adjacente  $$$$$$$$$$$$$$$$$$$$ Verificar valor
        if(informacao.direcao==0):                          #Virado para cima
            informacao.posicao = informacao.posicao + 6
            if(informacao.posicao==7):
                robot.turn(90)
                informacao.direcao = informacao.direcao+90
        elif(informacao.direcao==90):                       #Virado para a direita
            informacao.posicao = informacao.posicao + 1
            if(informacao.posicao==7):
                robot.turn(90)
                informacao.direcao = informacao.direcao+90
        elif(informacao.direcao==180):                      #Virado para baixo
            informacao.posicao = informacao.posicao - 6
            if(informacao.posicao==7):
                robot.turn(90)
                informacao.direcao = informacao.direcao+90
        elif(informacao.direcao==270):                      #Virado para a esquerda
            informacao.posicao = informacao.posicao - 1
            if(informacao.posicao==7):
                robot.turn(90)
                informacao.direcao = informacao.direcao+90
    elif(sensor_cor.color()==Color.RED): #Encontra parede $$$$$$$$$$$$$$$$$$ Verificar cor
        encontrou_parede = 1
        robot.straight(-100) # Retorna ao centro do cacifo de onde saiu
    


def main():
    while 1:
        andar()
        if(sensor_cor.color()==Color.BLUE):
            robot.Stop()   

if (__name__ == "__main__"):
    main() 

            


