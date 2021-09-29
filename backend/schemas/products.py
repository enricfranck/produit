from typing import Optional

from pydantic import BaseModel


# shared properties
class ProductBase(BaseModel):
    nom: str
    cathegorie: Optional[str] = None
    description: Optional[str] = None


# this will be used to validate data while creating a Job
class ProductCreate(ProductBase):
    nom: str
    cathegorie: str
    description: str


# this will be used to format the response to not to have id,owner_id etc
class ShowProduct(ProductBase):
    nom: str
    cathegorie: str
    description: Optional[str]

    class Config:  # to convert non dict obj to json
        orm_mode = True
