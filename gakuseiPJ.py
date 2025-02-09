import time
import RPi.GPIO as GPIO
import socket

from stspin import (
    SpinChain,
    Constant as StConstant,
    Register as StRegister,
)

# ピンの定義
SW1_PIN = 22
SW2_PIN = 23
SW3_PIN = 24
SW4_PIN = 27

# サーバーIPとポート番号
IPADDR = "192.168.11.3"
PORT   = 49152

# ディジー・チェインでモータードライバを接続（total_devices=3, spi_select=(0, 0)）
st_chain = SpinChain(total_devices=3, spi_select=(0, 0))
# 各モータードライバのインスタンス生成
moter_x = st_chain.create(0)
moter_y1 = st_chain.create(1)
moter_y2 = st_chain.create(2)

# ボタン押下時のコールバック関数
def SW1_stop(channel):
    print("button pushed", channel)
    moter_x.stopSoft()

def SW2_stop(channel):
    print("button pushed", channel)
    moter_x.stopSoft()

# GPIOの設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SW1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SW4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(SW1_PIN, GPIO.RISING, callback=SW1_stop, bouncetime=300)
GPIO.add_event_detect(SW2_PIN, GPIO.RISING, callback=SW2_stop, bouncetime=300)

# TCPサーバソケットの作成（SOCK_STREAMを指定）
sock_sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# TIME_WAIT状態でも再利用できるようにSO_REUSEADDRオプションを設定
sock_sv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_sv.bind((IPADDR, PORT))
sock_sv.listen(1)
print("TCPサーバを開始。クライアントの接続待ちです。")

sock_cl, addr = sock_sv.accept()
print("接続完了:", addr)

try:
    while True:
        # データ受信（1024バイトまで）
        data = sock_cl.recv(1024)
        if not data:
            print("クライアントが切断しました。")
            break  # 接続が切断された場合はループを終了

        # 受信したバイナリデータをUTF-8としてデコードする
        try:
            data_str = data.decode("utf-8").strip()
        except UnicodeDecodeError:
            print("受信したデータはUTF-8でデコードできませんでした。バイナリデータが送られた可能性があります。")
            continue  # デコードできない場合は次のデータ受信へ

        # 文字列を整数に変換
        try:
            step_count = int(data_str)
        except ValueError:
            print("受信したデータは整数ではありません:", data_str)
            continue

        print("受信したステップ数:", step_count)

        # モーターの設定（各レジスタの値は例示）
        moter_x.setRegister(StRegister.StepMode, 0x07)
        moter_x.setRegister(StRegister.SpeedMax, 0x22)
        moter_x.setRegister(StRegister.Acc, 0x8A)
        moter_x.setRegister(StRegister.Dec, 0x8A)
        moter_x.setDirection(StConstant.DirReverse)
        moter_x.move(steps=step_count)

        # モーターの回転が完了するまで待機
        while moter_x.isBusy():
            print("Motor is rolling.")
            time.sleep(1)

        # モーターの保持電流を停止
        moter_x.hiZHard()
        print("モーター動作完了。")

except Exception as e:
    print("エラー発生:", e)
finally:
    sock_cl.close()
    sock_sv.close()
