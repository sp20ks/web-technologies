from django import forms
from ..models import User, Profile


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=4)


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput,  min_length=4)
    confirm_password = forms.CharField(label='Repeat password', widget=forms.PasswordInput,  min_length=4)


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    bio = forms.CharField(label='Bio', widget=forms.Textarea)
    avatar = forms.ImageField(label='Avatar', required=False)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        profile = Profile.objects.get(user=user)
        recieved_avatar = self.cleaned_data.get('avatar')
        if recieved_avatar:
            profile.avatar = self.cleaned_data.get('avatar')
        received_bio = self.cleaned_data.get('bio')
        if received_bio:
            profile.bio = self.cleaned_data.get('bio')
        profile.save()
        return user