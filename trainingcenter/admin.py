from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView
from trainingcenter.models import Category, Course, UserRole, User, Receipt, ReceiptDetails
from trainingcenter import app, db, dao
from flask_login import logout_user, current_user
from flask import redirect, request, url_for
from datetime import datetime
from flask import flash, redirect, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SubmitField, FileField, FloatField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from cloudinary.uploader import upload
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import func
import os
import cloudinary.uploader


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ... các cấu hình khác
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')  # Thay đổi 'uploads' thành tên thư mục bạn muốn
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Giới hạn kích thước file tải lên (16 MB)


class CategoryForm(FlaskForm):
    name = StringField('Tên thể loại', validators=[DataRequired()])
    submit = SubmitField('Lưu')


class CourseForm(FlaskForm):
    name = StringField('Tên khóa học', validators=[DataRequired()])
    price = FloatField('Giá khóa học', validators=[DataRequired()])
    image = FileField('Hình ảnh khóa học')
    description = TextAreaField('Mô tả khóa học')
    category_id = SelectField('Thể loại', coerce=int, choices=[(c.id, c.name) for c in Category.query.all()],
                                  validators=[DataRequired()])


class UserForm(FlaskForm):
    name = StringField('Họ tên')  # Không có validation
    username = StringField('Tên đăng nhập')  # Không có validation
    password = PasswordField('Mật khẩu')  # Không có validation
    confirm = PasswordField('Xác nhận mật khẩu')  # Không có validation
    email = StringField('Email')  # Không có validation
    role = SelectField('Vai trò', choices=[
        (UserRole.USER.value, 'USER'),
        (UserRole.ADMIN.value, 'ADMIN')
    ])  # Mỗi phần tử trong choices phải là một tuple (value, label)
    avatar = FileField('Ảnh đại diện')  # Không có validation


# class ReceiptForm(FlaskForm):
#     user_id = SelectField('Người dùng', coerce=int, validators=[DataRequired()])
#     total = DecimalField('Tổng tiền', validators=[DataRequired()])
#     status = SelectField('Trạng thái', choices=[
#         ('pending', 'Chờ xử lý'),
#         ('paid', 'Đã thanh toán'),
#         ('canceled', 'Đã hủy')
#     ], validators=[DataRequired()])
#     created_date = StringField('Ngày tạo')
#     submit = SubmitField('Lưu')


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyCourseView(AuthenticatedView):
    column_list = ['id', 'name', 'price', 'category_id']
    column_labels = {'name': 'Tên khóa học', 'category_id': 'Thể loại'}
    column_sortable_list = ['id', 'name', 'price']  # Cho phép sắp xếp theo id, name, price
    column_default_sort = ('id', False)

    def get_redirect_url(self):
        return "/admin/course/"
    # @expose('/new-course', methods=['GET', 'POST'])
    # def create_view(self):
    #     form = CourseForm()
    #     if form.validate_on_submit():
    #         self.on_model_change(form, None, True)
    #         return redirect(self.get_redirect_url())
    #     return self.render('admin/new-course.html', form=form)

    @expose('/new-course', methods=['GET', 'POST'])
    def create_view(self):
        form = CourseForm()
        if form.validate_on_submit():
            # Tải ảnh lên Cloudinary nếu có ảnh
            image_url = None
            if form.image.data:
                upload_result = cloudinary.uploader.upload(form.image.data)
                image_url = upload_result.get('secure_url')

            self.on_model_change(form, None, True, image_url)
            return redirect(self.get_redirect_url())
        return self.render('admin/new-course.html', form=form)

    @expose('/edit-course/<int:id>', methods=['GET', 'POST'])
    def edit_view(self, id):
        course = Course.query.get_or_404(id)
        form = CourseForm(obj=course)

        if form.validate_on_submit():
            # Tải ảnh lên Cloudinary nếu có ảnh mới
            image_url = course.image  # Giữ lại ảnh cũ nếu không có ảnh mới
            if form.image.data:
                upload_result = cloudinary.uploader.upload(form.image.data)
                image_url = upload_result.get('secure_url')

            self.on_model_change(form, course, False, image_url)
            return redirect(self.get_redirect_url())

        return self.render('admin/edit-course.html', form=form, course=course)

    def on_model_change(self, form, model, is_created, image_url):
        if is_created:
            dao.add_course(name=form.name.data, price=form.price.data,
                           image=image_url, description=form.description.data,
                           category_id=form.category_id.data)
        else:
            dao.update_course(model.id, name=form.name.data, price=form.price.data,
                              image=image_url, description=form.description.data,
                              category_id=form.category_id.data)


class MyCategoryView(AuthenticatedView):
    column_list = ['id', 'name']
    column_labels = {'name': 'Tên thể loại'}
    column_sortable_list = ['id', 'name']  # Cho phép sắp xếp theo id và name
    column_default_sort = ('id', False)

    def get_redirect_url(self):
        # Sử dụng URL rõ ràng cho `/admin/category/`
        return "/admin/category/"

    @expose('/new-category', methods=['GET', 'POST'])
    def create_view(self):
        form = CategoryForm()
        if form.validate_on_submit():
            self.on_model_change(form, None, True)
            return redirect(self.get_redirect_url())
        return self.render('admin/new-category.html', form=form)

    @expose('/edit-category/<int:id>', methods=['GET', 'POST'])
    def edit_view(self, id):
        category = Category.query.get_or_404(id)
        form = CategoryForm(obj=category)

        if form.validate_on_submit():
            self.on_model_change(form, category, False)
            return redirect(self.get_redirect_url())

        return self.render('admin/edit-category.html', form=form)

    def on_model_change(self, form, model, is_created):
        if is_created:
            dao.add_category(name=form.name.data)
        else:
            dao.update_category(model.id, name=form.name.data)


class MyUserView(AuthenticatedView):
    column_list = ['id', 'name', 'username', 'email', 'user_role', 'avatar']
    column_labels = {
        'name': 'Họ tên',
        'username': 'Tên đăng nhập',
        'email': 'Email',
        'user_role': 'Vai trò',
        'avatar': 'Ảnh đại diện'
    }
    column_formatters = {
        'avatar': lambda v, c, m, p: f'<img src="{m.avatar}" width="50" height="50">' if m.avatar else 'No Avatar'
    }
    column_sortable_list = ['id', 'name', 'username']
    column_default_sort = ('id', False)

    def get_redirect_url(self):
        return "/admin/user/"

    @expose('/new-user', methods=['GET', 'POST'])
    def create_view(self):
        form = UserForm()
        if form.validate_on_submit():
            # Kiểm tra nếu có ảnh đại diện
            avatar_url = None
            if form.avatar.data:
                upload_result = cloudinary.uploader.upload(form.avatar.data)
                avatar_url = upload_result.get('secure_url')

            self.on_model_change(form, None, True, avatar_url)
            return redirect(self.get_redirect_url())
        return self.render('admin/new-user.html', form=form)

    @expose('/edit-user/<int:id>', methods=['GET', 'POST'])
    def edit_view(self, id):
        user = User.query.get_or_404(id)
        form = UserForm(obj=user)

        if form.validate_on_submit():
            avatar_url = user.avatar  # Giữ lại ảnh cũ nếu không có ảnh mới
            if form.avatar.data:
                upload_result = cloudinary.uploader.upload(form.avatar.data)
                avatar_url = upload_result.get('secure_url')

            self.on_model_change(form, user, False, avatar_url)
            flash("Thông tin người dùng đã được cập nhật!", "success")
            return redirect(self.get_redirect_url())

        # Pass 'user' explicitly to the template
        return self.render('admin/edit-user.html', form=form, user=user)

    def on_model_change(self, form, model, is_created, avatar_url=None):
        if is_created:
            # Tạo mới người dùng
            dao.add_user(name=form.name.data, username=form.username.data, password=form.password.data,
                         email=form.email.data, role=form.role.data, avatar=avatar_url)
        else:
            # Cập nhật thông tin người dùng
            dao.update_user(model.id, name=form.name.data, username=form.username.data,
                            password=form.password.data, email=form.email.data,
                            role=form.role.data, avatar=avatar_url)


class MyReceiptView(AuthenticatedView):
    column_list = [
        'id',
        'user.name',
        'course_name',  # Tên khóa học
        'time_table',   # Thời khóa biểu
        'school_start_date',  # Ngày bắt đầu
        'school_end_date'  # Ngày kết thúc
    ]

    column_labels = {
        'id': 'Mã hóa đơn',
        'user.name': 'Người dùng',
        'course_name': 'Khóa học',
        'time_table': 'Thời khóa biểu',
        'school_start_date': 'Ngày bắt đầu học',
        'school_end_date': 'Ngày kết thúc học',
    }

    # Tùy chỉnh cách hiển thị bằng formatter
    column_formatters = {
        'course_name': lambda v, c, m, p: m.details.course.name if m.details and m.details.course else 'N/A',
        'time_table': lambda v, c, m, p: m.details.time_table if m.details else 'N/A',
        'school_start_date': lambda v, c, m, p: m.details.school_start_date if m.details else 'N/A',
        'school_end_date': lambda v, c, m, p: m.details.school_end_date if m.details else 'N/A',
    }

    column_sortable_list = ['id', 'user.name']
    column_default_sort = ('id', True)

    # Tắt chức năng tạo mới và chỉnh sửa
    can_create = False
    can_edit = False

    # Bật chức năng xem chi tiết
    can_view_details = True

    # Cho phép xóa
    can_delete = True

    def delete_model(self, model):
        try:
            db.session.delete(model)
            db.session.commit()
            flash("Hóa đơn đã được xóa thành công!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Đã có lỗi xảy ra khi xóa hóa đơn: {str(e)}", "error")

    #
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class StatsView(BaseView):
    @expose('/')
    def index(self):
        # Lấy dữ liệu thống kê doanh thu theo khóa học
        revenue_by_courses = self.stats_revenue_by_course(kw=request.args.get('kw'))

        # Lấy dữ liệu thống kê doanh thu theo tháng/năm
        revenue_by_period = self.stats_revenue_by_period(
            year=request.args.get('year', datetime.now().year),
            period=request.args.get('period', 'month')
        )

        # Render template hiển thị thống kê
        return self.render(
            'admin/stats.html',
            revenue_by_courses=revenue_by_courses,
            revenue_by_period=revenue_by_period
        )

    def stats_revenue_by_course(self, kw=None):
        query = db.session.query(
            Course.id,
            Course.name,
            func.sum(Course.price).label('total_revenue')
        ).join(ReceiptDetails, ReceiptDetails.course_id == Course.id)\
         .join(Receipt, Receipt.id == ReceiptDetails.receipt_id)\
         .filter(Receipt.active == True)

        if kw:
            query = query.filter(Course.name.contains(kw))

        return query.group_by(Course.id).all()

    def stats_revenue_by_period(self, year=datetime.now().year, period='month'):
        query = db.session.query(
            func.extract(period, Receipt.created_date).label('time_period'),
            func.sum(Course.price).label('total_revenue')
        ).join(ReceiptDetails, ReceiptDetails.receipt_id == Receipt.id)\
         .join(Course, Course.id == ReceiptDetails.course_id)\
         .filter(Receipt.active == True)\
         .filter(func.extract('year', Receipt.created_date) == year)

        return query.group_by('time_period')\
                    .order_by('time_period').all()

    def is_accessible(self):
        # Chỉ cho phép người dùng đã đăng nhập
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_courses_by_cate()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app, name='E-commerce Website', template_mode='bootstrap4', index_view=MyAdminIndexView())
# admin.add_view(MyCategoryView(Category, db.session))
# admin.add_view(MyCategoryView(Category, db.session, name='Thể loại', endpoint='my_category_view'))
admin.add_view(MyCategoryView(Category, db.session, name="Category", endpoint="category"))
admin.add_view(MyReceiptView(Receipt, db.session, name="Receipt"))
admin.add_view(MyCourseView(Course, db.session, name='Course', endpoint="course"))
admin.add_view(MyUserView(User, db.session, name="User", endpoint="user"))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))

