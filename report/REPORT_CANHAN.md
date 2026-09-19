# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** [Hoàng Trung Anh]  
**Nhóm:** [Akatsuki]  
**Ngày:** [19/9/2026]

> **Trạng thái:** Phần code đạt 44/44 bài kiểm thử. Đã chạy benchmark 5 câu trên 9 tài liệu với `SentenceChunker` và embedding local đa ngữ `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**

> Hai vector biểu diễn văn bản hướng gần giống nhau, thường cho thấy hai đoạn nói về nội dung gần nhau. Điểm gần 1 là rất gần về hướng; điểm gần 0 là ít liên quan, còn điểm âm là hướng đối nhau trong không gian vector.

**Ví dụ có độ tương tự CAO:**

- Câu A: "Sinh viên cần đăng ký học phần trước hạn chót."
- Câu B: "Học viên phải chọn môn học trước ngày kết thúc đăng ký."
- Tại sao tương đồng: Hai câu dùng từ khác nhau nhưng cùng nói về việc đăng ký môn trước thời hạn.

**Ví dụ có độ tương tự THẤP:**

- Câu A: "Thư viện cho sinh viên mượn sách trong hai tuần."
- Câu B: "Máy chủ cần được khởi động lại sau khi cập nhật phần mềm."
- Tại sao khác: Một câu nói về dịch vụ thư viện, câu kia nói về vận hành máy chủ.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**

> Cosine đo góc giữa hai vector nên tập trung vào hướng biểu diễn, ít bị ảnh hưởng bởi độ lớn vector. Khoảng cách Euclid còn phụ thuộc độ lớn; hai vector cùng hướng nhưng khác độ dài vẫn có thể bị xem là cách xa nhau.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**

> Bước trượt là `500 - 50 = 450`. Số chunk là `ceil((10.000 - 50) / 450) = ceil(22,11...) = 23`. Kiểm tra bằng `FixedSizeChunker(chunk_size=500, overlap=50)` trên chuỗi 10.000 ký tự cũng cho **23 chunk**.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**

> Bước trượt còn `500 - 100 = 400`, nên số chunk là `ceil((10.000 - 100) / 400) = 25`; chạy `FixedSizeChunker` cũng cho **25 chunk**. Overlap lớn hơn giúp giữ ngữ cảnh ở ranh giới hai chunk, nhưng làm tăng số chunk cần lưu và tìm kiếm.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

> Các mô tả dưới đây phản ánh mã nguồn hiện tại trong `src/`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:

> Tôi tách tại khoảng trắng sau `.`, `!`, `?` bằng biểu thức có lookbehind để giữ lại dấu câu, rồi gom tối đa `max_sentences_per_chunk` câu vào một chunk. Văn bản rỗng trả `[]`; các chữ viết tắt và số thập phân vẫn có thể bị tách sai.

**`RecursiveChunker.chunk` / `_split**` — hướng tiếp cận:

> Tôi thử các dấu phân cách theo thứ tự `\n\n`, `\n`, `. `, dấu cách, rồi từng ký tự. Đoạn vượt `chunk_size` được tách tiếp bằng mức kế tiếp; các mảnh ngắn liền kề được gom lại đến gần giới hạn. Trường hợp dừng là văn bản rỗng, đoạn đã đủ ngắn hoặc đã hết dấu phân cách.

### Lớp EmbeddingStore

**`add_documents` + `search**` — hướng tiếp cận:

> Tôi dùng kho trong bộ nhớ, lưu mỗi `Document` thành một record gồm ID, nội dung, bản sao metadata và embedding. Khi tìm kiếm, tôi nhúng câu hỏi bằng cùng hàm embedding, tính tích vô hướng với các vector tài liệu đã chuẩn hóa, sắp xếp điểm giảm dần và lấy `top_k`.

**`search_with_filter` + `delete_document**` — hướng tiếp cận:

> Tôi lọc ứng viên theo metadata **trước khi** xếp hạng tương đồng, để các kết quả không khớp không chiếm chỗ trong top-k. Khi xóa, tôi bỏ toàn bộ chunk có `metadata['doc_id']` khớp ID tài liệu gốc; hàm trả `True` nếu có bản ghi bị xóa.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:

> Tôi lấy `top_k` chunk liên quan từ store, đánh số và ghi nguồn từng chunk trong ngữ cảnh của prompt. Prompt yêu cầu chỉ trả lời theo ngữ cảnh và trích số đoạn đã dùng; sau đó tôi gọi `llm_fn`. Nếu store không trả về chunk nào, hàm báo không tìm thấy tài liệu mà không gọi LLM.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
Lệnh đã chạy: python -m pytest tests/ -v --tb=short -p no:cacheprovider
Python 3.13.9; pytest 9.1.1; collected 44 items
42 test trong tests/test_solution.py và 2 test trong tests/test_benchmark_eval.py đều PASSED.
============================= 44 passed in 0.06s ==============================
```

**Số lượng bài test vượt qua (pass):** **44 / 44**.

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A                                      | Câu B                                               | Dự đoán | Điểm thực tế | Đúng?        |
| --- | ------------------------------------------ | --------------------------------------------------- | ------- | ------------ | ------------ |
| 1   | Sinh viên đăng ký học phần trực tuyến.     | Học viên chọn môn học trên cổng đăng ký.            | Cao     | -0,1665      | Trái dự đoán |
| 2   | Thư viện mở cửa vào cuối tuần.             | Giờ hoạt động của thư viện ngày thứ bảy là khi nào? | Cao     | -0,1115      | Trái dự đoán |
| 3   | Sinh viên xin học bổng theo thành tích.    | Quy trình cập nhật máy chủ gồm ba bước.             | Thấp    | 0,2139       | Trái dự đoán |
| 4   | Hạn nộp học phí là cuối tháng.             | Ngày cuối cùng để đóng học phí là ngày nào?         | Cao     | 0,1424       | Gần dự đoán  |
| 5   | Quy định mượn sách áp dụng cho giảng viên. | Ký túc xá có bao nhiêu phòng trống?                 | Thấp    | -0,0176      | Gần dự đoán  |

> Điểm thực tế được tính bằng `compute_similarity(_mock_embed(câu A), _mock_embed(câu B))`. `MockEmbedder` tạo vector giả lập, nên các nhãn "đúng/trái dự đoán" chỉ mô tả kết quả của mock, không đo chất lượng hiểu nghĩa.

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**

> Cặp 3 ít liên quan về nghĩa nhưng lại có điểm cao nhất (0,2139), còn cặp 1 gần nghĩa lại có điểm thấp nhất (-0,1665). Điều này cho thấy `MockEmbedder` phù hợp để kiểm thử luồng code, nhưng không thể dùng kết quả của nó để kết luận embedding hiểu ngữ nghĩa tốt hay kém.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

> Kết quả lấy từ `ket_qua_benchmark.txt` (`SentenceChunker`, tối đa 3 câu/chunk, 75 chunk, embedding local đa ngữ). Mỗi ô top-3 ghi `chunk_id` và cosine score theo thứ tự hạng. Điểm retrieval dưới đây chỉ chấm top-3 và nội dung, chưa phải điểm rubric đầy đủ vì chưa có câu trả lời từ agent để đối chiếu.

| #              | Câu hỏi (Query)                                                                                 | Top-3 chunk / score                                                                                                    | Gold `doc_id` trong top-3? | Có đủ dữ kiện trả lời?                                                                                    | Điểm retrieval tạm |
| -------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------ |
| 1              | Quy trình đăng ký hai lớp trùng giờ là gì?                                                      | `registration-start-times#3` 0,523 `plan-course-schedule#0` 0,508 `course-registration#0` 0,489                        | Có, hạng 3                 | Không; chunk đúng tài liệu chỉ là phần giới thiệu, thiếu Course Time Conflict Request và chuỗi phê duyệt. | 0/2                |
| 2              | Sinh viên đại học năm nhất đăng ký vào ngày nào trong kỳ thu/xuân?                              | `registration-start-times#4` 0,574 `registration-start-times#2` 0,570 `registration-start-times#3` 0,554               | Có, hạng 1                 | Có; `#2` ghi first-years register on Friday.                                                              | 2/2                |
| 3              | Trước khi dùng voucher sau hạn drop/P/NP, sinh viên phải làm gì?                                | `course-changes#14` 0,788 `course-changes#16` 0,747 `course-changes#1` 0,668                                           | Có, hạng 1                 | Không; thiếu primary academic advisor, S3 và xác nhận trong 24 giờ ở `#17–#18`.                           | 0/2                |
| 4              | Sinh viên đại học có bao nhiêu voucher trong toàn khóa và trong một kỳ?                         | `course-changes#15` 0,665 `course-changes#16` 0,654 `faculty-staff-non-degree-registration#11` 0,583                   | Có, hạng 1                 | Có; `#15` ghi ba voucher toàn khóa và một mỗi kỳ.                                                         | 2/2                |
| 5, không lọc   | Nếu là sinh viên đại học, giờ đăng ký được xếp theo ID Card hay phải đợi hết Registration Week? | `registration-start-times#3` 0,620 `faculty-staff-non-degree-registration#12` 0,596 `registration-start-times#4` 0,592 | Có, hạng 1                 | Không; thiếu quy tắc ba chữ số cuối ID Card.                                                              | 0/2                |
| 5, lọc student | Cùng câu hỏi với `metadata_filter={"audience": "student"}`                                      | `registration-start-times#3` 0,620 `registration-start-times#4` 0,592 `registration-start-times#1` 0,585               | Có, hạng 1                 | Có; `#1` ghi ba chữ số cuối ID Card, `#3` ghi được đăng ký sau giờ đã gán.                                | 2/2                |

**Hai mức chấm:** Với 5 lượt không lọc, kiểm tra theo `doc_id` cho **5/5**, nhưng kiểm tra chuỗi đáp án trong các chunk gold chỉ cho **2/5**; điểm retrieval tạm là **4/10**. Câu 3 là lỗi rõ nhất: cả ba kết quả cùng `course-changes`, nhưng không có đoạn chứa bước nhập S3 và xác nhận trong 24 giờ. Ở câu 5, filter thay chunk faculty bằng đoạn undergraduate, giúp điểm nội dung tăng từ **0/2 lên 2/2**; đây là bằng chứng thực tế cho lợi ích lọc metadata trên chiến lược cá nhân.

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**

> Chưa có dữ liệu từ buổi demo; cần ghi lại một nhận xét thực tế sau khi nghe thành viên hoặc nhóm khác trình bày.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí                                        | Điểm tự đánh giá                                                         |
| ----------------------------------------------- | ------------------------------------------------------------------------ |
| Khởi động (Warm-up)                             | 5/ 5                                                                     |
| Hướng tiếp cận của tôi (My Approach)            | 9/10                                                                     |
| Hoàn thiện code (Core Implementation — tests)   | 30 / 30 (44/44 test)                                                     |
| Dự đoán độ tương tự (Similarity Predictions)    | 5/5                                                                      |
| Kết quả truy xuất của tôi (Competition Results) | 4/10 điểm retrieval tạm; chưa có câu trả lời agent để chấm rubric đầy đủ |
| **Tổng phần cá nhân**                           | **53/60**                                                                |
