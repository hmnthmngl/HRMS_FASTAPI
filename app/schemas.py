from pydantic import BaseModel, validator, Field
from datetime import datetime
from typing import Optional,List
from enum import IntEnum

class Status(IntEnum):
    active = 1
    inactive = 0
    
class PaymentMode(IntEnum):
    cash = 0
    card = 1

class BaseEntity(BaseModel):
    created_by : Optional[int]
    created_at : Optional[datetime]
    modified_by : Optional[int]
    modified_at : Optional[datetime]
    comments : Optional[str]
    status : Optional[int]

    @validator('status')
    def set_name(cls, status):
        return Status(status).name 

class UserLogin(BaseModel):

	username :str
	password :str

class PasswordChange(BaseModel):

	current_password :str
	new_password :str

class User(BaseModel):
    id:int
    username:str
    first_name:str
    middle_name:Optional[str] = ""
    last_name:str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class BrandCreate(BaseModel):
    brand_name: str = Field(max_length=120,strip_whitespace=True)
    class Config:
        orm_mode = True

class Brand(BaseEntity,BaseModel):
    id:int
    name:str
    class Config:
        orm_mode = True   

class BrandUpdate(BaseModel):
    brand_name: str = Field(max_length=120,strip_whitespace=True)
    status:str 
    class Config:
        orm_mode = True
    @validator('status')
    def set_name(cls, status):
        return Status[status].value

class Category(BaseEntity,BaseModel):
    id:int
    name:str
    class Config:
        orm_mode = True   

class CategoryCreate(BaseModel):
    category_name: str = Field(max_length=120,strip_whitespace=True)
    class Config:
        orm_mode = True

class CategoryUpdate(BaseModel):
    category_name: str = Field(max_length=120,strip_whitespace=True)
    status:str 
    class Config:
        orm_mode = True
    @validator('status')
    def set_name(cls, status):
        return Status[status].value

class SubCategory(BaseEntity,BaseModel):
    id:int
    name:str
    category:Category
    class Config:
        orm_mode = True   

class SubCategoryCreate(BaseModel):
    subCategory_name: str = Field(max_length=120,strip_whitespace=True)
    category_id:int
    class Config:
        orm_mode = True

class SubCategoryUpdate(BaseModel):
    Subcategory_name: str = Field(max_length=120,strip_whitespace=True)
    category_id:int
    status:str 
    class Config:
        orm_mode = True
    @validator('status')
    def set_name(cls, status):
        return Status[status].value

class Product(BaseEntity,BaseModel):
    id:int
    name:str
    brand:Brand
    category:Category
    sub_category:SubCategory
    units:int
    price:float
    model_number:Optional[str]
    remaining_units:Optional[int]
    class Config:
        orm_mode = True 


class ProductCreate(BaseModel):
    name:str
    brand_id:int
    category_id:int
    sub_category_id:int
    units:int
    price:float
    model_number:Optional[str] = ""
    remaining_units:Optional[int] = None
    class Config:
        orm_mode = True 

class ProductUpdate(BaseEntity,BaseModel):
    id:int
    name:str
    brand_id:int
    category_id:int
    sub_category_id:int
    units:int
    price:float
    model_number:Optional[str] = ""
    class Config:
        orm_mode = True 
    @validator('status')
    def set_name(cls, status):
        return Status[status].value
    
class ProductsCart(BaseModel):
    product_id:int
    units:int
    price:float

class InvoiceCreate(BaseModel):
    customer_name:str
    customer_phone:str=Field(max_length=15)
    payment_mode:str
    total_amount:float
    products: List[ProductsCart]
    class Config:
        orm_mode = True 
    @validator('payment_mode')
    def set_name(cls, payment_mode):
        return PaymentMode[payment_mode].value

class Invoice(BaseModel):
    pass