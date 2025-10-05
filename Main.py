#-----------------------------------------EJERCICIO 1------------------------------

# from ejercicio_1.desarollo1 import ParcelaConRiego
# import sys

# def separador(titulo):
#     print("\n" + "="*80)
#     print(f"--- {titulo} ---")
#     print("="*80)

# def main():
#     separador("1. CREACIÓN DE PARCELA Y ASOCIACIÓN DE RIEGO")
    
#     try:
#         parcela_riego = ParcelaConRiego(
#             id_parcela="A-42", 
#             superficie_ha=10.50, 
#             cultivo_actual="Trigo"
#         )
#         print(f"Parcela ID: {parcela_riego.id_parcela}, Superficie: {parcela_riego.superficie_ha} ha, Cultivo: {parcela_riego.cultivo_actual}, Estado: {parcela_riego.estado}")
        
#     except ValueError as e:
#         print(f"Error al crear la parcela: {e}")
#         sys.exit(1)
        
#     separador("2. ACTUALIZAR CULTIVO")
#     parcela_riego.actualizar_cultivo("Maíz")
#     print(f"Nuevo Cultivo: {parcela_riego.cultivo_actual}")


#     separador("3. CONFIGURAR RIEGO Y CARGAR AGUA")
    

#     parcela_riego.configurar_tasa(1500.0) 
#     parcela_riego.configurar_umbral(2000.0)
#     parcela_riego.cargar_agua(20000.0)
    
#     print(f"Litros Disponibles: {parcela_riego.litros_disponibles} L")
#     print(f"Tasa Riego: {parcela_riego.tasa_riego_l_ha} L/ha, Umbral Mínimo: {parcela_riego.umbral_min_litros} L")


#     separador("4. RIEGO ESTRICTO (ÉXITO)")

#     parcela_riego.regar_automatico("estricto")
#     print(f"Litros Disponibles después de riego estricto: {parcela_riego.litros_disponibles} L")

#     separador("5. DESACTIVAR PARCELA E INTENTAR RIEGO")
    
#     parcela_riego.desactivar("Rotación de cultivo finalizada")

#     print(f"Estado de Riego: {parcela_riego.estado_riego}") 
    
#     parcela_riego.regar_automatico("estricto")

#     separador("6. RIEGO PARCIAL (APLICACIÓN MÁXIMA PERMITIDA)")

#     parcela_riego.activar("Inicio de nueva temporada")
#     parcela_riego.habilitar_riego()
    
#     saldo_actual = parcela_riego.litros_disponibles
    
#     parcela_parcial = ParcelaConRiego(id_parcela="B-12", superficie_ha=10.50, cultivo_actual="Avena")
#     parcela_parcial.configurar_tasa(1500.0)
#     parcela_parcial.configurar_umbral(2000.0)
#     parcela_parcial.cargar_agua(3000.0)
    
#     print(f"\n--- Prueba Riego Parcial en Parcela B-12 ---")
#     print(f"Demanda: 15750 L, Saldo Inicial: {parcela_parcial.litros_disponibles} L, Umbral: {parcela_parcial.umbral_min_litros} L")

#     parcela_parcial.regar_automatico("parcial")
#     print(f"Litros Disponibles después de riego parcial: {parcela_parcial.litros_disponibles} L")

#     separador("7. INTENTO DE MODIFICACIÓN DIRECTA DE ATRIBUTOS (ENCAPSULAMIENTO)")
    
#     try:
#         parcela_riego.litros_disponibles = 100000.0
#     except AttributeError as e:
#         print(f"[BLOQUEADO] Intento de fijar 'litros_disponibles' fallido (Correcto): {e}")

#     try:
#         parcela_riego.superficie_ha = 5.0 
#     except AttributeError as e:
#         print(f"[BLOQUEADO] Intento de fijar 'superficie_ha' fallido (Correcto): {e}")
#     print(f"Superficie actual (sin cambios): {parcela_riego.superficie_ha} ha")
    
#     separador("8. REVISIÓN DE HISTORIALES")
    
#     print("\n--- ÚLTIMOS EVENTOS DE LA PARCELA A-42 (HISTORIAL GENERAL) ---")
#     for evento in parcela_riego.historial_eventos[-5:]:
#         print(f"[{evento['fecha']}] {evento['tipo']}: {evento['detalle']}")
        
#     print("\n--- ÚLTIMOS EVENTOS DE RIEGO A-42 ---")
#     for evento in parcela_riego.eventos_riego[-1:]:
#         print(f"[{evento['fecha']}] Aplicados: {evento['litros_aplicados']} L, Saldo Antes: {evento['saldo_antes']} L, Modo: {evento['modo']}")

# if __name__ == "__main__":
#     main()

#----------------------------------EJERCICIO 2-------------------------------------

# from ejercicio_2.desarollo2 import Publicacion, Libro
# import sys

# def separador(titulo):
#     """Función simple para separar las secciones de prueba."""
#     print("\n" + "—"*80)
#     print(f"--- {titulo} ---")
#     print("—"*80)

# def main():
    
#     separador("1. PRUEBA DE RECHAZO: AÑO INVÁLIDO (Regla Publicacion)")
#     try:
#         Publicacion(id_publicacion="P-001", titulo="Los Canterbury Tales", anio=1400)
#     except ValueError as e:
#         print(f"[RECHAZO - ÉXITO] El sistema bloqueó la creación correctamente: {e}")
    
#     separador("2. CREACIÓN DE LIBRO Y ESTADO INICIAL")
#     try:
#         libro_gabo = Libro(
#             id_publicacion="L-002", 
#             titulo="Cien años de soledad", 
#             anio=1967, 
#             paginas_totales=500
#         )
#         print(f"Libro creado: {libro_gabo.titulo} ({libro_gabo.anio}) con {libro_gabo.paginas_totales} páginas.")
#     except Exception as e:
#         print(f"Error fatal al crear el libro: {e}")
#         sys.exit(1)

#     separador("3. ACTUALIZACIÓN DE CAMPO HEREDADO (AÑO)")
#     libro_gabo.actualizar_anio(1980)
#     print(f"Año actual del libro: {libro_gabo.anio}")

#     separador("4. OPERACIÓN DE LECTURA SIMPLE: leer(120)")
#     libro_gabo.leer(120)
    
#     libro_gabo.consultar_progreso()
#     print(f"Páginas leídas: {libro_gabo.paginas_leidas} (120/500 = 24%)")

#     separador("5. PRUEBA DE RECHAZO/AJUSTE: SUPERAR EL TOTAL DE PÁGINAS")

#     libro_gabo.leer(400) 
#     libro_gabo.consultar_progreso()
#     print(f"Páginas leídas finales: {libro_gabo.paginas_leidas} (Esperado: 500)")

#     libro_gabo.leer(-10) 

#     separador("6. INTENTO DE ALTERACIÓN DIRECTA (Encapsulamiento)")
    
#     print("Intentando alterar paginas_leidas directamente...")
#     try:
#         libro_gabo.paginas_leidas = 0 
#     except AttributeError as e:
#         print(f"[BLOQUEADO - ÉXITO] No se pudo alterar 'paginas_leidas' directamente: {e}")

#     print("Intentando alterar paginas_totales directamente...")
#     try:
#         libro_gabo.paginas_totales = 100 
#     except AttributeError as e:
#         print(f"[BLOQUEADO - ÉXITO] No se pudo alterar 'paginas_totales' directamente: {e}")

#     separador("7. REVISIÓN DE HISTORIALES")
    
#     print("--- Historial General del Libro (L-002) ---")

#     for evento in libro_gabo.historial_eventos:
#         print(f"[{evento['fecha']}] {evento['tipo']}: {evento['detalle']}")
        
#     print("\n--- Eventos de Lectura (Registros detallados) ---")
#     for evento in libro_gabo.eventos_lectura:
#         print(f"[{evento['fecha']}] Leídas ahora: {evento['paginas_leidas_ahora']} | Acumulado: {evento['paginas_acumuladas']}")

# if __name__ == "__main__":
#     main()

#----------------------------------------- Ejercicio 3 ---------------------------------------
# from ejercicio_3.desarollo3 import Actividad,Carrera

# def main():
#     print("--- 1. CREACIÓN DE ACTIVIDAD 'Yoga' ---")
#     try:

#         actividad_yoga = Actividad("Yoga", 60)
#         print(f"Creada: {actividad_yoga}")
#         print(f"Historial inicial: {len(actividad_yoga.historial_eventos)} evento(s)")
#     except Exception as e:
#         print(f"[ERROR CRÍTICO]: {e}")
    
#     print("-" * 20)
# # 2
#     print("--- 2. CREACIÓN CON DURACIÓN INVÁLIDA (0 min) ---")

#     try:
#         Actividad("Estiramiento", 0)
#     except ValueError as e:
#         print(f"[RECHAZO OK] Error al crear actividad con duración 0 min: {e}")
#     except Exception as e:
#         print(f"[ERROR NO ESPERADO]: {e}")
    
#     print("-" * 20)
# # 3
#     print("--- 3. CREACIÓN DE CARRERA (10 km en 50 min) ---")

#     try:
#         carrera_10k = Carrera("Carrera Matutina", 50, 10.0)
#         print(f"Creada: {carrera_10k}")
#     except Exception as e:
#         print(f"[ERROR CRÍTICO]: {e}")
    
#     print("-" * 20)
# # 4
#     print("--- 4. CÁLCULO DE RITMO (50 min / 10 km) ---")
#     # Criterio: calcular_ritmo() devuelve 5 min/km.
#     try:
#         ritmo = carrera_10k.calcular_ritmo()
#         print(f"Ritmo calculado: {ritmo} min/km")
#         assert ritmo == 5.0, "El ritmo no es 5.0 min/km"
#         print("[CRITERIO OK] El ritmo es correcto (5.0 min/km).")
#     except Exception as e:
#         print(f"[ERROR]: {e}")

#     print("-" * 20)
# # 5
#     print("--- 5. REGISTRAR DISTANCIA INVÁLIDA (-3 km) ---")
    
#     try:
#         carrera_10k.registrar_distancia(-3.0)
#     except ValueError as e:
#         print(f"[RECHAZO OK] Error al registrar distancia -3 km: {e}")
#     except Exception as e:
#         print(f"[ERROR NO ESPERADO]: {e}")
    
#     print("-" * 20)
# # 6
#     print("--- 6. ACTUALIZAR DURACIÓN DE CARRERA (50 min -> 55 min) ---")
#     duracion_anterior = carrera_10k.duracion_min
#     try:
#         carrera_10k.actualizar_duracion(55)
#         print(f"Nueva duración: {carrera_10k.duracion_min} min")
#         print(f"Historial general de carrera (último evento):")
        
#         ultimo_evento = carrera_10k.historial_eventos[-1]
#         print(f"   Fecha: {ultimo_evento['fecha']}")
#         print(f"   Campo: {ultimo_evento['campo']}, Valor Ant: {ultimo_evento['valor_anterior']}, Valor Nuevo: {ultimo_evento['valor_nuevo']}")
        
#         assert ultimo_evento['campo'] == 'duracion_min' and ultimo_evento['valor_nuevo'] == 55
#         print("[CRITERIO OK] La duración se actualizó y el cambio está en historial_eventos.")
        
#         nuevo_ritmo = carrera_10k.calcular_ritmo()
#         print(f"Nuevo ritmo calculado (55 min / 10 km): {nuevo_ritmo} min/km")
#     except Exception as e:
#         print(f"[ERROR]: {e}")

#     print("-" * 20)
# # 7
#     print("--- 7. INTENTO DE ALTERAR DISTANCIA DIRECTAMENTE (RECHAZO) ---")
#     try:
#         carrera_10k._distancia_km = 99.0 
#         print(f"[¡ADVERTENCIA!] Se pudo cambiar el valor directamente (distancia_km = {carrera_10k.distancia_km}).")

#         carrera_10k.distancia_km = 5.0
#     except AttributeError as e:
#         print(f"[RECHAZO OK] Error al intentar asignar a la propiedad/getter 'distancia_km': {e}")
#     except Exception as e:
#         print(f"[RECHAZO OK] El intento falló: {e}")

#     # Verificamos que el valor no cambió
#     print(f"Valor real de distancia_km después del intento de alteración: {carrera_10k.distancia_km} km")
#     if carrera_10k.distancia_km != 5.0:
#         print("[CRITERIO OK] El valor de distancia_km NO pudo ser alterado directamente.")

#     print("\n=========================================================")
#     print("            FIN DE LAS EJECUCIONES")
#     print("=========================================================")

# if __name__ == "__main__":
#     main()    
#----------------------------------------- Ejercicio 4 ------------------------------------------
# from ejercicio_4.desarollo4 import Vehiculo, Auto

# def main():
#     print("--- 1. PRUEBAS CON VEHÍCULO BASE ---")

#     try:
#         camioneta = Vehiculo("ABCD12", 1450.0)
#         print(f"Vehículo creado: Patente {camioneta.patente}, Estado: {camioneta.estado}")
#     except Exception as e:
#         print(f"[ERROR CRÍTICO] Falló la creación: {e}")
#         return

#     print("\n-- Prueba de Peso OK --")
#     camioneta.actualizar_peso(1500.0)
    
#     print("\n-- Prueba de Peso Inválido (0 kg) --")
#     camioneta.actualizar_peso(0)

#     print("\n-- Prueba de Estado (Inhabilitar) --")
#     camioneta.inhabilitar("mantención")
    
#     print("\n-- Prueba de Operación en Inhabilitado --")
#     camioneta.actualizar_peso(1600.0) 
    
#     print("\n-- Prueba de Estado (Habilitar) --")
#     camioneta.habilitar("mantención finalizada")
#     camioneta.actualizar_peso(1600.0)
    
#     camioneta.consultar_ficha()
    
#     print("-" * 60)

#     print("--- 2. PRUEBAS CON AUTO ---")
    
#     auto_familiar = Auto("XYZ789", 1200.0, 5)
#     print(f"Auto creado: Patente {auto_familiar.patente}, Asientos: {auto_familiar.asientos_totales}")
#     auto_familiar.consultar_ocupacion()

#     print("\n-- Prueba de Subir Personas --")

#     auto_familiar.subir_personas(3)

#     auto_familiar.subir_personas(3) 
#     auto_familiar.consultar_ocupacion()

#     print("\n-- Prueba de Bajar Personas --")

#     auto_familiar.bajar_personas(2)

#     auto_familiar.bajar_personas(5)
#     auto_familiar.consultar_ocupacion()

#     print("\n-- Prueba de Reconfiguración de Asientos --")

#     auto_familiar.reconfigurar_asientos(2, "instalación de equipo")

#     auto_familiar.reconfigurar_asientos(0, "error de prueba")
    
#     print("\n-- Prueba de Estado Inhabilitado en Auto --")

#     auto_familiar.inhabilitar("inspección de asientos")
#     auto_familiar.subir_personas(1)
    
#     auto_familiar.habilitar("inspección finalizada")

#     print("\n-- Prueba de Vaciar Auto --")
#     auto_familiar.vaciar_auto("fin de turno")
    
#     print("-" * 60)

#     print("--- 3. AUDITORÍA ---")

#     print(f"\nHistorial General de '{auto_familiar.patente}':")
#     for ev in auto_familiar.historial_eventos:
#         print(f"  [{ev['fecha']}] {ev['evento']} | Antes: {ev['anterior']}, Nuevo: {ev['nuevo']}")

#     print(f"\nHistorial de Ocupación de '{auto_familiar.patente}':")
#     for ev in auto_familiar.eventos_ocupacion:
#         print(f"  [{ev['fecha']}] {ev['accion']} ({ev['cantidad']}) | Ocupantes: {ev['antes']} -> {ev['despues']}")

# if __name__ == "__main__":
#     main()
#---------------------------------- Ejercicio 5 ------------------------------
# from ejercicio_5.desarollo5 import EventoCatalogo,CuerpoCeleste,Planeta

# def main():
#     print("=" * 70)
#     print("  INICIO: EJECUCIÓN DE CRITERIOS DE ACEPTACIÓN ")
#     print("=" * 70)

#     estrella_x = CuerpoCeleste("Estrella X", 2e30)
#     print(f"Cuerpo Celeste creado: ** {estrella_x.nombre} **")

#     Tierra = Planeta("Tierra", 5.97e24, 6371.0, 149600000.0)
#     print(f"Planeta creado: ** {Tierra.nombre} **")

#     Marte = Planeta("Marte", 6.42e23, 3389.0, 227900000.0)
#     print(f"Planeta creado: ** {Marte.nombre} **")
    
#     print("\n" + "--- Pruebas de Cálculos y Comparación ---")

#     Tierra.calcular_densidad()

#     Tierra.comparar_distancia(Marte)

#     print("\n--- Pruebas de Rechazo (Inicialización) ---")
#     try:
#         Planeta("Invalido_Radio", 1000, 0, 1000)
#     except ValueError as e:
#         print(f"RECHAZO ESPERADO: {e}")
        
#     try:
#         Planeta("Invalido_Distancia", 1000, 1000, -500)
#     except ValueError as e:
#         print(f"RECHAZO ESPERADO: {e}")

#     print("\n--- Prueba de Actualización y Auditoría ---")
#     Tierra.actualizar_masa(6.0e24)
    
#     try:
#         Tierra.actualizar_masa(5.97e24)
#         Tierra.__masa_kg = 1.0 
#         print(" Nota de Python: La modificación directa a '__masa_kg' no afecta la masa real que se usa en los métodos.")
#     except AttributeError:
        
#         print("\n" + "=" * 30 + f"\nFICHA FINAL: {Tierra.nombre}")
#     print(Tierra.consultar_ficha())
    
#     print("\n" + "=" * 30 + f"\nFICHA FINAL: {estrella_x.nombre}")
#     estrella_x.actualizar_nombre("Estrella Alfa")
#     print(estrella_x.consultar_ficha())

#     print("\n" + "=" * 70)
#     print("  FIN: EJECUCIÓN DE CRITERIOS DE ACEPTACIÓN")
#     print("=" * 70)

# if __name__ == "__main__":
#     main()