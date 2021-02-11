# Generated by Django 3.1.6 on 2021-02-11 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_auto_20210211_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follows',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_follows', to=settings.AUTH_USER_MODEL),
        ),
    ]