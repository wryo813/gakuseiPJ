import pigpio

class Servo:
    """
    サーボモータ制御ライブラリ
    0° が 0.5ms、180° が 2.5ms に対応する設定になっています。
    pigpio デーモンが起動していることを前提とします。
    """
    def __init__(self, pin=12, frequency=50):
        """
        コンストラクタ
        :param pin: 使用するGPIOピン番号（BCM番号）
        :param frequency: PWM周波数（Hz）
        """
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpioデーモンに接続できません。sudo pigpiod を実行してください。")
        self.pin = pin
        self.frequency = frequency

    def set_config(self, pin=None, frequency=None):
        """
        GPIOピン番号およびPWM周波数の設定を変更する関数
        :param pin: 新しいGPIOピン番号（BCM番号）。Noneの場合は変更しません。
        :param frequency: 新しいPWM周波数（Hz）。Noneの場合は変更しません。
        """
        if pin is not None:
            self.pin = pin
        if frequency is not None:
            self.frequency = frequency

    def set_angle(self, angle):
        """
        サーボモータの角度を設定する関数
        :param angle: 0〜270° の範囲で角度を指定します。
        """
        if angle < 0 or angle > 270:
            raise ValueError("角度は 0〜270 の範囲で指定してください。")
        # 角度に対応するパルス幅 (µs) の計算
        # 0°  → 500µs, 180° → 2500µs となるよう線形補間
        pulse_width = 500 + (angle / 270) * 2000
        # dutycycleの計算:
        # PWM周期は 1,000,000 / frequency  [µs] なので、
        # dutycycle = pulse_width / (1,000,000/frequency) * 1,000,000 = pulse_width * frequency
        dutycycle = int(pulse_width * self.frequency)
        self.pi.hardware_PWM(self.pin, self.frequency, dutycycle)

    def stop(self):
        """
        PWM出力を停止し、pigpioとの接続を終了する関数
        """
        self.pi.hardware_PWM(self.pin, self.frequency, 0)
        self.pi.stop()


if __name__ == "__main__":
    # ライブラリの動作確認用のサンプルコード
    import time

    # インスタンス生成時に、デフォルトはGPIO12, 50Hzとなります
    servo = Servo(pin=12, frequency=50)
    
    # 必要に応じて設定変更も可能です（例：GPIO18に変更する場合）
    # servo.set_config(pin=18)
    
    try:
        # 0°から180°まで30度刻みで角度を変化させるデモ
        for angle in range(0, 181, 30):
            print(f"角度を {angle}° に設定します。")
            servo.set_angle(angle)
            time.sleep(1)
    finally:
        servo.stop()