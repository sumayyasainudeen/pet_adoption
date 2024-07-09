# Generated by Django 5.0.6 on 2024-07-02 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets_api', '0006_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(default='', max_length=100)),
                ('breed', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=225)),
                ('image', models.ImageField(default='', upload_to='pet_images/')),
                ('available', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='pets_api.category')),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donor', to='pets_api.userdata')),
            ],
        ),
    ]