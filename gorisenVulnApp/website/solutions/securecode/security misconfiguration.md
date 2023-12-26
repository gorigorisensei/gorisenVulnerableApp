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



