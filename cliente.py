import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 12345

def receber_msg(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print("\n[Mensagem recebida]:", msg)
        except:
            print("[!] Conexão encerrada.")
            break

def enviar_arq(sock):
    arqs = [f for f in os.listdir() if os.path.isfile(f)]
    print("\n=== Arquivos disponíveis ===")
    for i, file in enumerate(arqs):
        print(f"{i + 1}: {file}")
    opc = int(input("Escolha o número do arquivo para enviar: ")) - 1
    nome_arq = arqs[opc]

    sock.sendall(f"FILE:{nome_arq}".encode())
    with open(nome_arq, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sock.sendall(data)
    sock.sendall(b"<EOF>")
    print(f"[+] Arquivo '{nome_arq}' enviado.")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    threading.Thread(target=receber_msg, args=(sock,), daemon=True).start()

    while True:
        print("\n=== MENU ===")
        print("1. Enviar mensagem")
        print("2. Enviar arquivo")
        print("3. Sair")
        op = input("Escolha: ")

        if op == "1":
            msg = input("Digite a mensagem: ")
            sock.sendall(msg.encode())
        elif op == "2":
            enviar_arq(sock)
        elif op == "3":
            sock.close()
            break
        else:
            print("Opção inválida.")

main()
