from typing import List,  Dict
import models, schemas, oauth2
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db    
from fastapi.exceptions import HTTPException
from sqlalchemy import func
from datetime import datetime


router = APIRouter(tags=['IMS'])

@router.post('/brand',status_code=status.HTTP_201_CREATED,response_model=schemas.Brand)
def create_brand(brand : schemas.BrandCreate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    brand_check = db.query(models.Brands).filter(func.lower(models.Brands.name)==func.lower(brand.brand_name)).first()
    if brand_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Already a brand exists with {brand.brand_name} name')
    new_brand = models.Brands(name=brand.brand_name,status=schemas.Status.active.value,created_by=user.id,modified_by=user.id)
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand  

@router.get('/brand',response_model=Dict[str,List[schemas.Brand]])
def get_all_brands(db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    brands = db.query(models.Brands).limit(limit).offset(skip).all()
    return {"brands":brands}

@router.put('/brand/{brand_id}',response_model=schemas.Brand)
def update_brand(brand_id:int,obj : schemas.BrandUpdate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    brand = db.query(models.Brands).filter_by(id=brand_id).first()
    if not brand:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'Brand not found')
    brand_check = db.query(models.Brands).filter(func.lower(models.Brands.name)==func.lower(obj.brand_name),models.Brands.id!=brand_id).first()
    if brand_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Already a brand exists with {obj.brand_name} name')
    brand.name = obj.brand_name
    brand.status = obj.status
    brand.modified_by = user.id
    brand.modified_at = datetime.now()
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand

@router.post('/category',status_code=status.HTTP_201_CREATED,response_model=schemas.Category)
def create_category(obj : schemas.CategoryCreate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    category_check = db.query(models.Categories).filter(func.lower(models.Categories.name)==func.lower(obj.category_name)).first()
    if category_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Already a category exists with {obj.category_name} name')
    new_category = models.Categories(name=obj.category_name,status=schemas.Status.active.value,created_by=user.id,modified_by=user.id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category  

@router.get('/category',response_model=Dict[str,List[schemas.Category]])
def get_all_categories(db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    categories = db.query(models.Categories).limit(limit).offset(skip).all()  
    return {"categories":categories}

@router.get('/categoryDD',response_model=Dict[str,List[schemas.Category]])
def get_all_categories_for_dd(db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    categories = db.query(models.Categories).all()  
    return {"categories":categories}

@router.put('/category/{category_id}',response_model=schemas.Category)
def update_category(category_id:int,obj : schemas.CategoryUpdate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    category = db.query(models.Categories).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'Category not found')
    category_check = db.query(models.Categories).filter(func.lower(models.Categories.name)==func.lower(obj.category_name),models.Categories.id!=category_id).first()
    if category_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Already a category exists with {obj.category_name} name')
    category.name = obj.category_name
    category.status = obj.status
    category.modified_by = user.id
    category.modified_at = datetime.now()
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.post('/subCategory',status_code=status.HTTP_201_CREATED,response_model=schemas.SubCategory)
def create_subCategory(subcat : schemas.SubCategoryCreate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    category_check = db.query(models.Categories).filter_by(id=subcat.category_id).first()
    if not category_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Category does not exist')
    subCategory_check = db.query(models.SubCategories).filter(func.lower(models.Brands.name)==func.lower(subcat.subCategory_name)).first()
    if subCategory_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Already a sub category exists with {subcat.subCategory_name} name')
    new_subCategory = models.SubCategories(name=subcat.subCategory_name,category_id=subcat.category_id,status=schemas.Status.active.value,created_by=user.id,modified_by=user.id)
    db.add(new_subCategory)
    db.commit()
    db.refresh(new_subCategory)
    return new_subCategory  

@router.get('/subCategory',response_model=Dict[str,List[schemas.SubCategory]])
def get_all_subCategories(db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    sub_categories = db.query(models.SubCategories).limit(limit).offset(skip).all()
    return {"sub_categories":sub_categories}

@router.put('/subCategory/{id}',response_model=schemas.SubCategory)
def update_brand(id:int,obj : schemas.SubCategoryUpdate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    category_check = db.query(models.Categories).filter_by(id=obj.category_id).first()
    if not category_check:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'Category not found')
    sub_category_check = db.query(models.SubCategories).filter_by(id=id).first()
    if not sub_category_check:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'Sub category not found')
    sub_category_name_check = db.query(models.SubCategories).filter(func.lower(models.SubCategories.name)==func.lower(obj.Subcategory_name),models.SubCategories.id!=id).first()
    if sub_category_name_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Already a sub category exists with {obj.Subcategory_name} name')
    sub_category = db.query(models.SubCategories).filter_by(id=id).first()
    sub_category.name = obj.Subcategory_name
    sub_category.status = obj.status
    sub_category.modified_by = user.id
    sub_category.modified_at = datetime.now()
    sub_category.category_id = obj.category_id
    db.add(sub_category)
    db.commit()
    db.refresh(sub_category)
    return sub_category

@router.get('/subCategoryDD/{category_id}',response_model=Dict[str,List[schemas.SubCategory]])
def get_all_subCategories_for_dd(category_id:int,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    sub_categories = db.query(models.SubCategories).filter_by(category_id=category_id).all()  
    return {"sub_categories":sub_categories}

@router.get('/product',response_model=Dict[str,List[schemas.Product]])
def get_all_products(db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    products = db.query(models.Products).limit(limit).offset(skip).all()
    return {"prodcuts":products}

@router.post('/product',status_code=status.HTTP_201_CREATED,response_model=schemas.Product)
def create_product(product_obj : schemas.ProductCreate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    print(product_obj)
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    brand = db.query(models.Brands).filter_by(id=product_obj.brand_id).first()
    if not brand:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'Brand not found')
    category_check = db.query(models.Categories).filter_by(id=product_obj.category_id).first()
    if not category_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Category does not exist')
    subCategory_check = db.query(models.SubCategories).filter_by(id=product_obj.sub_category_id).first()
    if not subCategory_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Sub category does not exist')
    new_product = models.Products(name=product_obj.name,category_id=product_obj.category_id,sub_category_id=product_obj.sub_category_id,brand_id=product_obj.brand_id,price=product_obj.price,status=schemas.Status['active'].value,created_by=user.id,modified_by=user.id,units=product_obj.units,model_number=product_obj.model_number,remaining_units=product_obj.units)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product  

@router.put('/product/{id}',response_model=schemas.Product)
def update_product(id:int,obj : schemas.ProductUpdate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    category_check = db.query(models.Categories).filter_by(id=obj.category_id).first()
    if not category_check:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'Category not found')
    brand_check = db.query(models.SubCategories).filter_by(id=obj.brand_id).first()
    if not brand_check:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'Brand not found')
    product_check= db.query(models.Products).filter(models.Products.name==obj.name,models.Products.category_id==obj.category_id,models.Products.sub_category_id==obj.sub_category_id,models.products.id!=id).first()
    if product_check :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Already a product exists in same category')     
    product = db.query(models.Products).filter_by(id=obj.id).first()
    product.brand_id = obj.brand_id
    product.category_id = obj.category_id
    product.sub_category_id = obj.sub_category_id
    product.name = obj.name
    product.units = obj.units
    product.price = obj.price
    product.model_number = obj.model_number
    product.modified_by = user.id
    product.modified_at = datetime.now()
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get('/product/{product_id}',response_model=Dict[str,schemas.Product])
def get_product(product_id:int,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    product = db.query(models.Products).filter_by(id=product_id).first()
    if product:
        return {"prodcut":product}
    raise HTTPException(status.HTTP_403_FORBIDDEN,'Product not found') 

# def get_invoice_details(invoice_id):


@router.post('/invoice')
def get_product(obj : schemas.InvoiceCreate,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User not found')
    customer = db.query(models.Customers).filter(func.lower(models.Customers.name)==func.lower(obj.customer_name),models.Customers.phone==obj.customer_phone).first()
    if customer:
        customer_id = customer.id
    else:
        new_customer = models.Customers(name=obj.customer_name,phone=obj.customer_phone,created_by=user.id,status=schemas.Status.active.value)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        customer_id = new_customer.id
    new_invoice = models.Invoices(customer_id=customer_id,payment_mode=obj.payment_mode,total_amount=obj.total_amount)
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    for item in obj.products:
        invoice_product = models.InvoicesProducts(invoice_id=new_invoice.id,product_id=item.product_id,quantity=item.units,price=item.price)
        db.add(invoice_product)
        db.commit()
        db.refresh(invoice_product)
        update_items = db.query(models.Products).filter_by(product_id=item.product_id).first()
        update_items.units = update_items.units - item.units
        update_items.modified_at = datetime.now()
        update_items.modified_by = user.id
        db.add(update_items)
        db.commit()
        db.refresh(update_items)
    

    return {"message":"Invoice generated successfully"}


@router.get('/test')
def test(db: Session = Depends(get_db)):  
    return schemas.Status['active'].value
