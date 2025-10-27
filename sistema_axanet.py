import os
import datetime
import re


class SistemaClientesAxanet:
    def __init__(self, directorio="axanet_clientes_python"):
        self.directorio = directorio
        self.clientes = {}  # Diccionario para asociar nombres con archivos

        # Crear el directorio si no existe
        if not os.path.exists(self.directorio):
            os.makedirs(self.directorio)

        # Cargar clientes existentes
        self.cargar_clientes_existentes()

    def cargar_clientes_existentes(self):
        """Carga los clientes existentes en el diccionario"""
        for archivo in os.listdir(self.directorio):
            if archivo.endswith(".txt"):
                nombre_cliente = archivo[:-4]  # Eliminar la extensión .txt
                self.clientes[nombre_cliente] = archivo

    def normalizar_nombre(self, nombre):
        """Convierte el nombre a formato de archivo (sin espacios, minúsculas)"""
        return nombre.lower().replace(" ", "_")

    def generar_id_cliente(self, nombre):
        """Genera un ID único para el cliente basado en el nombre y la fecha"""
        fecha_actual = datetime.datetime.now().strftime("%Y%m%d")
        nombre_normalizado = self.normalizar_nombre(nombre)
        return f"{nombre_normalizado}_{fecha_actual}"

    def crear_nuevo_cliente(self):
        """Crea un nuevo cliente y su archivo"""
        print("\n--- CREAR NUEVO CLIENTE ---")
        nombre = input("Nombre del cliente: ").strip()

        if not nombre:
            print("Error: El nombre no puede estar vacío.")
            return

        nombre_normalizado = self.normalizar_nombre(nombre)
        archivo_cliente = f"{nombre_normalizado}.txt"

        # Verificar si el cliente ya existe
        if nombre_normalizado in self.clientes:
            print(f"Error: Ya existe un cliente con el nombre '{nombre}'.")
            return

        # Solicitar información adicional
        telefono = input("Teléfono: ").strip()
        correo = input("Correo electrónico: ").strip()
        descripcion_servicio = input("Descripción del primer servicio: ").strip()

        # Generar datos automáticos
        id_cliente = self.generar_id_cliente(nombre)
        fecha_registro = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fecha_servicio = datetime.datetime.now().strftime("%Y-%m-%d")

        # Crear el contenido del archivo
        contenido = f"Nombre: {nombre}\n"
        contenido += f"ID_Cliente: {id_cliente}\n"
        contenido += f"Teléfono: {telefono}\n"
        contenido += f"Correo: {correo}\n"
        contenido += f"FechaRegistro: {fecha_registro}\n\n"
        contenido += "SERVICIOS:\n"
        contenido += f"  - Fecha: {fecha_servicio}, Descripción: {descripcion_servicio}\n"

        # Guardar el archivo
        ruta_archivo = os.path.join(self.directorio, archivo_cliente)
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)

        # Actualizar el diccionario
        self.clientes[nombre_normalizado] = archivo_cliente

        print(f"\nCliente '{nombre}' creado exitosamente.")
        print(f"Archivo: {archivo_cliente}")

    def visualizar_cliente(self):
        """Muestra la información de un cliente específico"""
        print("\n--- VISUALIZAR CLIENTE ---")

        if not self.clientes:
            print("No hay clientes registrados.")
            return

        nombre = input("Nombre del cliente a visualizar: ").strip()
        nombre_normalizado = self.normalizar_nombre(nombre)

        if nombre_normalizado not in self.clientes:
            print(f"Error: No se encontró el cliente '{nombre}'.")
            return

        archivo_cliente = self.clientes[nombre_normalizado]
        ruta_archivo = os.path.join(self.directorio, archivo_cliente)

        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()

            print(f"\n--- INFORMACIÓN DE {nombre.upper()} ---")
            print(contenido)
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo del cliente.")

    def listar_todos_clientes(self):
        """Lista todos los clientes existentes"""
        print("\n--- LISTA DE TODOS LOS CLIENTES ---")

        if not self.clientes:
            print("No hay clientes registrados.")
            return

        for i, (nombre_normalizado, archivo) in enumerate(self.clientes.items(), 1):
            nombre_formateado = nombre_normalizado.replace("_", " ").title()
            print(f"{i}. {nombre_formateado} (Archivo: {archivo})")

    def agregar_servicio(self):
        """Agrega un nuevo servicio a un cliente existente"""
        print("\n--- AGREGAR SERVICIO A CLIENTE ---")

        if not self.clientes:
            print("No hay clientes registrados.")
            return

        nombre = input("Nombre del cliente: ").strip()
        nombre_normalizado = self.normalizar_nombre(nombre)

        if nombre_normalizado not in self.clientes:
            print(f"Error: No se encontró el cliente '{nombre}'.")
            return

        archivo_cliente = self.clientes[nombre_normalizado]
        ruta_archivo = os.path.join(self.directorio, archivo_cliente)

        # Leer el contenido actual
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo del cliente.")
            return

        # Solicitar nueva descripción del servicio
        nueva_descripcion = input("Descripción del nuevo servicio: ").strip()
        fecha_servicio = datetime.datetime.now().strftime("%Y-%m-%d")

        # Encontrar la línea donde empiezan los servicios
        indice_servicios = -1
        for i, linea in enumerate(lineas):
            if linea.strip() == "SERVICIOS:":
                indice_servicios = i
                break

        # Agregar el nuevo servicio
        if indice_servicios != -1:
            nueva_linea = f"  - Fecha: {fecha_servicio}, Descripción: {nueva_descripcion}\n"
            lineas.insert(indice_servicios + 1, nueva_linea)
        else:
            # Si no hay sección de servicios, crear una
            lineas.append("\nSERVICIOS:\n")
            lineas.append(f"  - Fecha: {fecha_servicio}, Descripción: {nueva_descripcion}\n")

        # Guardar el archivo actualizado
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.writelines(lineas)

        print(f"\nNuevo servicio agregado al cliente '{nombre}'.")

    def eliminar_cliente(self):
        """Elimina un cliente existente"""
        print("\n--- ELIMINAR CLIENTE ---")

        if not self.clientes:
            print("No hay clientes registrados.")
            return

        nombre = input("Nombre del cliente a eliminar: ").strip()
        nombre_normalizado = self.normalizar_nombre(nombre)

        if nombre_normalizado not in self.clientes:
            print(f"Error: No se encontró el cliente '{nombre}'.")
            return

        # Confirmar eliminación
        confirmacion = input(f"¿Está seguro de que desea eliminar al cliente '{nombre}'? (s/n): ").strip().lower()

        if confirmacion == 's':
            archivo_cliente = self.clientes[nombre_normalizado]
            ruta_archivo = os.path.join(self.directorio, archivo_cliente)

            try:
                os.remove(ruta_archivo)
                del self.clientes[nombre_normalizado]
                print(f"Cliente '{nombre}' eliminado exitosamente.")
            except FileNotFoundError:
                print(f"Error: No se pudo encontrar el archivo del cliente.")
        else:
            print("Eliminación cancelada.")

    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 50)
        print("    SISTEMA DE GESTIÓN DE CLIENTES - AXANET")
        print("=" * 50)
        print("1. Crear nuevo cliente")
        print("2. Visualizar información de un cliente")
        print("3. Listar todos los clientes")
        print("4. Agregar servicio a cliente existente")
        print("5. Eliminar cliente")
        print("6. Salir")
        print("-" * 50)

    def ejecutar(self):
        """Ejecuta el sistema principal"""
        print("Bienvenido al Sistema de Gestión de Clientes de Axanet")

        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción (1-6): ").strip()

            if opcion == "1":
                self.crear_nuevo_cliente()
            elif opcion == "2":
                self.visualizar_cliente()
            elif opcion == "3":
                self.listar_todos_clientes()
            elif opcion == "4":
                self.agregar_servicio()
            elif opcion == "5":
                self.eliminar_cliente()
            elif opcion == "6":
                print("¡Gracias por usar el Sistema de Gestión de Clientes de Axanet!")
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 6.")

            input("\nPresione Enter para continuar...")


# Ejecutar el sistema
if __name__ == "__main__":
    sistema = SistemaClientesAxanet()
    sistema.ejecutar()