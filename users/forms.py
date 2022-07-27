# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

# 3rd party

# App
from .models import User

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    
    error_messages = {
        'password_mismatch': _('Password fields didn’t match.'),
    }
    
    password1 = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label='Password confirmation', 
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, to avoid errors.")        
        )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)        
        
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',)
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    
    def save(self, commit=True):        
        user = super(UserCreationForm, self).save(commit=False)
        # Save the provided password in hashed format
        user.set_password(self.cleaned_data["password1"])                                                              
        user.save() # Save user to database                                                        
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
        
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
    def save(self, commit=True):        
        user = super(UserChangeForm, self).save(commit=False)
        # Save the provided password in hashed format
        if self.cleaned_data.get("password1"):
            user.set_password(self.cleaned_data["password1"])
                                                        
        if commit:                                                                    
            user.save()            

        return user