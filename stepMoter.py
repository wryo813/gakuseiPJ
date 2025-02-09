import time
# ソケットライブラリ取り込み
import socket

from stspin import (
    SpinChain,
    Constant as StConstant,
    Register as StRegister,
)


# ディジー・チェイン(芋づる式)でモータードライバを接続できるが、1台だけ(total_devices=1)接続する
st_chain = SpinChain(total_devices=3, spi_select=(0, 0))
# 最初(と言っても1台だけだが…)のモータードライバのインスタンスを生成する
motor0 = st_chain.create(0)
motor1 = st_chain.create(1)
motor2 = st_chain.create(2)


# # 200ステップ/秒で10秒間回転させる

while True:
    motor0.run(200)
    time.sleep(10)
    motor0.stopSoft()
    time.sleep(1)
    motor1.run(200)
    time.sleep(10)
    motor1.stopSoft()
    time.sleep(1)
    motor2.run(200)
    time.sleep(10)
    motor2.stopSoft()
    time.sleep(1)
    
# # 逆方向に台形加速しながら500,000ステップ回転させる
# motor.setRegister(StRegister.StepMode, 0x07)
# motor.setRegister(StRegister.SpeedMax, 0x22) #[step/tick]
# motor.setRegister(StRegister.Acc, 0x8A) #[step/tick^2]
# motor.setRegister(StRegister.Dec, 0x8A)
# motor.setDirection(StConstant.DirReverse)
# motor.move(steps=data_)

# # 回転しきるまで待つ
# while motor.isBusy():
#     print("Motor is rolling.")
#     time.sleep(1)

# motor.hiZHard()