#!/usr/bin/env python3
import pigpio
import time
import sys

# 使用するGPIOピン番号（BCM番号）とPWM周波数の設定
SERVO_GPIO = 12      # GPIO12
PWM_FREQUENCY = 50   # サーボモータ用PWMは50Hz（周期20ms）

def set_servo_angle(pi, angle):
    """
    サーボモータを指定の角度に移動させる関数
    角度は 0～180° で指定する。
    
    サーボの駆動はパルス幅により行い、以下のように設定する：
      0°   → 0.5ms（500µs）のパルス幅
      180° → 2.5ms（2500µs）のパルス幅
      
    線形補間により、任意の角度に対応するパルス幅を計算します。
    """
    if angle < 0 or angle > 180:
        raise ValueError("角度は0〜180度の範囲で指定してください。")
    
    # パルス幅の計算 (µs)
    # 0° のとき: 500µs, 180° のとき: 2500µs
    # 線形補間: pulse_width = 500 + (angle/180) * 2000
    pulse_width = 500 + (angle / 180.0) * 2000
    
    # hardware_PWM の dutycycle は 0～1,000,000 の値
    # 50Hzの場合、周期は 20,000µs なので、
    # dutycycle = pulse_width * (1,000,000 / 20,000) = pulse_width * 50
    dutycycle = int(pulse_width * 50)
    
    # ハードウェアPWMの出力開始
    pi.hardware_PWM(SERVO_GPIO, PWM_FREQUENCY, dutycycle)
    print(f"角度 {angle}° に設定中：パルス幅 = {pulse_width:.1f}µs, dutycycle = {dutycycle} (ppm)")

def main():
    # コマンドライン引数から角度を取得
    # 引数が指定されない場合はデフォルトで 90° に設定
    if len(sys.argv) >= 2:
        try:
            angle = float(sys.argv[1])
        except ValueError:
            print("角度は数値で指定してください。")
            sys.exit(1)
    else:
        angle = 90.0

    # pigpio の初期化
    pi = pigpio.pi()
    if not pi.connected:
        print("pigpioデーモンに接続できません。sudo pigpiod を実行してください。")
        sys.exit(1)

    try:
        # 指定角度にサーボを移動
        set_servo_angle(pi, angle)
        # サーボが移動するのを待つ（必要に応じて時間を調整）
        time.sleep(1.0)
    finally:
        # PWM出力の停止と pigpio の終了処理
        pi.hardware_PWM(SERVO_GPIO, PWM_FREQUENCY, 0)
        pi.stop()

if __name__ == "__main__":
    main()