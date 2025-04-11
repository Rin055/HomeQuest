from flask import Flask, render_template

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
    return render_template('Shop.html')

@app.route('/aboutus')
def about_us():
    return render_template('about_us.html')

@app.route('/admin')
def adminpage():
    return render_template('Admin.html')

if __name__ == '__main__':
    app.run(debug=True)
