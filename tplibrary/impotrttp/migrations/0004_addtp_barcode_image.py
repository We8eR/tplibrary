# Generated by Django 5.1.3 on 2024-11-27 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impotrttp', '0003_userprofile_first_name_userprofile_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addtp',
            name='barcode_image',
            field=models.ImageField(blank=True, null=True, upload_to='barcodes/'),
        ),
    ]