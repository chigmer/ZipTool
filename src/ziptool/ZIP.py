from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from pathlib import Path
from datetime import datetime
import json
 
STATE_FILE = Path(".backup_state") / "state.json"

def load_index() -> int:
    
    if not STATE_FILE.exists():
        return 0

    try:
        data = json.loads(STATE_FILE.read_text())
        return int(data.get("i", 0))
    except Exception:
        # corrupted file fallback
        return 0
def save_index(i: int) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({"i": i}))




def index() -> int:
    i = load_index()
    i += 1
    save_index(i)
    return i
def is_excluded(path: Path, excluded: set[Path]) -> bool:    

    path = path.resolve()

    for ex in excluded:
        

        # exact match (file or folder explicitly excluded)
        if path == ex:
            return True

        # folder exclusion (path is inside excluded directory)
        try:
            path.relative_to(ex)
            return True
        except ValueError:
            pass

    return False
def backup_to_zip(sources: list[Path],to_exclude:list,dir_to_store:str,verbose:bool,compress_lvl:int,strict:bool) -> int:
    to_exclude = to_exclude or []
    p = Path(dir_to_store).resolve()
    now = datetime.now().strftime("%Y_%m_%d-%H%M")           
    p.mkdir(parents=True,exist_ok=True)
    i = index()
        
    user_exclusions = [s.resolve() for s in to_exclude]
    #returns current zip file number from index()
    
    EXCLUDED_PARTS = set(user_exclusions + [p])
    
    #output dir is automatically excluded to prevent recursion bugs
    for path in EXCLUDED_PARTS:        
        if strict and not path.exists():
            raise FileNotFoundError(path)
        elif not path.exists():
            print(f"WARNING: exclude not found: {path}")
   # "__pycache",".venv",".git"        
    
    
    
    #write the ZipFile
    with ZipFile(f"{p}/zip_backup_{i}_{now}.zip", "w") as zf:
        for source in sources:
            source = source.resolve()
            if not source.exists():
                if verbose:
                    print(f"path {source} is nonexistent.. skipping")
                continue
            if source.is_file():
                if is_excluded(source,EXCLUDED_PARTS):
                    if verbose:
                        print(f"EXCLUDING: {source.name}")
                    continue
                else:
                    zf.write(source,arcname=source.name, compress_type=ZIP_DEFLATED,compresslevel=compress_lvl)
                    if verbose:
                        print(f"zipped {source.name}")
            else:
                if is_excluded(source,EXCLUDED_PARTS):
                    if verbose:
                        print(f"EXCLUDING: {source.name}")
                    continue
                for f in source.rglob("*"):
                  
                    #not sure if f is abs
                    if is_excluded(f,EXCLUDED_PARTS):
                        if verbose:
                            print(f"EXCLUDING: {f.name}")                            
                        continue
                    else:
                        zf.write(f,arcname = f.relative_to(source),compress_type=ZIP_DEFLATED,compresslevel=compress_lvl)
                        if verbose:
                            print(f"zipped {f.name}")
    return i