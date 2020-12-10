#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint


class Pastor:
    def __init__(self,posicao,direcao): 
        self.posicao = posicao #quadrado em que se encontra
        self.direcao = direcao #lado para o qual esta virado (0 graus é para cima)


paredes = [] #array com as paredes 
ev3=EV3Brick()
precionado = 0
encontrou_parede = 0
batatadas_totais = 0
motor_esquerdo = Motor(Port.A)
motor_direito = Motor(Port.C)
motor_braco = Motor(Port.B,Direction.COUNTERCLOCKWISE)
toque = TouchSensor(Port.S1)
i = 0
#fala = SoundFile()
#cima = 0
#direita = 90
#baixo = 180
#esquerda = 270
obstacle_sensor = UltrasonicSensor(Port.S2)
sensor_toque = TouchSensor(Port.S1)
sensor_cor = ColorSensor(Port.S4)
graus=[90,180,270]
lugares_visitados = []

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

    if(([x_parede, y_parede] not in paredes)):#verifica se essa parede ja se encontra no array (pode ter as duas posiçoes em que encontra a parede)
        paredes.append([x_parede,y_parede])
        

def pode_avancar_parede():
    #percorrer o array das paredes para ver
    #ver se a posicao atual é y_parede x_parede
    #e devolver se tem parede adjacente ou seja se pode avancar ou nao
    for k in paredes: #percorre o array das paredes
        if(k[0] == informacao.posicao):
            if(informacao.posicao + 6 == k[1]):#caso a parede esteja para cima
                if(informacao.direcao == 0):#virado para cima
                    return False
                else:
                    return True
            elif(informacao.posicao + 1 == k[1]):#caso a parede esteja para a direita
                if(informacao.direcao == 270): #virado para a direita
                    return False
                else:
                    return True
            elif(informacao.posicao - 6 == k[1]):#caso a parede esteja para baixo
                if(informacao.direcao == 180):#virado para baixo
                    return False
                else:
                    return True
            elif(informacao.posicao - 1 == k[1]):#caso a parede esteja para a esquerda
                if(informacao.direcao == 90): #virado para a esquerda
                    return False
                else:
                    return True
        elif(k[1] == informacao.posicao):
            if(informacao.posicao + 6 == k[0]):#caso a parede esteja para cima
                if(informacao.direcao == 0):#virado para cima
                    return False
                else:
                    return True
            elif(informacao.posicao + 1 == k[0]):#caso a parede esteja para a direita
                if(informacao.direcao == 270): #virado para a direita
                    return False
                else:
                    return True
            elif(informacao.posicao - 6 == k[0]):#caso a parede esteja para baixo
                if(informacao.direcao == 180):#virado para baixo
                    return False
                else:
                    return True
            elif(informacao.posicao - 1 == k[0]):#caso a parede esteja para a esquerda
                if(informacao.direcao == 90): #virado para a esquerda
                    return False
                else:
                    return True
    return True


def ovelhas():#quando encontra ovelhas
    #encontrar maneira de ele saber quando gritar e quando dar porrada
    global batatadas_totais #total de vezes que ja bateu nas ovelhas
    aleatorio = randint(0,2)
    global precionado 
    #ev3.speaker.beep()
    if(obstacle_sensor.distance() < 200):#verificar distancia
        if(aleatorio == 0): #bate na ovelha
            while(precionado == 0):
                wait(1000)
                motor_braco.track_target(-1500)
                if(toque.pressed()):
                    precionado = 1
                    motor_braco.stop()
                    batatadas_totais += 1
            motor_braco.run_target(400,10)
            precionado=0
        elif(aleatorio == 1): #ladra com a ovelha
            ev3.speaker.play_file(SoundFile.DOG_BARK_2)
        wait(3000)


def vira(graus): #vira o robo pelos graus inseridos (sentido contrahorario)
    robot.turn(graus)
    if(graus == 270): #para endireitar o robo como ele nunca vira direito
        robot.turn(20)
    elif(graus == 180):#para endireitar o robo como ele nunca vira direito
        robot.turn(10)
    elif(graus == 90):#para endireitar o robo como ele nunca vira direito
        robot.turn(5)
    informacao.direcao = informacao.direcao + graus #atualiza a direçao do robo
    informacao.direcao = int (informacao.direcao % 360) #da o resto da divisao inteira da sua direçao por 360 para os graus nunca ultrapassarem 360

def pode_avancar():
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
    global graus #array com os graus que pode virar
    global i #serve para guardar quantas extremidades do quadrado ja verificou
    aleatorio = randint(0,2)
    virar=graus[aleatorio] #seliciona aleatoriamente se vai virar 90;180 ou 270 graus
    while(sensor_cor.color()== Color.WHITE):
        robot.drive(75,-1)
    robot.stop() #quando deixa de ver branco para de andar
    if(sensor_cor.color()==Color.BLACK): #Encontra limite do cacifo
        ovelhas()
        if(obstacle_sensor.distance() < 200):#verificar distancia
            robot.turn(90)
        robot.straight(-50)
        vira(90)
        i+=1
        if(i >= 4): #quando ja verificou todos os lados do quadrado
            vira(virar) #depois de ver as quatros paredes vira para um lado random
            if(pode_avancar() and pode_avancar_parede()):
                robot.straight(200) #Anda até o centro do cacifo adjacente
                atualiza_posicao()
                i = 0
            elif(pode_avancar() == False):
                #robot.straight(-50) # Volta para trás
                ev3.speaker.beep() 
                vira(virar) #Roda para aleatorio              
    elif(sensor_cor.color()==Color.RED): #Encontra parede
        ovelhas()
        if(obstacle_sensor.distance() < 200):#verificar distancia
            robot.turn(90)      
        adiciona_parede()
        ev3.speaker.beep()
        robot.straight(-50)
        i += 1
        vira(90)
        
def main():
    while True:
        andar()
        #ev3.speaker.beep()
        if(sensor_cor.color() == Color.BLUE):
            robot.Stop()

if (__name__ == "__main__"):
    main() 

            


