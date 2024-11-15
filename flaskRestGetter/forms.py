from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    username = StringField('Usuário')
    password = PasswordField('senha')
    submit = SubmitField('Entrar')

class cadastroMaquina(FlaskForm):
    nome = StringField('nome da maquina')
    submit = SubmitField('criar')

class dadosMaquina(FlaskForm):
    nomedado = StringField("Atributo:")
    minMaquina = FloatField('Min')
    msgErroMin = StringField('Mensagem de erro')
    optionMin = RadioField('Grau de Importância:', 
                        choices=[('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande')],
                        validators=[DataRequired()])
    maxMaquina = FloatField('Max')
    msgErroMax = StringField ('Mensagem de erro')
    optionMax = RadioField('Grau de Importância:', 
                        choices=[('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande')],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')