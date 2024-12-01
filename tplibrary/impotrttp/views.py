# impotrttp/views.py
import barcode
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings  # Импортируем settings
from .models import AddTP, UserProfile, Role, Workshop, Item
from .forms import (
    AddTPForm, UserCreateForm, UserProfileForm,
    RoleForm, WorkshopForm, ItemForm
)
import os

def is_admin(user):
    return user.is_superuser

@login_required
def addtp(request):
    if request.method == 'POST':
        form = AddTPForm(request.POST)
        if form.is_valid():
            addtp = form.save(commit=False)
            addtp.save()  # Сохраняем объект, чтобы получить его id

            # Генерация штрих-кода с использованием значения из поля title
            barcode_image = barcode.get('code128', addtp.title, writer=ImageWriter())
            barcode_filename = f'barcode_{addtp.title}_{addtp.id}.png'
            barcode_path = os.path.join(settings.MEDIA_ROOT, 'barcodes', barcode_filename)

            # Убедимся, что директория существует
            os.makedirs(os.path.dirname(barcode_path), exist_ok=True)

            barcode_image.save(barcode_path)

            # Сохранение штрих-кода в базе данных
            with open(barcode_path, 'rb') as f:
                addtp.barcode_image.save(barcode_filename, ContentFile(f.read()))

            addtp.save()
            return render(request, 'tplibrary/addtp.html', {'form': AddTPForm(), 'addtp': addtp})
    else:
        form = AddTPForm()
    return render(request, 'tplibrary/addtp.html', {'form': form})

@login_required
def data(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    if request.user.is_superuser:
        addtps = AddTP.objects.all().order_by(sort_by)
    else:
        addtps = AddTP.objects.filter(workshop=request.user.userprofile.workshop).order_by(sort_by)
    return render(request, 'tplibrary/data.html', {'addtps': addtps})

def index(request):
    return render(request, 'tplibrary/index.html')

@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().select_related('userprofile')
    return render(request, 'tplibrary/user_list.html', {'users': users})

@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('user_list')
    else:
        user_form = UserCreateForm()
        profile_form = UserProfileForm()
    return render(request, 'tplibrary/add_user.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_list')
    else:
        user_form = UserCreateForm(instance=user)
        profile_form = UserProfileForm(instance=user.userprofile)
    return render(request, 'tplibrary/edit_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'edit_user': user
    })

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if not user.is_superuser:
        user.delete()
    return redirect('user_list')

# Управление справочниками
@user_passes_test(is_admin)
def dictionaries(request):
    roles = Role.objects.all()
    workshops = Workshop.objects.all()
    items = Item.objects.all()
    role_form = RoleForm()
    workshop_form = WorkshopForm()
    item_form = ItemForm()

    return render(request, 'tplibrary/dictionaries.html', {
        'roles': roles,
        'workshops': workshops,
        'items': items,
        'role_form': role_form,
        'workshop_form': workshop_form,
        'item_form': item_form
    })

@user_passes_test(is_admin)
def add_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Должность успешно добавлена')
        else:
            messages.error(request, 'Ошибка при добавлении должности')
    return redirect('dictionaries')

@user_passes_test(is_admin)
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    try:
        role.delete()
        messages.success(request, 'Должность успешно удалена')
    except:
        messages.error(request, 'Невозможно удалить должность, так как она используется')
    return redirect('dictionaries')

@user_passes_test(is_admin)
def add_workshop(request):
    if request.method == 'POST':
        form = WorkshopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цех успешно добавлен')
        else:
            messages.error(request, 'Ошибка при добавлении цеха')
    return redirect('dictionaries')

@user_passes_test(is_admin)
def delete_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    try:
        workshop.delete()
        messages.success(request, 'Цех успешно удален')
    except:
        messages.error(request, 'Невозможно удалить цех, так как он используется')
    return redirect('dictionaries')

@user_passes_test(is_admin)
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изделие успешно добавлено')
        else:
            messages.error(request, 'Ошибка при добавлении изделия')
    return redirect('dictionaries')

@user_passes_test(is_admin)
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изделие успешно обновлено')
        else:
            messages.error(request, 'Ошибка при обновлении изделия')
    else:
        form = ItemForm(instance=item)
    return render(request, 'tplibrary/edit_item.html', {'form': form, 'item': item})

@user_passes_test(is_admin)
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    try:
        item.delete()
        messages.success(request, 'Изделие успешно удалено')
    except:
        messages.error(request, 'Невозможно удалить изделие, так как оно используется')
    return redirect('dictionaries')
