import pygame
import time
import random

# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (169, 169, 169)  # Color gris para el botón

# Definir tamaño de la ventana
ANCHO, ALTO = 800, 800
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Turnos - Tablero Cuadrado")

# Fuente
fuente = pygame.font.SysFont(None, 48)
boton_fuente = pygame.font.SysFont(None, 36)
dado_fuente = pygame.font.SysFont(None, 100)

# Colores de las fichas de los jugadores
COLOR_JUGADOR1 = ROJO
COLOR_JUGADOR2 = AZUL

# Número de casillas por lado
CASILLAS_LADO = 8
TAMANIO_CASILLA = ANCHO // CASILLAS_LADO

# Función para dibujar el tablero
def dibujar_tablero():
    numero_casilla = 0
    for fila in range(CASILLAS_LADO):
        for columna in range(CASILLAS_LADO):
            if fila == 0 or fila == CASILLAS_LADO - 1 or columna == 0 or columna == CASILLAS_LADO - 1:
                x = columna * TAMANIO_CASILLA
                y = fila * TAMANIO_CASILLA
                pygame.draw.rect(screen, VERDE, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA), 2)
                
                # Dibujar el número de la casilla
                texto_casilla = fuente.render(str(numero_casilla), True, NEGRO)
                texto_rect = texto_casilla.get_rect(center=(x + TAMANIO_CASILLA // 2, y + TAMANIO_CASILLA // 2))
                screen.blit(texto_casilla, texto_rect)
                numero_casilla += 1

# Función para calcular la posición en píxeles según la casilla
def calcular_posicion(casilla):
    if casilla < CASILLAS_LADO:  # Lado superior
        x = casilla * TAMANIO_CASILLA + TAMANIO_CASILLA // 2
        y = TAMANIO_CASILLA // 2
    elif casilla < CASILLAS_LADO * 2 - 1:  # Lado derecho
        x = (CASILLAS_LADO - 1) * TAMANIO_CASILLA + TAMANIO_CASILLA // 2
        y = (casilla - CASILLAS_LADO + 1) * TAMANIO_CASILLA + TAMANIO_CASILLA // 2
    elif casilla < CASILLAS_LADO * 3 - 2:  # Lado inferior
        x = ((CASILLAS_LADO * 3 - 3) - casilla) * TAMANIO_CASILLA + TAMANIO_CASILLA // 2
        y = (CASILLAS_LADO - 1) * TAMANIO_CASILLA + TAMANIO_CASILLA // 2
    else:  # Lado izquierdo
        x = TAMANIO_CASILLA // 2
        y = ((CASILLAS_LADO * 4 - 4) - casilla) * TAMANIO_CASILLA + TAMANIO_CASILLA // 2
    return x, y

# Función para dibujar las fichas de los jugadores
def dibujar_fichas(pos_jugador1, pos_jugador2):
    x1, y1 = calcular_posicion(pos_jugador1)
    x2, y2 = calcular_posicion(pos_jugador2)
    pygame.draw.circle(screen, COLOR_JUGADOR1, (x1, y1), 20)
    pygame.draw.circle(screen, COLOR_JUGADOR2, (x2, y2), 20)

# Función para mostrar mensaje de victoria
def mostrar_victoria(jugador):
    dibujar_mensaje(f"¡Jugador {jugador} ha ganado!", NEGRO, 0)
    pygame.display.update()
    time.sleep(2)

# Función para dibujar el mensaje
def dibujar_mensaje(texto, color, y_offset):
    texto_superficie = fuente.render(texto, True, color)
    texto_rect = texto_superficie.get_rect(center=(ANCHO // 2, ALTO // 2 + y_offset))
    screen.blit(texto_superficie, texto_rect)

# Función para dibujar el botón
def dibujar_boton(texto):
    boton_superficie = boton_fuente.render(texto, True, NEGRO)
    boton_rect = boton_superficie.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))
    pygame.draw.rect(screen, GRIS, boton_rect.inflate(20, 20))  # Botón gris
    screen.blit(boton_superficie, boton_rect)
    return boton_rect

# Función para animación de transición
def animacion_transicion():
    for i in range(10):
        screen.fill(NEGRO)
        pygame.display.update()
        time.sleep(0.05)  # Pausa corta para la animación
    screen.fill(BLANCO)

# Función para mostrar el dado con borde
def mostrar_dado(valor, color):
    dado_texto = dado_fuente.render(str(valor), True, color)
    dado_rect = dado_texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    
    # Dibujar borde cuadrado
    pygame.draw.rect(screen, NEGRO, dado_rect.inflate(20, 20), 5)  # Borde
    screen.blit(dado_texto, dado_rect)

# Bucle principal
def juego():
    turno = 1
    corriendo = True
    dado_lanzado = False
    valor_dado = 0
    pos_jugador1 = 0
    pos_jugador2 = 0
    casillas_totales = CASILLAS_LADO * 4 - 4

    while corriendo:
        screen.fill(BLANCO)

        # Dibujar el tablero
        dibujar_tablero()

        # Mostrar mensaje según el turno
        if turno == 1:
            dibujar_mensaje("Turno del Jugador 1 - LANZA EL DADO", ROJO, -100)
        else:
            dibujar_mensaje("Turno del Jugador 2 - LANZA EL DADO", AZUL, -100)

        # Si el dado ha sido lanzado, mostrar su valor
        if dado_lanzado:
            color_dado = COLOR_JUGADOR1 if turno == 1 else COLOR_JUGADOR2
            mostrar_dado(valor_dado, color_dado)

        # Dibujar el botón
        boton_rect = dibujar_boton("Acabar turno")

        # Comprobar si alguien ha llegado a la meta
        if pos_jugador1 == casillas_totales:
            mostrar_victoria(1)
            break
        if pos_jugador2 == casillas_totales:
            mostrar_victoria(2)
            break

        # Comprobar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    # Mover la ficha del jugador actual, asegurando que no sobrepase el total de casillas
                    nueva_pos = pos_jugador1 + valor_dado if turno == 1 else pos_jugador2 + valor_dado
                    nueva_pos = min(nueva_pos, casillas_totales)  # Evita que sobrepase el total de casillas

                    # Colocar la ficha en la nueva posición
                    if turno == 1:
                        pos_jugador1 = nueva_pos
                    else:
                        pos_jugador2 = nueva_pos

                    # Hacer la animación de transición
                    animacion_transicion()
                    # Cambiar el turno
                    turno = 2 if turno == 1 else 1
                    dado_lanzado = False  # Reseteamos el dado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not dado_lanzado:
                    # Lanzar el dado (solo si no ha sido lanzado aún)
                    valor_dado = random.randint(1, 6)
                    dado_lanzado = True

        dibujar_fichas(pos_jugador1, pos_jugador2)

        pygame.display.update()

# Ejecutar el juego
juego()

# Finalizar Pygame
pygame.quit()
