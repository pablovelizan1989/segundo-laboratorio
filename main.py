import os
import platform
from clase import VentaLocal, VentaOnline, ProductosVendidos

def limpiar_pantalla():
    ''' Limpiar la pantalla según el sistema operativo '''
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')  # para Linux/Unix/MacOS

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
        fecha = input('Ingrese la fecha que desea hacer la compra (Ej. 2024-01-01): ')
        cliente = input('Ingrese apellido y nombre: ')
        
        producto_vendido = int(input('Ingrese la cantidad de celulares que desea comprar: '))
        
        if tipo_venta == '1':
            venta = VentaOnline(dni, fecha, cliente, producto_vendido)
        elif tipo_venta == '2':
            venta = VentaLocal(dni, fecha, cliente, producto_vendido)
        else:
            print('Opción inválida')
            return
        
        ventas.crear_venta(venta)
        print(f'Venta creada y datos guardados exitosamente en el archivo {archivo_ventas}.')
        input('Presione enter para continuar...')
    except ValueError as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f'Error inesperado: {e}')

def buscar_venta_por_dni(ventas):
    dni = input('Ingrese el DNI del cliente a buscar: ') 
    venta = ventas.leer_venta(dni)
    if venta:
        print(venta)
    input('Presione enter para continuar...')

def actualizar_venta(ventas):
    dni = input("Ingrese el DNI del cliente para actualizar la venta: ")
    productos_vendidos = int(input('Ingrese la nueva cantidad de celulares: '))
    ventas.actualizar_venta(dni, productos_vendidos)
    input('Presione enter para continuar...')

def eliminar_venta(ventas):
    dni = input("Ingrese el DNI del cliente a eliminar: ")
    ventas.eliminar_venta(dni)
    input('Presione enter para continuar...')

def mostrar_todas_las_ventas(ventas):
    datos = ventas.leer_datos()
    print('================ Listado Completo de Clientes =================')
    for venta in datos.values():
        print(f"DNI: {venta['dni']}, Cliente: {venta['cliente']}, Fecha: {venta['fecha']}, Productos: {venta['producto_vendido']}")
    print('==============================================================')
    input('Presione enter para continuar...')

if __name__ == "__main__":
    archivo_ventas = 'ventas_db.json'
    ventas = ProductosVendidos(archivo_ventas)
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = input('Seleccione una opción: ')

        if opcion in ['1', '2']:
            agregar_venta(ventas, opcion)
        elif opcion == '3':
            buscar_venta_por_dni(ventas)
        elif opcion == '4':
            actualizar_venta(ventas)
        elif opcion == '5':
            eliminar_venta(ventas)
        elif opcion == '6':
            mostrar_todas_las_ventas(ventas)
        elif opcion == '7':
            print('Saliendo del programa...')
            break
        else:
            print('Opción no válida, por favor, seleccione una opción válida.')