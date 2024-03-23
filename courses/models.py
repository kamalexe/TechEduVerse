# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import models
from django.conf import settings  # Make sure you have this import to use settings.AUTH_USER_MODEL

class Course(models.Model):
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    Level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    Language = models.CharField(max_length=100)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(auto_now=True)
    Instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Image = models.ImageField(upload_to='course_images/', blank=True, null=True)  # Add this line

    def __str__(self):
        return self.Title

# Lessons Model
class Lesson(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Title = models.CharField(max_length=255)
    Content = models.TextField()
    Image = models.ImageField(upload_to='lession_images/', blank=True, null=True) 
    VideoURL = models.CharField(max_length=2048,blank=True, default='https://youtu.be/1xD7IqFO9L8?si=LK5yYtCoKmKvqDjI' )
    Order = models.IntegerField()

class Exercise(models.Model):
    Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    Description = models.TextField()
    Image = models.ImageField(upload_to='exercise_images/', blank=True, null=True)  # Add this line
    Solution = models.TextField()


class UserProgress(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    CompletionDate = models.DateTimeField(auto_now_add=True)


class UserSubmission(models.Model):
    Exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    SubmissionDate = models.DateTimeField(auto_now_add=True)
    Content = models.TextField()
    Feedback = models.TextField(blank=True, null=True)



class Category(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.TextField()
    Image = models.ImageField(upload_to='exercise_images/', blank=True, null=True)  # Add this line
    def __str__(self):
        return self.Name


class CourseCategory(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any additional fields here
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    # Permissions field can be handled via User's built-in groups and permissions

    def __str__(self):
        return self.user.username
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)  # Use get_or_create to avoid duplicates

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


