# Modelo 1
from datetime import datetime

class Publicacion:
    MIN_ANIO = 1450 

    def __init__(self, id_publicacion: str, titulo: str, anio: int):
    
        if not titulo:
            raise ValueError("El título no puede estar vacío.")
        if anio < self.MIN_ANIO:
            raise ValueError(f"El año de publicación debe ser >= {self.MIN_ANIO}.")

        self.id_publicacion = id_publicacion
        self._titulo = titulo
        self._anio = anio
        self._historial_eventos = []

        self._registrar_evento("CREACION", "Publicación creada.", 
            detalle=f"Título: {self._titulo}, Año: {self._anio}")

    @property
    def titulo(self):
        return self._titulo
    
    @property
    def anio(self):
        return self._anio
        
    @property
    def historial_eventos(self):

        return list(self._historial_eventos)

# --- Método Auxiliar ---
    def _registrar_evento(self, tipo: str, detalle: str, campo: str = None, valor_previo: any = None, valor_nuevo: any = None):
        """Método interno para registrar cualquier cambio con marca de tiempo."""
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "detalle": detalle,
            "campo_modificado": campo,
            "valor_anterior": valor_previo,
            "valor_nuevo": valor_nuevo
        }
        self._historial_eventos.append(evento)

    # --- Operaciones ---
    def actualizar_titulo(self, nuevo_titulo: str):
        """Actualiza el título de la publicación, validando que no sea vacío."""
        if not nuevo_titulo:
            print("[RECHAZO] El nuevo título no puede ser una cadena vacía.")
            return

        titulo_previo = self._titulo
        self._titulo = nuevo_titulo
        self._registrar_evento("ACTUALIZACION", 
            f"Título actualizado de '{titulo_previo}' a '{self._titulo}'.",
            campo="titulo", 
            valor_previo=titulo_previo, 
            valor_nuevo=self._titulo)
        print(f"[INFO] Título de '{titulo_previo}' actualizado a '{self._titulo}'.")

    def actualizar_anio(self, nuevo_anio: int):
        """Actualiza el año, validando que sea >= 1450."""
        if nuevo_anio < self.MIN_ANIO:
            print(f"[RECHAZO] El año {nuevo_anio} es inválido. Debe ser >= {self.MIN_ANIO}.")
            return

        anio_previo = self._anio
        self._anio = nuevo_anio
        self._registrar_evento("ACTUALIZACION", 
            f"Año actualizado de {anio_previo} a {self._anio}.",
            campo="anio", 
            valor_previo=anio_previo, 
            valor_nuevo=self._anio)
        print(f"[INFO] Año actualizado a {self._anio}.")

#Modelo 2

class Libro(Publicacion):
    
    def __init__(self, id_publicacion: str, titulo: str, anio: int, paginas_totales: int):
        
        super().__init__(id_publicacion, titulo, anio)
        
        if paginas_totales <= 0:
            raise ValueError("Las páginas totales deben ser un número positivo.")
        

        self._paginas_totales = paginas_totales
        self._paginas_leidas = 0
        self.eventos_lectura = [] 

        self._registrar_evento("CONFIGURACION_LIBRO", 
            f"Libro configurado con {self._paginas_totales} páginas totales.")

    @property
    def paginas_totales(self):
        return self._paginas_totales

    @property
    def paginas_leidas(self):
        return self._paginas_leidas
    
    def _registrar_evento_lectura(self, paginas_leidas_ahora: int, acumulado_despues: int):
        """Registra un evento específico de lectura."""
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "paginas_leidas_ahora": paginas_leidas_ahora,
            "paginas_acumuladas": acumulado_despues
        }
        self.eventos_lectura.append(evento)
        
        self._registrar_evento("LECTURA", f"Leídas {paginas_leidas_ahora} páginas. Acumulado: {acumulado_despues}.")

    # --- Operaciones ---
    def leer(self, paginas: int):
        """Incrementa las páginas leídas, validando que no se lean páginas negativas o más de las restantes."""
        
        if paginas <= 0:
            print("[RECHAZO] Debes indicar un número positivo de páginas para leer.")
            return

        paginas_restantes = self._paginas_totales - self._paginas_leidas

        if paginas_restantes == 0:
            print(f"[RECHAZO] ¡Felicidades! Ya terminaste este libro.")
            return

        if paginas > paginas_restantes:
            paginas_a_leer = paginas_restantes
            print(f"[ADVERTENCIA] Intentaste leer {paginas} páginas, pero solo quedan {paginas_restantes}. Leyendo el resto.")
        else:
            paginas_a_leer = paginas
            
        self._paginas_leidas += paginas_a_leer

        self._registrar_evento_lectura(paginas_a_leer, self._paginas_leidas)
        
        print(f"[INFO] Leídas {paginas_a_leer} páginas. Total leído: {self._paginas_leidas} de {self._paginas_totales}.")

    def consultar_progreso(self) -> str:
        """Devuelve el porcentaje de progreso de lectura redondeado."""
        if self._paginas_totales == 0:
            return "0%"