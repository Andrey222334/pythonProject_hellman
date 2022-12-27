import socket

def client_key_send(a, g, p):
    A = g**a % p
    return A

def client_receive(B, a, p):
    K_a = B**a % p  # Client key
    return K_a

sock = socket.socket()

sock.connect(('localhost', 9090))
print("Установка соединения с сервером")

print("Введите число g: ")
g = int(input())
print("Введите число p: ")
p = int(input())
print("Введите секретное число a: ")
a = int(input())
A = client_key_send(a, g, p)
msg = str(g) + " " + str(p) + " " + str(A)
sock.send(msg.encode())
print("Отправка данных")
K = ""
print("Начало приёма данных от сервера")
data = sock.recv(1024)
K = client_receive(int(data.decode()), a, p)
print("KEY:", K)
print("Сообщение от сервера: ", data.decode())
print("Конец приёма данных от сервера")

sock.close()
print("Разрыв соединения с сервером")
