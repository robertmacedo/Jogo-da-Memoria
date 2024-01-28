#IMPORTAÇÕES
import pygame, sys
import random
from pygame import mixer
from pygame.locals import *


#INICIALIZANDO O PYGAME
pygame.init()


#CORES
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 128, 0)
AZUL = (0, 0, 255)


#VÍDEO
'''CONFIGURAÇÕES DE TELA:'''
FPS = 60
Largura = 800
Altura = 100
Tela_do_Menu = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Jogo da Memória')
pygame.time.set_timer(pygame.USEREVENT, 1000)
Background = pygame.image.load("Imagens/Fundo.png")
Verso_da_Carta = pygame.image.load("Imagens/Verso.png")


#ÁUDIO
'''CONFIGURAÇÕES DE SOM:'''
Música_de_Fundo = mixer.music.load('Sons/retro-90s-arcade-machine.mp3')
Som_Acerto = mixer.Sound("Sons/arcade-game-complete-or-approved-mission-205.wav")
Som_Vitória = mixer.Sound("Sons/win.mp3")
mixer.music.set_volume(0.10)
mixer.music.play()


#JOGO
Número_de_Cartas = 16
Tamanho_da_Carta = [Largura / Número_de_Cartas, Altura]
Relógio = pygame.time.Clock()

def Inicializando():
    '''VARIÁVEIS GLOBAIS:'''
    global Frente_da_Carta, Expor, Carta_Virada, Carta_Correspondente
    global Estado, Número_de_Tentativas, Timer_do_Jogo, Centralizar_Texto, Fonte01, Texto01

    Mensagem("")
    '''VÁRIAVEL QUE ARMAZENA O TEMPO DE JOGO:'''
    Timer_do_Jogo = 0 

    '''VÁRIAVEL QUE ARMAZENA O ESTADO DO JOGO. ELA REFERE-SE AS CARTAS VIRADAS PELO JOGADOR (UMA OU DUAS):'''
    Estado = 0

    '''VÁRIAVEL QUE ARMAZENA O NÚMERO DE TENTATIVAS, OU SEJA, DUAS CARTAS VIRADAS = 1 TENTATIVA:'''
    Número_de_Tentativas = 0 

    '''VÁRIAVEL QUE ARMAZENA O PAR DE CARTAS CLICADAS:'''
    Carta_Virada = []

    '''VÁRIAVEL QUE ARMAZENA A QUANTIDADE DE PARES DE CARTAS DESCOBERTAS:'''
    Carta_Correspondente = 0 

    '''LISTA COM FUNÇÃO SHUFFLE DA BIBLIOTECA RANDOM - USADA PARA EMBARALHAR AS CARTAS:'''
    Frente_da_Carta = ["Imagens/imagem1.png", "Imagens/imagem1.png", "Imagens/imagem2.png", "Imagens/imagem2.png",
                  "Imagens/imagem3.png", "Imagens/imagem3.png", "Imagens/imagem4.png", "Imagens/imagem4.png",
                  "Imagens/imagem5.png", "Imagens/imagem5.png", "Imagens/imagem6.png", "Imagens/imagem6.png",
                  "Imagens/imagem7.png", "Imagens/imagem7.png", "Imagens/imagem8.png", "Imagens/imagem8.png"]
    random.shuffle(Frente_da_Carta)

    '''GUARDA O ÍNDICE RELATIVO AO BARALHO:'''
    Expor = [False] * Número_de_Cartas

    '''CONFIGURAÇÕES DE TEXTO:'''
    Fonte01 = pygame.font.Font('freesansbold.ttf', 20)
    Texto01 = pygame.font.Font.render(Fonte01, Msg01, True, VERDE)
    Centralizar_Texto = []
    for Contador in Frente_da_Carta:
        surf = pygame.font.Font.render(Fonte01, Contador, True, VERDE)
        rect = surf.get_rect()
        Centralizar_Texto.append([surf, rect])


'''MOSTRA MENSAGENS:'''
def Mensagem(Msg02):
    global Msg01
    Msg01 = Msg02


'''TEMPO DO JOGO:'''
def Timer():
    global Timer_do_Jogo
    Timer_do_Jogo += 1


'''DESENHA:'''
def Desenhar():
    global Centralizar_Texto
    i = 0
    j = Tamanho_da_Carta[0] / 2 - 25
    for X in range(Número_de_Cartas):
        '''SE UMA CARTA ESTIVER EXPOSTA, ENTÃO O VETOR "CENTRALIZAR_TEXTO" 
        DEVE SER USADO PARA CENTRALIZAR A SUA POSIÇÃO. CASO CONTRÁRIO,
        UM POLÍGONO DEVE SER DESENHADO. A VARIÁVEL "J" IRÁ AUXILIAR PARA
        DEFINIR A POSIÇÃO CENTRAL DO TEXTO DA CARTA E A VARIÁVEL "I" 
        IRÁ AUXILIAR A DEFINIR A POSIÇÃO DO POLÍGONO.'''
        if Expor[X]:
            Centralizar_Texto[X][1] = (j, 0, 28, 50)
        else:
            '''OBSERVAÇÃO: O "VERMELHO" SE REFERE AS BORDAS QUE SEPARA UMA CARTA DA OUTRA DURANTE O JOGO:'''
            pygame.draw.rect(Tela_do_Menu, VERMELHO, pygame.Rect(i, 0, Tamanho_da_Carta[0], Tamanho_da_Carta[1]), 1)
        i += Tamanho_da_Carta[0]
        j += Tamanho_da_Carta[0]
    pass


def Clique_do_Mouse(Posição02):
    '''RECUPERA O ÍNDICE DA CARTA CLICADA E ATUALIZA O NÚMERO DE TENTATIVAS:'''
    global Estado, Número_de_Tentativas, Carta_Virada, Carta_Correspondente
    global Msg01, Expor, Texto01
    Posição01 = 50
    Índice = 0
    Contador = 0
    while Contador == 0:
        for X in range(Posição01):
            if Posição02[0] == X:
                Contador = 1
        if Contador == 1:
            break
        Índice += 1
        Posição01 += 50

    if not Expor[Índice]:
        if Estado == 0:
            Estado = 1
        elif Estado == 1:
            Estado = 2
            Número_de_Tentativas += 1

            '''CONDIÇÃO DE FIM DE JOGO:'''
            if Carta_Correspondente == 7:
                Mensagem("VOCÊ TERMINOU EM {} MIN {} SEGS E FEZ {} JOGADAS".format(str(Timer_do_Jogo // 60), str(Timer_do_Jogo % 60), str(Número_de_Tentativas)))
                Texto01 = pygame.font.Font.render(Fonte01, Msg01, True, VERDE)
                Som_Vitória.play()
            
        else:
            Estado = 1
            '''CONDIÇÃO PARA VIRAR AS CARTAS PARA BAIXO SE ELAS NÃO FOREM IGUAIS:'''
            if Frente_da_Carta[Carta_Virada[0]] != Frente_da_Carta[Carta_Virada[1]]:
                Expor[Carta_Virada[0]] = False
                Expor[Carta_Virada[1]] = False
    
                '''CONDIÇÃO CONTRARIA PARA MANTER AS CARTAS VIRADAS PARA CIMA SE FOREM IGUAIS:'''
            else:
                Carta_Correspondente += 1
            Carta_Virada = []
        Carta_Virada.append(Índice)
        Expor[Índice] = True

    '''CONDIÇÃO PARA TOCAR UM SOM QUANDO DUAS CARTAS REVELADAS FOREM IGUAIS:'''
    if Carta_Virada.__len__() == 2 and Frente_da_Carta[Carta_Virada[0]] == Frente_da_Carta[Carta_Virada[1]]:
        Som_Acerto.play()


class Button():
    '''CONFIGURAÇÕES DE POSIÇÃO DOS TEXTOS:'''
    def __init__(self, Posição02, Entrada_de_Texto, Fonte, Posição_do_Texto):
        self.X = Posição02[0]
        self.Y = Posição02[1]
        self.Posição_X = Posição_do_Texto[0]
        self.Posição_Y = Posição_do_Texto[1]
        self.Fonte = Fonte
        self.Entrada_de_Texto = Entrada_de_Texto
        self.text = self.Fonte.render(self.Entrada_de_Texto, True, BRANCO)
        self.text_rect = self.text.get_rect(center=(self.Posição_X, self.Posição_Y))
    def create(self, Tela):
        Tela.blit(self.text, self.text_rect)

    def Clique(self, Posição01):
        if Posição01[0] in range(self.text_rect.left, self.text_rect.right) and Posição01[1] in range(self.text_rect.top, self.text_rect.bottom):
            return True
        return False


def Jogo():
    global Centralizar_Texto, Texto01
    Tela_do_Menu = pygame.display.set_mode((Largura, Altura))
    Inicializando()

    '''LAÇO DE REPETIÇÃO PARA MANTER A TELA DO JOGO ABERTA:'''
    while True:
        Tela_do_Menu.blit(Verso_da_Carta, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                Posição02 = pygame.mouse.get_pos()
                Clique_do_Mouse(Posição02)

            if event.type == pygame.USEREVENT:
                Timer()
        Desenhar()

        for X in range(Número_de_Cartas):
            if Expor[X]:
                cd = pygame.image.load(Frente_da_Carta[X])
                Tela_do_Menu.blit(cd, Centralizar_Texto[X][1])
        Tela_do_Menu.blit(Texto01, [5, Altura - 20])
        pygame.display.update()
        Relógio.tick(FPS)


def Menu():
    '''CONFIGURAÇÕES DA FONTE E TAMANHO DO TÍTULO "JOGO DA MEMÓRIA":'''
    Fonte02 = pygame.font.SysFont("comicsans", 70)

    '''CONFIGURAÇÕES DA FONTE E TAMANHO DO TÍTULO DAS OPÇÕES DO MENU:'''
    Fonte03 = pygame.font.SysFont("comicsans", 20)

    '''CONFIGURAÇÕES DOS TÍTULOS DOS BOTÕES DO MENU:'''
    Jogar = Button(Posição02=(325, 150), Entrada_de_Texto = "Jogar", Fonte = Fonte03, Posição_do_Texto=(400, 175))
    Créditos = Button(Posição02=(325, 250), Entrada_de_Texto ="Créditos", Fonte=Fonte03, Posição_do_Texto=(400, 275))
    Sair = Button(Posição02=(325, 350), Entrada_de_Texto ="Sair", Fonte=Fonte03, Posição_do_Texto=(400, 375))

    '''LAÇO DE REPETIÇÃO PARA MANTER A TELA DO MENU ABERTA:'''
    while True:
        Posição02 = pygame.mouse.get_pos()
        Tela_do_Menu.blit(Background, (0, 0))
        for Botão in [Jogar, Créditos, Sair]:
            Botão.create(Tela_do_Menu)

        '''CONFIGURAÇÕES DE TÍTULO DO JOGO:'''
        Texto_do_Menu = Fonte02.render("Jogo da Memória", False, BRANCO)
        Menu_rect = Texto_do_Menu.get_rect(center=(400, 50))
        Tela_do_Menu.blit(Texto_do_Menu, Menu_rect)
        pygame.display.update()
        '''CONDIÇÃO PARA FECHAR O JOGO CLICANDO NO "X" DA JANELA:'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            '''CONDIÇÃO QUE DIRECIONA PARA O JOGO:'''
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Jogar.Clique(Posição02):
                    Jogo()

                '''CONDIÇÃO QUE DIRECIONA PARA INFORMAÇÕES SOBRE CRÉDITOS DO JOGO:'''
                if Créditos.Clique(Posição02):
                    Créditos_do_Jogo()
                
                '''CONDIÇÃO PARA FECHAR O JOGO QUANDO CLICAR NO BOTÃO "SAIR":'''
                if Sair.Clique(Posição02):
                    pygame.quit()
                    sys.exit()


def Créditos_do_Jogo():
    '''CONFIGURAÇÕES DA FONTE E TAMANHO DO TÍTULO "CRÉDITOS":'''
    Fonte02 = pygame.font.SysFont("comicsans", 70)

    '''CONFIGURAÇÕES DA FONTE E TAMANHO DO TEXTO DE CRÉDITOS:'''
    Fonte03 = pygame.font.SysFont("comicsans", 20)

    '''LAÇO DE REPETIÇÃO PARA MANTER A TELA DE CRÉDITOS DO JOGO ABERTA:'''
    while True:
        Posição02 = pygame.mouse.get_pos()
        Tela_do_Menu.blit(Background, (0, 0))

        Texto02 = Fonte02.render("Créditos", True, BRANCO)
        Créditos_rect = Texto02.get_rect(center=(400, 50))
        Tela_do_Menu.blit(Texto02, Créditos_rect)

        Texto02 = Fonte03.render("Jogo da memória criado por Robert Macedo.", True, BRANCO)
        Créditos_rect = Texto02.get_rect(center=(400, 225))
        Tela_do_Menu.blit(Texto02, Créditos_rect)

        Voltar = Button(Posição02=(325, 150), Entrada_de_Texto="Voltar", Fonte=Fonte03, Posição_do_Texto=(400, 375))
        Voltar.create(Tela_do_Menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Voltar.Clique(Posição02):
                    Menu()
        pygame.display.update()
Menu()
