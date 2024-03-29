# NHK2024_Raspi_Library
R1とR2に使う共通のプログラムたち

## 使い方
`MainController`を継承したクラスを作成し, `main`関数を書き換える. 

### ログファイルへの書き込み
`Maincontroller`の`log_system`の`write`関数でログファイルへの書き込みができる. 

## ラズパイ起動時の設定
ラズパイ起動時に以下の設定を行う
- CANの設定・初期化（`can_init.sh`）
- プログラムの起動 (`main_pro.sh`とか？)

### 電源投入時に指定したプログラムの起動方法
`main_pro.sh`に, 実行したいコマンドをかく. 例えば, プログラムのディレクトリに移動→仮想環境を起動→pythonの実行を行うシェルファイルは
```
#!/bin/bash

cd /home/pi/NHK2024/NHK2024_R1_Raspi
. ./env/bin/activate
rm -rf logs
python src/main.py

exit 0
```

あとは, 所定の位置にシェルファイルを移動, 実行権限の変更, 起動時に実行するように設定する.
```
sudo cp can_init.sh /usr/local/bin/
sudo cp main_pro.sh /usr/local/bin/
sudo chmod 700 /usr/local/bin/can_init.sh
sudo chmod 700 /usr/local/bin/main_pro.sh
sudo vim /etc/rc.local
```
`/etc/rc.local`の最後にシェルファイルを実行する（`can_init.sh`を先に実行しないとエラーが出る）
```
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi
/usr/local/bin/can_init.sh & // <- これを追加
/usr/local/bin/main_pro.sh & // <- これを追加
exit 0
```
再起動
```
sudo reboot
```
以前までのログファイルが削除されて, 新しいログファイルが作成されていれば起動時の設定は完了. 