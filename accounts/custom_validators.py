from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class SpecialCharacterPasswordValidator:
    def validate(self, password, user=None):
        if not any(char in "!@#$%^&*()" for char in password):
            raise ValidationError(
                _("A senha deve conter pelo menos um caractere especial: !@#$%^&*()"),
                code='password_no_special',
            )

    def get_help_text(self):
        return _("Sua senha deve conter pelo menos um caractere especial: !@#$%^&*()")