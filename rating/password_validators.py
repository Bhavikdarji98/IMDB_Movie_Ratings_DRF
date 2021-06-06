
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def validate_password_length(value):
    """
    Validator that enforces minimum length of a password
    """
    message = _("Invalid Length ({0})")
    code = "length"

    min_length = getattr(settings, 'PASSWORD_MIN_LENGTH', None)
    max_length = getattr(settings, 'PASSWORD_MAX_LENGTH', None)

    if min_length and len(value) < min_length:
        raise ValidationError(message.format(_("must be {0} characters or more").format(min_length)), code=code)
    elif max_length and len(value) > max_length:
        raise ValidationError(message.format(_("must be {0} characters or fewer").format(max_length)), code=code)

    return True