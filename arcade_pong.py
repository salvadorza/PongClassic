import turtle
import tkinter as tk

# Aquí predefinimos la dificultad del juego en 1
velocidad = [1]
juego_en_pausa = False
limite_puntuacion = 5

# Establecemos las variables globales para las puntuaciones
puntuacion_izquierda = 0
puntuacion_derecha = 0

# Función para seleccionar la dificultad del juego, 1- la mas facil y 5- la mas dificil
def seleccionar_dificultad():
    ventana_dificultad = tk.Tk()
    ventana_dificultad.title("Seleccionar Dificultad")
    ventana_dificultad.resizable(False,False)

    ancho_ventana = 300
    alto_ventana = 200
    ancho_pantalla = ventana_dificultad.winfo_screenwidth()
    alto_pantalla = ventana_dificultad.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana_dificultad.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    nivel = tk.IntVar()
    nivel.set(1)
    etiqueta = tk.Label(ventana_dificultad, text="Elige un nivel de dificultad (1-5):")
    etiqueta.pack(pady=15)

    for i in range(1, 6):
        tk.Radiobutton(ventana_dificultad, text=f"Nivel {i}", variable=nivel, value=i).pack()
    def confirmar():
        ventana_dificultad.destroy()
        velocidad[0] = nivel.get()
    boton = tk.Button(ventana_dificultad, text="Confirmar", command=confirmar)
    boton.pack()
    ventana_dificultad.mainloop()

seleccionar_dificultad()

# Creamos la ventana principal
ventana = turtle.Screen()
ventana.setup(width=800, height=600)
ventana.bgcolor("black")
ventana.title("Pong - Juego Clásico")
ventana.tracer(0)
# Indicamos que no queremos que la ventana se pueda cambiar de tamaño
ventana.cv._rootwindow.resizable(False, False)


# Creamos la paleta izquierda
paleta_izquierda = turtle.Turtle()
paleta_izquierda.shape("square")
paleta_izquierda.shapesize(stretch_wid=5, stretch_len=1)
paleta_izquierda.color("red")
paleta_izquierda.penup()
paleta_izquierda.goto(-350, 0)

# Creamos la paleta derecha
paleta_derecha = turtle.Turtle()
paleta_derecha.shape("square")
paleta_derecha.shapesize(stretch_wid=5, stretch_len=1)
paleta_derecha.color("green")
paleta_derecha.penup()
paleta_derecha.goto(350, 0)

# Creamos la pelota
pelota = turtle.Turtle()
pelota.shape("circle")
pelota.color("yellow")
pelota.penup()
pelota.goto(0, 0)
pelota.dx = 2 * velocidad[0]
pelota.dy = 2 * velocidad[0]

# Creamos el marcador
marcador = turtle.Turtle()
marcador.color("white")
marcador.penup()
marcador.hideturtle()

def posicionar_marcador():
    ancho = ventana.window_width()
    alto = ventana.window_height()
    marcador.goto(0, alto / 2 - 40)

posicionar_marcador()
marcador.write("Jugador Rojo: 0  Jugador Verde: 0", align="center", font=("Courier", 24, "normal"))

# Con esta funcion actualizamos el marcador cada vez que haya un punto
def actualizar_marcador():
    marcador.clear()
    posicionar_marcador()
    marcador.write(f"Jugador Rojo: {puntuacion_izquierda}  Jugador Verde: {puntuacion_derecha}",
                   align="center", font=("Courier", 24, "normal"))

# Funcion principal para controlar el movimiento de la pelota
def mover_pelota():
    global puntuacion_izquierda, puntuacion_derecha, juego_en_pausa
    if juego_en_pausa:
        return

    ancho = ventana.window_width() / 2
    alto = ventana.window_height() / 2

    pelota.setx(pelota.xcor() + pelota.dx)
    pelota.sety(pelota.ycor() + pelota.dy)

    # Controlamos los rebotes en el borde superior e inferior
    if pelota.ycor() > alto - 10 or pelota.ycor() < -alto + 10:
        pelota.dy *= -1

    # Controlamos el rebote en la pala izquierda
    if (pelota.xcor() < paleta_izquierda.xcor() + 20 and
        paleta_izquierda.ycor() - 50 < pelota.ycor() < paleta_izquierda.ycor() + 50):
        pelota.setx(paleta_izquierda.xcor() + 30)
        pelota.dx *= -1

    # Controlamos el rebote en la pala derecha
    if (pelota.xcor() > paleta_derecha.xcor() - 20 and
        paleta_derecha.ycor() - 50 < pelota.ycor() < paleta_derecha.ycor() + 50):
        pelota.setx(paleta_derecha.xcor() - 30)
        pelota.dx *= -1


    # Le decimos cuando tiene que haber un punto y para quien, en este caso cuando supere los bordes laterales
    if pelota.xcor() > ancho - 10:
        puntuacion_izquierda += 1
        actualizar_marcador()
        pelota.goto(0, 0)
        pelota.dx *= -1

    if pelota.xcor() < -ancho + 10:
        puntuacion_derecha += 1
        actualizar_marcador()
        pelota.goto(0, 0)
        pelota.dx *= -1

    # Fin del juego
    if puntuacion_izquierda == limite_puntuacion or puntuacion_derecha == limite_puntuacion:
        juego_en_pausa = True
        if puntuacion_izquierda == limite_puntuacion:
            mostrar_mensaje("¡Jugador Rojo Gana!", "red")
        else:
            mostrar_mensaje("¡Jugador Verde Gana!", "green")
        mostrar_ventana_opciones()
        return

    ventana.update()
    ventana.ontimer(mover_pelota, 10)

# Con esta funcion mostramos el mensaje del jugador que ha ganado
def mostrar_mensaje(texto, color):
    marcador.clear()
    marcador.color(color)
    marcador.goto(0, 0)
    marcador.write(texto, align="center", font=("Impact", 24, "italic"))
    marcador.color("white")

# Al finalizar el juego mostramos esta ventana para saber si el usuario quiere seguir jugando o no
def mostrar_ventana_opciones():
    global juego_en_pausa
    juego_en_pausa = True

    ventana_opciones = tk.Tk()
    ventana_opciones.title("¡Fin del Juego!")
    ancho_ventana = 250
    alto_ventana = 120
    ancho_pantalla = ventana_opciones.winfo_screenwidth()
    alto_pantalla = ventana_opciones.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana_opciones.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def jugar_otra_vez():
        ventana_opciones.destroy()
        reiniciar_juego()

    def salir():
        ventana_opciones.destroy()
        ventana.bye()

    tk.Button(ventana_opciones, text="Jugar Otra Vez", command=jugar_otra_vez).pack(pady=25)
    tk.Button(ventana_opciones, text="Salir", command=salir).pack()
    ventana_opciones.mainloop()

# Si el usuario quiere seguir jugando reiniciamos el juego y volvemos a darle movimiento a la pelota
def reiniciar_juego():
    global puntuacion_izquierda, puntuacion_derecha, juego_en_pausa
    puntuacion_izquierda = 0
    puntuacion_derecha = 0
    pelota.goto(0, 0)
    pelota.dx = 2 * velocidad[0]
    pelota.dy = 2 * velocidad[0]
    marcador.color("white")
    actualizar_marcador()
    juego_en_pausa = False
    mover_pelota()

# Establecemos el rango en el que se pueden mover las palas
def paleta_izquierda_arriba():
    alto = ventana.window_height() / 2
    if paleta_izquierda.ycor() < alto - 50:
        paleta_izquierda.sety(paleta_izquierda.ycor() + 20)

def paleta_izquierda_abajo():
    alto = ventana.window_height() / 2
    if paleta_izquierda.ycor() > -alto + 50:
        paleta_izquierda.sety(paleta_izquierda.ycor() - 20)

def paleta_derecha_arriba():
    alto = ventana.window_height() / 2
    if paleta_derecha.ycor() < alto - 50:
        paleta_derecha.sety(paleta_derecha.ycor() + 20)

def paleta_derecha_abajo():
    alto = ventana.window_height() / 2
    if paleta_derecha.ycor() > -alto + 50:
        paleta_derecha.sety(paleta_derecha.ycor() - 20)

# Ajustar posiciones dinámicamente
def ajustar_posiciones():
    ancho = ventana.window_width()
    alto = ventana.window_height()
    paleta_izquierda.goto(-ancho / 2 + 50, max(min(paleta_izquierda.ycor(), alto / 2 - 50), -alto / 2 + 50))
    paleta_derecha.goto(ancho / 2 - 50, max(min(paleta_derecha.ycor(), alto / 2 - 50), -alto / 2 + 50))
    ventana.ontimer(ajustar_posiciones, 100)

# Le damos un valor a las teclas para que se puedan mover las palas
ventana.listen()
ventana.onkeypress(paleta_izquierda_arriba, "w")
ventana.onkeypress(paleta_izquierda_abajo, "s")
ventana.onkeypress(paleta_derecha_arriba, "Up")
ventana.onkeypress(paleta_derecha_abajo, "Down")

# Ejecutamos el programa
ajustar_posiciones()
mover_pelota()
ventana.mainloop()
