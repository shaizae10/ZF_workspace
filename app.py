from flask import Flask, render_template, request, session, redirect, url_for

from openai_integration import extract_details_from_response, get_openai_response

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'conversation' not in session:
        session['conversation'] = []

    if request.method == 'POST':
        if 'reset' in request.form:
            session['conversation'] = []
            return redirect(url_for('index'))

        description = request.form.get('description')
        session['conversation'].append(
            {'user': description, 'system': None})  # Adding user input to conversation history
        response_text = get_openai_response(session['conversation'])
        functionality_description, code, components = extract_details_from_response(response_text)
        if functionality_description and code and components:
            session['conversation'][-1][
                'system'] = functionality_description  # Update system response in conversation history
            session['functionality_description'] = functionality_description
            session['code'] = code
            session['components'] = components

    return render_template('index.html', session=session)


@app.route('/approve', methods=['GET', 'POST'])
def approve():
    if request.method == 'POST':
        if 'submit' in request.form:
            code_filename = "generated_skidl_code.py"
            components_filename = "components_list.txt"
            with open(code_filename, 'w') as code_file:
                code_file.write(session['code'])
            with open(components_filename, 'w') as components_file:
                components_file.write(session['components'])
            return render_template('success.html')

    return render_template('approve.html')


@app.route('/reset', methods=['POST'])
def reset():
    session['conversation'] = []
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
