# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** Chưa có tên nhóm trong tài liệu dự án

**Thành viên:** Nguyễn Chí Công (chiến lược heading), Hoàng Trung Anh (SentenceChunker); chưa có thông tin thành viên còn lại.

**Ngày lập báo cáo:** 19/09/2026

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Quy định và dịch vụ đăng ký học phần của Carnegie Mellon University (CMU).

**Tại sao nhóm chọn chủ đề này?**

> Chín tài liệu công khai từ University Registrar cùng xoay quanh lập lịch, đăng ký học phần, giờ bắt đầu đăng ký, thay đổi học phần và voucher. Các quy trình này có mốc thời gian, điều kiện và đối tượng áp dụng cụ thể, nên phù hợp để kiểm tra liệu hệ thống có truy xuất đúng đoạn làm căn cứ cho câu trả lời. Bộ tài liệu có bốn giá trị `audience` (`student`, `faculty`, `staff`, `all`), cho phép thử lọc metadata theo người dùng.

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

Thông tin của Nguyễn Chí Công và Hoàng Trung Anh lấy từ phần đã ghi trong báo cáo và mã hiện có. Chưa có tên, mã và kết quả của thành viên 2 trong dự án.

**Thành viên 1 — Nguyễn Chí Công**

- **Loại chiến lược:** custom `HeadingChunker` → `RecursiveChunker`
- **Mô tả & lý do chọn cho chủ đề này:** Trang quy định CMU có heading/mục sẵn, nên mỗi heading là đơn vị ngữ nghĩa tự nhiên. Chiến lược tách trước heading; nếu mục vượt 500 ký tự thì dùng recursive để cắt phần thân và lặp lại heading ở từng mảnh con, nhờ vậy chunk sau vẫn biết mình đang nói về mục nào.
- **Mã thực thi:** Chưa có file triển khai hoặc kết quả chạy của Nguyễn Chí Công trong dự án hiện tại; cần bổ sung để nhóm có thể tái lập phép so sánh. Mô tả ở trên là chiến lược do thành viên ghi trong báo cáo. Ở bản corpus hiện tại, ngoài tiêu đề cấp `#`, chỉ `staff-non-degree-registration.md` còn tiêu đề cấp `##`; các nhãn mục của tài liệu khác là văn bản thường, nên cần thống nhất bản corpus khi kiểm tra chiến lược theo heading.

**Thành viên 2 — Chưa có thông tin**

- **Loại chiến lược:** Chưa được cung cấp.
- **Mô tả & lý do chọn:** Cần thành viên bổ sung chiến lược thực tế, tham số và lý do chọn trước khi so sánh.
- **Mã thực thi:** Chưa được cung cấp.

**Thành viên 3 — Hoàng Trung Anh**

- **Loại chiến lược:** `SentenceChunker(max_sentences_per_chunk=3)`.
- **Mô tả & lý do chọn:** Tách theo dấu kết thúc câu rồi gom tối đa ba câu liên tiếp thành một chunk. Cách này giữ nguyên câu và các bước hướng dẫn ngắn trong tài liệu đăng ký, voucher và FAQ. Ranh giới có thể cắt giữa một quy trình nhiều câu, và chunk dài không bị giới hạn theo số ký tự; cần đối chiếu top-3 với đáp án chuẩn để đánh giá.
- **Code snippet:** Dùng lớp có sẵn trong `src/chunking.py`; dòng chọn chiến lược trong `bench.py` là:

```python
CHUNKER = SentenceChunker(max_sentences_per_chunk=3)
```

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược | Kết quả hiện có | Điểm mạnh | Điểm yếu / giới hạn |
| ---------- | ---------- | --------------- | --------- | ------------------- |
| Nguyễn Chí Công | Heading → Recursive | Bảng mục 3 ghi 5 kết quả top-1, nhưng thiếu log, cấu hình embedding và câu trả lời agent; chưa thể chấm /10. | Theo thiết kế, giữ tiêu đề khi chia mục dài. | Chưa có mã và dữ liệu chạy cùng phiên bản để xác minh các điểm số đã ghi. |
| Thành viên 2 | Chưa có thông tin | Chưa có kết quả. | Chưa đánh giá. | Chưa thể so sánh. |
| Hoàng Trung Anh | SentenceChunker, 3 câu/chunk | 75 chunk; top-3 có một đoạn liên quan một phần ở câu 1; chưa chạy agent nên chưa chấm /10. | Không cắt giữa câu; ít chunk hơn fixed/recursive trong baseline. | Một quy trình có thể trải qua nhiều chunk; lượt chạy hiện dùng embedding giả lập. |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**

> Chưa thể xếp hạng giữa các thành viên: kết quả SentenceChunker đã chạy bằng `MockEmbedder`, còn bảng điểm Heading hiện thiếu mã, cấu hình embedding và log để tái lập; thành viên 2 chưa có kết quả. Về mặt cấu trúc, các quy trình nhiều bước như Course Time Conflict và Voucher Instructions dễ bị `SentenceChunker` chia qua nhiều chunk; chiến lược theo mục có thể giữ ngữ cảnh tốt hơn nếu corpus có heading Markdown và được kiểm tra trên cùng bộ câu hỏi, embedding và `top_k`.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

Năm câu hỏi dùng chung đều có căn cứ trong corpus. Cột cuối giữ `doc_id` của tài liệu nguồn để `bench.py` đọc đúng bộ câu hỏi. Điều kiện “ít nhất một câu cần lọc `audience=student` mới trả lời đúng” chưa được chứng minh bằng lượt chạy hiện có (xem đối chiếu câu 5 bên dưới).

| #   | Câu hỏi (Query)                                                         | Câu trả lời chuẩn (Gold Answer)                                                                                                      | Tài liệu nguồn (`doc_id`) |
| --- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------- |
| 1   | Quy trình đăng ký hai lớp trùng giờ là gì?                              | Gửi Course Time Conflict Request trên SIO; advisor và hai giảng viên phê duyệt, sau đó sinh viên chấp nhận điều kiện và đăng ký.     | `course-registration` |
| 2   | Sinh viên đại học năm nhất đăng ký vào ngày nào trong kỳ thu/xuân?      | Thứ Sáu.                                                                                                                             | `registration-start-times` |
| 3   | Trước khi dùng voucher sau hạn drop/P/NP, sinh viên phải làm gì?        | Trao đổi với primary academic advisor; advisor nhập voucher vào S3, sinh viên xác nhận trong 24 giờ.                                 | `course-changes` |
| 4   | Sinh viên đại học có bao nhiêu voucher trong toàn khóa và trong một kỳ? | Ba voucher toàn khóa; tối đa một voucher mỗi kỳ (kể cả hè).                                                                          | `course-changes` |
| 5   | Tôi có giờ bắt đầu đăng ký cụ thể không?                                | Với sinh viên, giờ được gán và xem ở trang Registration hoặc Plan Schedule trong SIO; undergraduate dùng ba chữ số cuối của ID Card. | `registration-start-times` |

Trong lượt SentenceChunker hiện tại, các đoạn chứa dữ kiện tương ứng là: câu 1 `course-registration#5–#7`; câu 2 `registration-start-times#2`; câu 3 `course-changes#17–#18`; câu 4 `course-changes#15`; câu 5 `registration-start-times#0–#1`. Việc một đáp án nằm ở nhiều chunk là giới hạn cần tính khi đánh giá top-3.

### Tổng hợp chất lượng truy xuất của nhóm

Theo `docs/SCORING.md`, mỗi câu có tối đa 2 điểm nếu top-3 chứa căn cứ liên quan và câu trả lời của agent chính xác. Bảng dưới giữ nguyên các số top-1 Heading đã được điền trước đó; dự án hiện không có log, mã chạy hoặc tên embedding tương ứng để xác minh. Kết quả Sentence lấy từ [`ket_qua_benchmark.txt`](../ket_qua_benchmark.txt), dùng `MockEmbedder`, `top_k=3`; không có câu trả lời agent của hai lượt trong dự án để chấm điểm /10 hoặc chọn chiến lược tốt nhất.

| # | Heading → Recursive (số đã ghi, chưa xác minh) | SentenceChunker (đã chạy) | Đối chiếu với đáp án chuẩn |
| --- | --- | --- | --- |
| 1 | Top-1 `course-registration`, 0,764 | Top-3 có `course-registration#5`, 0,227 | Sentence nêu bước gửi yêu cầu trên SIO nhưng thiếu chuỗi phê duyệt ở `#6–#7`. |
| 2 | Top-1 `registration-start-times`, 0,760 | Top-3 đều thuộc `voucher-process-faq` | Sentence không lấy được đoạn nêu Friday. |
| 3 | Top-1 `course-changes`, 0,783; báo cáo ghi đã lọc student | Top-1 `course-changes#10`, 0,290; top-3 thiếu `#17–#18` | Sentence lấy phần late withdrawal, không đủ bước voucher. |
| 4 | Top-1 `course-changes`, 0,842; báo cáo ghi đã lọc student | Top-1 `course-changes#6`, 0,233; top-3 thiếu `#15` | Sentence lấy hạn drop, không lấy số voucher. |
| 5 | Top-1 `registration-four-steps`, 0,821; báo cáo ghi đã lọc student | Top-1 `course-registration#8`, 0,413; top-3 thiếu `registration-start-times` | Lọc student trong lượt Sentence không đổi top-3; kết quả Heading top-1 là tài liệu khác tài liệu gold. |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**

> Với SentenceChunker, lọc `audience=student` ở câu 5 giảm tập ứng viên từ 75 xuống 57 chunk, nhưng top-3 và đáp án có thể rút ra vẫn không đổi. Bảng Heading ghi đã lọc ở câu 3–5, song thiếu kết quả không lọc để đo tác động; do đó chưa thể kết luận lọc đã cải thiện truy xuất. Nhóm cần chạy hai lượt trên cùng embedding và corpus, rồi ghi top-3 trước/sau lọc cho một câu hỏi mà câu trả lời phụ thuộc đối tượng áp dụng.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**

- Corpus có 9 tài liệu chính thức về đăng ký học phần, gồm 6 tài liệu `student`, 1 `faculty`, 1 `staff` và 1 `all`; metadata cho phép lọc theo đối tượng trước khi xếp hạng.
- Với `course-registration.md` ở baseline `chunk_size=200`, SentenceChunker tạo 10 chunk, FixedSizeChunker 20 và RecursiveChunker 26. Sentence giữ nguyên câu nhưng không bảo đảm giữ trọn quy trình: đáp án câu 1 nằm ở ba chunk `#5–#7`.
- Benchmark Sentence dùng 75 chunk và `MockEmbedder`: chỉ câu 1 có đoạn top-3 liên quan một phần; lọc student ở câu 5 không thay đổi top-3. Điểm similarity của mock không chứng minh chất lượng hiểu nghĩa giữa câu hỏi tiếng Việt và tài liệu tiếng Anh.

**Bài học rút ra khi so sánh trong nhóm:**

> Cùng một tài liệu, ranh giới chunk quyết định agent nhìn thấy cả quy trình hay chỉ một bước: SentenceChunker giữ nguyên từng câu nhưng tách quy trình Course Time Conflict và voucher qua nhiều chunk. Baseline cho thấy đánh đổi giữa số chunk và độ dài trung bình; chưa thể kết luận Heading tốt hơn Sentence từ các điểm hiện có vì chưa có kết quả các thành viên trên cùng corpus, embedding và cách đánh giá. Phần trình bày nên đối chiếu trực tiếp nội dung chunk, không chỉ so score.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**

> Nhóm sẽ cố định một phiên bản corpus cho mọi thành viên, giữ cấu trúc Markdown heading nếu cần thử chiến lược theo mục, và lưu log gồm cấu hình embedding, chunk ID cùng top-3 của cả năm câu. Sau đó chạy lại bằng cùng một mô hình embedding có hỗ trợ tiếng Việt–Anh, thử cả lượt có/không lọc `audience=student`, và kiểm tra câu trả lời agent với đáp án chuẩn. Với các quy trình nhiều bước, nhóm sẽ thử kích thước hoặc độ chồng lấp câu để giảm việc đáp án nằm rải trên nhiều chunk.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí                                 | Điểm tự đánh giá |
| ---------------------------------------- | ---------------- |
| Lựa chọn tài liệu (Document Set Quality) | Chưa tự chấm / 10; đã có 9 tài liệu và metadata, còn thiếu bằng chứng câu hỏi cần lọc để trả lời đúng. |
| Thiết kế chiến lược (Strategy Design)    | Chưa tự chấm / 15; chưa có mã và kết quả của tất cả thành viên trên cùng cấu hình. |
| Chất lượng truy xuất (Retrieval Quality) | Chưa tự chấm / 10; mới có benchmark mock của Sentence, chưa có câu trả lời agent. |
| Thuyết trình (Demo)                      | Chưa tự chấm / 5; chưa có thông tin buổi demo. |
| **Tổng phần nhóm**                       | **Chưa thể cộng / 40** |
