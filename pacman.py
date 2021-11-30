import pygame
from abc import ABCMeta, abstractmethod
import random


pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
font = pygame.font.SysFont("arial", 26, True, False)


yellow = (255, 255, 0)
janela = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pacman")


beggining = pygame.image.load("pacman logo.png")
pygame.mixer.music.load('pacman_beginning.wav')
pygame.mixer.music.play()
janela.blit(beggining, (0, 0))
pygame.display.update()

open_win = True

pygame.mixer.music.load('pacman_beginning.wav')
pygame.mixer.music.play(-1)

while open_win:

    pygame.time.delay(50)

    for event in pygame.event.get(): 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                open_win = False

yellow = (255, 255, 0)
black = (0, 0, 0)
purple = (240 , 0 , 255)
red = (255, 0, 0)
white = (255, 255, 255)
orange = (255, 140, 0)
pink = (255, 15, 192)
cyan = (0, 255, 255)
Velo = 1
up = 1
down = 2
right = 3
left = 4



class Game(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass


class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


class Cenario(Game):
    def __init__(self, tamanho, pac):
        self.pacman = pac
        self.moviveis = []
        self.pontos = 0
        self.estado = 0
        self.tamanho = tamanho
        self.vidas = 5
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar_score(self, tela):
        pontos_x = self.tamanho * 30
        pontos_img = font.render("Score {}".format(self.pontos), True, yellow)
        vidas_img = font.render("Vidas {}".format(self.vidas), True, yellow)
        tela.blit(pontos_img, (pontos_x, 50))
        tela.blit(vidas_img, (pontos_x, 100))

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = black
            if coluna == 2:
                cor = purple
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, yellow, (x + half, y + half),
                                   self.tamanho // 10, 0)

    def pintar(self, tela):
        if self.estado == 0:
            self.pintar_jogando(tela)
        elif self.estado == 1:
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == 2:
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado == 3:
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    def pintar_texto_centro(self, tela, texto):
        texto_img = font.render(texto, True, yellow)
        texto_x = (tela.get_width() - texto_img.get_width()) // 3
        texto_y = (tela.get_height() - texto_img.get_height()) // 3
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "Y O U  W I N!")

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "Y  O U  L O S E")

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S E")

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela)

    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(up)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(down)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(left)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(right)
        return direcoes

    def calcular_regras(self):
        if self.estado == 0:
            self.calcular_regras_jogando()
        elif self.estado == 1:
            self.calcular_regras_pausado()
        elif self.estado == 2:
            self.calcular_regras_gameover()

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and \
                    movivel.coluna == self.pacman.coluna:
                self.vidas -= 1
                if self.vidas <= 0:
                    self.estado = 2
                    pygame.mixer.music.load('pacman_death.wav')
                    pygame.mixer.music.play()
                else:
                    self.pacman.linha = 1
                    self.pacman.coluna = 1
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and \
                        self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        pygame.mixer.music.load('pacman_chomp.wav')
                        pygame.mixer.music.play()
                        if self.pontos >= 306:
                            self.estado = 3
                else:
                    movivel.recusar_movimento(direcoes)

    def processar_eventos(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == 0:
                        self.estado = 1
                    else:
                        self.estado = 0

class Pacman(Game, Movivel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura = 0
        self.velocidade_abertura = 1

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def pintar(self, tela):
        pygame.draw.circle(tela, yellow, (self.centro_x, self.centro_y), self.raio, 0)

        self.abertura += self.velocidade_abertura
        if self.abertura > self.raio:
            self.velocidade_abertura = -1
        if self.abertura <= 0:
            self.velocidade_abertura = 1

        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, black, pontos, 0)

        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, black, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = Velo
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -Velo
                elif e.key == pygame.K_UP:
                    self.vel_y = -Velo
                elif e.key == pygame.K_DOWN:
                    self.vel_y = Velo
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass

class Fantasma(Game):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0
        self.linha = 15.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.velocidade = 1
        self.direcao = down
        self.tamanho = tamanho
        self.cor = cor

    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2),
                    (px + fatia * 2, py + fatia // 2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2

        olho_e_x = int(px + fatia * 2.5)
        olho_e_y = int(py + fatia * 2.5)

        olho_d_x = int(px + fatia * 5.5)
        olho_d_y = int(py + fatia * 2.5)

        pygame.draw.circle(tela, white, (olho_e_x, olho_e_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, black, (olho_e_x, olho_e_y), olho_raio_int, 0)
        pygame.draw.circle(tela, white, (olho_d_x, olho_d_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, black, (olho_d_x, olho_d_y), olho_raio_int, 0)

    def calcular_regras(self):
        if self.direcao == up:
            self.linha_intencao -= self.velocidade
        elif self.direcao == down:
            self.linha_intencao += self.velocidade
        elif self.direcao == left:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == right:
            self.coluna_intencao += self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, evts):
        pass

if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Fantasma(red, size)
    inky = Fantasma(cyan, size)
    clyde = Fantasma(orange, size)
    pinky = Fantasma(pink, size)
    cenario = Cenario(size, pacman)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)


    while True:
        pacman.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()
        cenario.calcular_regras()
        
        screen.fill(black)
        cenario.pintar(screen)
        pacman.pintar(screen)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        eventos = pygame.event.get()
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)
