from trainingcenter import app, login
from flask import render_template, request, redirect, session, jsonify, url_for, flash
import dao
from flask_login import login_user, logout_user, login_required, current_user
import cloudinary.uploader
from decorators import loggedin
import math
from trainingcenter.models import Category
from trainingcenter import app, db
from datetime import datetime, timedelta


@app.route('/')
def index():
    q = request.args.get('q')
    cate_id = request.args.get('category_id')
    page = request.args.get('page')

    courses = dao.load_courses(q=q, cate_id=cate_id, page=page)
    return render_template('index.html', courses=courses,
                           pages=math.ceil(dao.count_course()/app.config['PAGE_SIZE']))


# @app.route("/courses")
# def detail():
#     courses = dao.load_courses()
#     return render_template('courses-detail.html', courses=courses)


@app.route('/courses/<int:id>')
def details(id):
    course = dao.get_course_by_id(course_id=id)
    return render_template('courses-detail.html', course=course)


@app.route('/login', methods=['get', 'post'])
# @loggedin
def login_my_user():
    if current_user.is_authenticated:
        return redirect('/')
    err_msg = ''
    done_msg = request.args.get('done_msg')
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        # print(request.form)

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

            return redirect('/')

            # next = request.args.get('next')
            # return redirect(next if next else '/')
        else:
            err_msg = 'Username hoặc password không đúng!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route("/admin-login", methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password)
    if u:
        login_user(user=u)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
# @loggedin
def register_user():
    err_msg = None
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            avatar_path = None
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

            dao.add_user(name=request.form.get('name'),
                         username=request.form.get('username'),
                         password=password,
                         avatar=avatar_path)

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/courses/<int:course_id>')
def course_detail(course_id):
    # """
    # Hiển thị trang chi tiết khóa học, bao gồm danh sách bình luận.
    # """
    course = dao.get_course_by_id(course_id)  # Lấy thông tin khóa học
    comments = dao.get_comments(course_id)  # Lấy danh sách bình luận

    return render_template('course_detail.html', course=course, comments=comments)


@app.route('/courses/<int:course_id>/register', methods=['GET', 'POST'])
@login_required
def register_course(course_id):
    # Lấy thông tin khóa học
    course = dao.get_course_by_id(course_id)
    if not course:
        flash('Khóa học không tồn tại.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        time_table = request.form.get('time_table')
        school_start_date = request.form.get('school_start_date')

        try:
            school_start_date = datetime.strptime(school_start_date, '%Y-%m-%d')
        except ValueError:
            flash('Ngày bắt đầu không hợp lệ. Vui lòng nhập theo định dạng YYYY-MM-DD.', 'danger')
            return render_template('register-course.html', course=course)

        # Gọi hàm từ dao.py để thêm đăng ký khóa học
        success = dao.add_course_registration(
            user_id=current_user.id,  # Dùng user hiện tại
            course_id=course_id,
            time_table=time_table,
            school_start_date=school_start_date
        )

        if success:
            flash('Đăng ký khóa học thành công!', 'success')
            return redirect(url_for('course_detail', course_id=course_id))
        else:
            flash('Có lỗi xảy ra khi đăng ký. Vui lòng thử lại!', 'danger')

    return render_template('register-course.html', course=course)




@app.route('/courses/<int:course_id>/comments', methods=['POST'])
@login_required
def add_comment(course_id):
    content = request.form.get('content')  # Lấy nội dung bình luận từ form
    if not content.strip():
        flash('Nội dung bình luận không được để trống!', 'error')
    else:
        dao.add_comment(content=content, course_id=course_id)  # Thêm bình luận vào DB
        flash('Bình luận của bạn đã được thêm!', 'success')

    return redirect(url_for('course_detail', course_id=course_id))  # Quay lại trang chi tiết khóa học


# @app.route('/api/courses/<int:id>/comments', methods=['post'])
# @login_required
# def add_comment(id):
#     data = request.json
#     c = dao.add_comment(content=data.get('content'), course_id=id)
#
#     return jsonify({'id': c.id, 'content': c.content, 'user': {
#         'username': c.user.username,
#         'avatar': c.user.avatar
#     }})


@app.context_processor
def common_attributes():
    return {
        'categories': dao.load_categories()
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    with app.app_context():
        from trainingcenter import admin
        app.run(debug=True)

