from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library-collection.db"
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)


class BookForm(FlaskForm):
    book_name = StringField(label='Book Name', validators=[DataRequired()])
    author = StringField(label='Book Author', validators=[DataRequired()])
    rating = FloatField(label='Rating', validators=[DataRequired()])


@app.route('/')
def home():
    library_empty = True
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        all_books = result.scalars()
        library = []
        if len(library) == 0:
            for book in all_books:
                library.append(book)
        if len(library) == 0:
            library_empty = False


    return render_template(
        'index.html',
        library=library,
        library_populated=library_empty
    )


@app.route('/add', methods=['POST', 'GET'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        with app.app_context():
            db.create_all()
            new_book = Book(
                title = form.book_name.data,
                author = form.author.data,
                rating = form.rating.data
            )
            print(new_book.id)
            db.session.add(new_book)
            db.session.commit()
            print(new_book.id)

        return redirect(url_for('home'))


    return render_template(
        'add.html',
        form=form
    )


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == "POST":
        book_id = request.form['id']
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()

        return redirect(url_for('home'))

    book_id = request.args.get('book_id')
    book = db.get_or_404(Book, book_id)

    return render_template(
        'edit.html',
        book=book
    )

@app.route('/delete')
def delete():

    book_id = request.args.get('book_id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

