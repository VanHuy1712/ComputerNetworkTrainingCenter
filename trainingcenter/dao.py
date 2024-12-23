import json
from trainingcenter.models import Category, Course, User, Receipt, ReceiptDetails, Comment
import os.path
from flask_login import current_user
from trainingcenter import app, db
from sqlalchemy import func, desc
from werkzeug.security import generate_password_hash
from cloudinary.uploader import upload
import hashlib
from datetime import datetime, timedelta

from trainingcenter import app


# def read_json(path):
#     with open(path, "r") as f:
#         return json.load(f)


# def load_categories():
#     # return read_json(os.path.join(app.root_path, 'data/categories.json'))
#     with open('data/categories.json', encoding='utf8') as f:
#         return json.load(f)


# def load_courses(q=None, cate_id=None):
#     # courses = read_json(os.path.join(app.root_path, 'data/courses.json'))
#     #
#     # if cate_id:
#     #     courses = []
#     #
#     # return courses
#     with open('data/courses.json', encoding='utf8') as f:
#         courses = json.load(f)
#
#         if q:
#             courses = [co for co in courses if co['name'].find(q) >= 0]
#
#         if cate_id:
#             courses = [co for co in courses if co['category_id'].__eq__(int(cate_id))]
#
#         return courses


# def get_course_by_id(course_id):
#     with open('data/courses.json', encoding='utf8') as f:
#         courses = json.load(f)
#         for co in courses:
#             if co['id'] == course_id:
#                 return co


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_user(name, username, password, avatar, email):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password, avatar=avatar, email=email)
    db.session.add(u)
    db.session.commit()


def update_user(user_id, name, username, email, role, password=None, avatar=None):
    user = User.query.get(user_id)
    if user:
        # Cập nhật các trường cơ bản
        user.name = name
        user.username = username  # Không cho phép sửa username
        user.email = email
        user.user_role = role  # Cập nhật vai trò

        # Chỉ cập nhật mật khẩu nếu người dùng nhập mật khẩu mới
        if password:
            # Mã hóa mật khẩu trước khi lưu vào DB
            user.password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        # Chỉ cập nhật avatar nếu có ảnh mới được tải lên
        if avatar:
            # Tải ảnh lên Cloudinary và lấy URL của ảnh mới
            result = upload(avatar, folder="user_avatars")  # Xử lý upload ảnh đại diện
            user.avatar = result.get("secure_url")  # Cập nhật URL của avatar mới

        # Cập nhật lại dữ liệu trong cơ sở dữ liệu
        db.session.commit()


def get_user_by_id(id):
    return User.query.get(id)


def load_categories():
    return Category.query.all()


def count_course():
    return Course.query.count()


def load_courses(q=None, cate_id=None, page=None):
    query = Course.query

    if q:
        query = query.filter(Course.name.contains(q))

    if cate_id:
        query = query.filter(Course.category_id.__eq__(cate_id))

    if page:
        page_size = app.config['PAGE_SIZE']
        start = (int(page) - 1) * page_size
        query = query.slice(start, start + page_size)

    return query.all()


def get_course_by_id(course_id):
    return Course.query.get(course_id)


# def add_receipt(cart):
#     if cart:
#         r = Receipt(user=current_user)
#         db.session.add(r)
#
#         for c in cart.values():
#             d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
#                                receipt=r, course_id=c['id'])
#             db.session.add(d)
#
#         db.session.commit()


def count_courses_by_cate():
    return db.session.query(Category.id, Category.name,
                            func.count(Course.id)).join(Course, Course.category_id.__eq__(Category.id), isouter=True)\
                     .group_by(Category.id).all()


def stats_revenue_by_course(kw=None):
    query = db.session.query(Course.id, Course.name,
                             func.sum(ReceiptDetails.quantity*ReceiptDetails.unit_price))\
                      .join(ReceiptDetails, ReceiptDetails.course_id.__eq__(Course.id), isouter=True)

    if kw:
        query = query.filter(Course.name.contains(kw))

    return query.group_by(Course.id).all()


def stats_revenue_by_period(year=datetime.now().year, period='month'):
    query = db.session.query(func.extract(period, Receipt.created_date),
                             func.sum(ReceiptDetails.quantity*ReceiptDetails.unit_price))\
                      .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
                      .filter(func.extract('year', Receipt.created_date).__eq__(year))

    return query.group_by(func.extract(period, Receipt.created_date))\
                .order_by(func.extract(period, Receipt.created_date)).all()


def get_comments(course_id):
    # return Comment.query.filter(Comment.course_id.__eq__(course_id)).order_by(-Comment.id)
    return Comment.query.filter(Comment.course_id == course_id).order_by(Comment.id.desc()).all()


def add_comment(content, course_id):
    c = Comment(content=content, course_id=course_id, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c
# c = Comment(content=content, course_id=course_id, user=current_user)
#     db.session.add(c)
#     db.session.commit()
#     return c


def add_course_registration(user_id, course_id, time_table, school_start_date):
    try:
        # Tính ngày kết thúc
        school_end_date = school_start_date + timedelta(days=90)

        # Tạo hóa đơn mới cho người dùng
        receipt = Receipt(user_id=user_id)
        db.session.add(receipt)
        db.session.commit()  # Lưu hóa đơn

        # Lưu thông tin khóa học vào ReceiptDetails
        receipt_detail = ReceiptDetails(
            receipt_id=receipt.id,
            course_id=course_id,
            time_table=time_table,
            school_start_date=school_start_date,
            school_end_date=school_end_date
        )
        db.session.add(receipt_detail)
        db.session.commit()  # Lưu chi tiết hóa đơn

        return True  # Trả về True nếu thành công
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        print(f"Lỗi khi thêm đăng ký khóa học: {e}")
        return False  # Trả về False nếu có lỗi


def add_category(name):
    try:
        print(f"Thêm thể loại với tên: {name}")  # Ghi lại tên thể loại
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category
    except Exception as e:
        db.session.rollback()
        print("Error adding category:", e)
        return None


def update_category(category_id, name):
    try:
        print(f"Cập nhật thể loại với ID {category_id} và tên: {name}")  # Ghi lại thông tin
        category = Category.query.get(category_id)
        if category:
            category.name = name
            db.session.commit()
        return category
    except Exception as e:
        db.session.rollback()
        print("Error updating category:", e)
        return None


def add_course(name, price, image, description, category_id):
    try:
        print(f"Thêm khóa học với tên: {name}, giá: {price}, thể loại ID: {category_id}, ảnh: {image}")
        course = Course(name=name, price=price, image=image, description=description, category_id=category_id)
        db.session.add(course)
        db.session.commit()
        return course
    except Exception as e:
        db.session.rollback()
        print("Error adding course:", e)
        return None


def update_course(course_id, name, price, image, description, category_id):
    try:
        print(f"Cập nhật khóa học với ID {course_id} và tên: {name}, ảnh: {image}")
        course = Course.query.get(course_id)
        if course:
            course.name = name
            course.price = price
            course.image = image  # Cập nhật ảnh mới
            course.description = description
            course.category_id = category_id
            db.session.commit()
        return course
    except Exception as e:
        db.session.rollback()
        print("Error updating course:", e)
        return None


def add_receipt(user_id, total, status, created_date):
    receipt = Receipt(user_id=user_id, total=total, status=status, created_date=created_date)
    db.session.add(receipt)
    db.session.commit()
    return receipt


def update_receipt(receipt_id, user_id, total, status):
    receipt = Receipt.query.get(receipt_id)
    if receipt:
        receipt.user_id = user_id
        receipt.total = total
        receipt.status = status
        db.session.commit()

