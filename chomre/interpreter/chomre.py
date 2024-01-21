from pydantic import BaseModel
from typing import List, Optional

class Field(BaseModel):
    name: str
    type: str
    description: str

class DataStructure(BaseModel):
    description: str
    fields: List[Field]

class Parameter(BaseModel):
    name: str
    type: str
    description: str

class Function(BaseModel):
    description: str
    parameters: List[Parameter]
    returns: Optional[Field]

class Interface(BaseModel):
    name: str
    type: str
    description: str
    functions: dict[str, Function]
    data_structures: dict[str, DataStructure]

class Chom(BaseModel):
    purpose: str
    data_structures: dict[str, DataStructure]
    interfaces: dict[str, Interface]

class Root(BaseModel):
    """Root of the Chomre AST + interpreter."""
    chom: Chom