from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confairm Pasword"}))
    class Meta:
        model= User
        fields = [ 'username','email']



from django import forms

class WithdrawalForm(forms.Form):
    amount = forms.DecimalField()


from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(label='Deposit Amount', min_value=0.01)
