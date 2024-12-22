# ComputerNetworkTrainingCenter
Dùng công nghệ python và mysql tạo nên website buôn bán sản phẩm các khóa học online 

Trong project này sử dụng ngôn ngữ cho backend là python và framework là flask, phía cơ sở dữ liệu là mysql

Để cài các thư viên chạy project này thì cần vào đường dẫn trainingcenter và gõ lệnh: pip install requirements.txt

Hiện tại, em đã đính kèm cả file trainingcenerdb.sql (cơ sở dữ liệu) vào đây nếu mà muốn tọa người dùng và thử dữ liệu thì sau khi đã tải các requirements.txt rồi, 
thì sẽ chạy file models.py để tạo 2 người dùng với vai trò lần lượt là admin và user.

Khi mà muốn db mới thì sẽ vào __init__.py chỉnh phần tên của db lại.

Để liên kết vào database và liên kết vào cloudinary thì có thể chỉnh vào __init__.py

Ở đây dùng flask_admin nên sẽ có 2 trang giao diện là của người dùng và admin:
1. Là giao diện ai cũng vào được tức là người dùng đăng ký khóa học và có thể comment vào khóa học đó, đăng ký / đăng nhập
2. Là giao diện cho admin ở phía quản lý khóa học, người dùng, thể loại, hóa đơn, xem thống kê báo cáo doanh thu.

Nếu sử dụng database đã cung cấp thì sẽ có 2 tài khoản là admin và user:
- Tài khoản: admin, Mật khẩu: 123456 vai trò là admin
- Tài khoản: demo, Mật khẩu: 123456 vai trò là user
