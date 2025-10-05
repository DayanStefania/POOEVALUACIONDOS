from datetime import datetime
import uuid
import math
from typing import List

# --- Clases de Auditoría ---

class EventoCatalogo:
    """Clase para registrar eventos de auditoría en los cuerpos celestes."""
    def __init__(self, campo: str, valor_anterior: str, valor_nuevo: str):
        self.fecha_hora = datetime.now()
        self.fecha_formateada = self.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        self.campo_modificado = campo
        self.valor_anterior = valor_anterior
        self.valor_nuevo = valor_nuevo

    def __str__(self):
        return f"[{self.fecha_formateada}] Campo: {self.campo_modificado} | Antes: {self.valor_anterior} | Ahora: {self.valor_nuevo}"

# --- Modelo 1: Cuerpo Celeste ---

class CuerpoCeleste:
    """Clase base para todos los cuerpos celestes."""
    def __init__(self, nombre: str, masa_kg: float):
        # Validaciones iniciales
        if not nombre:
            raise ValueError("El nombre no puede ser vacío.")
        if masa_kg <= 0:
            raise ValueError("La masa inicial debe ser mayor a 0 kg.")
            
        # Datos mínimos
        self.__id_celeste = uuid.uuid4()
        self.__nombre = nombre
        self.__masa_kg = masa_kg
        self.__historial_eventos: List[EventoCatalogo] = []
        
        # Datos derivados/reportables
        self.__fecha_ultima_actualizacion_masa = datetime.now()
        self.__numero_modificaciones = 0
        
        self._registrar_auditoria("ALTA", "N/A", f"Masa: {masa_kg} kg")

    # Propiedades (Getters)
    @property
    def id_celeste(self): return self.__id_celeste
    @property
    def nombre(self): return self.__nombre
    @property
    def masa_kg(self): return self.__masa_kg
    @property
    def historial_eventos(self): return list(self.__historial_eventos)
    @property
    def fecha_ultima_actualizacion_masa(self): return self.__fecha_ultima_actualizacion_masa
    @property
    def numero_modificaciones(self): return self.__numero_modificaciones

    # Métodos de Ayuda
    def _registrar_auditoria(self, campo: str, valor_anterior: str, valor_nuevo: str):
        self.__historial_eventos.append(EventoCatalogo(campo, valor_anterior, valor_nuevo))
        if campo != "ALTA":
            self.__numero_modificaciones += 1
            
    # Operaciones
    def actualizar_nombre(self, nuevo_nombre: str):
        if not nuevo_nombre or nuevo_nombre.strip() == "":
            print("❌ ERROR: El nuevo nombre no puede quedar vacío.")
            return

        nombre_anterior = self.__nombre
        self.__nombre = nuevo_nombre
        self._registrar_auditoria("nombre", nombre_anterior, nuevo_nombre)
        print(f"✅ OK: Nombre de {nombre_anterior} actualizado a **{nuevo_nombre}**.")

    def actualizar_masa(self, nueva_masa: float):
        if nueva_masa <= 0:
            print("❌ ERROR: La nueva masa debe ser mayor a 0 kg.")
            return

        masa_anterior = self.__masa_kg
        self.__masa_kg = nueva_masa
        self.__fecha_ultima_actualizacion_masa = datetime.now()
        
        self._registrar_auditoria("masa_kg", f"{masa_anterior} kg", f"{nueva_masa} kg")
        print(f"✅ OK: Masa de {self.__nombre} actualizada a **{nueva_masa:.2e} kg**.")

    def consultar_ficha(self) -> str:
        output = [
            "\n--- Ficha del Cuerpo Celeste ---",
            f"ID: {self.id_celeste}",
            f"Nombre: **{self.nombre}**",
            f"Masa: {self.masa_kg:.2e} kg",
            f"Última Actualización Masa: {self.fecha_ultima_actualizacion_masa.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Número de Modificaciones: {self.numero_modificaciones}",
            "--- Historial de Eventos (Últimos 3) ---"
        ]
        
        if not self.__historial_eventos:
            output.append("No hay eventos registrados.")
        else:
            for evento in self.__historial_eventos[::-1][:3]:
                output.append(str(evento))
                
        return "\n".join(output)

# --- Modelo 2: Planeta (Extiende CuerpoCeleste) ---

class Planeta(CuerpoCeleste):
    """Extiende CuerpoCeleste con radio y distancia al sol."""
    def __init__(self, nombre: str, masa_kg: float, radio_km: float, distancia_sol_km: float):
        super().__init__(nombre, masa_kg)
        
        if radio_km <= 0:
            raise ValueError("El radio inicial debe ser mayor a 0 km.")
        if distancia_sol_km <= 0:
            raise ValueError("La distancia inicial al sol debe ser mayor a 0 km.")
            
        self.__radio_km = radio_km
        self.__distancia_sol_km = distancia_sol_km
        
        self._registrar_auditoria("ALTA_PLANETA", "N/A", f"Radio: {radio_km} km, Distancia: {distancia_sol_km} km")

    # Propiedades (Getters)
    @property
    def radio_km(self): return self.__radio_km
    @property
    def distancia_sol_km(self): return self.__distancia_sol_km

    @property
    def volumen_km3(self) -> float:
        return (4/3) * math.pi * (self.__radio_km ** 3)

    @property
    def densidad_kg_km3(self) -> float:
        volumen = self.volumen_km3
        return self.masa_kg / volumen if volumen > 0 else 0.0
        
    # Operaciones
    def actualizar_radio(self, nuevo_radio: float):
        if nuevo_radio <= 0:
            print("❌ ERROR: El nuevo radio debe ser mayor a 0 km.")
            return

        radio_anterior = self.__radio_km
        self.__radio_km = nuevo_radio
        
        self._registrar_auditoria("radio_km", f"{radio_anterior} km", f"{nuevo_radio} km")
        print(f"✅ OK: Radio de {self.nombre} actualizado a **{nuevo_radio} km**.")

    def actualizar_distancia_sol(self, nueva_distancia: float):
        if nueva_distancia <= 0:
            print("❌ ERROR: La nueva distancia al sol debe ser mayor a 0 km.")
            return

        distancia_anterior = self.__distancia_sol_km
        self.__distancia_sol_km = nueva_distancia
        
        self._registrar_auditoria("distancia_sol_km", f"{distancia_anterior} km", f"{nueva_distancia} km")
        print(f"✅ OK: Distancia al sol de {self.nombre} actualizada a **{nueva_distancia} km**.")

    def calcular_densidad(self) -> float:
        densidad = self.densidad_kg_km3
        print(f"ⓘ Densidad aproximada de **{self.nombre}**: **{densidad:.6f} kg/km³**.")
        return densidad

    def comparar_distancia(self, otro_planeta) -> str:
        if not isinstance(otro_planeta, Planeta):
            return "❌ ERROR: La comparación de distancia solo es válida con otro objeto de tipo Planeta."

        if self.distancia_sol_km < otro_planeta.distancia_sol_km:
            resultado = f"**{self.nombre}** está más cerca del Sol ({self.distancia_sol_km:,.0f} km) que {otro_planeta.nombre}."
        elif self.distancia_sol_km > otro_planeta.distancia_sol_km:
            resultado = f"**{otro_planeta.nombre}** está más cerca del Sol ({otro_planeta.distancia_sol_km:,.0f} km) que {self.nombre}."
        else:
            resultado = f"Ambos planetas, {self.nombre} y {otro_planeta.nombre}, están a la misma distancia del Sol ({self.distancia_sol_km:,.0f} km)."
        
        print("ⓘ " + resultado)
        return resultado

    # Sobreescribe la ficha
    def consultar_ficha(self) -> str:
        ficha_celeste = super().consultar_ficha()
        
        output = [
            ficha_celeste,
            "\n--- Datos Adicionales (Planeta) ---",
            f"Radio: {self.__radio_km:,.0f} km",
            f"Distancia al Sol: {self.__distancia_sol_km:,.0f} km",
            f"Volumen (Aprox.): {self.volumen_km3:.2e} km³",
            f"Densidad (Aprox.): {self.densidad_kg_km3:.6f} kg/km³"
        ]
        return "\n".join(output)