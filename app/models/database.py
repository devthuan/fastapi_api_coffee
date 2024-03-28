# from datetime import datetime
# from sqlalchemy import DATETIME, Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String
# from sqlalchemy.orm import relationship

# from ..database import Base



# class Users(Base):
#     __tablename__ = 'Users'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     email = Column(String(255))
#     password = Column(String(255))
#     status = Column(String(50))
#     role_id = Column(Integer, ForeignKey('Roles.id'))
#     created_date = Column(DateTime, default=datetime.now)
    
#     role = relationship("Role", back_populates="users")
#     user_cart = relationship("Cart", back_populates="users")
#     employee = relationship("Employees", back_populates="users",  lazy=True)
#     orders = relationship("Orders", back_populates="users", lazy=True)
    

# class Role(Base):
#     __tablename__ = 'Roles'
#     id = Column(Integer, primary_key=True)
#     code = Column(String(255), unique=True)
#     name = Column(String(255))
#     description = Column(String(255))
#     status = Column(String(50))
    
#     users = relationship("User", back_populates="role")
#     role_permissions = relationship("RolePermission", back_populates="role", lazy=True)

# class Permission(Base):
#     __tablename__ = 'Permissions'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     code = Column(String(255), unique=True)
#     name = Column(String(255))
#     description = Column(String(255))
#     url_api = Column(String(255))
#     method_api = Column(String(50))
#     type = Column(String(50))
#     status = Column(String(50))
    
#     permission_roles = relationship("RolePermission", back_populates="permission", lazy=True)

# class RolePermission(Base):
#     __tablename__ = 'Role_Permission'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     role_id = Column(Integer, ForeignKey('Roles.id'))
#     permission_id = Column(Integer, ForeignKey('Permissions.id'))
#     assigned_date = Column(Date)
#     status = Column(String(50))
    
#     role = relationship("Role", back_populates="role_permissions", lazy=True)
#     permission = relationship("Permission", back_populates="permission_roles", lazy=True)

# class Category(Base):
#     __tablename__ = 'Category'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_category = Column(String(100), nullable=True)
#     description = Column(String(100), nullable=False)
#     is_active = Column(Boolean, default=True)
#     created_date = Column(DateTime, default=datetime.now())
    
#     products = relationship("Products", back_populates="category", lazy=True)
    

# class Products(Base):
#     __tablename__ = 'Products'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name_product = Column(String(255), nullable=False)
#     image_product = Column(String(255))
#     category_id = Column(Integer, ForeignKey('Category.id'))
#     price = Column(Numeric(10, 2), nullable=False)
#     is_active = Column(Boolean, default=True)
#     created_date = Column(DATETIME, default=datetime.now())
    
#     category = relationship("Category", back_populates="products", lazy=True)
#     cart_product = relationship("Cart", back_populates="products", lazy=True)
#     order_details = relationship("OrderDetail", back_populates="products", lazy=True)
    
    

# class Cart(Base):
#     __tablename__ = 'Cart'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
#     product_id = Column(Integer, ForeignKey('Products.id'), nullable=False)
#     quantity = Column(Integer, nullable=False)
    
#     users = relationship("User", back_populates="user_cart",  lazy=True)
#     products = relationship("Products", back_populates="cart_product", lazy=True)
 
# class Employees(Base):
#     __tablename__ = 'Employees'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     employee_name = Column(String(255), nullable=False)
#     user_id = Column(Integer, ForeignKey('Users.id'))
#     employee_email = Column(String(255))
#     phone = Column(String(10), nullable=False)
#     position = Column(String(255))
#     created_date = Column(DATETIME, default=datetime.now())
    
#     users = relationship('User', back_populates='employee', lazy=True)
#     shift = relationship('Shifts', back_populates='employee')
#     salary = relationship('Salary', back_populates='employee')

# class Shifts(Base):
#     __tablename__= "Shifts"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     employee_id = Column(Integer, ForeignKey('Employees'))
#     shift_date = Column(DATETIME, nullable=False)
#     start_time = Column(DATETIME)
#     end_time = Column(DATETIME)
#     description = Column(String(255))
#     created_date = Column(DATETIME, default=datetime.now())
    
#     employee = relationship('Employees', back_populates='shift')

# class SalaryBonus(Base):
#     __tablename__= "SalaryBonus"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     employee_id = Column(Integer, ForeignKey('Employees'))
#     salary_amount = Column(Integer)
#     bonus_amount = Column(Integer)
#     reason_bonus = Column(String(255))
#     created_date = Column(DATETIME, default=datetime.now())
    
#     employee = relationship('Employees', back_populates='salary')



# class Orders(Base):
#     __tablename__ = 'Orders'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
#     full_name = Column(String(100), nullable=False)
#     phone_number = Column(String(10), nullable=False)
#     delivery_address = Column(String(255), nullable=False)
#     order_date = Column(DATETIME, nullable=False)
#     payment_methods = Column(String(255), nullable=False)
#     order_status = Column(String(255), nullable=False)
    
#     users = relationship("User", back_populates="orders", lazy=True)
#     order_details = relationship("OrderDetail", back_populates="order", lazy=True)

# class OrderDetail(Base):
#     __tablename__ = 'OrderDetail'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     order_id = Column(Integer, ForeignKey('Orders.id'), nullable=False)
#     product_id = Column(Integer, ForeignKey('Products.id'), nullable=False)
#     quantity = Column(Integer, nullable=False)
    
#     order = relationship("Orders", back_populates="order_details", lazy=True)
#     products = relationship("Products", back_populates="order_details", lazy=True)

    
    
# class ImageModel(Base):
#     __tablename__ = "images"

#     id = Column(Integer, primary_key=True, index=True)
#     file_path = Column(String(255))
