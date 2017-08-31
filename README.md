# gsycret
> script for google drive with encryption

### Requirement
* python3
* [pydrive](https://github.com/noname0930/PyDrive.git)

### Steps
* pydrive
    * clone and move to pydrive 
        ```
        git clone https://github.com/noname0930/PyDrive.git
        cd Pydrive
        ```
    * install pydrive
        ```
        python3 setup.py install
        ```
   
* gsycret
    * clone and move to gsycret
        ```
        git clone https://github.com/noname0930/gsycret.git
        cd gsycret
        ```
        
* Goto [Google API console](https://console.cloud.google.com/apis) and apply Google Drive key
* Move your api key to gsycret folder
* Rename the api key file from Google to ```client_secrets.json```

### Usages
##### Basic  
* push
    ```
    python3 gsycret.py push <local> <gdrive_folder_id>
    ```
* pull
    ```
    python3 gsycret.py pull <gdrive_folder_id> <local>
    ```
* merge
    ```
    python3 gsycret.py merge <src_folder_id> <dst_folder_id>
    ```

##### Advanced

| Arguments | Help | Others |
| ----- | ----- | ----- |
| -h, --help | show this help message and exit | |
| --password PASSWORD | password for {encrypt,decrypt} | Optional |
| --auto | auto {encrypt,decrypt} files by parent google_folder_id | Optional |
| --threads_num THREADS_NUM | number of threads | Optional, Default = 4 |

### Features
- [X] push
- [X] pull
- [X] merge
- [X] encryption
- [ ] match
    - [X] with file name
    - [ ] with hash
- [X] error message

### Version
V1.4
