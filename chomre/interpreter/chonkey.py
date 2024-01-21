import sqlite3
from cst import Root, load_cst_from_file, Function, DataStructure, Interface, ChomSyntaxTree
from dataclasses import dataclass
from pydantic import BaseModel


class Chomkey():
    """the chomkey is in charge of monkeying the chom syntax tree into a structured folder of files and folders, 
    as well as keeping track of previously written code and the
    current state of the program to provide context for the code completion engine
    """

    def __init__(self, cst:Root):
        self.cst = cst
        self.mem_db = set_up_in_memory_database()

@dataclass
class TreeNode():
    """a file in the chomkey"""
    node_location: str
    name: str
    node_type: str
    description: str
    node_model: BaseModel
    code: str

def walk_cst(cst:Root):
    """walk the cst and map out nodes to files and folders"""
    node_map: dict[str, TreeNode] = {}
    
    


    
        

def set_up_in_memory_database()-> sqlite3.Connection:
    # create the tables
    mem_db = sqlite3.connect(":memory:")
    mem_db.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            file_location TEXT NOT NULL,
            node_type TEXT NOT NULL,
            description TEXT NOT NULL,
            code TEXT NOT NULL
        );
    """)

    mem_db.execute("""
    CREATE TRIGGER file_location_trigger
    BEFORE INSERT ON files
    FOR EACH ROW
    BEGIN
        SELECT CASE
            WHEN NEW.file_location NOT LIKE '/root/%' THEN
            RAISE (ABORT, 'file_location must start with /root/')
        END;
    END;
    """)

    mem_db.execute("""
    CREATE TRIGGER node_type_trigger
    BEFORE INSERT ON files
    FOR EACH ROW
    BEGIN
        SELECT CASE
            WHEN NEW.node_type NOT IN ('interface', 'function', 'data_structure') THEN
            RAISE (ABORT, 'node_type must be either interface, function, or data_structure')
        END;
    END;
    """)

    return mem_db

def generate_node_map(cst:Root) -> dict[str, TreeNode]:
    node_map:dict[str, TreeNode] = {}

    def recursive_add_node_to_tree(model, location=""):
        if isinstance(model, Interface):
            print(f"Interface location: {location}")
            node_map[f"{location}.{model.name}"] = TreeNode(
                node_location=f"{location}.{model.name}",
                name=model.name,
                node_type="interface",
                description=model.description, 
                node_model=model,
                code=""
                )
            #print(node_map)
            for name, function in model.functions.items():
                recursive_add_node_to_tree(function, f"{location}.{name}")
            if model.data_structures:
                for name, data_structure in model.data_structures.items():
                    recursive_add_node_to_tree(data_structure, f"{location}.{name}")
            if model.interfaces:
                for name, interface in model.interfaces.items():
                    recursive_add_node_to_tree(interface, f"{location}.{name}")


        elif isinstance(model, Function):
            print(f"Function location: {location}")
            node_map[f"{location}.{model.name}"] = TreeNode(
                node_location=f"{location}.{model.name}",
                name=model.name,
                node_type="function",
                description=model.description, 
                node_model=model,
                code=""
                )
        elif isinstance(model, DataStructure):
            print(f"DataStructure location: {location}")
            node_map[f"{location}.{model.name}"] = TreeNode(
                node_location=f"{location}.{model.name}",
                name=model.name,
                node_type="data_structure",
                description=model.description, 
                node_model=model,
                code=""
                )
        elif isinstance(model, Root):
            recursive_add_node_to_tree(model.root, "root")
        elif isinstance(model, ChomSyntaxTree):
            if model.data_structures:
                for name, data_structure in model.data_structures.items():
                    recursive_add_node_to_tree(data_structure, f"{location}.{name}")
            for name, interface in model.interfaces.items():
                recursive_add_node_to_tree(interface, f"{location}.{name}")

    recursive_add_node_to_tree(cst)

    return node_map


if __name__ == "__main__":
    cst: Root = load_cst_from_file("../../cst_examples/chom.example2.json")
    print(cst)
    node_map=generate_node_map(cst)

    print(node_map.keys())
    chonkey_monkey = Chomkey(cst)