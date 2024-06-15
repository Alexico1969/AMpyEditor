from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import io
import contextlib

editor_blueprint = Blueprint('editor', __name__)

@editor_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def editor():
    code = ""
    output = None
    if request.method == 'POST':
        code = request.form['code']
        try:
            # Capture the output of the code
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                exec(code)
                output = buf.getvalue()
        except Exception as e:
            output = str(e)

    return render_template('editor.html', code=code, output=output)
