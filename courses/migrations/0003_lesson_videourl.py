# Generated by Django 5.0.2 on 2024-02-29 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_category_course_coursecategory_lesson_exercise_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='VideoURL',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
