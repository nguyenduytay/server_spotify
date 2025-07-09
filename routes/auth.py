
import uuid
import bcrypt
from fastapi import Depends, HTTPException, Header
import jwt
from database import get_db
from middleware.auth_middleware import auth_middleware
from models.user import User
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from sqlalchemy.orm import Session
from pydantic_schemas.user_login import UserLogin
from sqlalchemy.orm import joinedload

router = APIRouter()
# create a user
@router.post("/signup", status_code=201)
def signup_user(user: UserCreate, db: Session=Depends(get_db)):
    # extract the data thats coming form req
    user_db = db.query(User).filter(User.email == user.email).first()
    # check if the user already exist in db
    if  user_db:
        raise HTTPException(status_code=400, detail="User with the same email already exist!")
    # hash the password
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    # create a new user
    user_db = User(id=str(uuid.uuid4()), name=user.name, email=user.email, password=hashed_pw)
    db.add(user_db)
    db.commit() 
    db.refresh(user_db)

    return user_db

# login a user
@router.post('/login', status_code=200)
def login_user(user: UserLogin, db: Session=Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="User with the same email does not exist!")
    if not bcrypt.checkpw(user.password.encode(), user_db.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token = jwt.encode({'id': user_db.id}, 'password_key')
    return {'token': token, 'user': user_db}

@router.get('/')
def current_user_data(db: Session=Depends(get_db),
                      user_dict=Depends(auth_middleware)):
   user =db.query(User).filter(User.id == user_dict['uid']).options(
       joinedload(User.favorites)
   ).first()
 
   if not user:
       raise HTTPException(status_code=404, detail="User not found!")
   return user