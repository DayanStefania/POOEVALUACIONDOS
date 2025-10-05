from datetime import datetime
import uuid

USUARIO_SISTEMA = "EstudiantePOO"

class Vehiculo:
    def __init__(self, patente: str, peso_kg: float):
        # Datos del vehículo
        self.id_vehiculo = str(uuid.uuid4())
        self.patente = self.validar_patente(patente)
        self.peso_kg = self.validar_peso(peso_kg)
        self.estado = "habilitado" 
        
        self.historial_eventos = []
        self.registrar_evento("Creación", None, f"Inicializado con {peso_kg} kg")

    # --- Validaciones ---
    def validar_patente(self, patente):
        if not patente:
            raise ValueError("¡Patente no puede estar vacía!")
        return patente.upper().strip()
    
    def validar_peso(self, peso):
        if peso <= 0:
            raise ValueError("¡El peso debe ser positivo, mayor que 0 kg!")
        return peso

    # --- Auditoría Básica ---
    def registrar_evento(self, tipo_evento: str, valor_anterior, valor_nuevo):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "usuario": USUARIO_SISTEMA,
            "evento": tipo_evento,
            "anterior": valor_anterior,
            "nuevo": valor_nuevo
        }
        self.historial_eventos.append(evento)

    # --- Operaciones ---
    def actualizar_peso(self, nuevo_peso_kg: float):
        if self.estado == "inhabilitado":
            print(f"[ERROR] Vehículo inhabilitado. No se puede cambiar el peso.")
            return

        try:
            peso_validado = self.validar_peso(nuevo_peso_kg)
            
            if self.peso_kg != peso_validado:
                anterior = self.peso_kg
                self.peso_kg = peso_validado
                self.registrar_evento("Actualización Peso", anterior, self.peso_kg)
                print(f"[OK] Peso cambiado de {anterior} kg a {self.peso_kg} kg.")
            else:
                print("[INFO] El peso es el mismo.")

        except ValueError as e:
            print(f"[RECHAZO] ¡Error de validación al actualizar peso! {e}")


    def inhabilitar(self, motivo: str):
        if self.estado == "habilitado":
            anterior = self.estado
            self.estado = "inhabilitado"
            self.registrar_evento("Cambio Estado", anterior, self.estado)
            print(f"[OK] ¡Inhabilitado! Motivo: {motivo}")
        else:
            print("[INFO] Ya estaba inhabilitado.")

    def habilitar(self, motivo: str):
        if self.estado == "inhabilitado":
            anterior = self.estado
            self.estado = "habilitado"
            self.registrar_evento("Cambio Estado", anterior, self.estado)
            print(f"[OK] ¡Habilitado de nuevo! Motivo: {motivo}")
        else:
            print("[INFO] Ya estaba habilitado.")

    def consultar_ficha(self):
        print("\n--- Ficha del Vehículo ---")
        print(f"Patente: {self.patente}")
        print(f"Peso: {self.peso_kg} kg")
        print(f"Estado: {self.estado}")
        if self.historial_eventos:
            print(f"Último Evento: {self.historial_eventos[-1]['evento']}")
        print("--------------------------")

class Auto(Vehiculo):
    def __init__(self, patente: str, peso_kg: float, asientos_totales: int):
        super().__init__(patente, peso_kg)

        if asientos_totales < 1:
            raise ValueError("El auto debe tener al menos 1 asiento.")
            
        self.asientos_totales = asientos_totales
        self.ocupantes_actuales = 0

        self.eventos_ocupacion = []
        self.registrar_evento_ocupacion("Creación", 0, 0, "Auto listo para ocupación.")


    # --- Auditoría Específica de Ocupación ---
    def registrar_evento_ocupacion(self, accion: str, cantidad: int, ocupantes_antes: int, detalle: str):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "accion": accion,
            "cantidad": cantidad,
            "antes": ocupantes_antes,
            "despues": self.ocupantes_actuales,
            "detalle": detalle
        }
        self.eventos_ocupacion.append(evento)


    # --- Operaciones de Ocupación ---
    def subir_personas(self, n: int):
        if self.estado == "inhabilitado":
            print(f"[ERROR] Auto inhabilitado. ¡No se puede subir gente!")
            return

        if n < 1:
            print("[RECHAZO] Tienes que subir al menos 1 persona.")
            return

        nueva_ocupacion = self.ocupantes_actuales + n

        if nueva_ocupacion > self.asientos_totales:
            print(f"[RECHAZO] ¡Excedes el límite! Asientos totales: {self.asientos_totales}. Intentas subir a {nueva_ocupacion} personas.")
            return
        
        antes = self.ocupantes_actuales
        self.ocupantes_actuales = nueva_ocupacion
        self.registrar_evento_ocupacion("Subida", n, antes, f"Subieron {n} personas.")
        print(f"[OK] Subieron {n}. Ocupantes: {self.ocupantes_actuales}")

    def bajar_personas(self, n: int):
        if self.estado == "inhabilitado":
            print(f"[ERROR] Auto inhabilitado. ¡No se puede bajar gente!")
            return

        if n < 1:
            print("[RECHAZO] Tienes que bajar al menos 1 persona.")
            return

        nueva_ocupacion = self.ocupantes_actuales - n

        if nueva_ocupacion < 0:
            print(f"[RECHAZO] No puedes bajar a {n} personas. Solo hay {self.ocupantes_actuales}.")
            return
        
        antes = self.ocupantes_actuales
        self.ocupantes_actuales = nueva_ocupacion
        self.registrar_evento_ocupacion("Bajada", n, antes, f"Bajaron {n} personas.")
        print(f"[OK] Bajaron {n}. Ocupantes: {self.ocupantes_actuales}")

    def reconfigurar_asientos(self, nuevo_total: int, motivo: str):
        if nuevo_total < 1:
            print("[RECHAZO] El auto debe tener al menos 1 asiento.")
            return

        if self.ocupantes_actuales > nuevo_total:
            print(f"[RECHAZO] ¡Hay {self.ocupantes_actuales} ocupantes! No puedes reducir a {nuevo_total} asientos.")
            return
        
        anterior = self.asientos_totales
        self.asientos_totales = nuevo_total
        self.registrar_evento("Reconfigurar Asientos", anterior, self.asientos_totales)
        print(f"[OK] Asientos cambiados a {self.asientos_totales}. Motivo: {motivo}")

    def vaciar_auto(self, motivo: str):
        if self.ocupantes_actuales > 0:
            a_bajar = self.ocupantes_actuales
            antes = self.ocupantes_actuales
            self.ocupantes_actuales = 0
            self.registrar_evento_ocupacion("Vaciar", a_bajar, antes, f"Vacío por: {motivo}")
            print(f"[OK] Auto completamente vacío. (Bajaron {a_bajar} personas)")
        else:
            print("[INFO] El auto ya está vacío.")

    def consultar_ocupacion(self):
        asientos_libres = self.asientos_totales - self.ocupantes_actuales
        print(f"Ocupantes: {self.ocupantes_actuales} / {self.asientos_totales} | Libres: {asientos_libres}")