## vuln code:
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