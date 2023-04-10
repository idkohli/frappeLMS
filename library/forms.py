from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from library.models import Member


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    number = StringField('Number', validators=[DataRequired()])
    register = SubmitField('Register')

    def validate_email(self, email):
        member = Member.query.filter_by(email=email.data).first()
        if member:
            raise ValidationError('Email id exists. Please use a different email.')
        
    def validate_number(self, number):
        member = Member.query.filter_by(mobile_number=number.data).first()
        if member:
            raise ValidationError('Mobile number already in use. Please use a new one.')

class IssuanceForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    issue = SubmitField('Issue')

    def validate_email(self, email):
        member = Member.query.filter_by(email=email.data).first()
        if not member:
            raise ValidationError('Member does not exist, please enter a valid email address.')
        
class SearchForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Import')