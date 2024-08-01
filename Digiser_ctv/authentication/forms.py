from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_no')


class CustomUserInfoChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('full_name', 'birthday' ,'address','qualification','identification','identification_address','note')


class CustomUserBankChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('account_number','bank_name','branch','owner','code_bank')