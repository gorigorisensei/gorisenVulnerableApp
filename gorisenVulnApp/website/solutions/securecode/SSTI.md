
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