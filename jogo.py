import pygame
import random

pygame.init()

# ============================================================
# CONFIGURAÇÕES DA JANELA
# ============================================================
LARGURA = 800
ALTURA = 600
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("SquareGame - Jelly Roger: Luffy vs Zoro")
clock = pygame.time.Clock()

# ============================================================
# CORES
# ============================================================
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)
CINZA = (50, 50, 50)

# ============================================================
# CARREGANDO AS IMAGENS
# ============================================================
TAMANHO_JOGADOR = 60  # Aumentei um pouco para a imagem ficar visível
TAMANHO_INIMIGO = 60

try:
    # Carrega e redimensiona a imagem do Luffy
    img_luffy = pygame.image.load("luffy.png").convert_alpha()
    img_luffy = pygame.transform.scale(img_luffy, (TAMANHO_JOGADOR, TAMANHO_JOGADOR))

    # Carrega e redimensiona a imagem do Zoro
    img_zoro = pygame.image.load("zoro.png").convert_alpha()
    img_zoro = pygame.transform.scale(img_zoro, (TAMANHO_INIMIGO, TAMANHO_INIMIGO))
except pygame.error:
    print("ERRO: Não foi possível encontrar 'luffy.png' ou 'zoro.png'.")
    print("Certifique-se de que as imagens estão na mesma pasta do código.")
    pygame.quit()
    exit()

# ============================================================
# VARIÁVEIS DO JOGADOR (LUFFY)
# ============================================================
VELOCIDADE_JOGADOR = 5

jogador_x = LARGURA // 2
jogador_y = ALTURA // 2

# ============================================================
# VARIÁVEIS DO INIMIGO (ZORO)
# ============================================================
VELOCIDADE_INIMIGO = 2.5

inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
inimigo_y = random.randint(0, ALTURA - TAMANHO_INIMIGO)

# ============================================================
# PONTUAÇÃO E FONTES
# ============================================================
pontuacao = 0
fonte = pygame.font.SysFont(None, 30)
fonte_game_over = pygame.font.SysFont(None, 60)
fonte_instrucao = pygame.font.SysFont(None, 24)


# ============================================================
# FUNÇÕES DO JOGO
# ============================================================
def reiniciar_jogo():
    global jogador_x, jogador_y
    global inimigo_x, inimigo_y
    global pontuacao, VELOCIDADE_INIMIGO

    jogador_x = LARGURA // 2
    jogador_y = ALTURA // 2

    inimigo_x = random.randint(0, LARGURA - TAMANHO_INIMIGO)
    inimigo_y = random.randint(0, ALTURA - TAMANHO_INIMIGO)

    pontuacao = 0
    VELOCIDADE_INIMIGO = 2.5


def desenhar_jogo():
    tela.fill(BRANCO)

    # Desenha as imagens nas posições atuais
    tela.blit(img_luffy, (jogador_x, jogador_y))
    tela.blit(img_zoro, (inimigo_x, inimigo_y))

    # Pontuação
    texto = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    tela.blit(texto, (10, 10))

    # Instrução
    instrucao = fonte_instrucao.render(
        "Setas: mover Luffy  |  Zoro te persegue!", True, PRETO)
    tela.blit(instrucao, (10, ALTURA - 30))


def mostrar_game_over():
    tela.fill(CINZA)

    texto = fonte_game_over.render("GAME OVER", True, VERMELHO)
    tela.blit(texto, texto.get_rect(center=(LARGURA // 2, 200)))

    texto_pontos = fonte.render(f"Pontuação final: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontos, texto_pontos.get_rect(center=(LARGURA // 2, 280)))

    texto_reiniciar = fonte.render("Pressione ENTER para jogar novamente", True, BRANCO)
    tela.blit(texto_reiniciar, texto_reiniciar.get_rect(center=(LARGURA // 2, 340)))


# ============================================================
# LOOP PRINCIPAL
# ============================================================
rodando = True
jogando = True

while rodando:
    # --- Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if not jogando and evento.key == pygame.K_RETURN:
                reiniciar_jogo()
                jogando = True

    if jogando:
        # --- Movimento do jogador ---
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            jogador_y -= VELOCIDADE_JOGADOR
        if teclas[pygame.K_DOWN]:
            jogador_y += VELOCIDADE_JOGADOR
        if teclas[pygame.K_LEFT]:
            jogador_x -= VELOCIDADE_JOGADOR
        if teclas[pygame.K_RIGHT]:
            jogador_x += VELOCIDADE_JOGADOR

        # --- Limites da tela ---
        if jogador_x < 0:
            jogador_x = 0
        if jogador_x > LARGURA - TAMANHO_JOGADOR:
            jogador_x = LARGURA - TAMANHO_JOGADOR
        if jogador_y < 0:
            jogador_y = 0
        if jogador_y > ALTURA - TAMANHO_JOGADOR:
            jogador_y = ALTURA - TAMANHO_JOGADOR

        # --- Perseguição do Zoro ---
        if inimigo_x < jogador_x:
            inimigo_x += VELOCIDADE_INIMIGO
        elif inimigo_x > jogador_x:
            inimigo_x -= VELOCIDADE_INIMIGO

        if inimigo_y < jogador_y:
            inimigo_y += VELOCIDADE_INIMIGO
        elif inimigo_y > jogador_y:
            inimigo_y -= VELOCIDADE_INIMIGO

        # --- Retângulos de colisão (Hitboxes) ---
        jogador_rect = pygame.Rect(jogador_x, jogador_y, TAMANHO_JOGADOR, TAMANHO_JOGADOR)
        inimigo_rect = pygame.Rect(inimigo_x, inimigo_y, TAMANHO_INIMIGO, TAMANHO_INIMIGO)

        # --- Colisão Pixel-Perfect (Máscara) ---
        # Em vez de usar apenas o quadrado, usamos as máscaras das imagens para colidir
        mascara_jogador = pygame.mask.from_surface(img_luffy)
        mascara_inimigo = pygame.mask.from_surface(img_zoro)

        # Calcula a distância entre os retângulos
        offset_x = int(inimigo_x - jogador_x)
        offset_y = int(inimigo_y - jogador_y)

        # Verifica se as máscaras se sobrepõem na posição atual
        colidiu = mascara_jogador.overlap(mascara_inimigo, (offset_x, offset_y))

        if colidiu:
            jogando = False
        else:
            # --- Pontuação ---
            pontuacao += 1
            # A cada 300 pontos, o Zoro fica mais rápido
            if pontuacao % 300 == 0:
                VELOCIDADE_INIMIGO += 0.5

        desenhar_jogo()
    else:
        mostrar_game_over()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()