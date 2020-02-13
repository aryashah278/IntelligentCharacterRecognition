import os
import shutil
def main():
    print("Cleaner started")
    for dir, sub, files in os.walk(os.getcwd()):
        
        if any([dir.split("/").__contains__("Alphabet"),
                dir.split("/").__contains__("Cropped"),
                dir.split("/").__contains__("DST"),
                dir.split("/").__contains__("ForGUI"),
                dir.split("/").__contains__("Foto")]):
            
            for file in files:
                
                os.remove(os.path.join(dir, file))
        if os.path.exists("results.npy"):
            os.remove("./results.npy")
        if dir.split("/").__contains__("FromPhone"):
            for file in files:
                shutil.move(os.path.join(dir, file),os.path.join("Past", file))


if __name__ == "__main__":
    main()
