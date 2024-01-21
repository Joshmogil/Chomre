import sqlite3
from cst import Root, load_cst_from_file, Function, DataStructure, Interface, ChomSyntaxTree
from dataclasses import dataclass

class Chomkey():
    """the chomkey is in charge of monkeying the chom syntax tree into a structured folder of files and folders, 
    as well as keeping track of previously written code and the
    current state of the program to provide context for the code completion engine
    """

    def __init__(self, cst:Root):
        self.cst = cst
        self.mem_db = set_up_in_memory_database()

@dataclass
class file():
    """a file in the chomkey"""
    file_location: str
    name: str
    node_type: str
    description: str
    code: str

def walk_cst(cst:Root):
    """walk the cst and map out nodes to files and folders"""
    node_map: dict[str, file] = {}
    

    
        

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


def print_model_location(model, location=""):
    if isinstance(model, Interface):
        print(f"Interface location: {location}")
        for name, function in model.functions.items():
            print_model_location(function, f"{location}.{name}")
        if model.data_structures:
            for name, data_structure in model.data_structures.items():
                print_model_location(data_structure, f"{location}.{name}")
        if model.interfaces:
            for name, interface in model.interfaces.items():
                print_model_location(interface, f"{location}.{name}")
    elif isinstance(model, Function):
        print(f"Function location: {location}")
    elif isinstance(model, DataStructure):
        print(f"DataStructure location: {location}")
    elif isinstance(model, Root):
        print_model_location(model.root, "root")
    elif isinstance(model, ChomSyntaxTree):
        if model.data_structures:
            for name, data_structure in model.data_structures.items():
                print_model_location(data_structure, f"{location}.{name}")
        for name, interface in model.interfaces.items():
            print_model_location(interface, f"{location}.{name}")


if __name__ == "__main__":
    cst: Root = load_cst_from_file("../../cst_examples/chom.example2.json")
    print(cst)
    print_model_location(cst)
    chonkey_monkey = Chomkey(cst)