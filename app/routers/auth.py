import models, schemas, utils, oauth2
from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db    
from fastapi.exceptions import HTTPException


router = APIRouter(tags=['Auth'])


@router.post('/login')
def login(user_cred:schemas.UserLogin,db: Session = Depends(get_db)):
    user = db.query(models.Users).filter_by(username=user_cred.username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,'User Not Found')
    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials')
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token, "token_type":"bearer","email":user.username,"first_name":user.first_name,"last_name":user.last_name}

@router.post('/changePassword')
def change_password(password_details:schemas.PasswordChange,db: Session = Depends(get_db),user_id:int=Depends(oauth2.get_current_user)):
    user = db.query(models.Users).filter_by(id=user_id.user_id).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,'User Not Found')
    if not utils.verify(password_details.current_password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')
    if utils.verify(password_details.new_password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials')
    user.password = utils.hash(password_details.new_password)
    user.modified_by = user.user_id
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message":"Password Changed Successfully"}

