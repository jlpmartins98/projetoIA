#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Sound
import random


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
motor_braco = Motor(Port.D)
toque = TouchSensor(Port.S1)
fala = Sound()
#cima = 0
#direita = 90
#baixo = 180
#esquerda = 270
obstacle_sensor = UltrasonicSensor(Port.S2)
sensor_toque = TouchSensor(Port.S1)
sensor_cor = ColorSensor(Port.S4)

n_random = random.randint(0,1)  

robot = DriveBase(motor_esquerdo, motor_direito, wheel_diameter = 55.5, axle_track= 104)

informacao = Pastor(1,0)  #Informação sobre o robot

def adiciona_parede():
    x_parede = informacao.posicao
    y_parede = 0
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

def ovelhas():#quando encontra ovelhas
    #encontrar maneira de ele saber quando gritar e quando dar porrada
    toque = 0
    if(obstacle_sensor.distance() < 200):#verificar distancia
        robot.stop()
        if(n_random == 0):
            motor_braco.drive(75,0)
            if(toque.pressed()):
                toque += 1
                return toque #ver como depois guardar as batatas q deu nas ovelhas
        elif(n_random == 1):
            fala.speak("SHEEP")

def vira(graus):
    #while(informacao.direcao != graus):   #enquanto a direção não for a pretendida
     #   if(informacao.direcao > graus):      #Roda uma vez para a esquerda
      #      informacao.direcao = informacao.direcao -90
       #     robot.turn(-90)
        #elif(informacao.direcao > graus):   #Roda uma vez para a direita
         #   informacao.direcao = informacao.direcao +90
          #  robot.turn(90)
    robot.turn(graus)
    informacao.direcao = informacao.direcao + graus
    informacao.direcao = informacao.direcao % 360

def pode_avancar():
    if(informacao.direcao ==0): #Se estiver virado para cima
        if(informacao.posicao >=30): # E na linha de cima 
            return False #não pode avançar
        else:
            return True #caso contrario avança
    elif(informacao.direcao==90): #Se estiver virado para a direita
        if(informacao.posicao %6 ==0): #e na coluna da direita
            return False #não pode avançar
        else:
            return True #caso contrario avança
    elif(informacao.direcao ==180): #Se estiver virado para baixo
        if(informacao.posicao<7): # e na linha de baixo
            return False #não pode avançar
        else:
            return True #caso contrario avança
    else:                       #Se estiver virado para a esquerda
        if(informacao.posicao %6 ==1):  # e na coluna da esquerda
            return False #não pode avançar
        else:
            return True #caso contrario avança

def atualiza_posicao():
    if(informacao.direcao==0):                          #Virado para cima
        informacao.posicao = informacao.posicao + 6            
    elif(informacao.direcao==90):                       #Virado para a direita
        informacao.posicao = informacao.posicao + 1            
    elif(informacao.direcao==180):                      #Virado para baixo
        informacao.posicao = informacao.posicao - 6            
    elif(informacao.direcao==270):                      #Virado para a esquerda
        informacao.posicao = informacao.posicao - 1

def andar():
    while(sensor_cor.color()== Color.WHITE):
        robot.drive(100,-1)
    robot.stop()
    if(sensor_cor.color()==Color.BLACK): #Encontra limite do cacifo
        ovelhas()
        #ev3.speaker.beep()
        if(pode_avancar()):
            robot.straight(150) #Anda até o centro do cacifo adjacente
            atualiza_posicao()
        else:
            robot.straight(-50) # Volta para trás
            vira(270) #Roda para a esquerda               
    elif(sensor_cor.color()==Color.RED): #Encontra parede 
        ovelhas()
        adiciona_parede()
        robot.straight(-50)
        vira(270)
        
    


def main():
    while 1:
        motor_braco.hold()
        andar()
        if(sensor_cor.color()==Color.BLUE):
            robot.Stop()
         

if (__name__ == "__main__"):
    main() 

            


