# MiniFTP
Project for IS301 Computer Communication and Network -- Ftp server and client

Use FTP commands standardized in [RFC 959](https://tools.ietf.org/html/rfc95) by the IETF. [This document](http://www.nsftools.com/tips/RawFTP.htm) provides a detailed introduction for FTP commands.


## How Does FILE TRANSFER PROTOCOL (FTP) Work

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

## Usage
Developed on MacOS.

```bash
$ sudo python ftp_server.py (--port PORT --dir LOCALDIR)
```

## DONE
- Listen on a given port (default 21)
- Connect to ftp client
- User login
- PASV: Passive mode
- POST: Active mode
- PWD: Print working directory. Returns the current directory of the host.
- CWD: Change working directory.
- DELE: Delete file.
- RMD: remove a remote directory
- LIST: Returns information of a file or directory if specified, else information of the current working directory is returned.
- STOR: Accept the data and to store the data as a file at the server site
- RETR: Retrieve a remote file
- NLST: name list of remote directory
- RNFR
- RNTO
- Authority control for different users

## TODO
- debug: A/I type
On MacOS, it can only use binary(I) to upload and ascii(A) to download. Also, the file cannot contain any Chinese characters.



