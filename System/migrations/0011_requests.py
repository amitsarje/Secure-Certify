# Generated by Django 3.0.8 on 2020-10-16 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0010_auto_20201015_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254)),
                ('Proof', models.ImageField(null=True, upload_to='certificates')),
            ],
        ),
    ]