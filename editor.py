from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

editor_blueprint = Blueprint('editor', __name__)

@editor_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def editor():
    code = ""
    output = None
    if request.method == 'POST':
        code = request.form['code']
        try:
            # Execute the code safely
            exec_globals = {}
            exec_locals = {}
            exec(code, exec_globals, exec_locals)
            output = exec_locals.get('result', 'Code executed successfully.')
        except Exception as e:
            output = str(e)

    return render_template('editor.html', code=code, output=output)
