# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** [Tên nhóm]

**Thành viên:** [Họ tên từng thành viên]  
**Ngày:** [Ngày nộp]

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** [ví dụ: Customer support FAQ, Luật Việt Nam, công thức nấu ăn, ...]

**Tại sao nhóm chọn chủ đề này?**

> *Viết 2-3 câu:*

### Danh sách tài liệu (Data Inventory)

Số ký tự được tính trên phần nội dung sau YAML frontmatter của từng file `.md` (gồm tiêu đề trong nội dung, không tính metadata). Cả 9 tài liệu đều có `department=registrar`, `language=en`, `retrieved_at=2026-09-19` và `document_version=not-stated`.

| #   | Tên tài liệu                                                                                            | Nguồn (Source URL)                                                                     | Ngày lấy / Phiên bản    | Số ký tự | Metadata đã gán                                                                             |
| --- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------- | -------- | ------------------------------------------------------------------------------------------- |
| 1   | [Course Adds Drops and Withdrawals](../data/university_services/course-changes.md)                      | [CMU Registrar](https://www.cmu.edu/hub/registrar/course-changes/index.html)           | 2026-09-19 / not-stated | 7.040    | `doc_id=course-changes`; `audience=student`; `category=course-changes`                      |
| 2   | [Course Registration](../data/university_services/course-registration.md)                               | [CMU Registrar](https://www.cmu.edu/hub/registrar/registration/)                       | 2026-09-19 / not-stated | 3.865    | `doc_id=course-registration`; `audience=student`; `category=registration`                   |
| 3   | [Non-Degree Faculty Registration](../data/university_services/faculty-staff-non-degree-registration.md) | [CMU Registrar](https://www.cmu.edu/hub/registrar/registration/vnd/faculty-staff.html) | 2026-09-19 / not-stated | 4.900    | `doc_id=faculty-staff-non-degree-registration`; `audience=faculty`; `category=registration` |
| 4   | [Non-Degree Staff Registration](../data/university_services/staff-non-degree-registration.md)           | [CMU Registrar](https://www.cmu.edu/hub/registrar/registration/vnd/faculty-staff.html) | 2026-09-19 / not-stated | 1.116    | `doc_id=staff-non-degree-registration`; `audience=staff`; `category=registration`           |
| 5   | [Plan Course Schedule](../data/university_services/plan-course-schedule.md)                             | [CMU Registrar](https://www.cmu.edu/hub/registrar/courses-and-scheduling/index.html)   | 2026-09-19 / not-stated | 1.775    | `doc_id=plan-course-schedule`; `audience=student`; `category=registration-planning`         |
| 6   | [University Registrar Services Overview](../data/university_services/registrar-services-overview.md)    | [CMU Registrar](https://www.cmu.edu/hub/registrar/)                                    | 2026-09-19 / not-stated | 711      | `doc_id=registrar-services-overview`; `audience=all`; `category=registration-services`      |
| 7   | [Register for Courses in 4 Easy Steps](../data/university_services/registration-four-steps.md)          | [CMU Registrar](https://www.cmu.edu/hub/registrar/registration/steps/)                 | 2026-09-19 / not-stated | 4.695    | `doc_id=registration-four-steps`; `audience=student`; `category=registration`               |
| 8   | [Registration Start Time Assignments](../data/university_services/registration-start-times.md)          | [CMU Registrar](https://www.cmu.edu/hub/registrar/registration/start-times.html)       | 2026-09-19 / not-stated | 2.515    | `doc_id=registration-start-times`; `audience=student`; `category=registration`              |
| 9   | [Voucher Process Frequently Asked Questions](../data/university_services/voucher-process-faq.md)        | [CMU Registrar](https://www.cmu.edu/hub/registrar/course-changes/faq.html)             | 2026-09-19 / not-stated | 2.540    | `doc_id=voucher-process-faq`; `audience=student`; `category=course-changes`                 |

Hai file về đăng ký học không cấp bằng cho giảng viên và nhân viên cùng trích từ một URL, nhưng được tách theo `audience`. `sources.csv` ghi một dòng cho mỗi file.

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**

- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata    | Kiểu                                           | Ví dụ giá trị                                     | Tại sao hữu ích cho truy xuất (retrieval)?                                                                                 |
| ------------------ | ---------------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `doc_id`           | Chuỗi, duy nhất                                | `course-registration`                             | Gắn các chunk với tài liệu gốc để truy vết và xóa theo tài liệu.                                                           |
| `title`            | Chuỗi                                          | `Course Registration`                             | Hiển thị tên tài liệu trong kết quả và giúp nhận diện nội dung nguồn.                                                      |
| `source_url`       | URL                                            | `https://www.cmu.edu/hub/registrar/registration/` | Dẫn về trang nguồn để kiểm chứng câu trả lời.                                                                              |
| `retrieved_at`     | Ngày `YYYY-MM-DD`                              | `2026-09-19`                                      | Cho biết thời điểm nhóm lấy nội dung, hỗ trợ kiểm tra độ mới.                                                              |
| `document_version` | Chuỗi                                          | `not-stated`                                      | Ghi phiên bản hoặc ngày hiệu lực để đối chiếu quy định; các file hiện đang ghi `not-stated`.                               |
| `audience`         | Một trong `student`, `faculty`, `staff`, `all` | `student`                                         | Lọc đúng nhóm người được áp dụng quy định; corpus hiện có cả bốn giá trị.                                                  |
| `department`       | Chuỗi                                          | `registrar`                                       | Xác định đơn vị phụ trách; hiện tất cả tài liệu cùng giá trị nên trường này chưa phân biệt được các tài liệu trong corpus. |
| `category`         | Chuỗi                                          | `registration`, `course-changes`                  | Giới hạn tìm kiếm theo loại dịch vụ/quy trình khi cần.                                                                     |
| `language`         | Mã ngôn ngữ                                    | `en`                                              | Cho biết ngôn ngữ tài liệu; hiện tất cả tài liệu là tiếng Anh nên trường này chưa có tác dụng lọc trong corpus hiện tại.   |

Trường `license_or_permission=public-source` được lưu trong `sources.csv` để ghi căn cứ sử dụng nguồn, không nằm trong YAML frontmatter của các file `.md`.

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare(body, chunk_size=200)` trên ba tài liệu dưới đây. `body` là nội dung sau YAML frontmatter (`text.split("---", 2)[2].strip()`), vì metadata không phải phần cần chia chunk. Trong comparator, `fixed_size` dùng `overlap=0`, còn `by_sentences` gom tối đa ba câu nên có thể tạo chunk dài hơn 200 ký tự. Nhận xét ngữ cảnh dựa trên việc đọc ranh giới các chunk, không phải điểm benchmark truy xuất.

| Tài liệu                           | Chiến lược (Strategy)            | Số lượng Chunk | Độ dài trung bình (ký tự) | Giữ được ngữ cảnh không?                           |
| ---------------------------------- | -------------------------------- | -------------- | ------------------------- | -------------------------------------------------- |
| `course-registration.md`           | FixedSizeChunker (`fixed_size`)  | 20             | 193,2                     | Không tốt: có ranh giới cắt giữa từ.               |
| `course-registration.md`           | SentenceChunker (`by_sentences`) | 10             | 384,0                     | Giữ trọn câu, nhưng chunk khá dài.                 |
| `course-registration.md`           | RecursiveChunker (`recursive`)   | 26             | 148,7                     | Tương đối tốt ở ranh giới câu và đoạn.             |
| `staff-non-degree-registration.md` | FixedSizeChunker (`fixed_size`)  | 6              | 186,0                     | Không tốt: cắt giữa “Staff” và “members”.          |
| `staff-non-degree-registration.md` | SentenceChunker (`by_sentences`) | 3              | 370,3                     | Giữ trọn câu nhưng không giữ rõ cấu trúc heading.  |
| `staff-non-degree-registration.md` | RecursiveChunker (`recursive`)   | 7              | 159,4                     | Tương đối: có heading tách khỏi nội dung ngay sau. |
| `course-changes.md`                | FixedSizeChunker (`fixed_size`)  | 36             | 195,6                     | Không tốt: có ranh giới cắt giữa từ.               |
| `course-changes.md`                | SentenceChunker (`by_sentences`) | 19             | 366,1                     | Giữ trọn câu, nhưng chunk dài hơn 200 ký tự.       |
| `course-changes.md`                | RecursiveChunker (`recursive`)   | 44             | 160,0                     | Tương đối: chunk đầu chỉ chứa tiêu đề.             |

### Chiến lược của từng thành viên

> Mỗi thành viên điền một khối dưới đây (copy thêm nếu nhóm có nhiều hơn 3 người).

**Thành viên 1 — [Tên]**

- **Loại chiến lược:** [FixedSize / Sentence / Recursive / custom]
- **Mô tả & lý do chọn cho chủ đề này:** *(2-3 câu)*
- **Code snippet (nếu custom):**

```python
# Dán mã nguồn (implementation) vào đây
```

**Thành viên 2 — [Tên]**

- **Loại chiến lược:**
- **Mô tả & lý do chọn:**
- **Code snippet (nếu custom):**

**Thành viên 3 — [Hoàng Trung Anh]**

- **Loại chiến lược:** `SentenceChunker(max_sentences_per_chunk=3)`.
- **Mô tả & lý do chọn:** Tách theo dấu kết thúc câu rồi gom tối đa ba câu liên tiếp thành một chunk. Cách này giữ nguyên câu và các bước hướng dẫn ngắn trong tài liệu đăng ký, voucher và FAQ. Ranh giới có thể cắt giữa một quy trình nhiều câu, và chunk dài không bị giới hạn theo số ký tự; cần đối chiếu top-3 với đáp án chuẩn để đánh giá.
- **Code snippet:** Dùng lớp có sẵn trong `src/chunking.py`; dòng chọn chiến lược trong `bench.py` là:

```python
CHUNKER = SentenceChunker(max_sentences_per_chunk=3)
```

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
| ---------- | --------------------- | -------------------- | --------- | -------- |
|            |                       |                      |           |          |
|            |                       |                      |           |          |
|            |                       |                      |           |          |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**

> *Viết 2-3 câu — đây là phần được đánh giá cao nhất (khả năng suy nghĩ & giải thích):*

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| #   | Câu hỏi (Query)                                                         | Câu trả lời chuẩn (Gold Answer)                                                                                                      | Chunk nào chứa thông tin?  |
| --- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| 1   | Quy trình đăng ký hai lớp trùng giờ là gì?                              | Gửi Course Time Conflict Request trên SIO; advisor và hai giảng viên phê duyệt, sau đó sinh viên chấp nhận điều kiện và đăng ký.     | `course-registration`      |
| 2   | Sinh viên đại học năm nhất đăng ký vào ngày nào trong kỳ thu/xuân?      | Thứ Sáu.                                                                                                                             | `registration-start-times` |
| 3   | Trước khi dùng voucher sau hạn drop/P/NP, sinh viên phải làm gì?        | Trao đổi với primary academic advisor; advisor nhập voucher vào S3, sinh viên xác nhận trong 24 giờ.                                 | `course-changes`           |
| 4   | Sinh viên đại học có bao nhiêu voucher trong toàn khóa và trong một kỳ? | Ba voucher toàn khóa; tối đa một voucher mỗi kỳ (kể cả hè).                                                                          | `course-changes`           |
| 5   | Tôi có giờ bắt đầu đăng ký cụ thể không?                                | Với sinh viên, giờ được gán và xem ở trang Registration hoặc Plan Schedule trong SIO; undergraduate dùng ba chữ số cuối của ID Card. | `registration-start-times` |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| #   | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
| --- | ------- | ------------------------------- | ------------------------------- | ------- |
| 1   |         |                                 |                                 |         |
| 2   |         |                                 |                                 |         |
| 3   |         |                                 |                                 |         |
| 4   |         |                                 |                                 |         |
| 5   |         |                                 |                                 |         |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**

> *Viết 2-3 câu:*

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**

> *Liệt kê 2-3 ý:*

**Bài học rút ra khi so sánh trong nhóm:**

> *Viết 2-3 câu — cùng tài liệu nhưng chiến lược khác nhau dẫn tới khác biệt gì?*

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**

> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí                                 | Điểm tự đánh giá |
| ---------------------------------------- | ---------------- |
| Lựa chọn tài liệu (Document Set Quality) | / 10             |
| Thiết kế chiến lược (Strategy Design)    | / 15             |
| Chất lượng truy xuất (Retrieval Quality) | / 10             |
| Thuyết trình (Demo)                      | / 5              |
| **Tổng phần nhóm**                       | **/ 40**         |
