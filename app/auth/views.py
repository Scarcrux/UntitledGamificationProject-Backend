from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..email import send_email
from . import auth
from .. import db
from models.user import User
from .forms import RegistrationForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # The form we just created
    form = RegistrationForm()
    # Check and see if all the validation checks pass
    if form.validate_on_submit():
        # Create a new user
        user = User(email=form.email.data.lower(),
                  username=form.username.data,
                  password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
       return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
   	token = current_user.generate_confirmation_token()
   	send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
