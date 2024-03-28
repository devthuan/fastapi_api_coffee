

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from app.models.entities import generate_response
from app.schemas.order import OrderCreate
from sqlalchemy.orm import Session, load_only, Load
from sqlalchemy.exc import IntegrityError
from ..models import tables


def create_order_crud(order: OrderCreate, user_id : int, db: Session):
    if not order.order_details:
        raise HTTPException(status_code=400, detail=generate_response("error", 400, "Order details are required"))
    
    try:
        with db.begin():
            order_new = tables.Orders(
                user_id=user_id,
                full_name=order.full_name,
                phone_number=order.phone_number,
                delivery_address=order.delivery_address,
                payment_methods=order.payment_method,
                order_status=order.order_status,
            )
            db.add(order_new)
            db.flush()  # Tạo ra một đơn hàng mới và lấy ID của nó trước khi thêm các chi tiết đơn hàng
            
            for item in order.order_details:
                order_detail = tables.OrderDetail(**item, order_id=order_new.id)
                db.add(order_detail)
                
                # Trừ số lượng sản phẩm từ bảng products và cập nhật số lượng nguyên liệu
                product_id = order_detail.product_id
                quantity = order_detail.quantity
                product = db.query(tables.Products).filter_by(id=product_id).first()
                if product:
                    if product.quantity < quantity:
                        raise HTTPException(status_code=400, detail=generate_response("error", 400, f"Not enough quantity available for product: {product.name_product}"))
                    product.quantity -= quantity
                    
                    db.add(product)  # Thêm lại sản phẩm sau khi cập nhật
                    if product.quantity < 0:
                        raise HTTPException(status_code=400, detail=generate_response("error", 400, f"Invalid quantity available for product: {product.name_product}"))
        
        return generate_response("success", 200, "Create order successfully", order_new.id)
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=generate_response("error", 500, "Cart creation failed. Please check foreign key constraints.", str(e)))
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=generate_response("error", 500, "Internal server error.", str(e)))
# def create_order_crud(order: OrderCreate, user_id : int, db: Session):
#     if not order.order_details:
#         raise HTTPException(status_code=400, detail=generate_response("error", 400, "Order details are required"))
        
#     order_new = tables.Orders(
#         user_id = user_id,
#         full_name =  order.full_name,
#         phone_number=  order.phone_number,
#         delivery_address=  order.delivery_address,
#         payment_methods=  order.payment_method,
#         order_status=  order.order_status,
#     )
    
#     try:
#         with db.begin():
#             db.add(order_new)
#             db.flush()  # Tạo ra một đơn hàng mới và lấy ID của nó trước khi thêm các chi tiết đơn hàng
#             for item in order.order_details:
#                 db.add(tables.OrderDetail(**item, order_id=order_new.id))
#         return generate_response("success", 200, "Create order successfully", order_new.id)
#     except RequestValidationError as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=generate_response("error", 500, "Internal server error.", str(e)))
#     except IntegrityError  as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=generate_response("error", 500, "Cart creation failed. Please check foreign key constraints.", str(e)))
#     except Exception as e:
#          raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))

def get_order_by_user(user_id: int, db: Session):
    try:

        orders = db.query(tables.Orders).filter(tables.Orders.user_id == user_id).all()
        if orders:
            orders_data = []
            for order in orders:
                order_details = []
                total_payment = 0;
                for order_detail, product in db.query(tables.OrderDetail, tables.Products)\
                        .join(tables.Products, tables.OrderDetail.product_id == tables.Products.id)\
                        .filter(tables.OrderDetail.order_id == order.id)\
                        .all():
                    order_details.append({
                        "product_id": order_detail.product_id,
                        "name_product": product.name_product,
                        "image_product": product.image_product,
                        "price": product.price,
                        "quantity": order_detail.quantity
                    })
                    total_payment += product.price * order_detail.quantity
                order_data = {
                    "id": order.id,
                    "full_name": order.full_name,
                    "phone_number": order.phone_number,
                    "delivery_address": order.delivery_address,
                    "payment_methods": order.payment_methods,
                    "order_status": order.order_status,
                    "total_payment": total_payment,
                    "order_details": order_details
                }
                
                orders_data.append(order_data)
            return generate_response("success", 200, "Get orders success", orders_data)
        else:
            return generate_response("error", 404, "Orders not found."), 404
    except Exception as e:
        raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))


def get_all_order(page: int, limit: int, db: Session):
    offset = (page - 1 ) * limit
    try:
        orders = db.query(tables.Orders)\
                    .offset(offset)\
                    .limit(limit)\
                    .all()
        total_items = db.query(tables.Orders).count()
        total_pages = (total_items + limit - 1) // limit
        if orders:
            orders_data = []
            for order in orders:
                order_details = []
                total_payment = 0;
                for order_detail, product in db.query(tables.OrderDetail, tables.Products)\
                        .join(tables.Products, tables.OrderDetail.product_id == tables.Products.id)\
                        .filter(tables.OrderDetail.order_id == order.id)\
                        .all():
                    order_details.append({
                        "product_id": order_detail.product_id,
                        "name_product": product.name_product,
                        "image_product": product.image_product,
                        "price": product.price,
                        "quantity": order_detail.quantity
                    })
                    total_payment += product.price * order_detail.quantity
                order_data = {
                    "id": order.id,
                    "full_name": order.full_name,
                    "phone_number": order.phone_number,
                    "delivery_address": order.delivery_address,
                    "payment_methods": order.payment_methods,
                    "order_status": order.order_status,
                    "total_payment": total_payment,
                    "order_date": order.created_date,
                    "order_details": order_details
                }
                
                
                orders_data.append(order_data)
            data_res = {
                "page": page,   
                "total_page": total_pages,
                "limit": limit,
                "total_items": total_items,
                "data": orders_data
            }
            return generate_response("success", 200, "Get orders success", data_res)
        else:
            return generate_response("error", 404, "Orders not found."), 404
    except Exception as e:
        raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))
    

def update_status_order_crud(order_id: int, new_status: str, db: Session):
    try:
        result_order = db.query(tables.Orders).filter(tables.Orders.id == order_id).first()
        if result_order:
            result_order.order_status = new_status
            db.add(result_order)
            db.commit()
            db.refresh(result_order)
            return generate_response("success", 200, "update status successfully.", result_order)
        else:
            raise HTTPException(status_code=404, detail=generate_response("error", 404, "Order not found."))
    except Exception as e:
            raise HTTPException(500, detail=generate_response("error", 500, "Internal server error.", str(e)))