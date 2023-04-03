from flask import render_template, url_for, flash, redirect
from library import app, db
from library.forms import RegistrationForm, IssuanceForm
from library.models import Books, Member
import requests, json


@app.route("/")
@app.route("/books", methods=['GET'])
def home():
    books = Books.query.all()
    data = json.loads(requests.get('https://frappe.io/api/method/frappe-library').content)['message']
    for temp in data:
        book = Books(id= temp['bookID'], title=temp['title'], authors=temp['authors'], average_rating=temp['average_rating'])
        if not Books.query.filter_by(id=book.id).first():
            db.session.add(book)
            db.session.commit()
    return render_template('books.html', books=books)

@app.route("/members", methods=['GET'])
def members():
    members = Member.query.all()
    return render_template('members.html', title='Members', members=members)

@app.route("/members/register", methods=['GET', 'POST'])
def register_member():
    form = RegistrationForm()
    if form.validate_on_submit():
        member = Member(username=form.name.data, email=form.email.data, mobile_number=form.number.data)
        db.session.add(member)
        db.session.commit()
        flash(f'{form.name.data} registered successfully!', 'success')
    return render_template('register.html', title='Register', form=form)


@app.route("/books/<bookID>", methods=['GET'])
def book(bookID):
    book = Books.query.filter_by(id=bookID).first()
    if book.member_id:
        member = book.member
        return render_template('book.html', title=book.title, book=book, member=member)
    return render_template('book.html', title=book.title, book=book)

@app.route("/books/<bookID>/issue", methods=['GET', 'POST'])
def issue_book(bookID):
    book = Books.query.filter_by(id=bookID).first()
    form = IssuanceForm()
    if form.validate_on_submit():
        member = Member.query.filter_by(email=form.email.data).first()
        if member.dues < 500:
            book.member_id = member.id
            member.dues += 100
            db.session.commit()
            flash('Book issued successfully!', 'success')
            return redirect(url_for('book', bookID=book.id))
        else:
            flash('Member needs to clear previous dues before issuing a new book!', 'danger')
    return render_template('issue.html', title=book.title, form=form, book=book)