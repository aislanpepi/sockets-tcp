import socket
import threading

clientes = {}

def broadcast(mensagem, cliente_atual):
    for cliente in clientes:
        if cliente != cliente_atual:
            try:
                cliente.send(mensagem)
            except:
                cliente.close()
                if cliente in clientes:
                    del clientes[cliente]

def lidar_com_cliente(cliente, endereco):
    while True:
        try:
            mensagem = cliente.recv(1024)
            if not mensagem:
                break
            texto = f"[{endereco[0]}:{endereco[1]}] {mensagem.decode('utf-8')}"
            broadcast(texto.encode('utf-8'), cliente)
        except:
            cliente.close()
            if cliente in clientes:
                del clientes[cliente]
            break

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('0.0.0.0', 5555))
    servidor.listen()

    print("Servidor iniciado. Aguardando conexões...")

    while True:
        cliente, endereco = servidor.accept()
        print(f"Conectado com {endereco}")
        clientes[cliente] = endereco
        cliente.send("Conectado ao servidor!".encode('utf-8'))

        thread = threading.Thread(target=lidar_com_cliente, args=(cliente, endereco))
        thread.start()

iniciar_servidor()
