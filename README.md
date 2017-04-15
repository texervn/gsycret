# gdrive-backup
> clone file from account to another account

### Requirement
* Python3
* Pydrive
* Google Drive API key

### Steps
* Clone this project
    ```
    git clone https://github.com/noname0930/gdrive-backup.git
    cd gdrive-backup
    ```
    
* Get Google Drive API key
    > Please reference the following links
    
    * [ITO の 學習筆記](http://vito-note.blogspot.tw/2015/04/google-oauth-20.html)
* Rename the json file from Google to ```client_secrets.json```
* Run script
    ```
    python3 backup.py <source_folder_id> <destination_folder_id>
    ```

### Features
- [X] Downlink
- [X] Uplink
- [ ] Encryption
- [ ] Match (by hash)
- [ ] Error message
- [ ] Log file

### Version
V1.0
