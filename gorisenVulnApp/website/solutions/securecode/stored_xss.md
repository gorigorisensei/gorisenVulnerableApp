### vuln code
### views.py
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


### home.html

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



### Secure code:
#### views.py


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



#### home.html

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