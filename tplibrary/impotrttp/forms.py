# impotrttp/forms.py
from django import forms
from .models import AddTP, UserProfile, Role, Workshop, Item
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddTPForm(forms.ModelForm):
    author = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя автора'}),
        label='Автор'
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название техпроцесса'}),
        label='Название'
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Введите описание техпроцесса'}),
        label='Описание'
    )
    item = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Изделие'
    )

    class Meta:
        model = AddTP
        fields = ['author', 'title', 'description', 'workshop', 'item']
        widgets = {
            'workshop': forms.Select(attrs={'class': 'form-control'})
        }

class UserCreateForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}),
        label='Логин'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
        label='Пароль'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}),
        label='Подтверждение пароля'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите фамилию'
        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя'
        })
    )
    middle_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите отчество'
        }),
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'middle_name', 'workshop', 'role']
        widgets = {
            'workshop': forms.Select(attrs={
                'class': 'form-control'
            }),
            'role': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'workshop': 'Цех',
            'role': 'Должность'
        }

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название должности'
            })
        }

class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['number']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер цеха'
            })
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название изделия'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание изделия'
            })
        }
