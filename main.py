from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route('/')
def index():
    items = []
    conn = sqlite3.connect('HomeQuest.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 8")
    rows = c.fetchall()

    for row in rows:
        items.append({
            'id': row['id'],
            'title': row['title'],
            'description': row['description'],
            'publisher': row['publisher'],
            'short_description': row['short_description'],
            'photo_url': row['photo_url'],
            'price': row['price']
        })

    return render_template('index.html', items=items)


@app.route('/add_question', methods=['POST'])
def add_question():
    name = request.form.get('name')
    mail = request.form.get('mail')
    question = request.form.get('question')

    conn = sqlite3.connect('HomeQuest.db')
    conn.execute('''
                 INSERT INTO contacts (name, email, question)
                 VALUES (?, ?, ?)
                 ''', (name, mail, question))
    conn.commit()
    conn.close()

    return redirect(url_for('contact'))

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/contact')
def contact():
    conn = sqlite3.connect('HomeQuest.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    rows = c.fetchall()
    conn.close()
    questions = []
    for row in rows:
        questions.append({'id': row[0], 'name': row[1], 'email': row[2], 'question': row[3]})
    return render_template('contact.html', questions=questions)

@app.route('/posts')
def posts():
    main_posts = []
    conn = sqlite3.connect('HomeQuest.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    search = request.args.get('search-value')
    if search:
        c.execute("SELECT * FROM posts WHERE title LIKE ?", ('%' + search + '%',))
    else:
        c.execute("SELECT * FROM posts")
    rows = c.fetchall()
    for row in rows:
        main_posts.append(
            {'id': row['id'], 'title': row['title'], 'description': row['description'], 'publisher': row['publisher'], 'short_description': row['short_description'], 'photo_url': row['photo_url'], 'price': row['price']}
        )
    return render_template('posts.html', posts = main_posts)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        conn = sqlite3.connect('HomeQuest.db')
        c = conn.cursor()
        c.execute("SELECT email, username FROM users WHERE email = ?", (user_email,))
        rows = c.fetchall()
        if rows:
            user_name = rows[0][1]
            session.permanent = True
            session['user'] = user_email
            session['user_name'] = user_name
            return redirect(url_for('admin'))
        conn.close()
    return render_template('sign_in.html')

@app.route('/logout')
def logout():
    del session['user']
    del session['user_name']
    return redirect(url_for('sign_in'))

@app.route('/admin')
def admin():
    if 'user' in session:
        return render_template('admin.html', user=session['user_name'])
    else:
        return redirect(url_for('sign_in'))


@app.route('/admin/admin_contacts')
def admin_contacts():
    conn = sqlite3.connect('HomeQuest.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    rows = c.fetchall()
    conn.close()

    questions = []
    for row in rows:
        questions.append({'id': row[0], 'name': row[1], 'email': row[2], 'question': row[3]})

    return render_template('admin_contacts.html', questions=questions)


@app.route('/admin/create_items', methods=['GET', 'POST'])
def create_items():
    conn = sqlite3.connect('HomeQuest.db')
    c = conn.cursor()
    c.execute("PRAGMA table_info(posts)")
    columns = [info[1] for info in c.fetchall()]
    if 'short_description' not in columns:
        c.execute("ALTER TABLE posts ADD COLUMN short_description TEXT")
        conn.commit()
    if 'photo_url' not in columns:
        c.execute("ALTER TABLE posts ADD COLUMN photo_url TEXT")
        conn.commit()
    # Add this block to ensure price column exists
    if 'price' not in columns:
        c.execute("ALTER TABLE posts ADD COLUMN price TEXT")
        conn.commit()
    if request.method == 'POST':
        title = request.form.get('title')
        short_description = request.form.get('short_description')
        description = request.form.get('description')
        publisher = request.form.get('publisher')
        photo_url = request.form.get('photo_url')
        price = request.form.get('price')

        conn.execute('''
                     INSERT INTO posts (title, short_description, description, publisher, photo_url, price)
                     VALUES (?, ?, ?, ?, ?, ?)
                     ''', (title, short_description, description, publisher, photo_url, price))
        conn.commit()

    posts = []
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM posts")
    rows = c.fetchall()
    conn.close()
    for row in rows:
        posts.append({
            'id': row['id'],
            'title': row['title'],
            'description': row['description'],
            'publisher': row['publisher'],
            'short_description': row['short_description'],
            'photo_url': row['photo_url'],
            'price': row['price']
        })
    return render_template('create_items.html', posts=posts)

@app.route('/admin/delete_item/<int:id>')
def delete_item(id):
    conn = sqlite3.connect('HomeQuest.db')
    conn.execute('''
        DELETE FROM posts WHERE id = ?
    ''', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('create_items'))

@app.route('/admin/update_item/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    posts = []
    conn = sqlite3.connect('HomeQuest.db')
    conn.row_factory = sqlite3.Row

    if request.method == 'GET':
        c = conn.cursor()
        c.execute(''' SELECT * FROM posts WHERE id = ? ''', (id,))
        rows = c.fetchall()
        conn.close()
        for row in rows:
            posts.append(
                {'id': row['id'], 'title': row['title'], 'description': row['description'], 'publisher': row['publisher'], 'short_description': row['short_description'], 'photo_url': row['photo_url'], 'price': row['price']}
            )
        return render_template('update_item.html', post = posts[0])
    else:
        title = request.form.get('title')
        short_description = request.form.get('short_description')
        description = request.form.get('description')
        publisher = request.form.get('publisher')
        photo_url = request.form.get('photo_url')
        price = request.form.get('price')

        conn.execute(''' UPDATE posts SET title = ?, short_description = ?, description = ?, publisher = ?, photo_url = ?, price = ? WHERE id = ? ''',
                     (title, short_description, description, publisher, photo_url, price, id))
        conn.commit()
        conn.close()
        return redirect(url_for('create_items'))

@app.route('/posts/<int:id>')
def show_post(id):
    post = []
    conn = sqlite3.connect('HomeQuest.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(''' SELECT * FROM posts WHERE id = ? ''', (id,))
    rows = c.fetchall()
    for row in rows:
        post.append(
            {'id': row['id'], 'title': row['title'], 'description': row['description'], 'publisher': row['publisher'], 'short_description': row['short_description'], 'photo_url': row['photo_url'], 'price': row['price']}
        )
    return render_template('show_post.html', post = post[0])

@app.route('/admin/delete_question/<int:id>')
def delete_question(id):
    conn = sqlite3.connect('HomeQuest.db')
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_contacts'))

@app.route('/admins')
def admins():
    return render_template('admins.html')

if __name__ == '__main__':
    app.run(debug=True)
