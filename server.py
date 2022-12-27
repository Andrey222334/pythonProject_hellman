import socket

def server_key_send_receive(b, g, p, A):
    B = g**b % p
    K_b = A**b % p  # Ключ сервера
    return (B, K_b)

sock = socket.socket()

sock.bind(('', 9090))
print("Запуск сервера...")

sock.listen(1)
print("Начало прослушивания порта...")

while True:

    conn, addr = sock.accept()
    print("Подключился клиент: ", addr)

    print("Введите секретное число b: ")
    b = int(input())
    print("Начало передачи данных...")
    data = conn.recv(1024)
    msg = data.decode()
    msg = msg.split()
    msg = list(map(int, msg))
    g = msg[0]
    p = msg[1]
    A = msg[2]
    server_rec = server_key_send_receive(b, g, p, A)
    B = server_rec[0]
    K = server_rec[1]
    print("KEY:", K)
    print("Сообщение от клиента:", msg)
    print("Конец передачи данных...")
    print("Начало отправки данных...")
    conn.send(str(B).encode())
    print("Конец отправки данных...")
    conn.close()
    print("Клиент отключился")
    print("Введите <<exit>> для выхода")
    work_case = input()
    if work_case == "exit":
        break
print("Сервер остановлен...")
