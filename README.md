# IoT Powerlifting & Squatting Optimize

# Demo
https://github.com/ryanlinjui/iot-powersquat-optimize/assets/57468611/4f90c237-efdd-4276-8540-3afed87c66a7

# LineBot for Everyone
<img src="https://github.com/ryanlinjui/iot-powersquat-optimize/assets/57468611/7994f8fb-fd7f-4a32-9f97-9f5b4bdfa6bd" width="200" height="200" alt="QRCode"/>

# Getting Started with [M5StickC](https://github.com/m5stack/M5StickC)

> Install `arduino-cli`: https://github.com/arduino/arduino-cli

## Install Core & Library
```
arduino-cli core install m5stack:esp32 --config-file arduino-cli.yaml
arduino-cli lib install M5StickC
arduino-cli lib install --git-url https://github.com/arduino-libraries/NTPClient --config-file arduino-cli.yaml
```

## Initialize board
#### Attach board and Find usb port name
```
arduino-cli board list
```

#### Check board's FBQN
```
arduino-cli board listall M5StickC
```

#### Set board
```
arduino-cli board attach M5StickC --fqbn m5stack:esp32:m5stack_stickc --port <your-usb-port-name>
```

## Compile & Upload code
```
arduino-cli compile M5StickC --upload
```

## Monitor
```
arduino-cli monitor M5StickC --config 115200
```

# Some Notes
#### Vulnerability Test Rating
- **0%** - 在當前任何 event 還沒結束時就觸發下一個 event 
- **0%** - 在 HomeMenu 做非點選菜單的動作
- **0%** - 在輸入 IoT UUID menu 輸入非法 UUID
- **0%** - 在輸入 IoT UUID menu 做非輸入或非點擊返回的動作
- **0%** - 在上傳骨架影片時做非上傳影片或非點擊返回的動作
- **30%** - 在上傳骨架影片時上傳非法的影片檔案
- **0%** - 在上傳 Inbody 照片時做非上傳照片或非點擊返回的動作
- **30%** - 在上傳 Inbody 照片時上傳非法的照片檔案
- **0%** - 在上傳深蹲影片時做非上傳影片或非點擊返回的動作
- **30%** - 在上傳深蹲影片時上傳非法的影片檔案
- **5%** - 瘋狂送 IoT IMU data to server
- **50%** - 傳很大的 IoT IMU data to server
- **10%** - 發送偽裝的 IoT IMU data to server request
- **0%** - 在任何輸入的介面上做 SQL injection 動作
- **1%** - server 資料庫消失狀況
- **20%** - 在傳 IMU sensor 資料時，有一樣的對應的 UUID 做一樣的 request
- **20%** - 偽造 IMU sensor 資料， 做一樣的對應 UUID 的request
- **80%** - IMU sensor 資料跟要分析的影片不是同一批次的

#### Line Beacon
- Line Beacon 不適用此專案因為只能傳送 13 bytes
- 可以去 developer 在官方帳號下產生隨機 hardware ID 然後 copy ID 燒錄到 sensor 當 Line Beacon
- 有加官方帳號好友 Line 的使用者，在進入 sensor 發送電波範圍 (功率越高，偵測範圍廣但就是會太多雜訊而導致難偵測，所以功率低範圍小，叫好偵測近的手機) 時會被偵測到然後可以用 webhook handle 獲得 event 與 13 bytes 的 device message `dm`，Line app 會資訊記錄該 Line Beacon 到 list 中，直到使用者真的離開電波範圍時，資訊記錄才會從 Line app 的 Line Beacon list 中刪除
- 如果將電波關掉再開啟，沒辦法獲得 event，因 Line Beacon list 不會做刪除動作
