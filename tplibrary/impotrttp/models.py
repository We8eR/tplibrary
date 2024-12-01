# impotrttp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название должности')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']

    def __str__(self):
        return self.name

class Workshop(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name='Номер цеха')

    class Meta:
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'
        ordering = ['number']

    def __str__(self):
        return f"Цех {self.number}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.PROTECT, verbose_name='Цех')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name='Должность')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', default='')
    first_name = models.CharField(max_length=150, verbose_name='Имя', default='')
    middle_name = models.CharField(max_length=150, verbose_name='Отчество', blank=True, default='')

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        return f"{full_name} - {self.workshop}"

class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название изделия')
    description = models.TextField(verbose_name='Описание изделия')

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'
        ordering = ['name']

    def __str__(self):
        return self.name

class AddTP(models.Model):
    author = models.CharField(max_length=200, null=False, blank=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    workshop = models.ForeignKey(Workshop, on_delete=models.PROTECT, verbose_name='Цех')
    date = models.DateTimeField(default=timezone.now)
    barcode_image = models.ImageField(upload_to='barcodes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Поле для даты и времени создания
    updated_at = models.DateTimeField(auto_now=True)  # Поле для даты и времени обновления
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name='Изделие')  # Поле для изделия

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
