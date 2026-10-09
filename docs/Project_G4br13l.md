 ***Từ một dòng code bị comment đến nghi vấn phân quyền trong G4br13l***

Nhật ký tự học và điều tra bảo mật của một sinh viên năm 02 An toàn Thông tin.

## 0. Cơ hội để nghịch code

Làm Huynh trưởng và đã xài cái website quản lý Thiếu nhi này suốt ba năm trời, nay tôi có cơ hội tham gia Team Dev website ***doantnttbinhthuan***. Mấy khi được chạm tay vào một hệ thống tầm cỡ, thực tế thế này, nên sau khi được invite collaborator, tôi bắt đầu mổ xẻ đống code để xem bên trong có gì.

P/s: Tôi hoàn toàn - thật sự mù tịt về website development… *Cũng dễ hiểu thôi mà nhỉ... Các học kì trước tôi toàn ngặm ngoạn Computer Architecture, Operating System, Computer Network hay gần đây là môn System Programming, nên nói tới Low Level tôi còn biết chứ Web đồ thì bó tay.

Để học nhanh và tiện, tôi clone --mirror kéo toàn bộ mã nguồn về, rồi lại đẩy lên một repo GitHub private của riêng tôi để ChatGPT có thể access được mà giải đáp các thắc mắc từ tôi. Chiến thuật vọc rất đơn giản: không hiểu chỗ nào thì hỏi chỗ đó, hổng kiến thức nào thì đắp ngay lỗ hổng đó. 

- Bản gốc: Gabriel.
    
- Bản sao tôi clone về: G4br13l.
    

## 1. Hữu duyên với @permission

Trong lúc bị đống code đè và đang học về decorator Python, tôi tình cờ thấy một decorator tên @permission đang bị comment out.

*Ủa, bộ team dev viết dư function này hả ta?*

Có chút máu Séc(-cu-ri-ty) trong người, cứ thấy chữ “permission” là tôi tò mò rồi. Đằng này nó còn đang bị vô hiệu hóa ngay tại một route. Từ đây tôi bắt đầu tìm hiểu đến hai khái niệm:

- Authentication - AuthN (Xác thực): Hệ thống xác định người dùng là ai, chẳng hạn thông qua một phiên đăng nhập hợp lệ.
    
- Authorization - AuthZ (Phân quyền): Hệ thống quyết định người dùng đó được phép làm gì, trên tài nguyên nào.

****Tham khảo tại đây:*** https://www.cloudflare.com/learning/access-management/authn-vs-authz/

Tôi bắt đầu đặt câu hỏi: Nếu route vẫn cho người dùng đăng nhập đi qua (pass AuthN), nhưng cơ chế kiểm tra quyền tại đây đang bị comment out (AuthZ disabled), vậy điều gì ngăn người dùng yêu cầu dữ liệu mà họ không được phép xem?

Vậy là tôi có giả thuyết đầu tiên để kiểm chứng:

## 2. Hypothesis 1

Giả thuyết H1: ***Route trả về dữ liệu của một đối tượng khác chỉ dựa trên phiên đăng nhập hợp lệ của đối tượng hiện tại mà không kiểm tra quyền truy cập của đối tượng hiện tại.***

### Thí nghiệm

Tôi dựng G4br13l trên localhost và tạo hai tài khoản thử nghiệm: User A và User B.

Tôi đăng nhập bằng User A, sau đó dùng curl gửi yêu cầu đến endpoint tra cứu với phiên đăng nhập của User A nhưng ID được yêu cầu là của User B.

### Kết quả quan sát

Server trả về HTTP 200 OK cùng một phản hồi JSON.

[Chèn lệnh đã sử dụng và kết quả đã được loại bỏ thông tin nhạy cảm tại đây.]

Kết quả này ủng hộ giả thuyết H1: yêu cầu đã được xử lý thành công và có phản hồi dữ liệu. 
Nhưng khoan đã! Việc này chỉ ra rằng một Huynh trưởng có thể GET thông tin của một Huynh trưởng khác. 
Đây là điều bình thường hợp với thiết kế phân quyền của hệ thống đó giờ rồi nên chưa chắc đã là lỗi phân quyền.

Tôi cần tìm đến một testcase vững chắc hơn, một kịch bản mà ở đó, Huynh trưởng chắc chắn 100% không được phép nhúng tay vào: Tính năng Điểm danh (Attendance)!
Rõ ràng, Huynh trưởng lớp A chẳng có lý do và quyền hạn gì để xem sổ điểm danh của lớp B.

## 3. Hypothesis 2

Dễ dàng hiểu rằng Huynh trưởng được phân công phụ trách lớp A không mặc nhiên có quyền xem sổ điểm danh của lớp B. 

Giả thuyết H2: Một tài khoản Huynh trưởng có thể đọc dữ liệu điểm danh của lớp nằm ngoài phạm vi quyền được cấp bằng cách yêu cầu API với mã của lớp đó, nếu server chỉ kiểm tra đăng nhập mà không kiểm tra quyền trên lớp được yêu cầu.

Tôi đã tìm thấy route lấy điểm danh theo mã lớp trong mã nguồn. Route này sử dụng @authn mà không hề đụng đến decorator @permission, cũng có thể route để kiểm tra AuthZ nằm ở 1 nơi nào khác. Nên chúng ta cần kiểm tra thực tế.

## 4. Thử nghiệm trên hệ thống đang chạy

Tôi tạo một tình huống gồm hai Teacher, hai Thiếu nhi và hai lớp:

| Đối tượng   | Mã giả       | Phân công |
| ----------- | ------------ | --------- |
| Teacher A   | `HQ261009T1` | Lớp A     |
| Teacher B   | `HQ261009T2` | Lớp B     |
| Thiếu nhi A | `HQ261009S1` | Lớp A     |
| Thiếu nhi B | `HQ261009S2` | Lớp B     |

- Hai lớp sử dụng mã `HQ261009A` và `HQ261009B`; cả hai thuộc grade thử nghiệm `HQ261009G`. (Ở đây dễ hiểu là Courses A và B thuộc Grade G, còn tiền tố `HQ261009` để dễ nhận biết đây là dữ liệu giả)
- Mỗi lớp có một buổi điểm danh vào ngày `2024-01-07`.

Tôi sẽ xét 3 trường hợp:
1. Teacher A xem Lớp A 
2. Teacher A xem Lớp B
3. Teacher B xem Lớp B
Kết quả mong đợi:
- Nếu cả 3 ra 200 -> H2 được ủng hộ.
- Nếu Th 2 ra 403, còn TH 1 và TH 3 ra 200 -> Route vẫn có bước AuthZ, chỉ là đang nằm đâu đó và chúng ta cần tìm hiểu vì sao


BẢNG KẾT QUẢ

| Trường hợp  | HTTP | Dữ liệu trả về |
| ----------- | ---: | -------------- |
| A xem lớp A |  200 | `HQ261009S1`   |
| A xem lớp B |  200 | `HQ261009S2`   |
| B xem lớp B |  200 | `HQ261009S2`   |
Đây là một dấu hiệu đáng chú ý hơn nhiều so với thí nghiệm đầu tiên: Đáng nhẽ tài khoản Teacher A không được phép xem dữ liệu điểm danh của Lớp B, nhưng lại được -> H2 được ủng hộ.

## 5. Vấn đề lớn hơn!

Không dừng lại ở đó! Việc xem và tìm kiếm: Mã định của người dùng (ID User - từ H1), và Mã lớp (ID Courses) là public hoàn toàn trên hệ thống tìm kiếm!

Nhưng mã định danh có thể nhìn thấy không tự nó tạo thành lỗi phân quyền nhưng vấn đề cốt lõi vẫn là liệu server có kiểm tra người gửi yêu cầu được phép truy cập đối tượng đó hay không.

Một 'Huynh trưởng mũ đen' (maybe UITer năm 2) có thể tự động hóa bruce force để thu thập dữ liệu hàng loạt.


## 6. Suggest a fix

Nhưng tìm ra vấn đề mới chỉ là một nửa câu chuyện. Dù gì tôi cũng đã join vào Team Dev rồi, biết đâu đây sẽ là contribution đầu tiên của tôi thì sao ^^. Tôi muốn thử xem liệu mình có thể tự đề xuất một bản sửa, với sự hỗ trợ của AI, thay vì chỉ dừng lại ở việc phát hiện vấn đề.

Thật ra có nhiều hướng xử lý: Nhưng đơn giản là Trước khi truy vấn điểm danh, server phải kiểm tra người đang đăng nhập có được phân công vào lớp đang yêu cầu hay không.

Thế là tôi promt AI viết đoạn code fix bổ sung đoạn kiểm tra vào `getAttendancesByCourse()`:

```python
user_courses = course_service.getUserCourses(
    user_code=g.user.code,
    year_code=course.get('year_code')
)

has_access = any(
    c.get('code') == code
    and c.get('level') in (
        UserLevel.TEACHER.value,
        UserLevel.ASSISTANT.value
    )
    and not c.get('is_abandoned')
    for c in user_courses
)

if not has_access:
    abort(403, "Bạn không có quyền xem điểm danh chi đoàn này")
```


## 7. Retest — Thử lại sau khi sửa

Nhờ tình yêu với UIT (cụ thể là AI Pro) mạnh mẽ hơn sự newbie của tôi, nên code cuối cùng cũng chạy được. Và đưa ra kết quả đẹp như mơ!

|Trường hợp|Trước sửa|Sau sửa|
|---|--:|--:|
|A xem lớp A|`200`|`200`|
|A xem lớp B|`200`|`403`|
|B xem lớp B|`200`|`200`|

Đúng với kỳ vọng của quy tắc phân quyền đang thử nghiệm: Teacher A vẫn xem được Lớp A mà mình phụ trách, nhưng bị từ chối khi yêu cầu Lớp B ngoài phạm vi được phân công.

**Vậy là tôi đã có một bản fix hoạt động đúng với ba testcase trên môi trường localhost!** Dĩ nhiên, đây chưa phải bằng chứng rằng production có cùng hành vi, và quy tắc phân quyền vẫn cần được Team Dev xác nhận.

## 9. What I learnt & what I will do next

Điều tôi học được không chỉ là sự khác biệt giữa Authentication và Authorization. Tôi còn hiểu hơn cách biến một nghi vấn thành một thí nghiệm có thể kiểm chứng, và vì sao phải phân biệt kết quả thực tế với điều mình chỉ đang suy đoán.

Tiếp theo thì tôi muốn hoàn thiện bộ bằng chứng để người khác có thể review: lưu script kiểm thử, dữ liệu giả và `git diff`. Đồng thời, tôi sẽ hỏi Team Dev về chính sách phân quyền thực tế trước khi đề xuất đưa bản sửa vào nhánh chính và có contribution đầu tiên ^^