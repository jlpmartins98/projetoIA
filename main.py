#!/usr/bin/env pybricks-micropython
from os import close
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from random import randint
import copy as cp #preciso para fazer o algoritmo sena o python altera a variave global

class Pastor:
    def __init__(self,posicao,direcao): 
        self.posicao = posicao #quadrado em que se encontra
        self.direcao = direcao #lado para o qual esta virado (0 graus é para cima)

class cacifo:
    def __init__(self,parentCacifo,numeroCacifo,distanciaObjetivo,custoCaminho,custoTotal):
        self.numeroCacifo = numeroCacifo #o numero do quadrado (para o robo saber a posiçao)
        self.distanciaOjetivo = distanciaObjetivo #a heuristica, distancia até a cerca/ovelha
        self.custoCaminho = custoCaminho #o G na funçao do A*
        self.custoTotal = custoTotal #O f na funçao do A*
        self.paredeUp = False
        self.paredeDown = False
        self.paredeRight = False
        self.paredeLeft = False
        self.parentCacifo = parentCacifo #de onde veio (so é usado no A*)
        self.movementDebuff = 0         #custo adicional qd encontra uma parede(para n ir para elas)


array_pode_avancar = []
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
arrayCacifos_com_heuristica = [cacifo(None,1,10,0,11)] #array que guarda os cacifos com o seu numero e heuristica ate á cerca

def guarda_posicao_ovelha():
    if(len(posicao_ovelhas) != 2):
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
    k = 9 #k é a heuristica do cacifo até a cerca
    for j in range(2,37):#j é o numero do cacifo
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
        CacifoClasse = cacifo(None,j,k,0,k)
        arrayCacifos_com_heuristica.append(CacifoClasse)
        k-=1

def CacifoAtual(numero_cacifo):
    cacifoFiller = cacifo(None,100,100,200,300) #caso esteja a procura dum cacifo fora do tabuleiro
    for j in arrayCacifos_com_heuristica:
        if(j.numeroCacifo == numero_cacifo):
            return j
    return cacifoFiller #quando procura algo fora dos limites do tabuleiro

def algoritmo_A_star(goal):#devolve um array com o caminho(nº dos cacifos a seguir começando na sua posiçao)
    global arrayCacifos_com_heuristica
    arrayBackup = cp.deepcopy(arrayCacifos_com_heuristica) #faz uma copia da variavel
    openList = []       #cacifos que nao verificou
    closedList = []     #cacifos que ja verificou 
    inicio = CacifoAtual(informacao.posicao)
    inicio.custoTotal = 0 #isto modifica a varivel global mas pq?
    openList.append(inicio)
    while(len(openList) > 0):
        #vai buscar o cacifo atual
        arrayCacifos_com_heuristica = cp.deepcopy(arrayBackup)#restora o array ao estado original para nao criar parentNodes infinitos
        currentNode:cacifo = openList[0]
        currentIndex = 0
        for index, item in enumerate(openList): #item é o elemento atual da lista; index é o index do elemento atual
            if(item.custoTotal < currentNode.custoTotal): #caso exista um cacifo mais barato do que o currentNode
                currentNode = item
                currentIndex = index
        #tira o cacifo verificado da openList e mete na lista dos que ja verificou
        openList.pop(currentIndex)
        closedList.append(currentNode)
        #mudar o current node para o mais barato 
        if(currentNode.numeroCacifo == goal): #caso chegue ao objetivo
            path = []
            current = currentNode
            while(current is not None):#ciclo para guardar o caminho, vai percorrendo os pais dos nos ate chegar ao inicio
                path.append(current.numeroCacifo)
                current = current.parentCacifo
            return path[::-1] #devolve o caminho ao contrario (ou seja na ordem começando onde ele esta)
        #caso esteja num dos limites
        children =[]
        childUp = CacifoAtual(37)
        childDown = CacifoAtual(37)
        childLeft = CacifoAtual(37)
        childRight = CacifoAtual(37)
        #gera os cacifos adjacentes 
        if(currentNode.numeroCacifo < 30):
            childUp = CacifoAtual(currentNode.numeroCacifo + 6) #abre o cacifo em cima do currentNode
            childUp.parentCacifo = currentNode
        if(currentNode.numeroCacifo > 6):
            childDown = CacifoAtual(currentNode.numeroCacifo - 6) #abre o cacifo abaixo do currentNode
            childDown.parentCacifo = currentNode
        if(currentNode.numeroCacifo not in [31,25,19,13,7,1]):
            childLeft = CacifoAtual(currentNode.numeroCacifo - 1) #abre o cacifo a esquerda
            childLeft.parentCacifo = currentNode
        if(currentNode.numeroCacifo not in [36,30,24,18,12,6]):
            childRight = CacifoAtual(currentNode.numeroCacifo + 1) #abre o cacifo a direita
            childRight.parentCacifo = currentNode
        #verificaçoes para saber se tem paredes a volta/esta nos limites do tabuleiro
        if(currentNode.paredeUp == True or currentNode.numeroCacifo > 30):#caso tenha uma parede em cima ou esteja nos cacifos do topo
            childUp.movementDebuff += 100
        if(currentNode.paredeDown == True or currentNode.numeroCacifo < 7):#caso parede em baixo ou esteja na primeira linha de cacifos
            childDown.movementDebuff += 100
        if(currentNode.paredeLeft == True or currentNode.numeroCacifo in [31,25,19,13,7,1]):#caso parede a esquerda ou esteja nos cacifos mais a esquerda
            childLeft.movementDebuff += 100
        if(currentNode.paredeRight == True or currentNode.numeroCacifo in [36,30,24,18,12,6]):#caso parede a direita ou esteja nos cacifos mais a direta
            childRight.movementDebuff += 100
        children.append(childUp)
        children.append(childDown)
        children.append(childLeft)
        children.append(childRight)
        for child in children:
            if(child in closedList):#se ja verificou este child
                continue
            child.custoCaminho = currentNode.custoCaminho + 1 #custa sempre 1 para andar para qq um dos child pois sao os cacifos adajacentes
            child.custoTotal = child.custoCaminho + child.distanciaOjetivo + child.movementDebuff #custo total para chegar a este cacifo
            if(child in openList):#caso nao tenha verificado este child
                var =  openList.index(child)
                if(child.custoCaminho >= openList[var].custoCaminho):#verifica se o custoCaminho do child atual é maior do que o proximo elemento na openList (ou seja se é o mais barato) se nao for passa po proximo
                    continue
            #adiciona a child á lista dos nao verificados
            openList.append(child)



def adiciona_parede():
    j=0
    while(j != len(arrayCacifos_com_heuristica)):
        if(arrayCacifos_com_heuristica[j].numeroCacifo == informacao.posicao):
            if(informacao.direcao==0): # Virado para cima
                #guarda que este cacifo tem uma parede em cima
                arrayCacifos_com_heuristica[j].paredeUp = True
                #colocamos a parede do cacifo acima 
                if(arrayCacifos_com_heuristica[j].numeroCacifo < 31):
                    #guarda que o cacifo de cima do atual tem uma parede em baixo
                    arrayCacifos_com_heuristica[j+6].paredeDown = True

            elif(informacao.direcao==270): # Virado para a direita
                #guarda que este cacifo tem uma parede a dirieta
                arrayCacifos_com_heuristica[j].paredeRight = True
                #colocamos a parede do cacifo a sua direita
                if(arrayCacifos_com_heuristica[j].numeroCacifo not in [36,30,24,18,12,6]): #caso nao esteja nos limites do mapa a direita
                    #guarda que o cacifo a direita do atual tem uma parde a sua esquerda
                    arrayCacifos_com_heuristica[j+1].paredeLeft = True

            elif(informacao.direcao==180): # Virado para baixo
                #guarda que este cacifo tem uma parede em baixo
                arrayCacifos_com_heuristica[j].paredeDown = True
                #colocamos a parede no cacifo abaixo
                if(arrayCacifos_com_heuristica[j].numeroCacifo > 6): #caso nao esteja nos limites do mapa em baixo
                    #guarda que o cacifo a abaixo do atual tem uma parede em cima
                    arrayCacifos_com_heuristica[j-6].paredeUp = True

            elif(informacao.direcao==90): # Virado para a esquerda
                arrayCacifos_com_heuristica[j].paredeLeft = True
                #colocamos a parede do cacifo a esquerda
                if(arrayCacifos_com_heuristica[j].numeroCacifo not in [1,7,13,19,25,31]): #caso nao esteja nos limites do mapa a esquerda
                    #guarda que o cacifo a direita do atual tem uma parde a sua esquerda
                    arrayCacifos_com_heuristica[j-1].paredeRight = True
        j+=1


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
    



        
def main():
    inicializaCacifos()
    algoritmo_A_star(30)

    #while True:
        #verifica_cacifo()
        #if(sensor_cor.color() == Color.BLUE):
            #robot.Stop()

if (__name__ == "__main__"):
    main() 

            


