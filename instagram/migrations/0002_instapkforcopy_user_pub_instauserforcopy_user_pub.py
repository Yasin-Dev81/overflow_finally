# Generated by Django 4.0.2 on 2022-11-28 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instapkforcopy',
            name='user_pub',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='instagram.myinstapage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instauserforcopy',
            name='user_pub',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='instagram.myinstapage'),
            preserve_default=False,
        ),
    ]
