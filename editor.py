from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import io
import contextlib

editor_blueprint = Blueprint('editor', __name__)
execution_context = {}

@editor_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def editor():
    code = ""
    output = None
    if request.method == 'POST':
        code = request.form['code']
        execution_context['code'] = code
        execution_context['output'] = ""
        execution_context['input_needed'] = False
        execution_context['exec_globals'] = {
            'input': get_input,
            '__name__': '__main__'
        }
        try:
            execute_code(code)
            output = execution_context['output']
        except Exception as e:
            output = str(e)

    return render_template('editor.html', code=code, output=output)

@editor_blueprint.route('/input', methods=['POST'])
@login_required
def user_input():
    user_input = request.form['user_input']
    execution_context['input_value'] = user_input
    execution_context['input_needed'] = False
    try:
        execute_code(execution_context['remaining_code'])
        output = execution_context['output']
    except Exception as e:
        output = str(e)
    return jsonify({'output': output})

def get_input(prompt=''):
    execution_context['output'] += prompt
    execution_context['input_needed'] = True
    raise InputNeededException()

def execute_code(code):
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
        try:
            exec(code, execution_context['exec_globals'])
        except InputNeededException:
            execution_context['remaining_code'] = code.splitlines()[1:]
            execution_context['output'] += buf.getvalue()
            raise
        execution_context['output'] += buf.getvalue()

class InputNeededException(Exception):
    pass
