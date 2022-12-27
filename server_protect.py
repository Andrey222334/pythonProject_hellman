import socket

def get_key_server():
    with open('key_server.txt', 'r') as txt:
        for row in txt:
            return row

def check_key(key):
    key_list = []
    with open('access.txt', 'r') as txt:
        for row in txt:
            key_list.append(row.replace('\n', ''))

        if not(str(key) in key_list):
            print('Сертификат доступа не существует')
            quit()

def client_key_send(a, g, p):
    A = g**a % p
    return A

def server_key_send_receive(b, g, p, A):
    B = g**b % p
    K_b = A**b % p  # Server key
    return (B, K_b)

def client_receive(B, a, p):
    K_a = B**a % p  # Client key
    return K_a

def vernam(line):  # Vernam encoding (2-side)
    key = '00001111'
    if len(key) != 8:
        print('Ключ меньше 8')
        quit()

    code_list = []
    for sym in line:

        bin_sym = bin(ord(sym))[2:]
        if len(bin_sym) != 8:
            bin_sym = '0' + bin_sym
            while len(bin_sym) != 8:
                bin_sym = '0' + bin_sym
        encrypt_sym = ''

        for i in range(len(key)):
            if bin_sym[i] == key[i]:
                encrypt_sym += '0'
            else:
                encrypt_sym += '1'

        code_list.append('0b'+encrypt_sym)
    sym_encrypt_list = list(map(lambda x: chr(int(x, base=2)), code_list))  # Symbol encoding
    return ''.join(sym_encrypt_list)

sock = socket.socket()

sock.bind(('', 9090))
print("Запуск сервера...")

sock.listen(1)
print("Начало прослушивания порта...")

while True:

    conn, addr = sock.accept()
    print("Подключился клиент: ", addr)

    b = int(get_key_server())

    print("Начало передачи данных...")
    data = conn.recv(1024)
    msg = data.decode()
    msg = vernam(msg)
    msg = msg.split()
    msg = list(map(int, msg))
    g = msg[0]
    p = msg[1]
    A = msg[2]
    server_rec = server_key_send_receive(b, g, p, A)
    B = server_rec[0]
    K = server_rec[1]
    check_key(K)
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
