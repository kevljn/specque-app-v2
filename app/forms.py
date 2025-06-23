from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
 
class LegislativeTextForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    submit = SubmitField('Créer')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=8, message='Le mot de passe doit contenir au moins 8 caractères')
    ])
    password2 = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(),
        EqualTo('password', message='Les mots de passe doivent correspondre')
    ])
    submit = SubmitField('S\'inscrire')

class RoleAssignmentForm(FlaskForm):
    role = SelectField('Type de compte', choices=[
        ('deputy', 'Député'),
        ('reporter', 'Rapporteur'),
        ('secretary', 'Secrétaire'),
        ('group_leader', 'Chef de groupe'),
        ('interest_representative', 'Représentant d\'intérêt'),
        ('fictive_reporter', 'Rapporteur fictif'),
        ('admin', 'Administrateur')
    ], validators=[DataRequired()])
    submit = SubmitField('Attribuer le rôle') 