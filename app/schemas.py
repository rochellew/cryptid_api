from pydantic import BaseModel, ConfigDict

class CryptidBase(BaseModel):
    name: str
    description: str
    image_url: str

class CryptidCreate(CryptidBase):
    pass

class CryptidUpdate(CryptidBase):
    pass

class CryptidResponse(CryptidBase):
    id: int # include `id` in the response schema
    model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True