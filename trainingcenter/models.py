from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from trainingcenter import app, db
from flask_login import UserMixin
from enum import Enum as RoleEnum
from datetime import datetime


class UserRole(RoleEnum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100))
    avatar = Column(String(100))
    username = Column(String(50), unique=True)
    password = Column(String(150))
    email = Column(String(100), unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    courses = relationship('Course', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Course(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100),
                   default='https://res.cloudinary.com/dn0kj5rfm/image/upload/v1719406622/vbefpx8jx0odvo0nodnh.png')
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    description = Column(String(255), nullable=True)
    details = relationship('ReceiptDetails', backref='course', lazy=True)
    comments = relationship('Comment', backref='course', lazy=True)

    def __str__(self):
        return self.name


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


class Receipt(Base):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', uselist=False, lazy=True)  # Quan hệ 1-1


class ReceiptDetails(Base):
    # course_price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    course_id = Column(Integer, ForeignKey(Course.id), nullable=False)
    time_table = Column(String(255), nullable=True)
    school_start_date = db.Column(db.Date, nullable=False)
    school_end_date = db.Column(db.Date, nullable=False)
    # school_start_date = Column(String(100), nullable=True)
    # school_end_date = Column(String(100), nullable=True)


class Comment(Base):
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    course_id = Column(Integer, ForeignKey(Course.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        c1 = Category(name='An ninh Mang')
        c2 = Category(name='Quan tri Mang')
        c3 = Category(name='Quan tri he thong')
        db.session.add_all([c1, c2, c3])
        db.session.commit()

        # import json
        # with open('data/products.json', encoding='utf-8') as f:
        #     products = json.load(f)
        #     for p in products:
        #         prod = Product(**p)
        #         db.session.add(prod)
        #
        # db.session.commit()

        import hashlib
        u = User(name='admin', username='admin', email='abc@gmail.com',
                 avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679731974/jlad6jqdc69cjrh9zggq.jpg',
                 password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
                 user_role=UserRole.ADMIN)
        u2 = User(name='demo', username='demo', email='xyz@gmail.com',
                 avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679731974/jlad6jqdc69cjrh9zggq.jpg',
                 password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
                 user_role=UserRole.USER)
        db.session.add_all([u, u2])
        db.session.commit()

