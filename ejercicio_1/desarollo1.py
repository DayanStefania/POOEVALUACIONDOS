# Modelo 1

from datetime import datetime

class Parcela:

    def __init__(self, id_parcela: str, superficie_ha: float, cultivo_actual: str):
        
        if superficie_ha <= 0:
            raise ValueError("superficie_ha debe ser mayor que 0.")
        if not cultivo_actual:
            raise ValueError("cultivo_actual no puede estar vacío.")
        
        self.id_parcela = id_parcela
        self._superficie_ha = round(superficie_ha, 2)  
        self.cultivo_actual = cultivo_actual
        self._estado = "activa" 
        self._historial_eventos = []
        
        self._registrar_evento("CREACION", "Parcela creada inicialmente.", 
            detalle=f"Superficie: {self._superficie_ha} ha, Cultivo: {self.cultivo_actual}, Estado: {self._estado}")

    @property
    def superficie_ha(self):
        return self._superficie_ha

    @property
    def historial_eventos(self):
        return tuple(self._historial_eventos)
    @property
    def estado(self):
        return self._estado

    def _registrar_evento(self, tipo: str, detalle: str, ** kwargs):
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo,
            "detalle": detalle,
            **kwargs
        }
        self._historial_eventos.append(evento)

    def actualizar_cultivo(self, nuevo_cultivo: str):
        """Actualiza el cultivo actual de la parcela."""
        if self._estado == "inactiva":
            print(f"[RECHAZO] No se puede actualizar el cultivo. La parcela {self.id_parcela} está inactiva.")
            return

        if not nuevo_cultivo:
            raise ValueError("El nuevo cultivo no puede ser una cadena vacía.")

        cultivo_previo = self.cultivo_actual
        self.cultivo_actual = nuevo_cultivo
        self._registrar_evento("ACTUALIZACION_CULTIVO", 
            f"Cambio de cultivo de '{cultivo_previo}' a '{nuevo_cultivo}'.")
        print(f"[INFO] Cultivo actualizado a '{nuevo_cultivo}'.")

    def activar(self, motivo: str):
        """Activa la parcela."""
        if self._estado == "activa":
            print(f"[ADVERTENCIA] La parcela {self.id_parcela} ya está activa.")
            return
            
        self._estado = "activa"
        self._registrar_evento("CAMBIO_ESTADO", 
            f"Parcela activada. Motivo: {motivo}")
        print(f"[INFO] Parcela {self.id_parcela} activada. Motivo: {motivo}")

    def desactivar(self, motivo: str):
        """Desactiva la parcela."""
        if self._estado == "inactiva":
            print(f"[ADVERTENCIA] La parcela {self.id_parcela} ya está inactiva.")
            return

        self._estado = "inactiva"
        self._registrar_evento("CAMBIO_ESTADO", 
            f"Parcela desactivada. Motivo: {motivo}")
        print(f"[INFO] Parcela {self.id_parcela} desactivada. Motivo: {motivo}")

    def rectificar_superficie(self, nueva_superficie: float, motivo: str):
        """Rectifica la superficie_ha de la parcela."""
        if nueva_superficie <= 0:
            raise ValueError("La nueva superficie debe ser mayor que 0.")
        
        superficie_previa = self._superficie_ha
        self._superficie_ha = round(nueva_superficie, 2)
        self._registrar_evento("RECTIFICACION_SUPERFICIE", 
            f"Superficie rectificada. Motivo: {motivo}", 
            valor_previo=superficie_previa, 
            valor_nuevo=self._superficie_ha)
        print(f"[INFO] Superficie de la parcela {self.id_parcela} rectificada de {superficie_previa} ha a {self._superficie_ha} ha.")

# Modelo 2
class ParcelaConRiego(Parcela):
    
    TASA_RIEGO_DEFECTO = 1500.0

    def __init__(self, id_parcela: str, superficie_ha: float, cultivo_actual: str, 
                tasa_riego_l_ha: float = TASA_RIEGO_DEFECTO, umbral_min_litros: float = 0.0):
        
        super().__init__(id_parcela, superficie_ha, cultivo_actual)
        
        self._litros_disponibles = 0.0
        self._tasa_riego_l_ha = self._validar_tasa(tasa_riego_l_ha)
        self._umbral_min_litros = self._validar_umbral(umbral_min_litros)
        
        self._estado_riego = "habilitado" if self.estado == "activa" else "inhabilitado"
        self.eventos_riego = [] # Solo lectura
        
        self._registrar_evento_parcela("CONFIG_RIEGO", f"Sistema de riego asociado. Tasa: {self._tasa_riego_l_ha} L/ha, Umbral: {self._umbral_min_litros} L")

    def desactivar(self, motivo: str):
        """Desactiva la parcela e inhabilita el riego automáticamente."""
        super().desactivar(motivo)
        if self._estado_riego == "habilitado":
            self.inhabilitar_riego(motivo_automatico="Parcela inactiva")

    def _validar_tasa(self, tasa: float):
        if tasa <= 0:
            raise ValueError("La tasa de riego por hectárea debe ser mayor que 0.")
        return tasa

    def _validar_umbral(self, umbral: float):
        if umbral < 0:
            raise ValueError("El umbral mínimo de litros no puede ser negativo.")
        return umbral

    def _registrar_evento_parcela(self, tipo: str, detalle: str, **kwargs):
        """Alias para registrar evento en el historial de la clase base."""
        super()._registrar_evento(tipo, detalle, **kwargs)

    def _registrar_evento_riego(self, litros_solicitados: float, litros_aplicados: float, saldo_antes: float, saldo_despues: float, modo: str):
        """Registra un evento específico de riego."""
        evento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "litros_solicitados": litros_solicitados,
            "litros_aplicados": litros_aplicados,
            "saldo_antes": saldo_antes,
            "saldo_despues": saldo_despues,
            "modo": modo
        }
        self.eventos_riego.append(evento)
        self._registrar_evento_parcela("EVENTO_RIEGO", f"Riego aplicado: {litros_aplicados} L. Modo: {modo}.")
        
    @property
    def litros_disponibles(self):
        return self._litros_disponibles
    
    @property
    def tasa_riego_l_ha(self):
        return self._tasa_riego_l_ha

    @property
    def umbral_min_litros(self):
        return self._umbral_min_litros

    @property
    def estado_riego(self):
        return self._estado_riego
    
    def configurar_tasa(self, l_ha: float):
        """Configura la tasa de riego por hectárea."""
        tasa_previa = self._tasa_riego_l_ha
        self._tasa_riego_l_ha = self._validar_tasa(l_ha)
        self._registrar_evento_parcela("CONFIG_TASA", 
            f"Tasa de riego actualizada de {tasa_previa} L/ha a {self._tasa_riego_l_ha} L/ha.")
        print(f"[INFO] Tasa de riego actualizada a {self._tasa_riego_l_ha} L/ha.")

    def configurar_umbral(self, litros: float):
        """Configura el umbral mínimo de litros disponibles."""
        umbral_previo = self._umbral_min_litros
        self._umbral_min_litros = self._validar_umbral(litros)
        self._registrar_evento_parcela("CONFIG_UMBRAL", 
                f"Umbral mínimo actualizado de {umbral_previo} L a {self._umbral_min_litros} L.")
        print(f"[INFO] Umbral mínimo actualizado a {self._umbral_min_litros} L.")

    def habilitar_riego(self):
        """Habilita el riego si la parcela está activa."""
        if self.estado == "inactiva":
            print(f"[RECHAZO] Riego no se puede habilitar. La parcela {self.id_parcela} está inactiva.")
            return

        if self._estado_riego == "habilitado":
            print(f"[ADVERTENCIA] Riego ya está habilitado.")
            return

        self._estado_riego = "habilitado"
        self._registrar_evento_parcela("CAMBIO_ESTADO_RIEGO", "Riego habilitado.")
        print(f"[INFO] Riego habilitado para parcela {self.id_parcela}.")

    def inhabilitar_riego(self, motivo: str = "Manual", motivo_automatico: str = None):
        """Inhabilita el riego."""
        if self._estado_riego == "inhabilitado":
            print(f"[ADVERTENCIA] Riego ya está inhabilitado.")
            return

        self._estado_riego = "inhabilitado"
        
        if motivo_automatico:
            self._registrar_evento_parcela("CAMBIO_ESTADO_RIEGO", f"Riego inhabilitado automáticamente. Motivo: {motivo_automatico}.")
            print(f"[INFO] Riego inhabilitado automáticamente para parcela {self.id_parcela}. Motivo: {motivo_automatico}")
        else:
            self._registrar_evento_parcela("CAMBIO_ESTADO_RIEGO", f"Riego inhabilitado manualmente. Motivo: {motivo}.")
            print(f"[INFO] Riego inhabilitado para parcela {self.id_parcela}. Motivo: {motivo}")

    def cargar_agua(self, litros: float):
        """Añade agua a los litros disponibles."""
        if litros <= 0:
            print("[ADVERTENCIA] Solo se pueden cargar cantidades positivas de agua.")
            return

        saldo_antes = self._litros_disponibles
        self._litros_disponibles += litros
        saldo_despues = self._litros_disponibles
        
        self._registrar_evento_riego(
            litros_solicitados=litros, litros_aplicados=litros, 
            saldo_antes=saldo_antes, saldo_despues=saldo_despues, 
            modo="CARGA"
        )
        print(f"[INFO] Cargados {litros} L. Saldo actual: {self._litros_disponibles} L.")
    
    def regar_automatico(self, modo: str):
        modo = modo.lower()
        
        if self.estado == "inactiva":
            print(f"[RECHAZO] Riego fallido: Parcela {self.id_parcela} está inactiva.")
            return
        if self._estado_riego == "inhabilitado":
            print(f"[RECHAZO] Riego fallido: Riego inhabilitado para parcela {self.id_parcela}.")
            return
        if self._tasa_riego_l_ha <= 0:
            print(f"[RECHAZO] Riego fallido: Tasa de riego no configurada correctamente ({self._tasa_riego_l_ha} L/ha).")
            return
        if modo not in ["estricto", "parcial"]:
            print(f"[RECHAZO] Riego fallido: Modo de riego '{modo}' no es válido. Use 'estricto' o 'parcial'.")
            return
        
        demanda = round(self.superficie_ha * self._tasa_riego_l_ha, 2)
        litros_aplicados = 0.0
        saldo_antes = self._litros_disponibles
        
        if modo == "estricto":
            saldo_final_esperado = self._litros_disponibles - demanda
            
            if saldo_final_esperado >= self._umbral_min_litros:
                litros_aplicados = demanda
                self._litros_disponibles -= litros_aplicados
                print(f"[APLICADO - ESTRICTO] Riego exitoso: Aplicados {litros_aplicados} L (Demanda: {demanda} L). Saldo final: {self._litros_disponibles} L.")
            else:
                print(f"[RECHAZO - ESTRICTO] Riego rechazado: Aplicar {demanda} L dejaría el saldo ({saldo_final_esperado:.2f} L) por debajo del umbral mínimo ({self._umbral_min_litros} L). Saldo actual: {self._litros_disponibles} L.")
                litros_aplicados = 0.0
        
        elif modo == "parcial":
            max_gasto = self._litros_disponibles - self._umbral_min_litros
            
            if max_gasto <= 0:
                print(f"[RECHAZO - PARCIAL] Riego no es posible: Saldo actual ({self._litros_disponibles} L) es igual o menor al umbral mínimo ({self._umbral_min_litros} L).")
                litros_aplicados = 0.0
            else:
                litros_aplicados = min(demanda, max_gasto)
                self._litros_disponibles -= litros_aplicados
                
                if litros_aplicados == 0:
                    print(f"[RECHAZO - PARCIAL] Riego no es posible. Se necesita más agua. Saldo actual: {self._litros_disponibles} L, Umbral: {self._umbral_min_litros} L.")
                elif litros_aplicados < demanda:
                    print(f"[APLICADO - PARCIAL] Riego parcial aplicado: Aplicados {litros_aplicados:.2f} L (Demanda: {demanda:.2f} L). Saldo final: {self._litros_disponibles:.2f} L (Exactamente el umbral si el saldo fue el limitante).")
                else:
                    print(f"[APLICADO - PARCIAL] Riego exitoso: Aplicados {litros_aplicados:.2f} L (Demanda completa: {demanda:.2f} L). Saldo final: {self._litros_disponibles:.2f} L.")

        if litros_aplicados > 0:
            self._registrar_evento_riego(
                litros_solicitados=demanda, litros_aplicados=litros_aplicados, 
                saldo_antes=saldo_antes, saldo_despues=self._litros_disponibles, 
                modo=modo
            )
        else:
            self._registrar_evento_parcela("RIEGO_RECHAZADO", f"Intento de riego {modo} con demanda {demanda} L fue rechazado.")