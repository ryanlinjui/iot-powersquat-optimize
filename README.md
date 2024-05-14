# IoT PowerSquat Optimize

Smart Wearable Devices & Pose Estimation for Optimizing Powerlifting and Squatting

## Demo
https://github.com/ryanlinjui/iot-powersquat-optimize/assets/57468611/4f90c237-efdd-4276-8540-3afed87c66a7

## LineBot for Everyone
![389rdemt](https://github.com/ryanlinjui/iot-powersquat-optimize/assets/57468611/7994f8fb-fd7f-4a32-9f97-9f5b4bdfa6bd)

## Aim
- Develops explosiveness
- Boosts overall strength and endurance
- Improves posture and balance
- Prevents injuries and strains
- Customize the user’s movement to maximum the weight limit

## Methodology
- Find: Optimized squat form
- Through: Reinforcement Learning
- With: Joint position data
- From: Wearable devices

## Report
### 測試案例
- 在當前任何 event 還沒結束時就觸發下一個 event 0%
- 在 HomeMenu 做非點選菜單的動作 0%
- 在輸入 IoT UUID menu 輸入非法 UUID 0%
- 在輸入 IoT UUID menu 做非輸入或非點擊返回的動作 0%
- 在上傳骨架影片時做非上傳影片或非點擊返回的動作 0%
- 在上傳骨架影片時上傳非法的影片檔案 30%
- 在上傳 inbody 照片時做非上傳照片或非點擊返回的動作 0%
- 在上傳 inbody 照片時上傳非法的照片檔案 30%
- 在上傳深蹲影片時做非上傳影片或非點擊返回的動作 0%
- 在上傳深蹲影片時上傳非法的影片檔案 30%
- 瘋狂送 iot imu data to server 5%
- 傳很大的 iot imu data to server 50%
- 發送偽裝的 iot imu data to server request 10%
- 在任何輸入的介面上做 sql injection 動作 0%
- server 資料庫消失狀況 1%
- 在傳 IMU sensor資料時，有一樣的對應的 UUID 做一樣的 request 20%
- 偽造 IMU sensor資料， 做一樣的對應 UUID 的request  20%
- IMU sensor 資料跟要分析的影片不是同一批次的 80%

### Line Beacon
- line beacon 沒用因為只能傳送 13 bytes
- 可以去 developer 在官方帳號下產生隨機 hardware id 然後 copy id 燒錄到 senso r當 line beacon
- 有加官方帳號好友 line 的使用者，在進入sensor發送電波範圍(功率越高，偵測範圍廣但就是會太多雜訊而導致難偵測，所以功率低範圍小，叫好偵測近的手機)時會被偵測到然後可以用 webhook handle 獲得 event 與13 byte 的 dm，line app 會資訊記錄該 line beacon 到 list 中，直到使用者真的離開電波範圍時，資訊記錄才會從 line app 的 line beacon list 中刪除
- 如果將電波關掉再開啟，沒辦法獲得 event，因 line beacon list 不會做刪除動作
