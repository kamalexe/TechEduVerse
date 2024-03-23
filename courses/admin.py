
from django.contrib import admin
from .models import Profile
from .models import Course, Lesson, Exercise, UserProgress, UserSubmission, Category, CourseCategory, Profile


admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Exercise)
admin.site.register(UserProgress)
admin.site.register(UserSubmission)
admin.site.register(Category)
admin.site.register(CourseCategory)
admin.site.register(Profile)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']  # Customize the columns displayed

class CourseAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Level', 'Language', 'CreatedDate', 'UpdatedDate', 'Instructor')
    list_filter = ('Level', 'Language', 'CreatedDate')
    search_fields = ('Title', 'Description')

# Register the Course model with the CourseAdmin options
