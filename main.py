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

class cacifo:
    def __init__(self,numeroCacifo,distanciaObjetivo,paredeUp,paredeDown,paredeRight,paredeLeft):
        self.numeroCacifo = numeroCacifo #o numero do quadrado (para o robo saber a posiçao)
        self.distanciaOjetivo = distanciaObjetivo #a heuristica, distancia até a cerca/ovelha
        #self.custoCaminho = custoCaminho
        self.paredeUp = False
        self.paredeDown = False
        self.paredeRight = False
        self.paredeLeft = False

array_pode_avancar = []
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
obstacle_sensor = UltrasonicSensor(Port.S2)
sensor_toque = TouchSensor(Port.S1)
sensor_cor = ColorSensor(Port.S4)
graus=[90,180,270]
lugares_visitados = []
cacifos_visitados = [1]
cacifos_prioritarios = []
posicao_ovelhas = []

robot = DriveBase(motor_esquerdo, motor_direito, wheel_diameter = 55.5, axle_track= 104)

informacao = Pastor(1,0)  #Informação sobre o robot
arrayCacifos_com_heuristica = [] #array que guarda os cacifos com o seu numero e heuristica ate á cerca

def guarda_posicao_ovelha():
    k = informacao.posicao
    if(informacao.direcao == 0):#se a ovelha estiver acima do robo
        k += 6
    if(informacao.direcao == 90):#se a ovelha estiver a esquerda 
        k -= 1
    if(informacao.direcao == 180):#se a ovelha estiver abaixo
        k -= 6
    if(informacao.posicao == 270):#se a ovelha estiver a direita
        k += 1
    if(k not in posicao_ovelhas):
        posicao_ovelhas.append(k)

def inicializaCacifos():#funcao que da os valores da heuristica e custo do caminho a todos os cacifos (antes de encontrar paredes/ovelhas)
    k = 10 #k é a heuristica do cacifo até a cerca
    for j in range(1,37):#j é o numero do cacifo
        if(j==7):
            k=9
        if(j==13):
            k=8
        if(j==19):
            k=7
        if(j==25):
            k=6
        if(j==31):
            k=5
        CacifoClasse = cacifo(j,k,False,False,False,False)
        arrayCacifos_com_heuristica.append(CacifoClasse)
        k-=1

def adiciona_parede():
    #x_parede = informacao.posicao
    #y_parede = 0
    for j in arrayCacifos_com_heuristica: #percorre cada elemento da classe cacifo do array
        if(j.numeroCacifo == informacao.posicao): #quando encontra o cacifo atual 
            if(informacao.direcao==0): # Virado para cima
                #y_parede = x_parede + 6
                j.paredeUp = True
            elif(informacao.direcao==270): # Virado para a direita
                #y_parede = x_parede + 1
                j.paredeRight = True
            elif(informacao.direcao==180): # Virado para baixo
                #y_parede = x_parede - 6
                j.paredeDown = True
            elif(informacao.direcao==90): # Virado para a esquerda
                #y_parede = x_parede -1
                j.paredeLeft = True
            #if(([x_parede, y_parede] not in paredes)):#verifica se essa parede ja se encontra no array (pode ter as duas posiçoes em que encontra a parede)
                #paredes.append([x_parede,y_parede])
                #return True
            #elif(([x_parede, y_parede] in paredes)):
                #return False
        

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
#adiciona o cacifo, ao array cacifos visitados 
def adiciona_visitados(pos):
    visitado = procura_visitado(pos) #procura se já está no array
    if(visitado == False):
        cacifos_visitados.append(pos)
    print(cacifos_visitados)

#percorre o array dos visitados 
def procura_visitado(t):
    for j in cacifos_visitados:
        if (j==t): #e ve se o cacifo já está lá 
            return True
    return False


def verifica_cacifo():
    global i
    global array_pode_avancar#Array que guarda as direções que o robot pode ir
    global cacifos_prioritarios
    while(sensor_cor.color()==Color.WHITE): #Avança até ao limite do cacifo
        robot.drive(75,-1)
    robot.stop()
    if(sensor_cor.color()==Color.RED):  #Encontrou parede
        ovelhas()
        adiciona_parede()
        ev3.speaker.beep()          #Adiciona parede ao array
        robot.straight(-50)     #Volta para trás
        i +=1                   #Atualiza o i
        vira(90)
    elif(sensor_cor.color()==Color.BLACK): #Encontrou limite do cacifo
        ovelhas()
        if(obstacle_sensor.distance() < 200):#verificar distancia
            vira(90)
        robot.straight(-50)     #Volta para trás
        teste_pode_avancar = pode_avancar() #Verifica se pode avançar(Se não é limite do tabuleiro)
        i+=1                    #Atualiza o i
        if(teste_pode_avancar == True): #Caso possa avançar nessa direção
            array_pode_avancar.append(informacao.direcao) #Adiciona essa direção ao array
        vira(90)
    if(i>=4):       #Já verificou todos os lados do cacifo
        escolhe_prioridade(array_pode_avancar) #Dos arrays possíveis procura um que não foi visitado
        opcoes_prioridade = len(cacifos_prioritarios)       #Obtem tamanho do array prioritario
        print(cacifos_prioritarios)
        print(array_pode_avancar)
        if(opcoes_prioridade > 0):                  #Se existir algum com prioridade
            op_prio = opcoes_prioridade -1        
            if(op_prio>0):
                aleatorio_prio = randint(0,op_prio)   #Escolhe um aleatóriamente
                direcao_prioridade = cacifos_prioritarios[aleatorio_prio]       
                coloca_direcao(direcao_prioridade)
            else: 
                coloca_direcao(cacifos_prioritarios[0])
        else:      
            opcoes = len(array_pode_avancar) - 1 # numero de opcoes disponiveis
            if(opcoes >0):
                aleatorio = randint(0,opcoes) #Escolhe uma aleatoriamente
                direcao = array_pode_avancar[aleatorio]
                coloca_direcao(direcao) #coloca o robot nesse direção
            else:
                coloca_direcao(array_pode_avancar[0])
        robot.straight(200) #Avança até o próximo cacifo
        adiciona_visitados(informacao.posicao)
        atualiza_posicao() 
        i= 0 #Reseta o contador
        array_pode_avancar = [] #Limpa o array
        cacifos_prioritarios = [] # Limpa prioritários

#muda a direcao
def coloca_direcao(direcao):
    while(informacao.direcao != direcao):   # Roda para a esquerda até a direção ser a pretendida
        vira(90)

#escolhe qual cacifo ir 
def escolhe_prioridade(lista):
    for k in lista:
        if (k== 0):
            if(procura_visitado(informacao.posicao + 6)==False): #verifica o cacifo de cima
                cacifos_prioritarios.append(k)
        if (k== 90):
            if(procura_visitado(informacao.posicao - 1)==False): #verifica o cacifo da esquerda
                cacifos_prioritarios.append(k)          
        if (k== 180):
            if(procura_visitado(informacao.posicao - 6)==False): #verifica o cacifo de baixo
                cacifos_prioritarios.append(k)
        if (k== 270):
            if(procura_visitado(informacao.posicao + 1)==False): #verifica o cacifo da direita
                cacifos_prioritarios.append(k)


def ovelhas():#quando encontra ovelhas
    #encontrar maneira de ele saber quando gritar e quando dar porrada
    global batatadas_totais #total de vezes que ja bateu nas ovelhas
    aleatorio = randint(0,2)
    global precionado 
    #ev3.speaker.beep()
    if(obstacle_sensor.distance() < 200):#verificar distancia
        if(len(posicao_ovelhas) != 2): #se ainda nao tiver encontrado as duas ovelhas guarda a posiçao da q encontrou
            guarda_posicao_ovelha()
        else:
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
            vira(90)
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
        verifica_cacifo()
        #if(sensor_cor.color() == Color.BLUE):
            #robot.Stop()

if (__name__ == "__main__"):
    main() 

            


