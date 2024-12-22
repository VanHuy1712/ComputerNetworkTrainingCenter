# ComputerNetworkTrainingCenter
Dùng công nghệ python và mysql tạo nên website buôn bán sản phẩm các khóa học online 

Trong project này sử dụng ngôn ngữ cho backend là python và framework là flask, phía cơ sở dữ liệu là mysql

Để cài các thư viên chạy project này thì cần vào đường dẫn trainingcenter và gõ lệnh: pip install requirements.txt

Hiện tại, em đã đính kèm cả file trainingcenerdb.sql vào đây nếu mà muốn tọa người dùng và thử dữ liệu thì sau khi đã tải các requirements.txt rồi, 
thì sẽ chạy file models.py để tạo 2 người dùng với vai trò lần lượt là admin và user.

Để liên kết vào database và liên kết vào cloudinary thì có thể chỉnh vào __init__.py

Ở đây dùng flask_admin nên sẽ có 2 trang giao diện:
1. Là giao diện ai cũng vào được tức là người dùng đăng ký khóa học và có thể comment vào khóa học đó, đăng ký / đăng nhập
2. Là giao diện cho admin ở phía quản lý khóa học, người dùng, thể loại, hóa đơn, xem thống kê báo cáo doanh thu.
