from pydantic import BaseModel

class CryptidBase(BaseModel):
    name: str
    description: str
    image_url: str

class CryptidCreate(CryptidBase):
    pass

class CryptidResponse(CryptidBase):
    id: int # include `id` in the response schema

    class Config:
        orm_mode = True