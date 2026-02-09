from pydantic import BaseModel
from typing import Optional

# Schema untuk data yang dikirim saat Login
class LoginRequest(BaseModel):
    username: str # Di FastAPI OAuth2, 'username' biasanya diisi email
    password: str

# Schema untuk Token yang dikirim balik ke Client
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema untuk isi dari Token (Payload)
class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None