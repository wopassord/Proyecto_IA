from procesador_imagenes import ProcesadorImagenes

def main():
    # Rutas principales
    carpeta_redimensionamiento_origen = "C:\\Users\\Bernarda\\Desktop\\Proyecto IA\\DB"
    carpeta_redimensionamiento_destino = "C:\\Users\\Bernarda\\Desktop\\Proyecto IA\\Test_Redim"

    carpeta_filtros_origen = "C:\\Users\\Bernarda\\Desktop\\Proyecto IA\\Test_Redim"
    carpeta_filtros_destino = "C:\\Users\\Bernarda\\Desktop\\Proyecto IA\\Test_Filtros"

    # Crear instancia del procesador
    procesador = ProcesadorImagenes()


    while True:
        #Menú de opciones
            print("\n------- Opciones de Procesamiento -------")
            print("1. Redimensionar imágenes")
            print("2. Aplicar filtros gaussianos")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                 print("Redimensionando imágenes...")
                 procesador.redimensionar_carpeta(carpeta_redimensionamiento_origen, carpeta_redimensionamiento_destino)
                 print("Redimensionamiento completado.")
            if opcion == "2":
                 print("Aplicando filtros gaussianos...")
                 procesador.aplicar_filtros_gaussianos(carpeta_filtros_origen, carpeta_filtros_destino)
                 print("Filtrado Gaussiano completado.")
            if opcion == "3":
                 print("Saliendo...")
                 break
            else:
                 print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
