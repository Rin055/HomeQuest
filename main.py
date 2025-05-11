from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

items = [
    {'title': 'Elegant Design',
     'description': 'Discover our elegant furniture selection, thoughtfully made to add warmth, timeless style, and a touch of sophistication to every corner of your home',
     'photo_url': 'https://img.pikbest.com/wp/202345/modern-living-room-decor-in-3d-with-black-sofa-and-plant-decorations-home-interior-render_9615670.jpg!w700wp'},
    {'title': 'Luxury Style',
     'description': 'Indulge in luxury with our top furniture pieces, crafted for both exceptional comfort and exquisite design to elevate your living space',
     'photo_url': 'https://c4.wallpaperflare.com/wallpaper/850/684/35/interior-design-style-design-home-wallpaper-preview.jpg'},
    {'title': 'Best Seller',
     'description': 'These popular items are cherished for their timeless beauty and excellent value, perfect for enhancing any home or space',
     'photo_url': 'https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'},
    {'title': 'Sales',
     'description': 'Take advantage of our current sales and enjoy fantastic discounts on the furniture pieces you’ve been eyeing for your home',
     'photo_url': 'https://images.pexels.com/photos/90319/pexels-photo-90319.jpeg?auto=compress&cs=tinysrgb&w=600'}
]

@app.route('/')
def index():
    return render_template('index.html', items=items)

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/aboutus')
def about_us():
    return render_template('about_us.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    conn = sqlite3.connect('HomeQuest.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        mail = request.form.get('mail')
        question_text = request.form.get('question')

        if not name or not mail or not question_text:
            return render_template('contact.html', error="All fields are required!")

        # Insert the question into the database only if it doesn't already exist
        c.execute('''INSERT INTO contacts (name, mail, question) VALUES (?, ?, ?)''', (name, mail, question_text))
        conn.commit()

        # Redirect to avoid re-submitting on page refresh
        return redirect(url_for('contact'))

    c.execute('SELECT * FROM contacts')
    rows = c.fetchall()
    conn.close()

    questions = [{'id': row[0], 'name': row[1], 'mail': row[2], 'question': row[3]} for row in rows]

    return render_template('contact.html', questions=questions)

@app.route('/admin')
def adminpage():
    return render_template('admin.html')

@app.route('/admin_contacts')
def admin_contacts():
    conn = sqlite3.connect('HomeQuest.db')
    c = conn.cursor()
    c.execute('SELECT * FROM contacts')
    rows = c.fetchall()
    conn.close()

    questions = [{'id': row[0], 'name': row[1], 'mail': row[2], 'question': row[3]} for row in rows]

    return render_template('admin_contacts.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
