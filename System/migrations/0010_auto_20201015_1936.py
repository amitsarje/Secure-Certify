# Generated by Django 3.0.8 on 2020-10-15 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0009_remove_students_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificates',
            name='Barcode',
        ),
        migrations.AddField(
            model_name='certificates',
            name='QRcode',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes'),
        ),
        migrations.AlterField(
            model_name='students',
            name='Gender',
            field=models.CharField(choices=[('M', 'male'), ('F', 'female'), ('O', 'other')], max_length=5, null=True),
        ),
    ]
