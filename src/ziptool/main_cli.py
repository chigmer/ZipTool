#main script
import argparse
from ziptool.ZIP import backup_to_zip
from pathlib import Path
def parse_args() -> tuple:
    cl_choices = list(range(1,10))
    parser = argparse.ArgumentParser(
        description="Creates versioned ZIP backups of files and folders."
    )  
    parser.add_argument("source",type=Path,nargs='+',help="files or directories to zip, use quotes if file contains whitespace")
    parser.add_argument("-X","--exclude",type=Path,nargs='+',help="files or directories to exclude from the zipping process")
    parser.add_argument("-v","--verbose",action="store_true",help="show script processes")
    parser.add_argument("-o","--output",type=str,default="MyZipFiles",help="The name of the output directory, fallbacks to default if unspecified")
    parser.add_argument("-cl","--compresslevel",type=int,default=6,choices=cl_choices,help="specify compress level")
    parser.add_argument("--strict-excludes",action="store_true",help="Treat invalid exclude paths as errors instead of warnings")
    
    
    args = parser.parse_args()   
    exclude = args.exclude
    source = args.source
    verbose = args.verbose
    output = args.output
    compress_lvl = args.compresslevel
    strict = args.strict_excludes
    return exclude,source,output,verbose,compress_lvl,strict
    
          
    
    
             
def main() -> None:   
    exclude,source,output,verbose,compress_lvl,strict = parse_args()
    try:
        i = backup_to_zip(source,exclude,output,verbose,compress_lvl,strict)
    except Exception as e:
        print(f"Couldn't back up your files: {e}")
        return None
    print(f"Backup version {i} completed.")
