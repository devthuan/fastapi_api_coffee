import json
import os
from typing import Annotated, List, Optional, Union
from urllib.parse import quote
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Depends, Form, HTTPException, Query, staticfiles, status, File, UploadFile, FastAPI
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError
from ..schemas.users import EditUser, UserBase
from ..schemas.product import CreateProduct, UpdateProduct, UpdateProductDetail


from ..database import  SessionLocal
from ..crud import user, product
from ..models.entities import ResponseStatus, generate_response
import os
load_dotenv()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router_product = APIRouter()
app = FastAPI()




@router_product.post("/product")
async def create_product(name: Annotated[str, Form()],category_id: Annotated[int, Form()], price: Annotated[float, Form()], file: UploadFile = File(...) , db: Session = Depends(get_db)):
    try:
        # Đảm bảo thư mục uploads tồn tại hay chưa
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        # xây dựng path uploads\\file_path
        file_path = os.path.join("uploads", file.filename)
        image_url = f"http://{os.getenv('IP')}:{os.getenv('PORT')}/{file_path}" 
        
        # lưu ảnh vào folder uploads
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        new_product = CreateProduct(name=name, image=image_url, category_id=category_id, price=price)
        return product.create_product(new_product, db)
    except Exception as e:
      raise HTTPException(500, detail=generate_response("error", 500,f"Internal server error: {str(e)}"))
    
# API post multi product
# @router_product.post("/products")
# async def create_products(
#     names: List[str] = Form(...),
#     category_ids: List[int] = Form(...),
#     prices: List[float] = Form(...),
#     files: List[UploadFile] = File(...),
#     db: Session = Depends(get_db)
# ):
#     product_models = []
#     for name, category_id, price, file in zip(names, category_ids, prices, files):
#         # Đảm bảo thư mục uploads tồn tại hay chưa
#         if not os.path.exists("uploads"):
#             os.makedirs("uploads")

#         # xây dựng path uploads\\file_path
#         file_path = os.path.join("uploads", file.filename)
#         image_url = f"http://{os.getenv('IP')}:{os.getenv('PORT')}/{file_path}"

#         # lưu ảnh vào folder uploads
#         with open(file_path, "wb") as f:
#             f.write(file.file.read())

#         new_product = CreateProduct(name=name, image=image_url, category_id=category_id, price=price)
#         product_models.append(new_product)

#     return product.insert_multi_products(product_models, db)


@router_product.get("/products")
def get__all_product(page: int = Query(1, gt=0), limit: int = Query(30, gt=0), db: Session = Depends(get_db)):
    return product.get_all_product(page, limit, db)

@router_product.get("/product/{product_id}")
def get_product(product_id, db: Session = Depends(get_db)):
    return product.get_product_by_id(product_id,db)


@router_product.get("/product")
def get_product(search: Optional[str] = Query(...), db: Session = Depends(get_db)):
    return product.get_product_by_name(search,db)




@router_product.patch("/product/{product_id}")
async def update_product(product_id,
    name: Annotated[str,Form()],
    category_id: Annotated[int,Form()], 
    price: Annotated[float, Form()], 
    quantity: Annotated[int, Form()], 
    file: Union[str, UploadFile] = [File(...)],
    db: Session = Depends(get_db)
    ):
    
   
    try:
        if isinstance(file, str):
            new_product = UpdateProductDetail(name=name,price=price,quantity=quantity, image=file, category_id=category_id)
            return product.update_product_CRUD(new_product, product_id, db)
        else:
        # Đảm bảo thư mục uploads tồn tại hay chưa
            if not os.path.exists("uploads"):
                os.makedirs("uploads")
            
            # xây dựng path uploads\\file_path
            file_path = os.path.join("uploads", file.filename)
            image_url = f"http://{os.getenv('IP')}:{os.getenv('PORT')}/{file_path}" 
            
            # lưu ảnh vào folder uploads
            with open(file_path, "wb") as f:
                f.write(file.file.read())
            
            # new_product = CreateProduct(name=name, image=image_url, category_id=category_id, price=price)
            product_update = UpdateProductDetail(name=name,price=price, quantity=quantity, image=file_path, category_id=category_id)
            return product.update_product_CRUD(product_update, product_id, db)
    except Exception as e:
      raise HTTPException(500, detail=generate_response("error", 500,f"Internal server error: {str(e)}"))


@router_product.patch("/product/active/{product_id}")
def change_status_user(product_id, db : Session = Depends(get_db)):
    return product.change_status_product(product_id,db)



# @router_product.post("/uploadfile")
# async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     # Ensure the uploads directory exists
#     if not os.path.exists("uploads"):
#         os.makedirs("uploads")
    
#     # Dynamically construct the file path
#     file_path = os.path.join("uploads", file.filename)
    
#     # Write the file to disk
#     with open(file_path, "wb") as f:
#         f.write(file.file.read())
    
#     # Save the file path to the database
#     product = ImageModel(file_path=file_path)
#     db.add(product)
#     db.commit()
#     db.refresh(product)
    
#     # Return the uploaded file name
#     return {"filename": file.filename}

# @router_product.get("/image/{image_id}")
# async def get_image(image_id: int):
#     db = SessionLocal()
#     image_model = db.query(ImageModel).filter(ImageModel.id == image_id).first()
#     db.close()
#     if not image_model:
#         raise HTTPException(status_code=404, detail="Image not found")
    
#     file_path = image_model.file_path
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="Image file not found")
#     image_url = f"http://localhost:8000/{file_path}"  
    
#     return {"image_url": image_url}





  