import os
import stat
import pwd
import grp
import time

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

class FtpFile():
    '''
        /bin/ls fromat

        -rw-r--r-- 1 owner group           213 Aug 26 16:31 README

        1. - for a regular file or d for a directory;
        2. the literal string rw-r--r-- 1 owner group for a regular file, or rwxr-xr-x 1 owner group for a directory;
        3. the file size in decimal right-justified in a 13-byte field;
        4. a three-letter month name, first letter capitalized;
        5. a day number right-justified in a 3-byte field;
        6. a space and a 2-digit hour number;
        7. a colon and a 2-digit minute number;
            ** modification time in the server's local time zone **
        8. a space and the abbreviated pathname of the file.
    '''
    def __init__(self, filepath):
        self.filepath = filepath
        self.statinfo = os.stat(filepath)
        self.formatStr = ''
    def fileAuth(self):
        modes = [
            stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR, # user
            stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP, # group
            stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH, # others
        ]
        authStr=''
        if os.path.isdir(self.filepath):
            authStr +='d'
        else:
            authStr += '-'
        fmode = self.statinfo.st_mode
        Str = 'rwxrwxrwx'
        for i in range(9):
            if (modes[i] & fmode):
                authStr += Str[i]
            else:
                authStr += '-'
        return authStr
    def fileNumber(self):
        return str(self.statinfo.st_nlink)
    def fileUser(self):
        return pwd.getpwuid(self.statinfo.st_uid).pw_name
    def fileGroup(self):
        return grp.getgrgid(self.statinfo.st_gid).gr_name
    def fileSize(self):
        return str(self.statinfo.st_size)
    def fileModTime(self):
        return time.strftime('%b %d %H:%M', time.gmtime(self.statinfo.st_mtime))
    def fileName(self):
        return os.path.basename(self.filepath)
    def listFormat(self):
        fun = ['self.fileAuth()', 'self.fileNumber()', 'self.fileUser()', 'self.fileGroup()', 'self.fileSize()','self.fileModTime()', 'self.fileName()']
        formatlist = []
        for f in fun:
            formatlist.append(eval(f))
        self.formatStr = ' '.join(formatlist)
        return self.formatStr



def fileProperty(filepath):
    """
    return information from given file, like this "-rw-r--r-- 1 User Group 312 Aug 1 2014 filename"
    """
    st = os.stat(filepath)
    fileMessage = [ ]
    def _getFileMode( ):
        modes = [
            stat.S_IRUSR, stat.S_IWUSR, stat.S_IXUSR,
            stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
            stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH,
        ]
        mode     = st.st_mode
        fullmode = ''
        fullmode += os.path.isdir(filepath) and 'd' or '-'

        for i in range(9):
            fullmode += bool(mode & modes[i]) and 'rwxrwxrwx'[i] or '-'
        return fullmode

    def _getFilesNumber( ):
        return str(st.st_nlink)

    def _getUser( ):
        return pwd.getpwuid(st.st_uid).pw_name

    def _getGroup( ):
        return grp.getgrgid(st.st_gid).gr_name

    def _getSize( ):
        return str(st.st_size)

    def _getLastTime( ):
        return time.strftime('%b %d %H:%M', time.gmtime(st.st_mtime))
    for func in ('_getFileMode()', '_getFilesNumber()', '_getUser()', '_getGroup()', '_getSize()', '_getLastTime()'):
        fileMessage.append(eval(func))
    fileMessage.append(os.path.basename(filepath))
    return ' '.join(fileMessage)
