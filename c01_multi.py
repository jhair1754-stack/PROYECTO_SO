import socket
import threading
import sys
import time

# Bandera global para coordinar la finalización limpia de los hilos
stop_chat = False

def receive_messages(client_socket):
    """
    Hilo secundario: Recibe continuamente mensajes desde el servidor y los muestra en pantalla.
    """
    global stop_chat
    while not stop_chat:
        try:
            # Leer datos del servidor
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                # El servidor cerró la conexión
                if not stop_chat:
                    print("\n[INFO] Conexión cerrada por el servidor.")
                break
            
            # Comprobar si hubo un error de registro en el servidor
            if data.startswith("ERROR:"):
                print(f"\n[RECHAZADO] {data.strip()}")
                stop_chat = True
                break
                
            # Asegurar que el mensaje termine con salto de línea para formatear correctamente el prompt
            if not data.endswith('\n'):
                data += '\n'
                
            # Imprimir el mensaje de forma limpia
            # \r mueve el cursor al inicio de la línea para reescribir el prompt " -> "
            sys.stdout.write(f"\r{data} -> ")
            sys.stdout.flush()
            
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            if not stop_chat:
                print("\n[ERROR] Conexión perdida con el servidor.")
            break
            
    stop_chat = True

def client_program():
    """
    Programa principal del cliente: Conecta al servidor y maneja el envío de datos.
    """
    global stop_chat
    print("=========================================")
    print("   CLIENTE DE CHAT TCP CONCURRENTE       ")
    print("=========================================")
    
    # Solicitar datos de conexión
    host_input = input("Introduce la IP del Servidor (Enter para 127.0.0.1): ").strip()
    host = host_input if host_input else '127.0.0.1'
    
    port_input = input("Introduce el puerto del Servidor (Enter para 8089): ").strip()
    port = int(port_input) if port_input else 8089
    
    # Solicitar nombre de usuario
    username = ""
    while not username:
        username = input("Introduce tu nombre de usuario (ej. C1, C2): ").strip()
        if not username:
            print("El nombre de usuario no puede estar vacío.")
        elif '>' in username or ' ' in username:
            print("El nombre de usuario no puede contener espacios ni el carácter '>'.")
            username = ""

    # Crear socket de conexión
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"[CONECTADO] Conectado exitosamente al servidor {host}:{port}")
    except Exception as e:
        print(f"[ERROR] No se pudo establecer conexión con el servidor: {e}")
        return

    try:
        # 1. Enviar el nombre de usuario como primer mensaje para el registro
        client_socket.send(username.encode('utf-8'))
        
        # Dar un breve instante para procesar el registro y recibir la bienvenida
        time.sleep(0.2)
        
        # 2. Iniciar el hilo de recepción en segundo plano
        recv_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
        recv_thread.start()
        
        # 3. Bucle de envío (Hilo principal)
        print(" -> ", end="", flush=True)
        while not stop_chat:
            try:
                # Leer entrada del usuario
                message = sys.stdin.readline()
                if not message:
                    # Si detecta EOF (Ctrl+D / Ctrl+Z)
                    break
                
                # Si el hilo de recepción detuvo el chat (ej. desconexión remota)
                if stop_chat:
                    break
                    
                message_stripped = message.strip()
                if not message_stripped:
                    # Si se presiona enter vacío, reimprimir el prompt
                    sys.stdout.write(" -> ")
                    sys.stdout.flush()
                    continue
                
                # Enviar mensaje al servidor
                client_socket.send(message_stripped.encode('utf-8'))
                
                # Si el usuario ingresó un comando de salida
                if message_stripped.upper() in ('> END', '> EXIT'):
                    stop_chat = True
                    break
                
                # Reimprimir el prompt si no es un comando de salida
                if not stop_chat:
                    sys.stdout.write(" -> ")
                    sys.stdout.flush()
                    
            except (KeyboardInterrupt, SystemExit):
                print("\n[SALIDA] Interrupción por teclado detectada. Saliendo...")
                try:
                    client_socket.send("> EXIT".encode('utf-8'))
                except OSError:
                    pass
                stop_chat = True
                break
                
    except OSError as e:
        print(f"\n[ERROR] Error de red: {e}")
    finally:
        stop_chat = True
        client_socket.close()
        print("[DESCONECTADO] Conexión cerrada. ¡Hasta luego!")

if __name__ == '__main__':
    client_program()
