# gdrive-scripts
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
* Get Google Drive API key
    > Please reference the following links

    * [ITO の 學習筆記](http://vito-note.blogspot.tw/2015/04/google-oauth-20.html)
* Rename the json file from Google to ```client_secrets.json```

### Usages
```
python3 backup.py [-h] [-m {push,pull,merge}] [-s S] [-d D] [-p P] [-a] [-t T]
```

| Arguments | Help | Others |
| ----- | ----- | ----- |
| -h, --help | show this help message and exit | |
| -m {push,pull,merge} | mode choices | |
| -s S | source folder | |
| -d D | destination folder | |
| -p P | password | Optional |
| -a | auto encrypt | Optional |
| -t T | number of threads | Optional, Default = 4 |

### Features
- [X] push
- [X] pull
- [X] merge
- [X] encryption
- [ ] match
    - [X] with file name
    - [ ] with hash
- [X] error message
- [ ] log file

### Version
V1.3
