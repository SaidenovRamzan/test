from typing import Any
from django.core.exceptions import ValidationError
from django import forms
import phonenumbers
from yandex_geocoder import Client
from yandex_geocoder.exceptions import NothingFound
from decimal import Decimal


def validate_address(value):
    client = Client("58e3f0b7-4b3f-4375-afee-1c084e4ef7ea")
    
    try:
        location = client.coordinates(value)
        if (45 <= location[0].quantize(exp=Decimal('1')) <= 87) and ( 40 <= location[1].quantize(exp=Decimal('1')) <= 50):
            adress = client.address(location[0], location[1])
            return adress
        else:
            raise ValidationError('Неверный адрес')
    except NothingFound:
        raise ValidationError('Неверный адрес')
    
    
class PhoneNumberField(forms.CharField):
    def validate(self, value: Any) -> None:
        try:
            parsed_number = phonenumbers.parse(value, "KZ")

            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Invalid phone number.")

            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            return formatted_number
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number format.")
