# 🎓 BÀI TẬP LỚN CÁ NHÂN MÔN TRÍ TUỆ NHÂN TẠO
## Bài toán 8 Quân Hậu - 17 Thuật toán AI

**Sinh viên thực hiện:** Phạm Đăng Quang

**MSSV:** 23110143 

**Lớp:** 251ARIN330585_04CLC

**Môn học:** Trí tuệ nhân tạo

**Giảng viên:** Phan Thị Huyền Trang

**Link Github:** https://github.com/DanggQuangg/B-o-c-o-cu-i-k-c-nh-n-m-n-AI.git
---

## 📋 THÔNG TIN BÀI TẬP

### Yêu cầu đề bài:
Triển khai bài toán 8 quân hậu sử dụng 17 thuật toán AI khác nhau bao gồm:
- Tìm kiếm không có thông tin
- Tìm kiếm có thông tin  
- Thỏa mãn ràng buộc
- Tìm kiếm cục bộ
- Tìm kiếm trong môi trường phức tạp

### Mục tiêu bài toán:
Đặt 8 quân hậu trên bàn cờ 8x8 sao cho không có quân nào tấn công được quân nào khác. Quân hậu di chuyển theo hàng ngang và hàng dọc và đường chéo.

## 🎬 DEMO CHƯƠNG TRÌNH

![Demo Tổng Quan - 8 Quân Xe AI](images/demo.gif)

*Minh họa tổng quan giao diện và menu chọn thuật toán*

---

## 🚀 HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

### Bước 1: Kiểm tra yêu cầu hệ thống
```bash
# Kiểm tra Python (cần Python 3.7+)
python --version

# Kiểm tra pip
pip --version
```
### Bước 2: Tải và giải nén file nộp bài
- Giải nén file ZIP đã nộp
- Mở file bằng Visual studio code

---
## 🎮 CÁCH CHẠY CHƯƠNG TRÌNH

- Chạy chương trình trong visual studio code
- Click chuột chọn nút Sinh trạng thái mục tiêu để sinh trạng thái mục tiêu ngẫu nhiên trên bàn cờ bên phải
- Nhấn vào các nút thuật toán để chạy thuật toán tương ứng
- Bấm reset để xóa trống bàn cờ bên trái và ô thông báo
---

## 📊 17 THUẬT TOÁN ĐÃ TRIỂN KHAI

### 🔍 TÌM KIẾM KHÔNG CÓ THÔNG TIN

| STT | Thuật toán | Mô tả | Demo |
|-----|------------|-------|------|
| 1 | **BFS** - Breadth-First Search | Tìm kiếm theo chiều rộng | ![BFS Demo](demo/BFS_demo.gif) |
| 2 | **DFS** - Depth-First Search | Tìm kiếm theo chiều sâu | ![DFS Demo](demo/DFS_demo.gif) |
| 3 | **IDS** - Iterative Deepening Search | Tìm kiếm sâu dần | ![IDS Demo](demo/IDS_demo.gif) |
| 4 | **DLS** - Depth-Limited Search | Tìm kiếm theo chiều sâu có giới hạn độ sâu | ![IDL Demo](demo/DLS_demo.gif) |

### 🎯 TÌM KIẾM CÓ THÔNG TIN

| STT | Thuật toán | Mô tả | Demo |
|-----|------------|-------|------|
| 5 | **UCS** - Uniform Cost Search | Tối ưu cost | ![Greedy Demo](demo/Greedy_demo.gif) |
| 6 | **Greedy** - Greedy Best-First | Tham lam theo heuristic | ![Greedy Demo](demo/Greedy_demo.gif) |
| 7 | **A*** - A-star Search | Tối ưu với heuristic | ![A* Demo](demo/AStar_demo.gif) |

### 🔒 THỎA MÃN RÀNG BUỘC (CSP)

| STT | Thuật toán | Mô tả | Demo |
|-----|------------|-------|------|
| 8 | **Backtracking** | Quay lui cơ bản | ![Backtracking Demo](demo/Backtracking.gif) |
| 9 | **Forward Checking** | Kiểm tra tiến | ![Forward Checking Demo](demo/ForwardChecking.gif) |
| 10 | **AC-3** - Arc Consistency | Tính nhất quán cung | ![AC-3 Demo](demo/AC3.gif) |

### 🏔️ TÌM KIẾM CỤC BỘ

| STT | Thuật toán | Mô tả | Demo |
|-----|------------|-------|------|
| 11 | **Hill Climbing** | Leo đồi | ![Hill Climbing Demo](demo/HillClimbing_demo.gif) |
| 12 | **Simulated Annealing** | Luyện kim mô phỏng | ![Simulated Annealing Demo](demo/SimulatedAnnealing_demo.gif) |
| 13 | **Beam Search** | Tìm kiếm chùm | ![Beam Search Demo](demo/BeamSearch_demo.gif) |
| 14 | **Genetic Algorithm** | Thuật toán di truyền | ![Genetic Demo](demo/GeneticAglorithm_demo.gif) |

### 🌳 TÌM KIẾM TRONG MÔI TRƯỜNG PHỨC TẠP

| STT | Thuật toán | Mô tả | Demo |
|-----|------------|-------|------|
| 15 | **AND-OR Search** | Tìm kiếm đồ thị AND-OR | ![AND-OR Demo](demo/AndOrSearch_demo.gif) |
| 16 | **Belief State Search** | Tìm kiếm không nhìn thấy | ![AND-OR Demo](demo/BeliefStateSearch_demo.gif) |
| 17 | **Partial Belief Search** | Tìm kiếm nhìn thấy một phần | ![AND-OR Demo](demo/PartialBeliefSearch_demo.gif) |

---

## 🎯 CÁCH KIỂM TRA BÀI TẬP

### Test cơ bản:
1. Chạy chương trình - Kiểm tra giao diện có hoạt động
2. Nhấn nút Sinh trạng thái - Kiểm tra có sinh được trạng thái mục tiêu
3. Nhấn các nút thuật toán - Kiểm tra thuật toán có chạy
4. Nhấn reset - Kiểm tra xem có rest được giao diện

### Test chi tiết:
1. Thử từng thuật toán riêng lẻ
2. Kiểm tra thông tin trong hai ô thông báo
3. Xem kết quả hiển thị có chính xác không
4. **Quan sát demo GIFs** - So sánh với kết quả thực tế

### Kết quả mong đợi:
- **Thành công**: Tìm được vị trí quân hậu không xung đột
- **Visual**: Giao diện giống như trong demo GIFs

## 🎨 VISUAL SHOWCASE

Bài tập này có **18 demo GIFs** cho thấy:
- 🎬 **Demo tổng quan**: Giao diện chính và cách sử dụng
- 🧠 **17 thuật toán AI**: Mỗi thuật toán có demo riêng
- 🎯 **So sánh trực quan**: Thấy rõ sự khác biệt giữa các thuật toán

---

## 📈 KẾT QUẢ MONG ĐỢI KHI CHẤM BÀI

### Điểm tối đa nếu:
- ✅ Chạy được tất cả 17 thuật toán
- ✅ Giao diện không bị lỗi
- ✅ Code có comment rõ ràng
- ✅ Kết quả chính xác

---

**Cảm ơn cô đã xem xét bài tập! 🙏**
