# MiniFTP
Project for IS301 Computer Communication and Network -- Ftp server and client in python 

⛑ still under construction

🚩 estimated time of completion: 12.15 

Use FTP commands standardized in [RFC 959](https://tools.ietf.org/html/rfc95) by the IETF. 

MiniFTP server is designed be connected with any common ftp tool.


## How does FILE TRANSFER PROTOCOL (FTP) work

                                            -------------
                                            |/---------\|
                                            ||   User  ||    --------
                                            ||Interface|<--->| User |
                                            |\----^----/|    --------
                  ----------                |     |     |
                  |/------\|  FTP Commands  |/----V----\|
                  ||Server|<---------------->|   User  ||
                  ||  PI  ||   FTP Replies  ||    PI   ||
                  |\--^---/|                |\----^----/|
                  |   |    |                |     |     |
      --------    |/--V---\|      Data      |/----V----\|    --------
      | File |<--->|Server|<---------------->|  User   |<--->| File |
      |System|    || DTP  ||   Connection   ||   DTP   ||    |System|
      --------    |\------/|                |\---------/|    --------
                  ----------                -------------

                  Server-FTP                   USER-FTP

      NOTES: 1. The data connection may be used in either direction.
             2. The data connection need not exist all of the time.

                      Figure 1  Model for FTP Use


# My progress
## DONE
- Listen on a given port (default 21)
- Connect to ftp client
- User login
- PASV: Passive mode
- PWD: Print working directory. Returns the current directory of the host.
- CWD: Change working directory.
- DELE: Delete file.
- LIST: Returns information of a file or directory if specified, else information of the current working directory is returned.
- STOR: Accept the data and to store the data as a file at the server site

## TODO
- RETR 下载文件
- POST 主动模式
- Authority control for different users



