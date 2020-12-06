#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random


class Pastor:
    def __init__(self,posicao,direcao): 
        self.posicao = posicao
        self.direcao = direcao


paredes = [] #array com as paredes 
ev3=EV3Brick()
encontrou_parede = 0
batatadas_totais = 0
precionado = 0
motor_esquerdo = Motor(Port.A)
motor_direito = Motor(Port.C)
motor_braco = Motor(Port.B,Direction.COUNTERCLOCKWISE)
toque = TouchSensor(Port.S1)
#fala = SoundFile()
#cima = 0
#direita = 90
#baixo = 180
#esquerda = 270
obstacle_sensor = UltrasonicSensor(Port.S2)
sensor_toque = TouchSensor(Port.S1)
sensor_cor = ColorSensor(Port.S4)

  

robot = DriveBase(motor_esquerdo, motor_direito, wheel_diameter = 55.5, axle_track= 104)

informacao = Pastor(1,0)  #Informação sobre o robot

def adiciona_parede():
    #ev3.speaker.beep()
    x_parede = informacao.posicao
    y_parede = 0
    if(informacao.direcao==0): # Virado para cima
        y_parede = x_parede + 6
    elif(informacao.direcao==270): # Virado para a direita
        y_parede = x_parede + 1
    elif(informacao.direcao==180): # Virado para baixo
        y_parede = x_parede - 6
    elif(informacao.direcao==90): # Virado para a esquerda
        y_parede = x_parede -1

    if(len(paredes)<6):
        paredes.append([x_parede,y_parede])
        #ev3.screen.print("adicionou parede X: " + x_parede + " e Y: " + y_parede)

def ovelhas():#quando encontra ovelhas
    #encontrar maneira de ele saber quando gritar e quando dar porrada
    global batatadas_totais
    n_random = 0
    global precionado
    #ev3.speaker.beep()
    if(obstacle_sensor.distance() < 200):#verificar distancia
        #ev3.speaker.beep()
        #robot.stop()
        if(n_random == 0): #bate na ovelha
            if (precionado == 0):
                motor_braco.run_target(10000, -360)
                if(toque.pressed()):
                    precionado = 1
                #motor_braco.run(-200)
            else:
                #ev3.speaker.beep()
                motor_braco.run_target(400,90)
                batatadas_totais += 1
                #motor_braco.stop()
        elif(n_random == 1): #berra com a ovelha
            ev3.speaker.beep()
            #ev3.speaker.beep()


def vira(graus):
    #while(informacao.direcao != graus):   #enquanto a direção não for a pretendida
     #   if(informacao.direcao > graus):      #Roda uma vez para a esquerda
      #      informacao.direcao = informacao.direcao -90
       #     robot.turn(-90)
        #elif(informacao.direcao > graus):   #Roda uma vez para a direita
         #   informacao.direcao = informacao.direcao +90
          #  robot.turn(90)
    robot.turn(graus)
    robot.turn(20)
    informacao.direcao = informacao.direcao + graus
    #ev3.speaker.beep()
    informacao.direcao = int (informacao.direcao % 360)

def pode_avancar():
    #ev3.speaker.beep()
    if(informacao.direcao ==0): #Se estiver virado para cima
        if(informacao.posicao >30): # E na linha de cima 
            return False #não pode avançar
        else:
            return True #caso contrario avança
    elif(informacao.direcao==270): #Se estiver virado para a direita
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
    elif(informacao.direcao==270):                       #Virado para a direita
        informacao.posicao = informacao.posicao + 1            
    elif(informacao.direcao==180):                      #Virado para baixo
        informacao.posicao = informacao.posicao - 6            
    elif(informacao.direcao==90):                      #Virado para a esquerda
        informacao.posicao = informacao.posicao - 1
    
    

def andar():
    while(sensor_cor.color()== Color.WHITE):
        robot.drive(75,-1)
    robot.stop() #quando deixa de ver branco para de andar
    #wait(10)
    if(sensor_cor.color()==Color.BLACK): #Encontra limite do cacifo
        #ovelhas()
        #ev3.speaker.beep()
        teste = pode_avancar()
        if(teste):
            robot.straight(200) #Anda até o centro do cacifo adjacente
            atualiza_posicao()
        else:
            robot.straight(-50) # Volta para trás
            vira(270) #Roda para a esquerda               
    elif(sensor_cor.color()==Color.RED): #Encontra parede        
        adiciona_parede()
        ev3.speaker.beep()
        robot.straight(-50)
        vira(270)
        
    


def main():
    while True:
        #andar()
        ovelhas()
        #ev3.speaker.beep()
        #if(informacao.posicao==36 or sensor_cor.color() == Color.BLUE):
        #    robot.Stop()
        #ev3.screen.print("cacifo atual: " + informacao.posicao)

if (__name__ == "__main__"):
    main() 

            


