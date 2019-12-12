import os

def removeDir(dirPath):
    if not os.path.isdir(dirPath): 
        os.remove(dirPath);         #直接删除文件
    else:
        files = os.listdir(dirPath);   
        for file in files:
            filePath = os.path.join(dirPath, file);  
            if os.path.isfile(filePath):
                os.remove(filePath); 
            elif os.path.isdir(filePath): 
                removeDir(filePath);
        os.rmdir(dirPath); 