
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