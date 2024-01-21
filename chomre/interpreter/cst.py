from pydantic import BaseModel
from typing import List, Optional
import json

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
    parameters: Optional[List[Parameter]] = None
    returns: Optional[Field] = None

class Interface(BaseModel):
    name: str
    description: str
    functions: dict[str, Function]
    data_structures: Optional[dict[str, DataStructure]] = None
    interfaces: Optional[dict[str, "Interface"]] = None

class ChomSyntaxTree(BaseModel):
    purpose: str
    data_structures: Optional[dict[str, DataStructure]] = None
    interfaces: dict[str, Interface]

class Root(BaseModel):
    root: ChomSyntaxTree
 
def load_cst_from_file(file:str):
    with open(file) as f:
        data = json.dumps(json.load(f))
    return Root.model_validate_json(data)

class ChomArchitecturalStructure():


    def __init__(self, cst:Root):
        self.cst = cst

    
    
    


if __name__ == "__main__":
    print (json.dumps(Root.model_json_schema(), indent=2))

    with open("../../cst_examples/chom.example2.json") as f:
        data = json.dumps(json.load(f))

    cst2 = Root.model_validate_json(data)

    #print(cst2)