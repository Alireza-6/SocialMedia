from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import re


def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) is None:
        raise ValidationError(
            _("Password Must Include Number"),
            code="Password_Must_Include_Number"
        )


def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) is None:
        raise ValidationError(
            _("Password Must Include Letter"),
            code="Password_Must_Include_Letter"
        )


def special_character_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) is None:
        raise ValidationError(
            _("Password Must Include Special Character"),
            code="Password_Must_Include_Special_Character"
        )
