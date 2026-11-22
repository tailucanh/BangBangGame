# BangBang HTML5 — server riêng chạy trên máy cá nhân

Server riêng cho game bắn tank BangBang, viết lại bằng Python (chỉ dùng thư viện chuẩn) cùng client HTML5 chạy trên trình duyệt. Gói chạy trên **một máy Windows**, không cần cài Python, Flash Player hay phần mềm database.

> **Repo này chỉ chứa mã nguồn.** Tài nguyên gốc của game (ảnh, âm thanh, SWF), database mẫu và Python portable không được đưa lên GitHub vì dung lượng (~3,2 GB) và vì là tài sản của chủ sở hữu game. Muốn chạy, bạn cần thêm các thư mục đó từ **gói đầy đủ** (xem mục 2).

## Mục lục

1. [Repo có gì](#1-repo-có-gì)
2. [Cài đặt](#2-cài-đặt)
3. [Mở game và đăng nhập](#3-mở-game-và-đăng-nhập)
4. [Chơi](#4-chơi)
5. [Web buff](#5-web-buff)
6. [Ghi log chẩn đoán](#6-ghi-log-chẩn-đoán)
7. [Thoát và sao lưu](#7-thoát-và-sao-lưu)
8. [Lỗi thường gặp](#8-lỗi-thường-gặp)
9. [Chơi LAN](#9-chơi-lan)
10. [Thay đổi so với gói gốc](#10-thay-đổi-so-với-gói-gốc)
11. [Dành cho người phát triển](#11-dành-cho-người-phát-triển)
12. [Bản quyền](#12-bản-quyền)

## 1. Repo có gì

| Có trong repo | Không có trong repo (lấy từ gói đầy đủ) |
|---|---|
| `server/` — toàn bộ server Python, mã C++ tăng tốc (`server/native/`) và bản build sẵn | `www/rez/`, `www/assets/`, `www/html5/assets*/` — tài nguyên game |
| `www/html5/*.js`, `*.css`, `index.html` — client HTML5 | `www/html5/*catalog*.json` — danh mục tài nguyên (~200 MB) |
| `www/admin/` — trang web buff | `www/html5/vendor_m82/` — trình phát Ruffle 0.7.1 |
| `www/index.html`, `bots.html`, `offline.html` | `www/*.swf`, `*.swz`, `*.dat`, `*.cub`, `mdlist.xml` |
| `StartGame.bat`, `data/advertise_host.txt` | `data/xmlpack/`, `data/bangbang.sqlite3`, `data/fileList_unpacked.xml` |
| | `runtime/python/` — Python 3.13 portable x64 |

## 2. Cài đặt

Yêu cầu: **Windows 10/11 64-bit**, trình duyệt Edge hoặc Chrome, khoảng **5 GB trống**.

1. Clone repo vào thư mục bạn có quyền ghi, ví dụ `C:\Games\BangBang`:
   ```
   git clone https://github.com/tailucanh/BangBangGame.git C:\Games\BangBang
   ```
2. Giải nén gói đầy đủ ra một thư mục tạm, rồi chép **đè vào thư mục clone** các mục ở cột phải của bảng trên, giữ nguyên đường dẫn. Kiểm tra lại có đủ:
   - `runtime\python\python.exe`
   - `data\bangbang.sqlite3` và `data\xmlpack\`
   - `www\rez\`, `www\html5\assets\`, `www\html5\vendor_m82\` và các file `www\html5\*catalog*.json`
3. Không đổi tên hoặc xoá thư mục tài nguyên chỉ vì tên có số phiên bản cũ (`assets_m4`, `assets_m5`…): client vẫn dùng tất cả.

Nếu chỉ có gói đầy đủ mà không dùng git, bạn có thể chép mã nguồn từ repo đè lên gói để nhận các bản sửa mới nhất.

## 3. Mở game và đăng nhập

1. Nhấp đúp **`StartGame.bat`**.
2. Giữ cửa sổ server mở và đợi dòng **SẴN SÀNG**.
3. Trình duyệt tự mở hai trang: **game** và **web buff**.
4. Trong trang game, nhập tài khoản rồi nhấn **Đăng nhập & vào sảnh**.

Database mẫu trong gói đầy đủ có sẵn tài khoản:

| Mục | Giá trị |
|---|---|
| Tài khoản | `html5_m5_xayda` |
| Mật khẩu | `nxAZXXe5MzepFg` |

Muốn dùng tài khoản riêng, tạo trong web buff (mục 5). Nên xoá các tài khoản thử nghiệm dùng mật khẩu `123456` có sẵn trong database mẫu.

Game thường mở tại `http://127.0.0.1:19083/html5/`. Nếu cổng bận, server tự chọn cổng khác: hãy dùng địa chỉ in trong cửa sổ server. Nhấp BAT lần nữa khi server đang chạy chỉ mở lại hai trang, không chạy thêm server.

## 4. Chơi

1. Ở sảnh, chọn tank.
2. Chọn **Đấu trường (PvP)** hoặc **Phụ bản (PvE)**. Đấu trường cho phép tạo phòng với bot cùng đội và bot đối thủ.
3. Chọn phòng/chế độ, thiết lập rồi bắt đầu trận.

| Thao tác | Điều khiển mặc định |
|---|---|
| Di chuyển | W, A, S, D hoặc phím mũi tên |
| Ngắm | Di chuyển chuột trong vùng trận |
| Bắn thường | Chuột trái |
| Kỹ năng | Phím hiện trên ô kỹ năng, thường là E, Space, R, Q |

Có thể đổi phím trong phần cài đặt. Nếu đang gõ chat, bấm lại vào vùng trận trước khi điều khiển tank.

## 5. Web buff

Trang quản lý local để tạo tài khoản và gửi đồ/tiền qua hòm thư. Chỉ truy cập được từ chính máy chạy server.

**Mở khoá:** mở `data\admin_buff.key` bằng Notepad (file tự tạo ở lần chạy đầu), chép **nội dung** vào ô *Khóa quản trị riêng*, bấm **Mở khóa**. Không dùng khoá này làm mật khẩu game, không chia sẻ nó.

**Tạo tài khoản:** vào *Quản lý tài khoản* → tạo tài khoản → đăng nhập game bằng tài khoản đó một lần để tạo nhân vật.

**Gửi đồ:** chọn người nhận → chọn vật phẩm trong *kho tiếp tế* → **Kiểm tra trước khi gửi** → xác nhận. Người chơi nhận trong **Hòm thư** của game. Nếu trang báo mất kết nối, kiểm tra trạng thái yêu cầu trước khi gửi lại để tránh gửi trùng.

## 6. Ghi log chẩn đoán

- Mặc định **tắt**. Bật/tắt ngay trong web buff ở mục *Ghi log chẩn đoán*, không cần khởi động lại.
- File nằm trong `data\packet_log\`: `diagnostic.log` và tối đa hai file cũ, tổng khoảng 15 MB.
- Khi báo lỗi, ghi rõ thao tác, chế độ/map/tank, điều mong đợi và điều xảy ra thực tế; kèm ảnh hoặc log. Không gửi file khoá web buff.

## 7. Thoát và sao lưu

1. Rời trận về sảnh, đóng các tab game và web buff.
2. Ở cửa sổ server, nhấn **Ctrl+C** (hoặc đóng cửa sổ).

Tài khoản, túi đồ và tiến độ nằm trong **`data\bangbang.sqlite3`**. Để sao lưu: dừng server rồi chép **cả thư mục `data`** ra nơi khác. Không xoá `bangbang.sqlite3-wal`/`-shm` khi server đang chạy.

Trong trận đang diễn ra, trạng thái được lưu khoảng mỗi giây; kết quả trận, phần thưởng và sát thương world boss được lưu ngay. Nếu server bị tắt đột ngột giữa trận, trận chưa xong có thể lùi lại tối đa khoảng 1 giây.

## 8. Lỗi thường gặp

| Hiện tượng | Cách xử lý |
|---|---|
| Báo thiếu Python portable | Chép `runtime\python\` từ gói đầy đủ (mục 2). |
| Báo thiếu database mẫu | Chép `data\bangbang.sqlite3` từ gói đầy đủ hoặc bản sao lưu; không tạo file rỗng cùng tên. |
| Game báo thiếu tài nguyên / màn hình trống | Kiểm tra đã chép đủ `www\rez`, `www\html5\assets*`, `vendor_m82` và các file `*catalog*.json`; nhấn Ctrl+F5. Server không tự tải tài nguyên từ Internet. |
| Trình duyệt không tự mở | Dùng địa chỉ Game/Web buff in trong cửa sổ server. |
| Trang không kết nối được | Kiểm tra cửa sổ server còn mở, đã báo SẴN SÀNG, và dùng đúng cổng. |
| Web buff báo khoá sai | Dùng nội dung `data\admin_buff.key` của đúng thư mục đang chạy. |
| Không thấy tài khoản mới trong danh sách người nhận | Đăng nhập game bằng tài khoản đó một lần rồi tìm lại. |
| Phím không phản hồi | Bấm vào vùng trận; kiểm tra lại phím trong cài đặt. |

## 9. Chơi LAN

Bản hiện tại **chưa hỗ trợ LAN**. `StartGame.bat` chỉ nhận kết nối từ chính máy (`127.0.0.1`). Chỉ đổi địa chỉ bind là chưa đủ: client dùng `crypto.subtle` và `crypto.randomUUID`, vốn chỉ hoạt động trên `localhost` hoặc HTTPS, nên truy cập qua `http://192.168.x.x` sẽ lỗi nạp tài nguyên. Muốn chơi LAN cần thêm HTTPS với chứng chỉ được các máy khách tin cậy, mở tường lửa, và mỗi người một tài khoản riêng. Web buff luôn chỉ cho truy cập từ chính máy chủ.

Lưu ý: nếu chạy thẳng `server\app.py` mà không truyền `--bind 127.0.0.1 --html5-local`, server sẽ mở cổng HTTP và cổng game TCP 49119 cho mọi máy trong mạng.

## 10. Thay đổi so với gói gốc

**Bảo mật**
- Bỏ cơ chế tự tải file thiếu từ `netzone.id.vn` (cơ chế cũ tắt kiểm tra chứng chỉ TLS và ghi file tải về vào `www/`). File thiếu giờ trả về 404.
- Bỏ ngoại lệ cho tài khoản thử nghiệm `1` có mật khẩu 1 ký tự; mọi tài khoản dùng chung quy định tên 3–32 ký tự, mật khẩu từ 6 ký tự.
- Giới hạn body JSON của request HTTP ở 64 KB; từ chối `Content-Length` âm hoặc sai.

**Hiệu năng**
- Trong trận, trạng thái được ghi vào SQLite tối đa 1 lần/giây thay vì mỗi tick 20 ms (đo được: PvP 41 → 1 lần ghi/giây, PvE 15 → 1 lần ghi/giây). Gói tin gửi tới người chơi không đổi. Kết thúc trận, phần thưởng và world boss vẫn lưu ngay.
- SQLite dùng `synchronous=NORMAL` (an toàn với chế độ WAL) và giới hạn file WAL ở 4 MB.
- Mỗi lần khởi động tự dọn dữ liệu cũ (`server/maintenance.py`): phiên đăng nhập hết hạn, trận nhiều người đã xong quá 7 ngày, vòng world boss quá 30 ngày (luôn giữ 2 vòng mới nhất và các vòng còn phần thưởng chưa nhận); sau đó thu gọn WAL và chỉ VACUUM khi có nhiều trang trống.

## 11. Dành cho người phát triển

**Cấu trúc chính**

| Đường dẫn | Vai trò |
|---|---|
| `server/portable_launcher.py` | Điểm vào của `StartGame.bat`: chọn cổng trống, kiểm tra môi trường, mở trình duyệt |
| `server/app.py` | HTTP server (file tĩnh, đăng nhập, API, WebSocket `/html5/ws`) |
| `server/html5_bridge.py` | Cầu nối WebSocket ↔ giao thức TCP gốc |
| `server/sixcube_server.py` | Server game TCP: sảnh, phòng, trận solo/PvE |
| `server/multiplayer_*.py` | Phòng và trận nhiều người (tick 20 ms) |
| `server/battle_runtime.py`, `combat_*.py`, `*_actions.py` | Mô phỏng trận và kỹ năng từng tank |
| `server/bot_*.py` | AI bot |
| `server/pve_*.py` | Phụ bản |
| `server/storage.py`, `storage_import.py`, `maintenance.py` | SQLite: kết nối, khởi tạo, dọn dẹp |
| `server/admin_buff.py`, `admin_accounts.py` | Web buff (chỉ loopback, khoá + CSRF) |
| `server/native/` | Mã C++ tính hình học/checkpoint, kèm bản build và `build_manifest.json` (SHA-256); thiếu DLL thì server tự dùng Python |
| `www/html5/` | Client HTML5 |

**Chạy thủ công** (với Python portable trong gói):

```
runtime\python\python.exe -I -B -X utf8 server\portable_launcher.py --no-browser ^
    --database D:\test\copy.sqlite3 --state-dir D:\test\state --admin-key D:\test\admin.key
```

Các tuỳ chọn `--database`, `--state-dir`, `--admin-key` cho phép thử trên bản sao database mà không động vào dữ liệu thật. Biến môi trường `BB_DATABASE` chọn file database cho các module trong `server/`.

## 12. Bản quyền

Đây là dự án cá nhân, phi thương mại, chạy offline. Tên game, hình ảnh, âm thanh, dữ liệu và client gốc thuộc về chủ sở hữu tương ứng và **không** được phân phối trong repo này. Ruffle (`vendor_m82`) dùng giấy phép MIT/Apache-2.0; Python portable dùng giấy phép PSF, giữ nguyên trong gói đầy đủ.
