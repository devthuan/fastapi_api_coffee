import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .routes import authenticate, user, product, cart, order, warehouse, formulas

from .models import tables

from .database import engine, SessionLocal

load_dotenv()
# create the database tables
tables.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  
    # Add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

# Serve static files (images)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.include_router(authenticate.router_authenticate, prefix="/api/v1")
app.include_router(user.router_user, prefix="/api/v1")
app.include_router(product.router_product, prefix="/api/v1")
app.include_router(cart.router_cart, prefix="/api/v1")
app.include_router(order.router_order, prefix="/api/v1")
app.include_router(warehouse.router_warehouse, prefix="/api/v1")
app.include_router(formulas.router_formulas, prefix="/api/v1")