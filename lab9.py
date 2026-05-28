from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)#主键
    author = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(200), nullable=False)#不能为空
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Book {self.name} by {self.author}>'

@app.route('/', methods=['GET', 'POST']) #读取，提交修改
def index():
    if request.method == 'POST':
        book_author = request.form.get('author', '').strip()
        book_name = request.form.get('name', '').strip()

        if not book_author or not book_name:
            return "Поля не должны быть пустыми"
        
        new_book = Book(author=book_author, name=book_name)
        
        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка при добавлении'
    else:
        books = Book.query.order_by(Book.date_added).all()
        return render_template('index.html', books=books)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        return redirect('/')
    except:
        return 'Ошибка при удалении'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)