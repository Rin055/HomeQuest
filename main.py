from flask import Flask, render_template, request

app = Flask(__name__)

questions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/aboutus')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html', questions=questions)

@app.route('/add_question', methods=['POST'])
def add_question():
    name = request.form.get('name')
    mail = request.form.get('mail')
    question_text = request.form.get('question')

    if not name or not mail or not question_text:
        return render_template('contact.html', questions=questions, error="All fields are required!")

    questions.append({'name': name, 'mail': mail, 'question': question_text})
    return render_template('contact.html', questions=questions)

@app.route('/delete_question/<int:index>', methods=['GET'])
def delete_question(index):
    if 0 <= index < len(questions):
        questions.pop(index)
    return render_template('contact.html', questions=questions)

@app.route('/admin')
def adminpage():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
