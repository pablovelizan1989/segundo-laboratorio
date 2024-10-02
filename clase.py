import mysql.connector
from mysql.connector import Error
import json
import datetime
from decouple import config

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
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
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
        self.__descuento_efectivo = self.calcular_descuento()

    @property
    def descuento_efectivo(self):
        return self.__descuento_efectivo

    def calcular_descuento(self):
        if self.producto_vendido > 2:
            return self.producto_vendido * 0.10
        return 0

    def to_dict(self):
        data = super().to_dict()
        data["descuento_efectivo"] = self.descuento_efectivo
        return data

    def __str__(self):
        return f"{super().__str__()} - Descuento: {self.descuento_efectivo}"
    

class VentaLocal(Venta):
    def __init__(self, dni, fecha, cliente, producto_vendido):
        super().__init__(dni, fecha, cliente, producto_vendido)
        self.__envio_gratis = self.calcular_envio_gratis()

    @property
    def envio_gratis(self):
        return self.__envio_gratis

    def calcular_envio_gratis(self):
        return self.producto_vendido > 2

    def to_dict(self):
        data = super().to_dict()
        data["envio_gratis"] = self.envio_gratis
        return data

    def __str__(self):
        return f"{super().__str__()} - Envío gratis: {self.envio_gratis}"

    
class ProductosVendidos:
     
    def __init__(self):
        self.host = config('DB_HOST')
        self.database = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = int(config('DB_PORT')) 

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if connection.is_connected():
                print("Conexión a la base de datos establecida con éxito.")
                return connection
        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
            return None

    def crear_venta(self, venta):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                print(f'Conexión establecida, preparando para insertar venta {venta.cliente}')

                cursor.execute('SELECT dni FROM Venta WHERE dni = %s', (venta.dni,))
                if cursor.fetchone():
                    print(f'Error: Ya existe un cliente con DNI {venta.dni}')
                    return
                
                query = '''
                    INSERT INTO Venta (dni, fecha, cliente, producto_vendido)
                    VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(query, (venta.dni, venta.fecha, venta.cliente, venta.producto_vendido))
                print('Inserción en venta realizada.')

                if isinstance(venta, VentaOnline):
                    query = '''
                        INSERT INTO VentaOnline (dni, fecha, cliente, producto_vendido, descuento_efectivo)
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                    cursor.execute(query, (venta.dni, venta.fecha, venta.cliente, venta.producto_vendido, venta.descuento_efectivo))
                    print('Inserción en VentaOnline realizada.')
                elif isinstance(venta, VentaLocal):
                    query = '''
                        INSERT INTO VentaLocal (dni, fecha, cliente, producto_vendido, envio_gratis)
                        VALUES (%s, %s, %s, %s, %s)
                    '''
                    cursor.execute(query, (venta.dni, venta.fecha, venta.cliente, venta.producto_vendido, venta.envio_gratis))
                    print('Inserción en VentaLocal realizada.')

                connection.commit()
                print(f'Venta {venta.cliente} creada correctamente.')
        except Error as e:
            print(f'Error al conectar a la base de datos: {e}')
        except Exception as e:
            print(f'Error inesperado: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()
                print('Conexión cerrada.')

    def leer_venta(self, dni):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('SELECT * FROM Venta WHERE dni = %s', (dni,))
                    venta_data = cursor.fetchone()

                    if venta_data:
                        venta_data = {k.lower(): v for k, v in venta_data.items()}
                        cursor.execute('SELECT * FROM VentaOnline WHERE dni = %s', (dni,))
                        envio_gratis = cursor.fetchone()

                        if envio_gratis:
                            venta_data['descuento_efectivo'] = envio_gratis['descuento_efectivo']
                            venta = VentaOnline(**venta_data)
                        else:
                            cursor.execute('SELECT * FROM VentaLocal WHERE dni = %s', (dni,))
                            descuento_efectivo = cursor.fetchone()

                            if descuento_efectivo:
                                venta_data['envio_gratis'] = descuento_efectivo['envio_gratis']
                                venta = VentaLocal(**venta_data)
                            else:
                                print(f'No se encontró información específica para el cliente con DNI {dni}.')
                                return
    
                        print(f'Venta encontrado: {venta}')
                    else:
                        print(f'No se encontró venta con DNI {dni}.')
        except Exception as e:
            print(f'Error al leer ventas: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()

    def actualizar_venta(self, dni, campo, nuevo_valor):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM Venta WHERE dni = %s', (dni,))
                    if not cursor.fetchone():
                        print(f'No se encontró venta con DNI {dni}.')
                        return

                    if campo == 'producto_vendido':
                        cursor.execute('UPDATE Venta SET producto_vendido = %s WHERE dni = %s', (nuevo_valor, dni))
                    elif campo == 'fecha':
                        cursor.execute('UPDATE Venta SET fecha = %s WHERE dni = %s', (nuevo_valor, dni))
                    elif campo == 'cliente':
                        cursor.execute('UPDATE Venta SET cliente = %s WHERE dni = %s', (nuevo_valor, dni))
                    elif campo == 'envio_gratis':
                        cursor.execute('UPDATE VentaLocal SET envio_gratis = %s WHERE dni = %s', (nuevo_valor, dni))
                    elif campo == 'descuento_efectivo':
                        cursor.execute('UPDATE VentaOnline SET descuento_efectivo = %s WHERE dni = %s', (nuevo_valor, dni))
                    else:
                        print(f'Campo no reconocido: {campo}')
                        return

                    connection.commit()
                    print(f'Dato {campo} actualizado para el cliente con DNI: {dni}')
        except Exception as e:
            print(f'Error al actualizar el cliente: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()

    def eliminar_venta(self, dni):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute('DELETE FROM Venta WHERE dni = %s', (dni,))
                connection.commit()
                print(f'Venta con DNI {dni} eliminada.')
        except Exception as e:
            print(f'Error al eliminar venta: {e}')
        finally:
            if connection and connection.is_connected():
                connection.close()
