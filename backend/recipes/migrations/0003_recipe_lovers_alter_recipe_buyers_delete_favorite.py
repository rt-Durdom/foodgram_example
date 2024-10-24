# Generated by Django 4.2.16 on 2024-09-27 05:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='lovers',
            field=models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='buyers',
            field=models.ManyToManyField(blank=True, related_name='purchases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]