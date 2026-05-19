"""
config.py - Cấu hình ứng dụng Flask
Chứa thông tin kết nối Database, Secret Key, và các cấu hình chung.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key cho session và CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY', 'food-store-secret-key-2024')

    # ============================================================
    # CẤU HÌNH MYSQL - Flask-SQLAlchemy
    # Format: mysql+pymysql://username:password@host:port/database
    # ============================================================
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:123456789@localhost:3306/food_store_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Tắt tracking để tiết kiệm bộ nhớ

    # Cấu hình upload ảnh sản phẩm
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Giới hạn file upload 5MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Tham số α cho Hybrid Recommendation (mặc định 0.5)
    RECOMMENDATION_ALPHA = 0.5
    RECOMMENDATION_TOP_N = 8  # Số sản phẩm gợi ý hiển thị
