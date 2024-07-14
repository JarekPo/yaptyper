from django import forms
from .models import Chat


class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["room_name", "password"]
        widgets = {"password": forms.PasswordInput(attrs={"required": False})}


class JoinRoomForm(forms.Form):
    room_name = forms.CharField(max_length=100, label="Room Name")
    password = forms.CharField(
        max_length=128, label="Password", required=False, widget=forms.PasswordInput
    )
