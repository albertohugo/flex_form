from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import Book, Form, Object, Result, FormMember
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

class BookFilterForm(BSModalForm):
    type = forms.ChoiceField(choices=Book.BOOK_TYPES)

    class Meta:
        fields = ['type', 'clear']


class BookModelForm(BSModalModelForm):
    publication_date = forms.DateField(
        error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    )

    class Meta:
        model = Book
        exclude = ['timestamp']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


##### Forms #######

class FormModelForm(BSModalModelForm):
    class Meta:
        labels = {
            "title": _(u'Name'),
            "status": _(u'Status'),
            "private": _(u'Privado')
        }
        model = Form
        exclude = ['timestamp', 'created_by']

class ObjectModelForm(BSModalModelForm):
    class Meta:
        labels = {
            "label": _(u'Name'),
            "description": _(u'Description'),
            "type": _(u'Type')
        }
        model = Object
        exclude = ['form','timestamp', 'created_by']

class OpenModelForm(BSModalModelForm):
    class Meta:
        fields ='__all__'
        model = Object
        exclude = ['form', 'value','timestamp', 'created_by']

class FormMemberModelForm(BSModalModelForm):
    class Meta:
        labels = {
            "role": _(u'Role'),
            "user": _(u'User')
        }
        model = FormMember
        exclude = ['form',]

class UpdateFormMemberModelForm(BSModalModelForm):
    class Meta:
        labels = {
            "role": _(u'Role')
        }
        model = FormMember
        exclude = ['form','user']




