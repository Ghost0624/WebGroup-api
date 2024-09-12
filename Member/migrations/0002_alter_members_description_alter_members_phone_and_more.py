# Generated by Django 4.2.15 on 2024-09-06 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='members',
            name='description',
            field=models.CharField(max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='members',
            name='phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='members',
            name='photo',
            field=models.FileField(upload_to='media/members/'),
        ),
        migrations.AlterField(
            model_name='members',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Member.roles'),
        ),
    ]
