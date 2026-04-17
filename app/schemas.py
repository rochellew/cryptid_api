from pydantic import BaseModel, ConfigDict, Field

class CryptidBase(BaseModel):
    name: str = Field(description="The name of the cryptid")
    description: str = Field(description = "A brief description of the cryptid")
    image_url: str = Field(description="URL to an image of the cryptid")

class CryptidCreate(CryptidBase):
    pass

class CryptidUpdate(CryptidBase):
    pass

class CryptidResponse(CryptidBase):
    id: int # include `id` in the response schema
    model_config = ConfigDict(from_attributes=True)
