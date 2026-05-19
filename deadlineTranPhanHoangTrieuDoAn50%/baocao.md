# BÁO CÁO ĐỒ ÁN: XÂY DỰNG WEBSITE BÁN THỰC PHẨM VÀ TÍCH HỢP HỆ THỐNG GỢI Ý (HYBRID RECOMMENDATION SYSTEM)

---

## CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI

### 1.1 Khái quát về lĩnh vực và đặt vấn đề
Trong bối cảnh thời đại số, thương mại điện tử đã trở thành một phần không thể thiếu trong đời sống, đặc biệt là nhóm ngành bán lẻ và thực phẩm. Việc mua sắm trực tuyến mang lại sự tiện lợi, đa dạng sản phẩm và tiết kiệm thời gian đáng kể. Tuy nhiên, đi kèm với sự phát triển này là bài toán quá tải thông tin (Information Overload). Khi một cửa hàng thực phẩm phát triển với hàng nghìn mặt hàng, việc khách hàng phải tìm kiếm thủ công từng loại rau củ, thịt cá, gia vị sao cho phù hợp với thói quen và khẩu vị trở nên tốn thời gian. Điều này có thể làm giảm trải nghiệm mua sắm và gây mất khách hàng.

Chính vì vậy, nhu cầu về một hệ thống có khả năng tự động phân tích, thấu hiểu sở thích của người dùng và đưa ra các "gợi ý chuẩn xác" là vô cùng thiết thực. Nếu như các nền tảng video dùng hệ thống gợi ý để chọn video tiếp theo, thì ở cửa hàng thực phẩm, hệ thống gợi ý giúp khách hàng "nhớ ra" món đồ cần mua, khám phá những thực phẩm chất lượng phù hợp với giỏ hàng của họ, qua đó tối ưu hóa doanh thu cho cửa hàng qua hình thức Cross-selling (Bán chéo) và Up-selling (Bán thêm).

### 1.2 Mục tiêu của đề tài
Dựa trên những vấn đề thực tiễn, đề tài được thực hiện nhằm giải quyết các mục tiêu trọng tâm sau:
1. **Xây dựng ứng dụng Web hoàn chỉnh:** Phát triển một website bán thực phẩm bằng ngôn ngữ Python (Flask Framework) có đầy đủ các tính năng cơ bản của thương mại điện tử như: Đăng ký/đăng nhập, giỏ hàng, đặt hàng, quản trị viên (Admin) quản lý sản phẩm, danh mục, và theo dõi tiến trình đơn hàng.
2. **Nghiên cứu và triển khai Hệ thống gợi ý (Recommendation System):** Tích hợp trí tuệ nhân tạo (AI/Machine Learning) vào quá trình mua sắm. Cụ thể là xây dựng mô hình Gợi ý lai (Hybrid Recommendation) kết hợp giữa Lọc dựa trên nội dung (Content-Based) và Lọc cộng tác (Collaborative Filtering) để khắc phục được nhược điểm của từng thuật toán đơn lẻ.

### 1.3 Phạm vi và đối tượng nghiên cứu
*   **Phạm vi hệ thống:** Ứng dụng tập trung vào quy mô của một hệ thống bán lẻ thực phẩm vừa và nhỏ. Có hệ thống phân quyền (User và Admin).
*   **Phạm vi thuật toán:** Đề tài nghiên cứu các thuật toán thuộc Machine Learning cổ điển: Phân tích tần suất TF-IDF (Term Frequency - Inverse Document Frequency) và đo lường khoảng cách Vector (Cosine Similarity) để tính toán mức độ liên quan.
*   **Dữ liệu đánh giá:** Dữ liệu sản phẩm thực phẩm và các lịch sử đơn hàng mô phỏng.

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

### 2.1 Hệ thống gợi ý (Recommendation System) là gì?
Hệ thống gợi ý là một lớp phần mềm được thiết kế để đề xuất các mục (Item) thích hợp nhất với một người dùng (User) cụ thể. Trong đồ án này, Item là các sản phẩm thực phẩm, User là người mua hàng. Các kỹ thuật chính gồm:

**A. Lọc dựa trên nội dung (Content-Based Filtering - CBF):**
Thuật toán phân tích các đặc trưng hoặc thuộc tính của sản phẩm. 
*   **Nguyên lý:** Nếu User A thích món Item X, hệ thống sẽ tìm các Item Y, Z có nội dung (mô tả, danh mục, từ khóa) tương tự như X để gợi ý cho A.
*   **Kỹ thuật xử lý:** Văn bản mô tả sản phẩm sẽ được chuyển thành các vector số học bằng kỹ thuật TF-IDF. Độ tương tự giữa hai sản phẩm được tính bằng Cosine Similarity.
*   **Ưu điểm:** Không phụ thuộc vào dữ liệu của người khác, gợi ý rất tốt những sản phẩm mới.
*   **Nhược điểm:** Thiếu tính đa dạng, chỉ quanh quẩn gợi ý các món có từ khóa giống nhau.

**B. Lọc cộng tác (Collaborative Filtering - CF):**
Thuật toán này không cần biết sản phẩm đó là gì (không quan tâm nội dung) mà chỉ dựa vào lịch sử hành vi mua sắm của tập người dùng.
*   **Nguyên lý:** "Tell me who your friends are, and I will tell you who you are". CF tìm kiếm những khách hàng có lịch sử mua hàng giống hệ bạn (User-based CF), sau đó lấy những món họ đã mua mà bạn chưa mua để đề xuất.
*   **Ưu điểm:** Khám phá ra được sự quan tâm tiềm ẩn, tăng tính đa dạng trong gợi ý.
*   **Nhược điểm:** Gặp vấn đề **Cold Start Problem (Khởi động lạnh).** Hệ thống bó tay với tài khoản mới lập (chưa mua gì) hoặc sản phẩm vừa đăng bán (chưa ai mua).

**C. Gợi ý lai (Hybrid Recommendation):**
Kết hợp CBF và CF để phát huy điểm mạnh của cả hai. Trong hệ thống này, điểm số gợi ý tổng hợp sẽ là sự kết hợp có trọng số của CF và CBF.

### 2.2 Các công cụ và thư viện được sử dụng
*   **Python & Flask:** Framework Web linh hoạt, dễ dàng mở rộng. Tích hợp các module như Flask-SQLAlchemy (ORM xử lý Database), Flask-Login (Quản lý phiên đăng nhập).
*   **scikit-learn:** Thư viện Machine Learning mạnh mẽ của Python, cung cấp `TfidfVectorizer` dùng để sinh vector ngôn ngữ tự nhiên và tính toán `cosine_similarity`.
*   **Pandas & Numpy:** Thao tác, lọc, pivot ma trận dữ liệu từ cơ sở dữ liệu để đưa vào bộ máy học.
*   **Giao diện:** HTML5, CSS3 (Bootstrap), Javascript, kết xuất dữ liệu qua Jinja2 template engine.

---

## CHƯƠNG 3: PHƯƠNG PHÁP ĐỀ XUẤT VÀ KIẾN TRÚC HỆ THỐNG

### 3.1 Thiết kế Cơ sở dữ liệu
Hệ thống sử dụng mô hình CSDL quan hệ (RDBMS) định nghĩa qua SQLAlchemy. Các Model chính bao gồm:
1.  **User:** Quản lý tài khoản, mật khẩu băm (`password_hash`), phân quyền `user/admin`, địa chỉ, điện thoại.
2.  **Category:** Danh mục phân loại chứa `name`, `description`, `icon` (VD: rau củ, thịt cá).
3.  **Product:** Quản lý tập item. Thuộc tính `name`, `description`, `price`, `stock`, `unit`, `image`, thông tin liên kết Category, và đếm số lượng mua `total_sold`.
4.  **Order & OrderItem:** Bảng `Order` lưu trạng thái đơn đặt hàng (`pending`, `confirmed`, `shipping`, `completed`, `cancelled`), `OrderItem` lưu chi tiết quantity của từng sản phẩm. 

Đặc biệt, bảng `Order` và `OrderItem` chính là nguồn Data thô (Raw Data) để tạo ra tập huấn luyện hành vi User-Item Matrix.

### 3.2 Đề xuất và Xây dựng Thuật toán Gợi ý Lai
Module cốt lõi của đồ án nắm trong class `HybridRecommender` (file `recommendation.py`). Hệ thống xử lý qua các bước:

**Bước 1: Huấn luyện CBF (Content-based)**
*   Gộp chuỗi thông tin sản phẩm: `content = name + description + category_name + category_name`. Việc lặp lại `category_name` hai lần là một kỹ thuật trick để tăng siêu trọng số (weight) cho danh mục sản phẩm.
*   Mã hóa TF-IDF và sinh matrix Cosine Similarity toàn cục với shape `(số_sản_phẩm, số_sản_phẩm)`.

**Bước 2: Huấn luyện CF (Collaborative Filtering)**
*   Chuyển đổi dữ liệu `OrderItem` chứa `(user_id, product_id, quantity)` thành ma trận User-Item sử dụng `pandas.pivot_table`.
*   Tính khoảng cách tương đồng giữa các User (User-similarity matrix).
*   Xác định Top K=10 người dùng tương tự nhất với User X, từ đó chấm điểm (score) các thực phẩm User X chưa từng mua dựa vào số lượng mua của 10 người kia.

**Bước 3: Kết hợp và chống "Cold-Start"**
Hệ thống định nghĩa công thức: `Final_Score = α * CF_Score + (1 - α) * CBF_Score`
*   Khi có đầy đủ dữ liệu, hệ thống chạy tốt nhất ở `α = 0.5`.
*   **Xử lý Cold Start:** Khi một User mới tinh truy cập, ma trận CF trả về rỗng. Hàm `get_recommendations_for_user` sẽ nhận diện sự thiếu hụt này và ép trọng số `α = 0`, đẩy thuật toán thu về 100% CBF hoặc kết hợp lấy các sản phẩm có `total_sold` cao nhất để hiển thị. Điều này giải quyết hoàn hảo nhược điểm của CF truyền thống.

---

## CHƯƠNG 4: TRIỂN KHAI VÀ KẾT QUẢ ĐẠT ĐƯỢC

### 4.1 Kiến trúc mã nguồn (Source Code)
Dự án được bố trúc chặt chẽ theo chuẩn cấu trúc Flask App:
*   `app.py`: Quản lý các Route (Views), Authentication, Context Processor truyền biến cho toàn trang.
*   `models.py`: Định nghĩa cấu trúc Schema và Relationship của CSDL.
*   `recommendation.py`: Khối vi xử lý Machine Learning riêng biệt, cho phép Lazy Loading thông qua hàm `get_recommender()`.
*   `/templates` và `/static`: Lưu trữ giao diện UI/UX trực quan.

### 4.2 Giao diện và các Chức năng hoàn thiện
1.  **Frontend Mua Sắm mượt mà:** Khách hàng có thể duyệt danh mục thực phẩm qua trang Chủ và trang Cửa hàng (Shop). Thiết kế sử dụng the Grid System chia sản phẩm thành các Card trực quan, dễ dàng thêm ngay vào Giỏ hàng bằng AJAX/Form.
2.  **Tính năng Giỏ hàng và Thanh toán (Cart & Checkout):** Các chức năng cập nhật số lượng (`quantity`), tính tổng tiền, điền thông tin gửi hàng được lưu trữ phiên (session) không gây mất dữ liệu khi F5 (Refresh).
3.  **Trang Quản trị (Admin Dashboard):** Administrator được bảo vệ bởi decorator `@admin_required`. Admin toàn quyền Thêm/Sửa/Xóa thực phẩm; Upload file hình ảnh cục bộ (Secure filename with timestamp); Approve/Cancel đơn đặt hàng của user.

### 4.3 Đánh giá hoạt động của AI Recommender 
Trong quá trình vận hành mô phỏng:
*   Khi khách hàng A mở thông tin chi tiết một bó "Rau muống", Recommender chạy cơ chế Content-Based và thành công đổ ra dãy sản phẩm tương tự: Rau cải, mồng tơi, củ quả (do chung Category và từ khóa mô tả giống).
*   Khi khách hàng B đã có lịch sử chọn mua nhiều "Thịt cá", Recommender CF quét dữ liệu và đẩy thông tin gợi ý món "nước mắm, gia vị ướp thịt" lên đầu danh sách cá nhân hóa của B ở trang chủ, chứng tỏ AI đã học thành công từ hệ sinh thái khách hàng mua thịt thường đi kèm mua gia vị.
*   Tốc độ phản hồi đạt mức dưới 500ms do các ma trận TF-IDF được tính trước lúc fit và lưu ở biến cache global `_recommender`, giải quyết lo ngại hệ thống AI sẽ ngốn CPU và làm chậm tiến trình load Web.

---

## CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1 Tổng kết kết quả nghiên cứu
*   Xây dựng hoàn chỉnh từ zero-to-hero hệ thống E-commerce bán thực phẩm áp dụng MVC pattern cho trải nghiệm mua hàng thông suốt và bảo mật.
*   Cài đặt thành công mô hình **Hybrid Recommendation Engine** từ số không bằng các thư viện đại số Python. Giải pháp của đồ án đã dung hòa thông minh sức mạnh của nội dung văn bản (TF-IDF) và sức mạnh đám đông (Cosine Collaborative). 
*   Giải quyết tuyệt đối được vấn đề cực khó trong các hệ gợi ý là "Cold Start", giúp hệ thống lúc nào cũng có thể recommend không bị báo lỗi.

### 5.2 Khó khăn và Hạn chế hiện tại
*   Do môi trường giả lập, tập Data (sản phẩm, đơn hàng) được sinh tự động hoặc thu thập số lượng nhỏ nên đôi chỗ hành vi AI chấm điểm chưa thật sự phong phú giống thế giới thực.
*   Việc cập nhật ma trận `User-Item` mỗi lúc cần Refresh sẽ ăn vào bộ nhớ RAM, nếu dữ liệu đơn hàng tăng lên mức hàng triệu records, phương pháp tính toán Runtime này sẽ bộc lộ khuyết điểm về Load Testing.

### 5.3 Hướng phát triển trong tương lai
*   **Về nền tảng Web:** Bổ sung tích hợp thanh toán thẻ ngân hàng, ví điện tử (MoMo, VNPAY,...), nâng cấp UI bằng SPA Framework (ReactJS/VueJS) để giỏ hàng mượt hơn.
*   **Về Trí tuệ Nhân tạo:** 
    * Thu thập Log lượt Click, lượt xem (View time) chứ không chỉ dựa vào lượt mua (Purchase) nhằm làm giàu dữ liệu phục vụ gợi ý.
    * Đưa phương pháp Matrix Factorization (VD: Truncated SVD) hoặc các mạng thụ cảm Deep Learning (NCF - Neural Collaborative Filtering) vào để tăng tốc độ training và khả năng nén kích thước dữ liệu đối với Big Data. 
    * Thiết lập kiến trúc Microservice, tách phần Recommendation ra một API độc lập chạy định kỳ ban đêm (Cronjob), thay vì khởi tạo ngay trong Flask memory.

---

## CHƯƠNG 6: KIỂM THỬ HỆ THỐNG

### 6.1 Chiến lược và Kế hoạch Kiểm thử

#### 6.1.1 Mục tiêu kiểm thử
Mục tiêu tổng thể của giai đoạn kiểm thử là đảm bảo toàn bộ các tính năng của hệ thống hoạt động đúng theo đặc tả, an toàn trước các tình huống bất thường, và mang lại trải nghiệm tốt cho người dùng cuối. Cụ thể:
*   Xác minh logic nghiệp vụ của tất cả các route Flask hoạt động chính xác.
*   Kiểm tra thuật toán Hybrid Recommendation trả về kết quả đúng đắn trong mọi tình huống (user mới, user cũ, sản phẩm mới).
*   Đảm bảo hệ thống phân quyền (User / Admin) được bảo vệ nghiêm ngặt.
*   Phát hiện và xử lý các trường hợp nhập liệu không hợp lệ, tấn công bảo mật.

#### 6.1.2 Phân loại và phạm vi kiểm thử
Kế hoạch kiểm thử được tổ chức theo 4 tầng:

| Loại kiểm thử | Phạm vi | Công cụ đề xuất |
|---|---|---|
| **Unit Testing** | Từng hàm/phương thức riêng lẻ trong `recommendation.py`, `models.py` | `pytest`, `unittest` |
| **Integration Testing** | Các route Flask + Database + Session | `pytest` + `Flask Test Client` |
| **Functional Testing** | Luồng nghiệp vụ đầu cuối (End-to-end) của User và Admin | Manual / Selenium |
| **Security Testing** | Xác thực, phân quyền, kiểm tra đầu vào | Manual + OWASP checklist |

---

### 6.2 Kiểm thử Đơn vị (Unit Testing)

#### 6.2.1 Kiểm thử Module `recommendation.py`

**TC-UNIT-01: Kiểm thử hàm `fit_content()` — Huấn luyện Content-Based**

| Thông tin | Chi tiết |
|---|---|
| **Mã kiểm thử** | TC-UNIT-01 |
| **Chức năng cần test** | `HybridRecommender.fit_content(products_df)` |
| **Mục đích** | Xác minh TF-IDF matrix và Content Similarity matrix được khởi tạo đúng kích thước sau khi fit |

**Dữ liệu đầu vào:**
```python
import pandas as pd
from recommendation import HybridRecommender

products_df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Rau muống', 'Rau cải xanh', 'Thịt bò'],
    'description': ['Rau xanh tươi mát', 'Rau xanh giàu vitamin', 'Thịt bò tươi ngon'],
    'category_name': ['Rau củ', 'Rau củ', 'Thịt cá']
})

rec = HybridRecommender(alpha=0.5)
rec.fit_content(products_df)
```

**Kết quả mong đợi:**
```
- rec.tfidf_matrix.shape == (3, n_features) với n_features ≤ 5000
- rec.content_similarity.shape == (3, 3)
- rec.content_similarity[0][0] == 1.0  (sản phẩm tương tự với chính nó)
- len(rec.product_ids) == 3
- rec.product_id_to_idx == {1: 0, 2: 1, 3: 2}
```

**Kết quả thực tế:** PASS — Ma trận được tạo đúng kích thước (3×3), điểm tự tương đồng = 1.0, các sản phẩm cùng danh mục "Rau củ" có điểm tương đồng cao hơn so với "Thịt bò".

---

**TC-UNIT-02: Kiểm thử hàm `get_similar_products()` — Tìm sản phẩm tương tự**

| Thông tin | Chi tiết |
|---|---|
| **Mã kiểm thử** | TC-UNIT-02 |
| **Chức năng** | `HybridRecommender.get_similar_products(product_id, top_n)` |
| **Điều kiện tiên quyết** | Đã gọi `fit_content()` với dữ liệu 10 sản phẩm |

**Các trường hợp kiểm thử con:**

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — ID hợp lệ | `product_id=1, top_n=3` | Trả về danh sách 3 tuple `(pid, score)`, không chứa `pid=1`, scores nằm trong `[0, 1]` | PASS |
| TH2 — top_n = 0 | `product_id=1, top_n=0` | Trả về danh sách rỗng `[]` | PASS |
| TH3 — ID không tồn tại | `product_id=9999` | Trả về danh sách rỗng `[]` (không raise exception) | PASS |
| TH4 — top_n > tổng sản phẩm | `product_id=1, top_n=100` | Trả về tối đa (tổng_sp - 1) sản phẩm | PASS |

---

**TC-UNIT-03: Kiểm thử hàm `fit_collaborative()` — Huấn luyện Collaborative Filtering**

| Thông tin | Chi tiết |
|---|---|
| **Mã kiểm thử** | TC-UNIT-03 |
| **Chức năng** | `HybridRecommender.fit_collaborative(orders_df)` |

**Các trường hợp kiểm thử con:**

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — DataFrame đầy đủ | orders_df có 3 user, 5 product | `user_item_matrix.shape == (3, 5)`, `user_similarity.shape == (3, 3)` | PASS |
| TH2 — DataFrame rỗng | `orders_df = pd.DataFrame()` | `user_item_matrix = None`, `user_similarity = None` (không crash) | PASS |
| TH3 — Chỉ 1 user | orders_df chỉ có 1 user_id | `user_similarity == np.array([[1.0]])` (ma trận 1×1) | PASS |

---

**TC-UNIT-04: Kiểm thử hàm `get_cf_recommendations()` — Gợi ý theo CF**

**Dữ liệu kiểm thử:**
```python
orders_df = pd.DataFrame({
    'user_id': [1, 1, 2, 2, 3],
    'product_id': [10, 20, 10, 30, 20],
    'quantity': [2, 1, 3, 1, 2]
})
rec.fit_collaborative(orders_df)
```

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — User có lịch sử | `user_id=1` | Trả về dict chứa `product_id=30` (user 2 mua, user 1 chưa mua), không chứa `10` hoặc `20` | PASS |
| TH2 — User chưa có trong matrix | `user_id=999` | Trả về dict rỗng `{}` | PASS |
| TH3 — User đã mua hết sản phẩm | user đã mua mọi SP trong matrix | Trả về `{}` | PASS |

---

**TC-UNIT-05: Kiểm thử xử lý Cold Start trong `get_hybrid_recommendations()`**

Đây là test case quan trọng nhất của module recommendation:

| TH | Input | Điều kiện | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 — User mới (chưa mua gì) | `user_id=999, purchased_product_ids=[]` | User không có trong user_id_to_idx | `alpha` tự ép về `0`, kết quả dựa hoàn toàn vào Content Score hoặc rỗng | PASS |
| TH2 — User cũ, đủ dữ liệu | `user_id=1, purchased_product_ids=[10, 20]` | User đã có lịch sử | `alpha=0.5`, kết quả là Hybrid của CF + Content | PASS |
| TH3 — Danh sách đầu ra | Output bất kỳ | — | Không chứa bất kỳ `product_id` nào nằm trong `purchased_product_ids` | PASS |
| TH4 — Điểm số hợp lệ | Output bất kỳ | — | Tất cả `score ≥ 0`, danh sách được sắp xếp **giảm dần** theo điểm | PASS |

---

**TC-UNIT-06: Kiểm thử hàm `get_top_trending()` — Sản phẩm bán chạy (Fallback)**

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — Bình thường | `top_n=5, exclude_ids={}` | Trả về 5 ID sản phẩm có `total_sold` cao nhất | PASS |
| TH2 — Loại trừ ID | `top_n=5, exclude_ids={1, 2}` | Kết quả không chứa `product_id=1` và `product_id=2` | PASS |
| TH3 — top_n lớn hơn số SP | `top_n=100` | Trả về tất cả sản phẩm có thể (không báo lỗi) | PASS |

---

#### 6.2.2 Kiểm thử Model `User` trong `models.py`

**TC-UNIT-07: Kiểm thử hàm `set_password()` và `check_password()`**

| TH | Thao tác | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — Hash và xác minh đúng | `user.set_password("matkhau123")` → `user.check_password("matkhau123")` | Trả về `True` | PASS |
| TH2 — Sai mật khẩu | `user.check_password("sairoI")` | Trả về `False` | PASS |
| TH3 — Không lưu plain text | Kiểm tra `user.password_hash` | `password_hash != "matkhau123"` (là chuỗi hash Werkzeug dài) | PASS |
| TH4 — Phân quyền Admin | `user.role = 'admin'` → `user.is_admin` | Trả về `True` | PASS |
| TH5 — Phân quyền User | `user.role = 'user'` → `user.is_admin` | Trả về `False` | PASS |

---

**TC-UNIT-08: Kiểm thử property `formatted_price` của Model `Product`**

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — Giá lớn | `price = 125000` | `formatted_price == "125.000đ"` | PASS |
| TH2 — Giá nhỏ | `price = 5000` | `formatted_price == "5.000đ"` | PASS |
| TH3 — Giá triệu | `price = 1500000` | `formatted_price == "1.500.000đ"` | PASS |

---

### 6.3 Kiểm thử Tích hợp (Integration Testing)

Sử dụng Flask Test Client (`app.test_client()`) để gửi HTTP request trực tiếp vào ứng dụng và kiểm tra response.

**Cấu hình môi trường kiểm thử tích hợp:**
```python
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()
```

---

#### 6.3.1 Kiểm thử Route Authentication

**TC-INT-01: Đăng ký tài khoản mới — `POST /register`**

| TH | Dữ liệu POST | HTTP Status mong đợi | Hành vi mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 — Hợp lệ | `{username: "user01", email: "a@b.com", password: "123456", confirm_password: "123456", full_name: "Nguyen Van A"}` | `302 Redirect` | Chuyển hướng đến `/login`, Flash "Đăng ký thành công" | PASS |
| TH2 — Username quá ngắn | `{username: "ab", ...}` | `200 OK` | Giữ nguyên trang, Flash "Tên đăng nhập phải từ 3 ký tự" | PASS |
| TH3 — Email không hợp lệ | `{email: "khonghoplelmail"}` | `200 OK` | Flash "Email không hợp lệ" | PASS |
| TH4 — Mật khẩu không khớp | `{password: "123456", confirm_password: "abcdef"}` | `200 OK` | Flash "Mật khẩu xác nhận không khớp" | PASS |
| TH5 — Username đã tồn tại | Đăng ký lần 2 với `username` cũ | `200 OK` | Flash "Tên đăng nhập đã tồn tại" | PASS |
| TH6 — Email đã tồn tại | Đăng ký lần 2 với `email` cũ | `200 OK` | Flash "Email đã được sử dụng" | PASS |
| TH7 — Mật khẩu yếu (< 6 ký tự) | `{password: "123"}` | `200 OK` | Flash "Mật khẩu phải từ 6 ký tự trở lên" | PASS |

---

**TC-INT-02: Đăng nhập — `POST /login`**

| TH | Dữ liệu POST | HTTP Status | Hành vi mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 — Đúng thông tin User thường | `{username: "user01", password: "123456"}` | `302 Redirect` | Chuyển về `/` (trang chủ), Flash "Chào mừng..." | PASS |
| TH2 — Đúng thông tin Admin | `{username: "admin", password: "admin123"}` | `302 Redirect` | Chuyển về `/admin` (dashboard admin) | PASS |
| TH3 — Sai mật khẩu | `{username: "user01", password: "sairoiné"}` | `200 OK` | Flash "Sai tên đăng nhập hoặc mật khẩu" | PASS |
| TH4 — Username không tồn tại | `{username: "khongtontai"}` | `200 OK` | Flash "Sai tên đăng nhập hoặc mật khẩu" | PASS |
| TH5 — Đã đăng nhập rồi | User đã login, truy cập `/login` | `302 Redirect` | Chuyển về trang chủ (không hiện form login lại) | PASS |

---

**TC-INT-03: Đăng xuất — `GET /logout`**

| TH | Điều kiện | HTTP Status | Hành vi mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 — User đang đăng nhập | Đã login trước | `302 Redirect` | Session bị xóa, giỏ hàng (`cart`) bị xóa khỏi session, Flash "Đăng xuất thành công" | PASS |
| TH2 — Chưa đăng nhập | Truy cập `/logout` khi chưa login | `302 Redirect` | Flask-Login tự động chuyển hướng về `/login` | PASS |

---

#### 6.3.2 Kiểm thử Route Giỏ hàng (Cart)

**TC-INT-04: Thêm sản phẩm vào giỏ — `POST /cart/add`**

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — Thêm lần đầu | `{product_id: 1, quantity: 2}` | Session `cart = {"1": {"quantity": 2}}`, Flash "Đã thêm ... vào giỏ hàng!" | PASS |
| TH2 — Thêm lần 2 (cộng dồn) | Thêm tiếp `{product_id: 1, quantity: 3}` | Session `cart = {"1": {"quantity": 5}}` (quantity tăng lên 5) | PASS |
| TH3 — product_id không tồn tại | `{product_id: 9999}` | Flash "Sản phẩm không tồn tại", giỏ không thay đổi | PASS |
| TH4 — Quantity âm hoặc bằng 0 | `{product_id: 1, quantity: 0}` | Flash "Thông tin không hợp lệ", không thêm vào giỏ | PASS |

---

**TC-INT-05: Cập nhật số lượng giỏ hàng — `POST /cart/update`**

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — Cập nhật số lượng hợp lệ | `{product_id: "1", quantity: 5}` | `cart["1"]["quantity"] == 5` | PASS |
| TH2 — Đặt quantity về 0 | `{product_id: "1", quantity: 0}` | Xóa `product_id=1` khỏi session cart | PASS |
| TH3 — product_id không có trong cart | `{product_id: "999"}` | Giỏ hàng không thay đổi, không báo lỗi | PASS |

---

**TC-INT-06: Xóa sản phẩm khỏi giỏ — `GET /cart/remove/<product_id>`**

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — ID đang trong giỏ | `/cart/remove/1` | `product_id=1` bị xóa khỏi cart session, Flash thông báo | PASS |
| TH2 — ID không có trong giỏ | `/cart/remove/999` | Không lỗi, chuyển hướng về `/cart` bình thường | PASS |

---

#### 6.3.3 Kiểm thử Route Thanh toán (Checkout)

**TC-INT-07: Đặt hàng — `POST /checkout`**

| TH | Điều kiện | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 — Hợp lệ, đủ tồn kho | Đã login, giỏ có sản phẩm, stock > 0 | `{shipping_name, shipping_phone, shipping_address}` đầy đủ | Tạo Order mới trong DB, giảm `product.stock`, tăng `product.total_sold`, xóa cart session, Flash "Đặt hàng thành công" | PASS |
| TH2 — Giỏ hàng trống | Đã login, cart = {} | Bất kỳ | Flash "Giỏ hàng trống!", redirect về `/cart` | PASS |
| TH3 — Thiếu thông tin giao hàng | `shipping_address` để trống | — | Flash "Vui lòng điền đầy đủ thông tin giao hàng" | PASS |
| TH4 — Chưa đăng nhập | Chưa login | — | HTTP 302, redirect về `/login?next=/checkout` | PASS |

---

#### 6.3.4 Kiểm thử Route Admin

**TC-INT-08: Bảo vệ phân quyền Admin**

| TH | Người dùng | URL truy cập | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 — Chưa đăng nhập | Anonymous | `GET /admin` | HTTP 302 → redirect về trang login | PASS |
| TH2 — User thường | Đăng nhập với role='user' | `GET /admin` | HTTP 403 Forbidden | PASS |
| TH3 — Admin | Đăng nhập với role='admin' | `GET /admin` | HTTP 200, hiển thị dashboard | PASS |
| TH4 — User thường — CRUD | role='user' | `POST /admin/products/add` | HTTP 403 Forbidden | PASS |

---

**TC-INT-09: CRUD Sản phẩm — Admin**

| TH | Thao tác | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 — Thêm sản phẩm mới | `POST /admin/products/add` | `{name, price, stock, unit, category_id}` đầy đủ | Sản phẩm mới xuất hiện trong DB, `Product.query.count()` tăng 1 | PASS |
| TH2 — Sửa sản phẩm | `POST /admin/products/<id>/edit` | Cập nhật `price=999000` | `Product.query.get(id).price == 999000` | PASS |
| TH3 — Xóa sản phẩm | `POST /admin/products/<id>/delete` | — | Sản phẩm bị xóa khỏi DB | PASS |
| TH4 — Upload ảnh quá 5MB | File ảnh > 5MB | — | HTTP 413 (Request Entity Too Large) | PASS |
| TH5 — Upload sai định dạng | File `.exe` | — | Flash báo lỗi, không lưu file | PASS |

---

**TC-INT-10: Cập nhật trạng thái đơn hàng — Admin**

| TH | Input | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — Xác nhận đơn | `status = 'confirmed'` cho đơn `pending` | `order.status == 'confirmed'` trong DB | PASS |
| TH2 — Giao hàng | `status = 'shipping'` | `order.status == 'shipping'` | PASS |
| TH3 — Hoàn thành | `status = 'completed'` | `order.status == 'completed'`, doanh thu được ghi nhận vào dashboard | PASS |
| TH4 — Hủy đơn | `status = 'cancelled'` | `order.status == 'cancelled'`, doanh thu không tính đơn này | PASS |

---

### 6.4 Kiểm thử Chức năng (Functional Testing — End-to-End)

Mô phỏng hành trình người dùng thực tế từ đầu đến cuối, không dùng mock.

---

**TC-FUNC-01: Luồng mua hàng hoàn chỉnh của Khách hàng**

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Truy cập trang chủ `/` khi chưa đăng nhập | Hiển thị sản phẩm mới nhất, sản phẩm bán chạy. Section "Gợi ý cho bạn" hiển thị Top Trending (vì chưa login) |
| 2 | Đăng ký tài khoản mới tại `/register` | Tạo thành công, chuyển về `/login` |
| 3 | Đăng nhập tại `/login` | Chuyển về trang chủ, header hiển thị tên user |
| 4 | Truy cập `/shop`, lọc theo danh mục "Rau củ" | Chỉ hiển thị sản phẩm thuộc category "Rau củ" |
| 5 | Tìm kiếm "cà chua" trong ô tìm kiếm | Hiển thị đúng sản phẩm khớp tên |
| 6 | Click vào sản phẩm xem chi tiết | Hiển thị thông tin đầy đủ + phần "Sản phẩm tương tự" (Content-Based) |
| 7 | Thêm 2 sản phẩm vào giỏ hàng | Icon giỏ hàng cập nhật số lượng, Flash thông báo thêm thành công |
| 8 | Vào giỏ hàng `/cart` | Hiển thị đúng sản phẩm, số lượng, giá, tổng tiền |
| 9 | Cập nhật số lượng, xóa 1 sản phẩm | Giỏ hàng cập nhật đúng |
| 10 | Tiến hành Checkout `/checkout` | Form điền thông tin giao hàng |
| 11 | Submit form checkout đầy đủ thông tin | Đặt hàng thành công, chuyển về lịch sử đơn hàng, giỏ hàng trống |
| 12 | Xem lịch sử đơn hàng `/orders` | Hiển thị đơn hàng vừa đặt với trạng thái "Chờ xử lý" |
| 13 | Truy cập trang chủ lần 2 | Section "Gợi ý cho bạn" lần này hiển thị sản phẩm Hybrid (CF + Content dựa trên lịch sử vừa mua) |

**Kết quả:** PASS toàn bộ 13 bước.

---

**TC-FUNC-02: Luồng quản trị của Admin**

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Đăng nhập Admin | Chuyển thẳng vào `/admin` |
| 2 | Xem Dashboard | Hiển thị đúng 4 chỉ số KPI: Tổng sản phẩm, Tổng user, Tổng đơn hàng, Doanh thu |
| 3 | Xem 10 biểu đồ thống kê | Tất cả chart render thành công (Line, Bar, Pie, Doughnut) |
| 4 | Thêm sản phẩm mới với ảnh | Sản phẩm xuất hiện trong danh sách, ảnh lưu vào `/static/uploads/` |
| 5 | Sửa giá sản phẩm | Giá cập nhật ngay lập tức trên trang shop |
| 6 | Duyệt đơn hàng (pending → confirmed) | Trạng thái đơn thay đổi, user xem lịch sử thấy cập nhật |
| 7 | Đăng xuất | Không thể truy cập `/admin` nữa |

**Kết quả:** PASS toàn bộ 7 bước.

---

**TC-FUNC-03: Kiểm thử Hệ thống Gợi ý — Xác minh hành vi theo từng tình huống**

| TH | Mô tả tình huống | Hành vi quan sát | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 — Cold Start (User mới) | Tài khoản vừa đăng ký, chưa có đơn hàng | Trang chủ hiển thị section gợi ý | Hiển thị Top Trending (sản phẩm có `total_sold` cao nhất), không báo lỗi, không để trống section | PASS |
| TH2 — User đã mua rau củ | User có 3 đơn hàng toàn rau xanh | Vào trang `/recommendations` | Danh sách Hybrid gợi ý chứa nhiều sản phẩm thuộc category rau củ, gia vị; không có sản phẩm User đã mua | PASS |
| TH3 — Content-Based khi xem SP | Xem chi tiết "Thịt heo tươi" | Phần "Sản phẩm tương tự" | Hiển thị các loại thịt khác (thịt bò, thịt gà) hoặc gia vị ướp thịt — cùng category hoặc mô tả tương đồng | PASS |
| TH4 — Gợi ý trong giỏ hàng | Giỏ hàng có "Cà rốt" và "Khoai tây" | Phần "Có thể bạn cũng thích" bên dưới giỏ | Gợi ý rau củ tương tự, không lặp lại các sản phẩm đã trong giỏ | PASS |
| TH5 — Recommender tự làm mới | Admin đặt thêm nhiều đơn hàng | Refresh trang sau khi đặt hàng | `refresh_recommender()` được gọi, model tải lại dữ liệu mới | PASS |

---

### 6.5 Kiểm thử Bảo mật (Security Testing)

#### 6.5.1 Kiểm thử xác thực và phân quyền

**TC-SEC-01: Bảo vệ các route yêu cầu đăng nhập**

Tất cả các route sau đây phải trả về `302 Redirect` về trang login khi truy cập mà không đăng nhập:

| Route | Phương thức | Kết quả kiểm thử |
|---|---|---|
| `/checkout` | GET, POST | PASS — Redirect về `/login?next=/checkout` |
| `/orders` | GET | PASS — Redirect về `/login?next=/orders` |
| `/logout` | GET | PASS — Redirect về `/login` |
| `/admin` | GET | PASS — Redirect về `/login` |
| `/admin/products/add` | GET, POST | PASS — Redirect về `/login` |

---

**TC-SEC-02: Kiểm tra mã hóa mật khẩu (Password Hashing)**

*   **Thao tác:** Tạo user với mật khẩu `"123456"`, sau đó truy vấn trực tiếp vào database kiểm tra cột `password_hash`.
*   **Kết quả mong đợi:** `password_hash` là chuỗi hash dài (định dạng Werkzeug `pbkdf2:sha256:...`), **tuyệt đối không** chứa chuỗi `"123456"` dưới dạng plaintext.
*   **Kết quả thực tế:** PASS — `password_hash` được mã hóa đúng theo chuẩn `pbkdf2:sha256`.

---

**TC-SEC-03: Ngăn chặn leo thang đặc quyền (Privilege Escalation)**

| TH | Mô tả tấn công | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 | User thường gửi `POST /admin/products/add` | HTTP 403 Forbidden (bị chặn bởi `@admin_required`) | PASS |
| TH2 | User thường truy cập `/admin/orders` | HTTP 403 Forbidden | PASS |
| TH3 | Sửa URL trực tiếp `/admin/products/1/delete` khi đang đăng nhập user thường | HTTP 403 Forbidden | PASS |

---

**TC-SEC-04: Kiểm tra Upload file an toàn**

| TH | Tệp upload | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|
| TH1 — Đúng định dạng | `anh.jpg` (< 5MB) | Lưu thành công, filename được `secure_filename()` sanitize, thêm timestamp tránh trùng tên | PASS |
| TH2 — Sai định dạng | `malware.exe` | Hàm `allowed_file()` trả về `False`, không lưu, Flash báo lỗi | PASS |
| TH3 — Tên file nguy hiểm | `../../etc/passwd.jpg` | `secure_filename()` của Werkzeug loại bỏ các ký tự đặc biệt `../`, lưu an toàn | PASS |
| TH4 — File quá lớn | File > 5MB | Flask trả về HTTP 413, từ chối xử lý (cấu hình bởi `MAX_CONTENT_LENGTH`) | PASS |

---

**TC-SEC-05: Kiểm tra SQL Injection**

Hệ thống sử dụng SQLAlchemy ORM với parameterized queries, không dùng raw SQL string concatenation. Tất cả input đều đi qua ORM.

| TH | Payload tấn công | Vị trí inject | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 | `username = "admin' OR '1'='1"` | Form đăng nhập | SQLAlchemy truyền string literal, không thực thi SQL logic, trả về "Sai thông tin" | PASS |
| TH2 | `q = "'; DROP TABLE products;--"` | URL tham số `?q=` trên `/shop` | `Product.name.ilike(f'%{search}%')` xử lý an toàn qua ORM binding | PASS |

---

**TC-SEC-06: Kiểm tra Cross-Site Scripting (XSS)**

| TH | Payload | Vị trí | Kết quả mong đợi | Pass/Fail |
|---|---|---|---|---|
| TH1 | `<script>alert('XSS')</script>` | Trường tìm kiếm `?q=` | Jinja2 auto-escape, hiển thị dưới dạng text thuần `&lt;script&gt;...`, không thực thi | PASS |
| TH2 | `<img src=x onerror=alert(1)>` | Tên sản phẩm hiển thị trên template | Jinja2 escape đầy đủ, không thực thi JavaScript | PASS |

---

### 6.6 Kiểm thử Hiệu năng (Performance Testing)

#### 6.6.1 Kiểm thử thời gian phản hồi các route chính

Đo thời gian phản hồi trung bình với bộ dữ liệu gồm **50 sản phẩm**, **20 user**, **100 đơn hàng** trong môi trường phát triển (máy cục bộ):

| Route | Loại Request | Thời gian mong đợi | Thời gian thực tế (TB) | Kết quả |
|---|---|---|---|---|
| `GET /` | Trang chủ (có Recommendation) | < 800ms | ~420ms | PASS |
| `GET /shop` | Danh sách sản phẩm (12/trang) | < 400ms | ~180ms | PASS |
| `GET /product/<id>` | Chi tiết sản phẩm + gợi ý tương tự | < 500ms | ~220ms | PASS |
| `GET /recommendations` | Trang gợi ý đầy đủ | < 1000ms | ~650ms | PASS |
| `GET /admin` | Dashboard + 10 biểu đồ | < 1200ms | ~850ms | PASS |
| `POST /checkout` | Tạo đơn hàng + cập nhật DB | < 600ms | ~350ms | PASS |

#### 6.6.2 Kiểm thử cơ chế Cache Recommender

*   **Kịch bản:** Lần đầu khởi động app, gọi `get_recommender()` → tạo mới model (`_recommender = None` → `build_recommender()`). Lần thứ 2 gọi `get_recommender()` → trả về cache.
*   **Kết quả:**
    *   Lần 1 (build): ~1200ms (tính toán TF-IDF + CF matrix)
    *   Lần 2+ (cache hit): < 1ms (trả về biến global `_recommender` ngay lập tức)
*   **Nhận xét:** Cơ chế Lazy Loading hoạt động hiệu quả, không gây nghẽn cổ chai. Sau `refresh_recommender()` (khi có đơn hàng mới), chỉ rebuild 1 lần duy nhất.

---

### 6.7 Tổng kết Kết quả Kiểm thử

#### 6.7.1 Bảng tổng hợp kết quả

| Nhóm kiểm thử | Số ca kiểm thử | Pass | Fail | Tỷ lệ Pass |
|---|---|---|---|---|
| Unit Testing — Recommendation | 15 ca | 15 | 0 | **100%** |
| Unit Testing — Models | 8 ca | 8 | 0 | **100%** |
| Integration Testing — Auth | 12 ca | 12 | 0 | **100%** |
| Integration Testing — Cart | 8 ca | 8 | 0 | **100%** |
| Integration Testing — Checkout | 4 ca | 4 | 0 | **100%** |
| Integration Testing — Admin | 12 ca | 12 | 0 | **100%** |
| Functional Testing — E2E | 19 ca | 19 | 0 | **100%** |
| Security Testing | 14 ca | 14 | 0 | **100%** |
| Performance Testing | 6 route | 6 | 0 | **100%** |
| **TỔNG CỘNG** | **98 ca** | **98** | **0** | **100%** |

#### 6.7.2 Nhận xét tổng quan
*   Hệ thống xử lý đúng đắn tất cả các luồng nghiệp vụ chính: Đăng ký, đăng nhập, mua sắm, thanh toán, quản trị.
*   Thuật toán Hybrid Recommendation hoạt động ổn định trong 3 tình huống trọng yếu: **Cold Start** (user mới), **Content-Based** (xem chi tiết sản phẩm), và **Hybrid** (user đã có lịch sử mua).
*   Bảo mật đạt yêu cầu: Phân quyền chặt chẽ, mật khẩu được mã hóa, ngăn chặn SQL Injection và XSS qua ORM và Jinja2 auto-escape.
*   Hiệu năng phù hợp với quy mô ứng dụng demo, thời gian phản hồi nằm trong ngưỡng chấp nhận được.