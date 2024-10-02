import os
import platform
from clase import VentaLocal, VentaOnline, ProductosVendidos

def limpiar_pantalla():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def mostrar_menu():
    print('============ Venta de Celulares ============')
    print("1. Comprar por la página web")
    print("2. Comprar en nuestro local")
    print("3. Buscar Cliente por DNI")
    print("4. Actualizar Cliente")
    print("5. Eliminar Cliente por DNI")
    print("6. Mostrar todos los clientes")
    print("7. Salir")
    print("=============================================")

def agregar_venta(ventas, tipo_venta):
    try:
        dni = input('Ingrese DNI del cliente: ')
        fecha = input('Ingrese la fecha de la compra (Ej. 2024-01-01): ')
        cliente = input('Ingrese apellido y nombre: ')
        producto_vendido = int(input('Ingrese la cantidad de celulares que desea comprar: '))
        
        if tipo_venta == '1':
            venta = VentaOnline(dni, fecha, cliente, producto_vendido)
        elif tipo_venta == '2':
            venta = VentaLocal(dni, fecha, cliente, producto_vendido)
        
        ventas.crear_venta(venta)  
        print(f'Venta creada: {venta}')
        input('Presione enter para continuar...')
    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_cliente(ventas):
    dni = input('Ingrese el DNI del cliente a buscar: ') 
    cliente = ventas.leer_venta(dni)  
    if cliente:
        print(cliente)
    else:
        print("Cliente no encontrado.")
    input('Presione enter para continuar...')

def actualizar_venta(ventas):
    dni = input("Ingrese el DNI del cliente para actualizar la venta: ")
    print("¿Qué dato desea actualizar?")
    print("1. Producto vendido")
    print("2. Fecha")
    print("3. Cliente")
    print("4. Envío gratis")
    print("5. Descuento efectivo")
    
    opcion = input("Seleccione una opción (1-5): ")
    
    if opcion == '1':
        nuevo_valor = int(input("Ingrese la nueva cantidad de celulares: "))
        ventas.actualizar_venta(dni, 'producto_vendido', nuevo_valor)
    elif opcion == '2':
        nuevo_valor = input("Ingrese la nueva fecha (YYYY-MM-DD): ")
        ventas.actualizar_venta(dni, 'fecha', nuevo_valor)
    elif opcion == '3':
        nuevo_valor = input("Ingrese el nuevo nombre del cliente: ")
        ventas.actualizar_venta(dni, 'cliente', nuevo_valor)
    elif opcion == '4':
        nuevo_valor = int(input("Ingrese 1 para envío gratis, 0 para no: "))
        ventas.actualizar_venta(dni, 'envio_gratis', nuevo_valor)
    elif opcion == '5':
        nuevo_valor = float(input("Ingrese el nuevo descuento efectivo: "))
        ventas.actualizar_venta(dni, 'descuento_efectivo', nuevo_valor)
    else:
        print("Opción no válida.")
    input('Presione enter para continuar...')

def eliminar_cliente(ventas):
    dni = input("Ingrese el DNI del cliente a eliminar: ")
    ventas.eliminar_venta(dni)  
    print(f'Venta con DNI {dni} eliminada.')
    input('Presione enter para continuar...')

def mostrar_clientes(ventas):
    try:
        connection = ventas.connect()
        if connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute('SELECT * FROM Venta')
                resultados = cursor.fetchall()
                if resultados:
                    print("Clientes registrados:")
                    for row in resultados:
                        print(row)
                else:
                    print("No hay clientes registrados.")
    except Exception as e:
        print(f'Error al mostrar clientes: {e}')
    finally:
        if connection and connection.is_connected():
            connection.close()
    input('Presione enter para continuar...')

if __name__ == "__main__":
    ventas = ProductosVendidos()
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion in ['1', '2']:
            agregar_venta(ventas, opcion)
        elif opcion == '3':
            buscar_cliente(ventas)
        elif opcion == '4':
            actualizar_venta(ventas)
        elif opcion == '5':
            eliminar_cliente(ventas)
        elif opcion == '6':
            mostrar_clientes(ventas)
        elif opcion == '7':
            break
        else:
            print('Opción no válida.')
