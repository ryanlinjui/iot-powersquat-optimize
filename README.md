# IoT PowerSquat Optimize

Smart Wearable Devices & Pose Estimation for Optimizing Powerlifting and Squatting

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
- 在當前任何event 還沒結束時就觸發下一個event 0%
- 在HomeMenu 做非點選菜單的動作 0%
- 在輸入IoT UUID menu 輸入非法 UUID 0%
- 在輸入IoT UUID menu 做非輸入或非點擊返回的動作 0%
- 在上傳骨架影片時做非上傳影片或非點擊返回的動作 0%
- 在上傳骨架影片時上傳非法的影片檔案 30%
- 在上傳inbody照片時做非上傳照片或非點擊返回的動作 0%
- 在上傳inbody照片時上傳非法的照片檔案 30%
- 在上傳深蹲影片時做非上傳影片或非點擊返回的動作 0%
- 在上傳深蹲影片時上傳非法的影片檔案 30%
- 瘋狂送iot imu data to server 5%
- 傳很大的iot imu data to server 50%
- 發送偽裝的iot imu data to server request 10%
- 在任何輸入的介面上做sql injection動作 0%
- server 資料庫消失狀況 1%
- 在傳IMU sensor資料時，有一樣的對應的UUID做一樣的request 20%
- 偽造IMU sensor資料， 做一樣的對應UUID的request  20%
- IMU sensor 資料跟要分析的影片不是同一批次的 80%

### Line Beacon
- line beacon 沒用因為只能傳送13 bytes
- 可以去developer在官方帳號下產生隨機hardware id然後copy id燒錄到sensor當line beacon
- 有加官方帳號好友line 的使用者，在進入sensor發送電波範圍(功率越高，偵測範圍廣但就是會太多雜訊而導致難偵測，所以功率低範圍小，叫好偵測近的手機)時會被偵測到然後可以用webhook handle 獲得event 與13 byte 的dm，line app會資訊記錄該line beacon 到list 中，直到使用者真的離開電波範圍時，資訊記錄才會從line app的line beacon list 中刪除
- 如果將電波關掉再開啟，沒辦法獲得event，因line beacon list不會做刪除動作

## LineBot for Everyone (TBD)