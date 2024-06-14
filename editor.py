from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

editor_blueprint = Blueprint('editor', __name__)

@editor_blueprint.route('/code', methods=['GET', 'POST'])
@login_required
def code_screen():
    if request.method == 'POST':
        code = request.form['code']
        return redirect(url_for('editor.output_screen', code=code))
    return render_template('code_screen.html')

@editor_blueprint.route('/output')
@login_required
def output_screen():
    code = request.args.get('code')
    try:
        output = exec(code)
    except Exception as e:
        output = str(e)
    return render_template('output_screen.html', code=code, output=output)
