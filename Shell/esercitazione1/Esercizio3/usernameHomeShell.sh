cat /etc/passwd | grep -e "/bin/bash$" | cut -d ":" -f1,6 > usernameHomeShell.txt 
