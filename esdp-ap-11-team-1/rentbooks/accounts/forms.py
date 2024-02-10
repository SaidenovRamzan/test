from django import forms
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from accounts.validatorss import validate_address, PhoneNumberField

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), label='Confirm Password')        
        
class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), label='Confirm Password')
    phone = PhoneNumberField(
        max_length=17,
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}),
        label='Phone'
    )
    
    class Meta:
        model = User
        fields = ['username', 'phone', 'age', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'age': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }
        
        
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.age = self.cleaned_data['age']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'}),
        validators=[validate_address]  # Примените ваш валидатор к полю "address"
    )
    class Meta:
        model = User
        fields = ['phone', 'age', 'email', 'avatar', 'first_name', 'last_name', 'gender', 'education', 'city', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control mb-3'}),
            'age': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'gender': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'education': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'city': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }
        