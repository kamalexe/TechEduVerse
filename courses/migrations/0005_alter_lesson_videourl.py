# Generated by Django 5.0.2 on 2024-02-29 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_lesson_videourl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='VideoURL',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]