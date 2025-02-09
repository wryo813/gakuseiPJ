# ソケットライブラリ取り込み
import socket

# サーバーIPとポート番号
IPADDR = "192.168.0.17"
PORT = 49152

sock_sv = socket.socket(socket.AF_INET)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen()

# クライアントの接続受付
sock_cl, addr = sock_sv.accept()

while True:
    # データ受信
    data = sock_cl.recv(1024)
    data_ = int(data)
    print(data.decode("utf-8"))
    