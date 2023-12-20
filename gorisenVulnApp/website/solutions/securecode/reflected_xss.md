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