# Tomás de Camino Beck, Ph.D
# Universidad CENFOTEC

class Interprete:
    def __init__(self):
        self.comandos = {}

    def registrar(self, nombre, funcion):
        """Registra un comando con su función asociada."""
        self.comandos[nombre] = funcion

    def ejecutar(self, linea):
        """Ejecuta una línea de comando en texto."""
        partes = linea.strip().split()
        if not partes:
            return

        nombre = partes[0]
        args = partes[1:]

        if nombre in self.comandos:
            try:
                # Intenta convertir todos los argumentos a float si es posible
                argumentos = [self._convertir(arg) for arg in args]
                self.comandos[nombre](*argumentos)
            except Exception as e:
                print("Error al ejecutar comando:", nombre)
                print("Detalles:", e)
        else:
            print("Comando no reconocido:", nombre)

    def _convertir(self, valor):
        """Convierte una cadena a int, float o la deja como texto."""
        try:
            if '.' in valor:
                return float(valor)
            return int(valor)
        except ValueError:
            return valor
