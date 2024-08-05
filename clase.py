import json
from datetime import datetime

class Venta:
    def __init__(self, dni, fecha, cliente, producto_vendido):
        self.__dni = self.validar_dni(dni)
        self.__fecha = self.validar_fecha(fecha)
        self.__cliente = cliente  
        self.__producto_vendido = self.validar_producto(producto_vendido)

    @property
    def dni(self):
        return self.__dni
    
    @property
    def fecha(self):
        return self.__fecha
    
    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def producto_vendido(self):
        return self.__producto_vendido
    
    def validar_fecha(self, fecha_str):
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            return fecha
        except ValueError:
            raise ValueError("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")

    def validar_producto(self, producto):
        try:
            cantidad_producto = int(producto)
            return cantidad_producto
        except ValueError:
            raise ValueError("La cantidad ingresada no es correcta")
        
    def validar_dni(self, dni):
        try:
            dni_num = int(dni)
            if len(str(dni)) not in [7, 8]:
                raise ValueError("El DNI debe tener 7 u 8 dígitos")
            if dni_num <= 0:
                raise ValueError("El DNI debe ser un número positivo")
            return dni_num
        except ValueError:
            raise ValueError("El DNI debe ser numérico y estar compuesto por 7 u 8 dígitos")
            
    def to_dict(self):
        return {
            "dni": self.dni,
            "fecha": str(self.fecha),
            "cliente": self.cliente,
            "producto_vendido": self.producto_vendido,
        }

    def __str__(self):
        return f"{self.fecha} {self.cliente}"  
    
class VentaOnline(Venta):
    def __init__(self, dni, fecha, cliente, producto_vendido):
        super().__init__(dni, fecha, cliente, producto_vendido)
        self.__envio_gratis = self.producto_vendido >= 2

    @property
    def envio_gratis(self):
        return self.__envio_gratis

    def to_dict(self):
        data = super().to_dict()
        data["envio_gratis"] = self.envio_gratis
        return data

    def __str__(self):
        return f"{super().__str__()} - Envío gratis: {self.envio_gratis}"
    
class VentaLocal(Venta):
    def __init__(self, dni, fecha, cliente, producto_vendido):
        super().__init__(dni, fecha, cliente, producto_vendido)
        self.__descuento_efectivo = self.producto_vendido >= 2

    @property
    def descuento_efectivo(self):
        return self.__descuento_efectivo

    def to_dict(self):
        data = super().to_dict()
        data["descuento"] = self.descuento_efectivo
        return data

    def __str__(self):
        return f"{super().__str__()} - Descuento: {self.descuento_efectivo}"
    
class ProductosVendidos:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
            print(f'Archivo {self.archivo} creado y datos guardados exitosamente.')
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')

    def crear_venta(self, venta):
        try:
            datos = self.leer_datos()
            dni = venta.dni
            if str(dni) not in datos.keys():
                datos[dni] = venta.to_dict()
                self.guardar_datos(datos)
                print(f'Guardado exitoso')
            else:
                print(f'Cliente con DNI {dni} ya existe')
        except Exception as error:
            print(f'Error inesperado al crear la venta: {error}')

    def leer_venta(self, dni):
        try:
            datos = self.leer_datos()
            if dni in datos:
                venta_data = datos[dni]
                if 'envio_gratis' in venta_data:
                    venta_data.pop('envio_gratis') 
                if 'descuento' in venta_data:
                    venta_data.pop('descuento') 

                if 'envio_gratis' in venta_data: 
                    venta = VentaOnline(venta_data['dni'], venta_data['fecha'], venta_data['cliente'], venta_data['producto_vendido'])
                else:
                    venta = VentaLocal(venta_data['dni'], venta_data['fecha'], venta_data['cliente'], venta_data['producto_vendido'])
                
                print(f'Venta encontrada con el DNI {dni}')
                return venta
            else:
                print(f'No se encontró cliente con ese DNI {dni}')  
        except Exception as e:
            print(f'Error al leer ventas: {e}')

    def actualizar_venta(self, dni, producto_vendido):
        try:
            datos = self.leer_datos()
            if str(dni) in datos.keys():
                datos[dni]['producto_vendido'] = producto_vendido
                self.guardar_datos(datos)
                print(f'Cantidad de productos actualizada para el cliente con DNI: {dni}')
            else:
                print(f'No se encontró al cliente con DNI: {dni}')
        except Exception as e:
            print(f'Error al actualizar la cantidad de productos: {e}')
    
    def eliminar_venta(self, dni):
        try:
            datos = self.leer_datos()
            if str(dni) in datos.keys():
                del datos[dni]
                self.guardar_datos(datos)
                print(f'Cliente con DNI: {dni} eliminado correctamente')
            else:
                print(f'No se encontró cliente con DNI: {dni}')
        except Exception as e:
            print(f'Error al eliminar al cliente: {e}')