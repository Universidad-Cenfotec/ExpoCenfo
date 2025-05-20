from interprete import Interprete

# === Definir funciones que usará el intérprete ===
def mover(distancia):
    print("Moviendo", distancia, "cm")

def girar(angulo):
    print("Girando", angulo, "grados")

def decir(texto):
    print("Mensaje:", texto)

def parar():
    print("Robot detenido")

# === Crear el intérprete y registrar comandos ===
i = Interprete()
i.registrar("mover", mover)
i.registrar("girar", girar)
i.registrar("decir", decir)
i.registrar("parar", parar)

# === Bucle principal de lectura desde consola serial ===
print("Intérprete listo. Escribe comandos:")

while True:
    try:
        linea = input(">> ")
        i.ejecutar(linea)
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
        break
    except Exception as e:
        print("Error general:", e)
