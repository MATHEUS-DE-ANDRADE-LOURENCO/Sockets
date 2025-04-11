import socket
import threading
import os

HOST = '0.0.0.0'
PORT = 12345

clientes = []

def broadcast(msg, conexao):
    for cliente in clientes:
        if cliente != conexao:
            try:
                cliente.sendall(msg)
            except:
                clientes.remove(cliente)

def ouvir_cliente(conexao, end):
    print(f"[+] Nova conexão de {end}")
    clientes.append(conexao)
    try:
        while True:
            header = conexao.recv(1024).decode()
            if not header:
                break

            if header.startswith("FILE:"):
                filename = header[5:]
                with open(f"received_{filename}", "wb") as f:
                    while True:
                        data = conexao.recv(1024)
                        if data == b"<EOF>":
                            break
                        f.write(data)
                print(f"[Arquivo recebido] {filename}")
            else:
                print(f"[{end}] {header}")
                broadcast(header.encode(), conexao)
    finally:
        print(f"[-] Conexão encerrada: {end}")
        clientes.remove(conexao)
        conexao.close()

def main():
    print("[*] Iniciando servidor...")
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()

    print(f"[*] Servidor ouvindo em {HOST}:{PORT}")
    while True:
        conexao, end = servidor.accept()
        thread = threading.Thread(target=ouvir_cliente, args=(conexao, end))
        thread.start()

main()
