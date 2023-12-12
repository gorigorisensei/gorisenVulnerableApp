Vulnerable Code:

```
Vulnerable code:
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


```
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