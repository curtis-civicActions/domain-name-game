from wtforms import Form, StringField, FieldList, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re

def validate_domain_name(form, field):
    domain = str(field.data).strip()

    if len(domain) > 253:
        raise ValidationError('Field is too long.')

    pattern = r"^(?:[a-zA-Z0-9-]{1,63}\.)*[a-zA-Z0-9-]{1,63}\.[a-zA-Z]{2,63}$"
    if not re.match(pattern, domain):
        raise ValidationError('Field must contain a valid domain name.')


class UserForm(Form):
    name = StringField('Enter name of domain owner',
                       [DataRequired()],
                       render_kw={
                           'class': 'wtf-form-input',
                       })
    domains = FieldList(StringField("", validators=[validate_domain_name]), min_entries=1)
    submit = SubmitField('Load User')
