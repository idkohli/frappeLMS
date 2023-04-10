from flask import render_template, url_for, flash, redirect
from library import app, db
from library.forms import RegistrationForm, IssuanceForm, SearchForm
from library.models import Books, Member
import requests, json


@app.route("/", methods=['GET'])
def home():
    books = Books.query.all()
    return render_template('books.html', books=books)

@app.route("/import", methods=['GET', 'POST'])
def books():
    form = SearchForm()
    data = []
    if form.validate_on_submit():
        title = form.title.data
        quantity = form.quantity.data
        data = json.loads(requests.get(url = f'https://frappe.io/api/method/frappe-library?title={title}').content)['message']
        page = 1
        add = 1 
        while len(data) < quantity and add:
            page += 1
            url = f'https://frappe.io/api/method/frappe-library?title={title}&page={page}'
            add = json.loads(requests.get(url).content)['message']
            data.extend(add)
        del data[quantity:]

        if len(data) < quantity:
            flash(f'Only {len(data)} books available in that title.', 'warning')
        else:
            flash(f'{quantity} books imported successfully!', 'success')

        for temp in data:
            book = Books(id= temp['bookID'], title=temp['title'], authors=temp['authors'], average_rating=temp['average_rating'])
            if not Books.query.filter_by(id=book.id).first():
                db.session.add(book)
                db.session.commit()
    return render_template('import.html', title='Import', books=data, form=form)

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

@app.route("/books/<bookID>/return", methods=['GET', 'POST'])
def return_book(bookID):
    book = Books.query.filter_by(id=bookID).first()
    member = book.member
    member.dues -= 100
    book.member_id = None
    db.session.commit()
    flash('Book returned successfully!', 'success')
    return render_template('book.html', title=book.title, book=book)

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
        return redirect(url_for('members'))
    return render_template('register.html', title='Register', form=form)

@app.route("/members/<member_id>")
def member_details(member_id):
    member = Member.query.filter_by(id=member_id).first()
    return render_template('member.html', title=member.username, member=member)

@app.route("/members/<member_id>/delete")
def member_delete(member_id):
    member = Member.query.filter_by(id=member_id).first()
    if member.dues == 0:
        db.session.delete(member)
        db.session.commit()
        flash('Member deleted successfully!', 'success')
    else: 
        flash('Member has pending dues, please ensure they are cleared before removing them.', 'danger')
    return redirect(url_for('members'))