from flask import Flask, render_template, request, session, redirect, url_for
from openai_integration import extract_details_from_response, get_openai_response
from file_writer import write_files
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

FILES_DIRECTORY = 'Project_files'  # Directory to store generated files

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
            project_name = request.form.get('project_name', 'MyProject')  # Get project name from form or use default
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
            session['conversation'].append({'user': description, 'system': None})  # Adding user input to conversation history
            response_text = get_openai_response(session['conversation'])
            functionality_description, code, components = extract_details_from_response(response_text)
            if functionality_description and code and components:
                session['conversation'][-1]['system'] = functionality_description  # Update system response in conversation history
                session['functionality_description'] = functionality_description
                session['code'] = code
                session['components'] = components

    return render_template('main.html', session=session)

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('conversation', None)
    # Reset the project files directory
    if os.path.exists(FILES_DIRECTORY):
        import shutil
        shutil.rmtree(FILES_DIRECTORY)
    os.makedirs(FILES_DIRECTORY)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
