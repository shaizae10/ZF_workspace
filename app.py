import os
import webbrowser

from flask import Flask, render_template, request, session, redirect, url_for

from Utils.file_utils import write_files, json_reader
from Utils.openai_integration import OpenAiApi

# Adjust the path to your needs, considering the execution context
FILES_DIRECTORY = 'order_files'

# Ensure FILES_DIRECTORY exists
if not os.path.exists(FILES_DIRECTORY):
    os.makedirs(FILES_DIRECTORY)
    
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


config = json_reader(os.path.join(os.path.dirname(__file__), "Utils", "metadata.json"))

# Instantiate your assistant here
assistant = OpenAiApi(config)


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'conversation' not in session:
        session['conversation'] = []

    if request.method == 'POST':
        if 'reset' in request.form:
            session.pop('conversation', None)
            # Reset the project files directory
            if os.path.exists(FILES_DIRECTORY):
                import shutil
                shutil.rmtree(FILES_DIRECTORY)
            os.makedirs(FILES_DIRECTORY)
            return redirect(url_for('index'))

        elif 'approve' in request.form:
            project_name = request.form.get('project_name', 'MyProject')
            if 'code' in session and 'components' in session:
                files = {
                    f'{project_name}_code.py': session['code'],
                    f'{project_name}_components.txt': '\n'.join(session['components'])
                }
                write_files(FILES_DIRECTORY, files)
                session['message'] = 'Approval successful. Files have been saved.'
                return redirect(url_for('index'))
            else:
                session['message'] = 'No data to approve.'
                return redirect(url_for('index'))

        elif 'description' in request.form:
            description = request.form['description']
            session['conversation'].append({'user': description, 'system': None})

            # Use the assistant instance
            response_text = assistant.get_openai_response(description)
            functionality_description, code, components = assistant.extract_details_from_response(response_text)
            if functionality_description and code and components:
                session['conversation'][-1]['system'] = functionality_description
                session['functionality_description'] = functionality_description
                session['code'] = code
                session['components'] = components

    return render_template('main.html', session=session)


@app.route('/approve', methods=['GET', 'POST'])
def approve():
    if request.method == 'POST':
        if 'submit' in request.form:
            code_filename = "generated_skidl_code.py"
            components_filename = "components_list.txt"
            with open(code_filename, 'w') as code_file:
                code_file.write(session['code'])
            with open(components_filename, 'w') as components_file:
                components_file.write('\n'.join(session['components']))


    return render_template('main.html')  # Adjust if you have a specific template for approval



@app.route('/reset', methods=['POST'])
def reset():
    session.pop('conversation', None)
    # Reset the project files directory
    if os.path.exists(FILES_DIRECTORY):
        import shutil
        shutil.rmtree(FILES_DIRECTORY)
    os.makedirs(FILES_DIRECTORY)
    return redirect(url_for('index'))


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == '__main__':

    open_browser()
    app.run(debug=False, port=5000)

