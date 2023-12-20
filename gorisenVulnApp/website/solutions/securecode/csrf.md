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