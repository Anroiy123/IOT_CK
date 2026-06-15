Dùng đúng 8 label này. Nên giữ cử chỉ **dễ phân biệt bằng mắt**, ít giống nhau, và dễ làm ổn định trước webcam.

| Label        | Ký hiệu tay nên làm                                          | Ý nghĩa điều khiển           |
| ------------ | ------------------------------------------------------------ | ---------------------------- |
| `stop`       | Bàn tay mở, lòng bàn tay hướng vào camera, 5 ngón xòe rõ     | Dừng khẩn cấp                |
| `peace`      | Giơ 2 ngón chữ V                                             | Chuyển sang chế độ xe        |
| `rock`       | Ký hiệu rock: nắm đấm                                        | Chuyển sang chế độ tay máy   |
| `like`       | Ngón cái hướng lên                                           | Xe tiến / tăng góc servo     |
| `dislike`    | Ngón cái hướng xuống                                         | Xe lùi / giảm góc servo      |
| `one`        | Giơ 1 ngón trỏ sang ngang                                    | Xe rẽ trái / chọn khớp trước |
| `two`        | Giơ 2 ngón trỏ sang ngang                                    | Xe rẽ phải / chọn khớp tiếp  |
| `no_gesture` | Không đưa tay vào khung hình, hoặc tay đặt ngoài vùng camera | Không phát lệnh              |

**Cách quay dữ liệu cho mỗi label**

Mỗi clip 1.5 giây, bạn giữ cử chỉ ổn định trong khung hình:

```text
0.0s - 0.3s: đưa tay vào đúng vị trí
0.3s - 1.3s: giữ cử chỉ rõ, ít rung
1.3s - 1.5s: vẫn giữ, không đổi cử chỉ
```

Không nên đổi cử chỉ giữa clip.

**Thứ tự thu nên làm**

1. `no_gesture`: quay nền không có tay.
2. `stop`: bàn tay mở.
3. `like`
4. `dislike`
5. `one`
6. `two`
7. `peace`
8. `rock`

Khi thu thử lần đầu, chạy:

```powershell
.\.venv\Scripts\python.exe -m ml.collect_data --subject s01 --clips-per-label 5 --background simple --lighting bright
```
