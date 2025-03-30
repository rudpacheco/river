import pygame
import random

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()  # Inicializa o mixer de áudio

# Configurações da tela
LARGURA, ALTURA = 400, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("River Raid Clone")

# Cores
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

# Carregar imagens
aviao_img = pygame.image.load("./imagens/aviao.png")
aviao_img = pygame.transform.scale(aviao_img, (25, 25))
inimigo1_img = pygame.image.load("./imagens/barco.png")
inimigo1_img = pygame.transform.scale(inimigo1_img, (40, 50))
inimigo2_img = pygame.image.load("./imagens/helicoptero.png")
inimigo2_img = pygame.transform.scale(inimigo2_img, (40, 50))
posto_img = pygame.image.load("./imagens/fuel.png")
posto_img = pygame.transform.scale(posto_img, (50, 60))

# Carregar áudio
pygame.mixer.music.load("./sounds/fundo.mp3")  # Substitua pelo caminho do seu áudio de fundo
pygame.mixer.music.set_volume(0.5)  # Define o volume do áudio de fundo
pygame.mixer.music.play(-1)  # Reproduz o áudio em loop

tiro_som = pygame.mixer.Sound("./sounds/tiro.mp3")  # Substitua pelo caminho do seu efeito sonoro de tiro
explosao_som = pygame.mixer.Sound("./sounds/explosao.mp3")  # Substitua pelo caminho do seu efeito sonoro de explosão

# Posição inicial do avião
aviao_x = LARGURA // 2 - 20
aviao_y = ALTURA - 100
velocidade = 5

# Variáveis do cenário
fundo_y = 0
fundo_velocidade = 3

# Combustível
combustivel = 100
combustivel_consumo = 0.1
posto_x = random.randint(60, LARGURA - 110)
posto_y = -50
posto_velocidade = 3
posto_largura, posto_altura = 50, 30

# Lista de inimigos
inimigos = []
num_inimigos = 5
inimigo_tempo = 0
inimigo_intervalo = 100  # Intervalo para gerar novos inimigos (em frames)

# Velocidade dos inimigos
inimigo_velocidade = 4

# Lista de tiros
tiros = []
tiro_velocidade = 7

# Pontuação
score = 0
fonte = pygame.font.Font(None, 36)

# Loop do jogo
rodando = True
game_over = False
while rodando:
    pygame.time.delay(30)

    # Captura eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                tiros.append(pygame.Rect(aviao_x + 18, aviao_y, 5, 10))
                tiro_som.play()  # Reproduz o efeito sonoro de tiro

    if not game_over:
        # Movimentação do avião
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and aviao_x > 50:
            aviao_x -= velocidade
        if teclas[pygame.K_RIGHT] and aviao_x < LARGURA - 50 - 40:
            aviao_x += velocidade
        if teclas[pygame.K_UP] and aviao_y > 0:
            aviao_y -= velocidade
        if teclas[pygame.K_DOWN] and aviao_y < ALTURA - 40:
            aviao_y += velocidade

        # Movimento do fundo
        fundo_y += fundo_velocidade
        if fundo_y >= ALTURA:
            fundo_y = 0

        # Atualizar combustível
        combustivel -= combustivel_consumo
        if combustivel <= 0:
            combustivel = 0
            game_over = True

        # Movimento do posto de combustível
        posto_y += posto_velocidade
        if posto_y > ALTURA:
            posto_y = -50
            posto_x = random.randint(60, LARGURA - 110)

        # Verificar colisão com o posto de combustível
        if aviao_x < posto_x + posto_largura and aviao_x + 40 > posto_x and aviao_y < posto_y + posto_altura and aviao_y + 40 > posto_y:
            combustivel = min(100, combustivel + 30)
            posto_y = -50
            posto_x = random.randint(60, LARGURA - 110)

        # Movimentar inimigos
        for inimigo_data in inimigos[:]:
            inimigo_data['rect'].y += inimigo_velocidade
            if inimigo_data['rect'].y > ALTURA:
                inimigo_data['rect'].y = random.randint(-300, -50)
                inimigo_data['rect'].x = random.randint(60, LARGURA - 110)

            # Verificar colisão com o avião
            if aviao_x < inimigo_data['rect'].x + 40 and aviao_x + 40 > inimigo_data['rect'].x and aviao_y < inimigo_data['rect'].y + 40 and aviao_y + 40 > inimigo_data['rect'].y:
                game_over = True

            # Verificar colisão tiro-inimigo
            for tiro in tiros[:]:
                if tiro.colliderect(inimigo_data['rect']):
                    inimigos.remove(inimigo_data)
                    tiros.remove(tiro)
                    score += 10  # Adiciona 10 pontos por inimigo abatido
                    explosao_som.play()  # Reproduz o efeito sonoro de explosão
                    break

        # Movimentar tiros
        for tiro in tiros[:]:
            tiro.y -= tiro_velocidade
            if tiro.y < 0:
                tiros.remove(tiro)

        # Gerar novos inimigos
        inimigo_tempo += 1
        if inimigo_tempo > inimigo_intervalo:
            tipo_inimigo = random.choice([1, 2])
            inimigos.append({
                'rect': pygame.Rect(random.randint(60, LARGURA - 110), random.randint(-300, -50), 40, 40),
                'tipo': tipo_inimigo
            })
            inimigo_tempo = 0

    # Desenha o fundo
    tela.fill(AZUL)
    pygame.draw.rect(tela, VERDE, (0, 0, 50, ALTURA))
    pygame.draw.rect(tela, VERDE, (LARGURA - 50, 0, 50, ALTURA))

    # Desenha o posto de combustível
    tela.blit(posto_img, (posto_x, posto_y))

    # Desenha os inimigos
    for inimigo_data in inimigos:
        if inimigo_data['tipo'] == 1:
            tela.blit(inimigo1_img, inimigo_data['rect'])
        else:
            tela.blit(inimigo2_img, inimigo_data['rect'])

    # Desenha os tiros
    for tiro in tiros:
        pygame.draw.rect(tela, VERMELHO, tiro)

    # Desenha o avião
    tela.blit(aviao_img, (aviao_x, aviao_y))

    # Desenha a barra de combustível
    pygame.draw.rect(tela, VERMELHO, (10, 10, combustivel * 2, 10))
    pygame.draw.rect(tela, BRANCO, (10, 10, 200, 10), 2)

    # Exibe a pontuação
    texto_score = fonte.render(f"Player 1: {score}", True, BRANCO)
    tela.blit(texto_score, (10, 30))

    # Game Over
    if game_over:
        texto_game_over = fonte.render("Game Over!", True, BRANCO)
        tela.blit(texto_game_over,
                  (LARGURA // 2 - texto_game_over.get_width() // 2, ALTURA // 2 - texto_game_over.get_height() // 2))

    pygame.display.update()

pygame.quit()