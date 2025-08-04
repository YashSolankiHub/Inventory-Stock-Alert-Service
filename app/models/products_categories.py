from sqlalchemy import Table, ForeignKey, Column
from app.db.base import Base




#association table for products and categories (many to many relationship)
products_categories = Table(
    'student_course',
    Base.metadata,
    Column('product_id', ForeignKey("products.id"),primary_key=True),
    Column('category_id', ForeignKey("categories.id"),primary_key=True),
)
