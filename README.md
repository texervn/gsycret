# gsycret
> Scripts for syncing files between personal computer and google drive

### Requirement
* Python3
* Pydrive
* Google Drive API key

### Steps
* Clone this project
    ```
    git clone https://github.com/noname0930/gdrive-scripts.git
    ```
* Move to the folder
    ```
    cd gdrive-scripts
    ```
* Apply and download Google Drive API key
* Rename the json file from Google to ```client_secrets.json```

### Usages
##### Basic  
* push
    ```
        python3 backup.py -m push -s /home/$USER -d <google_folder_id>
    ```
* pull
    ```
    python3 backup.py -m pull -s <google_folder_id> -d /home/$USER
    ```
* merge
    ```
    python3 backup.py -m merge -s <google_folder_id> -d <google_folder_id>
    ```

##### Advanced

| Arguments | Help | Others |
| ----- | ----- | ----- |
| -h, --help | show this help message and exit | |
| -m {push,pull,merge} | mode choices | |
| -s S | source folder | |
| -d D | destination folder | |
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
V1.3
