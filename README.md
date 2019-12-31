# poke_auto_fuka
![screenshot_1577806093](https://user-images.githubusercontent.com/57222425/71625907-b03a9080-2c2d-11ea-92c7-d930c8b4dd48.png)
- [video](https://twitter.com/nohamanona/status/1209830781863882754)

pokemon sword and shield auto egg hatching system

## H/W Requirement
- [ebith/Switch-Fightstick's README](https://github.com/ebith/Switch-Fightstick/blob/master/README.md)
- HDMI Capture Device

## S/W Requirement
- AmarecTV : see [hasegaw/IkaLog](https://github.com/hasegaw/IkaLog/wiki/en_WinIkaLog)
- Video input divert IkaLog
- Python3.6 32bit
- Opencv3.0
- Numpy

## Usage
- ５番道路預かり屋の前で自転車に乗っていない状態でメニューのポケモンを開き、"c"を押す
- 必ず6匹持っている状態でスタートする
- 1匹目にほのおのからだの特性をもったポケモンを入れておくとよい
- 起動してから"c"を押す前（State : Prepare）では以下のキー入力が可能

| Key |  Action |
|:---:|:-------------------------|
|w | LY MIN |
|a | LX MIN |
|s | LY MAX |
|d | LX MAX |
|x | Button X |
|y | Button Y |
|v | Button A |
|b | Button B |
|r | Button R |
|p | Button START |
|q | Screenshot |
|c | start auto hatching |


## Efficiency
- 34 eggs par a hour (2019/12/25)

## Issues
- 橋の上のNPCにぶつかって止まるときがある
- 色違いが出たとき正しくマクロが動かない（復帰はする）
- 空を飛ぶを失敗することがある
- ボックスがいっぱいだと走り続ける（現状は仕様）

## Note
- 完全に自環境での動作のみを考えて制作しています
- 処理フレームでマクロを制御しているため、処理が速いor遅いPCではマクロが正しく動作しない可能性があります
- 今後効率と安定性の向上のための改修も考えています
- 素人のため中のソースは汚いです。ご指摘歓迎します → [nohamanona](https://twitter.com/nohamanona)

