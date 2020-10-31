from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from app.models import User
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired, Length, Email,EqualTo,ValidationError

class RegisterForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), 
                                            Length(max=20,min=2)])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Conform Password', validators=[DataRequired(), 
                                         EqualTo('password')])
    submit=SubmitField('Register')


    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Account with that Username Exist.Please Try another one")

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Account with that Email Exist.Please Try another one")        

class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')    


class updateProfileForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), 
                                            Length(max=20,min=2)])
    email=StringField('Email', validators=[DataRequired(), Email()])
    picture=FileField('Update Profile Picture',validators=[FileAllowed(['png','jpg','jpeg'])])
    submit=SubmitField('Update Profile')


    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Account with that Username Exist.Please Try another one")

    def validate_email(self,email):
        if email.data !=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Account with that Email Exist.Please Try another one")        


class RequestResetForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(),Email()])
    submit=SubmitField('Request Password Reset')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No Account with that Email.You Must Have an Account")


class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Conform Password', validators=[DataRequired(), 
                                         EqualTo('password')])
    submit=SubmitField('Reset Password')
