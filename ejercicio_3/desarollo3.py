from datetime import datetime
import uuid 

class Actividad:
    def __init__(self, nombre: str, duracion_min: int):
        self._id_actividad = str(uuid.uuid4())
        self._nombre = self._validar_nombre(nombre)
        self._duracion_min = self._validar_duracion(duracion_min)
        self._historial_eventos = []
        self._registrar_evento("Creación", None, f"Actividad: {nombre}, Duración: {duracion_min} min")

    # --- Propiedades (Getters) ---
    @property
    def id_actividad(self):
        return self._id_actividad

    @property
    def nombre(self):
        return self._nombre

    @property
    def duracion_min(self):
        return self._duracion_min

    @property
    def historial_eventos(self):

        return self._historial_eventos[:]

    # --- Métodos de Validación Internos ---
    def _validar_nombre(self, nombre):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la actividad no puede estar vacío.")
        return nombre.strip()

    def _validar_duracion(self, duracion):
        if not isinstance(duracion, int) or duracion < 1:
            raise ValueError("La duración debe ser un número entero y al menos 1 minuto.")
        return duracion

    # --- Método de Registro de Historial ---
    def _registrar_evento(self, campo_modificado: str, valor_anterior, valor_nuevo):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "campo": campo_modificado,
            "valor_anterior": valor_anterior,
            "valor_nuevo": valor_nuevo
        }
        self._historial_eventos.append(evento)

    # --- Operaciones ---
    def actualizar_nombre(self, nuevo_nombre: str):
        nombre_validado = self._validar_nombre(nuevo_nombre)
        if self._nombre != nombre_validado:
            anterior = self._nombre
            self._nombre = nombre_validado
            self._registrar_evento("nombre", anterior, self._nombre)
            print(f"[OK] Nombre actualizado de '{anterior}' a '{self._nombre}'.")
        else:
            print("[INFO] El nombre es el mismo, no se realiza la actualización.")

    def actualizar_duracion(self, nueva_duracion: int):
        duracion_validada = self._validar_duracion(nueva_duracion)
        if self._duracion_min != duracion_validada:
            anterior = self._duracion_min
            self._duracion_min = duracion_validada
            self._registrar_evento("duracion_min", anterior, self._duracion_min)
            print(f"[OK] Duración actualizada de {anterior} min a {self._duracion_min} min.")
        else:
            print("[INFO] La duración es la misma, no se realiza la actualización.")

    def __str__(self):
        return f"Actividad: {self.nombre} | Duración: {self.duracion_min} min | ID: {self.id_actividad[:8]}..."
    
class Carrera(Actividad):
    def __init__(self, nombre: str, duracion_min: int, distancia_km: float):
        super().__init__(nombre, duracion_min)
        self._distancia_km = 0.0
        self._eventos_registro = []

        self.registrar_distancia(distancia_km)


    # --- Propiedad (Getter) para el dato adicional ---
    @property
    def distancia_km(self):
        return self._distancia_km

    @property
    def eventos_registro(self):

        return self._eventos_registro[:]

    # --- Métodos de Validación Internos ---
    def _validar_distancia(self, distancia):

        if not isinstance(distancia, (int, float)) or distancia <= 0:
            raise ValueError("La distancia debe ser un número positivo (mayor a 0 km).")
        return float(distancia)

    # --- Operaciones Adicionales ---
    def registrar_distancia(self, nueva_distancia: float):
        distancia_validada = self._validar_distancia(nueva_distancia)

        self._distancia_km = distancia_validada

        registro = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "distancia_registrada": self._distancia_km,
            "duracion_acumulada": self.duracion_min
        }
        self._eventos_registro.append(registro)
        print(f"[OK] Distancia registrada: {self._distancia_km} km. Historial de registro actualizado.")

    def calcular_ritmo(self) -> float:

        if self._distancia_km <= 0:
            raise RuntimeError("No se puede calcular el ritmo. La distancia debe ser mayor a 0 km.")
        
        ritmo = self.duracion_min / self._distancia_km
        return round(ritmo, 2)

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str.replace('Actividad', 'Carrera')} | Distancia: {self.distancia_km} km"