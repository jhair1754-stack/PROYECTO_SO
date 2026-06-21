import socket
import threading

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 8089

# Diccionario global para almacenar los clientes activos: { "nombre_usuario": socket_conexion }
clientes_activos = {}
# Lock para garantizar el acceso seguro al diccionario desde múltiples hilos
lock = threading.Lock()

def client_handler(conn, address):
    """
    Maneja la comunicación individual de un cliente conectado.
    Ejecutado en un hilo independiente para evitar el bloqueo del servidor.
    """
    print(f"[CONEXIÓN] Nueva conexión establecida desde {address[0]}:{address[1]}")
    username = None
    destinatario = None
    
    try:
        # 1. Registro e Identificación del Cliente (El primer mensaje recibido)
        # Esperamos el nombre de usuario de forma inicial
        username_data = conn.recv(1024).decode('utf-8').strip()
        if not username_data:
            print(f"[REGISTRO] Cliente desde {address} no envió un nombre de usuario y se desconectó.")
            conn.close()
            return
        
        username = username_data
        
        # Validar si el nombre ya existe o está vacío
        with lock:
            if not username or username in clientes_activos:
                conn.send("ERROR: El nombre de usuario ya está en uso o no es válido. Conexión rechazada.\n".encode('utf-8'))
                conn.close()
                print(f"[REGISTRO] Conexión rechazada: el usuario '{username}' ya está activo o es inválido.")
                return
            
            # Registrar al cliente en el diccionario global
            clientes_activos[username] = conn
            
        print(f"[REGISTRO] Cliente registrado exitosamente como '{username}'")
        bienvenida = (
            f"Servidor: ¡Bienvenido '{username}' al chat concurrente!\n"
            f"Comandos disponibles:\n"
            f"  > Lista           - Ver los usuarios conectados actualmente.\n"
            f"  > NombreUsuario   - Habilitar canal de comunicación con ese usuario (ej: > C2).\n"
            f"  > END o > EXIT    - Desconectarse del chat de forma limpia.\n"
        )
        conn.send(bienvenida.encode('utf-8'))
        
        # 2. Bucle principal de escucha para este cliente
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                # Si el socket se cierra de forma no controlada por el cliente
                break
            
            mensaje = data.strip()
            if not mensaje:
                continue
            
            # Control de comandos especiales
            if mensaje.startswith('>'):
                comando = mensaje.upper()
                
                # Comando de salida
                if comando in ('> END', '> EXIT'):
                    conn.send("Servidor: Desconexión solicitada. ¡Adiós!\n".encode('utf-8'))
                    break
                
                # Comando para listar usuarios activos
                elif comando == '> LISTA':
                    with lock:
                        lista_usuarios = list(clientes_activos.keys())
                    respuesta_lista = f"Servidor: Usuarios conectados actualmente: {lista_usuarios}\n"
                    conn.send(respuesta_lista.encode('utf-8'))
                
                # Selección de destino
                else:
                    # El comando es el nombre del destinatario
                    # Quitamos el '>' y los espacios adicionales
                    posible_destinatario = mensaje[1:].strip()
                    
                    with lock:
                        existe_dest = posible_destinatario in clientes_activos
                    
                    if existe_dest:
                        destinatario = posible_destinatario
                        conn.send(f"Servidor: Canal con '{destinatario}' habilitado. Los siguientes mensajes se enviarán directamente.\n".encode('utf-8'))
                    else:
                        conn.send(f"Servidor: El usuario '{posible_destinatario}' no está conectado o no existe.\n".encode('utf-8'))
            
            # Envío de mensajes comunes
            else:
                if destinatario:
                    with lock:
                        socket_dest = clientes_activos.get(destinatario)
                    
                    if socket_dest:
                        try:
                            # Formato clásico en pantalla: "C1: Hola"
                            formato_mensaje = f"{username}: {mensaje}\n"
                            socket_dest.send(formato_mensaje.encode('utf-8'))
                        except (ConnectionResetError, BrokenPipeError):
                            conn.send(f"Servidor: Error al enviar mensaje. '{destinatario}' se desconectó abruptamente.\n".encode('utf-8'))
                            destinatario = None
                    else:
                        conn.send(f"Servidor: El usuario '{destinatario}' ya no está conectado.\n".encode('utf-8'))
                        destinatario = None
                else:
                    conn.send("Servidor: No has seleccionado un destinatario. Usa '> NombreUsuario' para elegir con quién hablar.\n".encode('utf-8'))
                    
    except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError) as e:
        print(f"[ERROR] Conexión rota con el cliente '{username or address}': {e}")
    finally:
        # 3. Desconexión Limpia y Controlada
        if username:
            with lock:
                if username in clientes_activos:
                    del clientes_activos[username]
            print(f"[DESCONEXIÓN] Cliente '{username}' ({address[0]}:{address[1]}) se ha desconectado.")
        else:
            print(f"[DESCONEXIÓN] Conexión desde {address[0]}:{address[1]} finalizada sin registro.")
            
        try:
            conn.close()
        except OSError:
            pass

def server_program():
    """
    Inicializa el socket del servidor, lo vincula a la interfaz/puerto y escucha nuevas conexiones.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reutilizar la dirección local inmediatamente si el servidor se reinicia
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
    except Exception as e:
        print(f"[ERROR] No se pudo vincular el socket a {HOST}:{PORT}: {e}")
        return
        
    server_socket.listen(5)
    print(f"[INICIADO] Servidor TCP escuchando en {HOST}:{PORT} (Backlog=5)...")
    
    try:
        while True:
            conn, address = server_socket.accept()
            # Crear e iniciar un nuevo hilo para manejar al cliente de manera concurrente
            thread = threading.Thread(target=client_handler, args=(conn, address), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n[APAGANDO] Servidor interrumpido por el usuario (Ctrl+C). Cerrando...")
    finally:
        server_socket.close()

if __name__ == '__main__':
    server_program()
