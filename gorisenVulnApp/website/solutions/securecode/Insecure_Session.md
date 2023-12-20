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
