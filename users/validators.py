from django import forms

'''
Проверка заполненности поля
'''


def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'Это поле необходимо заполнить',
            params={'value': value},
        )
