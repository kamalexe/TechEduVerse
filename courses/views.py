# Create your views here.
# myapp/views.py
from datetime import timezone
from gettext import translation
from sqlite3 import IntegrityError
from django.test import TransactionTestCase
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction

from courses.models import Category, Course, CourseCategory, Exercise, Lesson, UserProgress,Profile
from .forms import UserForm, UserRegisterForm, ProfileForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q


@login_required
def home(request):
    user = request.user
    # Attempt to fetch the user's profile. Consider handling the case where it doesn't exist.
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, 'home.html', {'profile': profile})

def get_user_enrolled_courses_with_completed_lessons(user):
    courses = Course.objects.filter(
        lesson__userprogress__User=user
    ).distinct()

    return courses

@login_required
def course_list(request):
    user = request.user
    courses = Course.objects.all()
    categories = Category.objects.all()
    enrolled_courses = get_user_enrolled_courses_with_completed_lessons(user)
    profile, created = Profile.objects.get_or_create(user=user)

    return render(request, 'courses/main_courses.html', {'courses': courses,"categories":categories, 'enrolled_courses':enrolled_courses,'profile':profile,'user':user})

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(Course_id=course_id).order_by('Order')
    return render(request, 'courses/course_detail.html', {'course': course,'lessons':lessons})



def lessons_list_by_course(request, course_id):
    
    lessons = Lesson.objects.filter(Course_id=course_id).order_by('Order')
    print("Received course_id:", course_id,lessons)
    return render(request, 'dash_board/lessons_list.html', {'lessons': lessons})

@login_required
def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    exercises = Exercise.objects.filter(Lesson_id=lesson_id)
    course = lesson.Course
    user = request.user
    progress_queryset = UserProgress.objects.filter(User=user, Course=course, Lesson=lesson)
    lesson_completed = progress_queryset.exists()  # Correctly checks if the lesson is completed
    progress = progress_queryset.first() if lesson_completed else None

    return render(request, 'lessons/lesson_detail.html', {'lesson': lesson, 'exercises': exercises,'course':course,        'lesson_completed': lesson_completed,
"progress":progress})


@login_required
def complete_exercise(request, exercise_id):
    if request.method == 'POST':
        user = request.user
        exercise = Exercise.objects.get(id=exercise_id)
        lesson = exercise.Lesson
        course = lesson.Course
        UserProgress.objects.update_or_create(
            User=user, Course=course, defaults={'Lesson': lesson}
        )
        return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        return HttpResponse("Invalid request", status=400)



@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # Redirect to a new URL:
            return redirect('home')  # Adjust the redirection as needed

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile':profile,
    }
    return render(request, 'registration/edit_profile.html', context)

@login_required
def user_progress(request):
    user_progresses = UserProgress.objects.filter(User=request.user).select_related('Course', 'Lesson')
    return render(request, 'users/user_progress.html', {'user_progresses': user_progresses})


@login_required
def dash_board(request):
    if request.user.is_authenticated:
        user_info = {
            'first_name':request.user.first_name,
            'username': request.user.username,
            'email': request.user.email,

        }
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        categories_count = Category.objects.count()
        lessons_count = Lesson.objects.count()
        courses_count = Course.objects.count()
        exercises_count = Exercise.objects.count()
        categories = Category.objects.all()
        lessons = Lesson.objects.all()
        courses = Course.objects.all()
        user_progresses_count = UserProgress.objects.filter(User=request.user).count()
    else:
        user_info = {}
        categories = {}
        lessons = {}
        courses = {}
        categories_count = lessons_count = courses_count = exercises_count = user_progresses_count = 0
    context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'over_view',"categories_count":categories_count,'lessons_count':lessons_count,'courses_count':courses_count,'exercises_count':exercises_count,'user_progresses_count':user_progresses_count,'user':user,'profile':profile}
    return render(request, 'dash_board/dash_board_base.html', context)

@login_required
def add_course_view(request):
    if request.user.is_authenticated:
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
        }
        categories = Category.objects.all()
        lessons = Lesson.objects.all()
        courses = Course.objects.all()
        context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'add_course'}
    else:
        context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'add_course'}
    return render(request, 'dash_board/dash_board_base.html', context)

@login_required
def add_category_view(request):
    if request.user.is_authenticated:
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
        }
        categories = Category.objects.all()
        lessons = Lesson.objects.all()
        courses = Course.objects.all()
        context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'add_category'}
    else:
        context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'add_category'}
    return render(request, 'dash_board/dash_board_base.html', context)

@login_required
def add_lession_view(request):
    if request.user.is_authenticated:
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
        }
        categories = Category.objects.all()
        lessons = Lesson.objects.all()
        courses = Course.objects.all()
        context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'add_lesson'}
    else:
        context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'add_lesson'}
    return render(request, 'dash_board/dash_board_base.html', context)

@login_required
def add_exercise_view(request):
    if request.user.is_authenticated:
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
        }
        categories = Category.objects.all()
        lessons = Lesson.objects.all()
        courses = Course.objects.all()
        context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'add_exercise'}
    else:
        context = {'user_info': user_info,'categories': categories,'courses':courses, 'lessons':lessons,'active_content': 'add_exercise'}
    return render(request, 'dash_board/dash_board_base.html', context)

@require_http_methods(["GET", "POST"])
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        image = request.FILES.get('image') 
        print("************")
        print(image)
        print("************")
        Category.objects.create(Name=name, Description=description,Image = image)     
        return redirect('dash_board')  # Assume you have a URL named 'categories_list'
    
    # For GET requests, just render the form template
    return render(request, 'dash_board/add_category.html')

@login_required
def update_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        description = request.POST.get('description')
        solution = request.POST.get('solution')
        
        lesson = get_object_or_404(Lesson, id=lesson_id)
        exercise.Lesson = lesson
        exercise.Description = description
        exercise.Solution = solution
        exercise.save()
        
        messages.success(request, 'Exercise updated successfully.')
        return redirect('some_view_name')  # Replace 'some_view_name' with the name of the view you want to redirect to
    
    # If not POST, or the form didn't validate, render the update page again with current exercise data
    lessons = Lesson.objects.all()
    return render(request, 'dash_board/update_exercise.html', {
        'exercise': exercise,
        'lessons': lessons,
        # Add any other context variables you need
    })


@require_http_methods(["GET", "POST"])
def update_category(request, category_id):  # category_id is now mandatory for updates
    # Get the existing category or return a 404 error if not found
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        # Update the category with form data
        category.Name = request.POST.get("name")
        category.Description = request.POST.get("description")
        category.save()
        return redirect('dash_board')  # Assuming this is your intended redirect

    # For GET requests, render the form with the existing category data
    context = {'category': category}
    return render(request, 'dash_board/add_category.html', context)

@login_required
def add_course(request):
    if request.method == "POST":
        # Extract form data from POST request
        selected_category_id = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        level = request.POST.get('level')
        image = request.FILES.get('image') 
        print("************")
        print(image)
        print("************")
        language = request.POST.get('language')
        instructor = request.user
        new_course = Course.objects.create(
            Title=title,
            Description=description,
            Level=level,
            Language=language,
            Instructor=instructor,
            Image = image
        )
        selected_category = Category.objects.get(id=selected_category_id)
        CourseCategory.objects.create(
            Course = new_course,
            Category = selected_category
        )
        # Optionally, use messages to provide feedback to the user
        messages.success(request, 'Course added successfully.')
        return redirect('dash_board')  # Redirect to the dashboard after saving
    
    # For GET requests, just render the form template
    return render(request, 'dash_board/add_course.html')


@login_required
def update_course(request, course_id):
    # Fetch the existing course or return a 404 error if not found
    course = get_object_or_404(Course, id=course_id)
    categories = Category.objects.all()  # Fetch all categories

    # Attempt to fetch existing CourseCategory, else set to None
    try:
        course_category_id = CourseCategory.objects.get(Course=course).Category.id
    except CourseCategory.DoesNotExist:
        course_category_id = None

    if request.method == "POST":
        # Extract form data from POST request
        selected_category_id = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('description')
        level = request.POST.get('level')
        language = request.POST.get('language')
        instructor = request.user
        
        # Update the course with new form data
        course.Title = title
        course.Description = description
        course.Level = level
        course.Language = language
        course.Instructor = instructor
        course.save()
        
        # Update or set the course category
        selected_category = Category.objects.get(id=selected_category_id)
        course_category, created = CourseCategory.objects.update_or_create(
            Course=course,
            defaults={'Category': selected_category}
        )
        
        # Optionally, use messages to provide feedback to the user
        messages.success(request, 'Course updated successfully.')
        return redirect('dash_board')  # Redirect to the dashboard after saving
    
    else:
        # For GET requests, pre-populate the form with the existing course data
        context = {
            'course': course,
            'categories': categories,
            'course_category': course_category_id  # Assuming each course has one category
        }
        return render(request, 'dash_board/update_course.html', context)    

@login_required
def add_lesson(request):
    if request.method == 'POST':
        course_id = request.POST.get('Course')
        title = request.POST.get('Title')
        videoURL = request.POST.get('videoURL')
        content = request.POST.get('Content')
        image = request.FILES.get('image') 
        order = request.POST.get('Order')
        
        course = Course.objects.get(id=course_id)
        print("##############################")
        print(course_id, title, videoURL, content, image, order)
        Lesson.objects.create(Course=course, Title=title, Content=content, Order=order,Image=image,VideoURL=videoURL)
        
        return redirect('dash_board')  # Redirect to your desired URL

    courses = Course.objects.all()
    return render(request, 'dash_board/add_course.html', {'courses': courses})

@login_required
def update_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    courses = Course.objects.all()
    
    if request.method == 'POST':
        course_id = request.POST.get('Course')
        title = request.POST.get('Title')
        content = request.POST.get('Content')
        order = request.POST.get('Order')
        
        course = get_object_or_404(Course, id=course_id)
        # Update the lesson with form data
        lesson.Course = course
        lesson.Title = title
        lesson.Content = content
        lesson.Order = order
        lesson.save()
        
        return redirect('dash_board')  # Redirect to your desired URL after update
    
    # For GET requests or if the form is not valid, render the form with the lesson's current data
    return render(request, 'dash_board/update_lesson.html', {'lesson': lesson, 'courses': courses})


def lessons_list(request):
    lessons = Lesson.objects.all().order_by('Order')
    return render(request, 'dash_board/lessons_list.html', {'lessons': lessons})

@login_required
def add_exercise(request):
    lessons = Lesson.objects.all()  # Fetch all lessons to display in the dropdown
    if request.method == 'POST':
        description = request.POST.get('description')
        lesson_id = request.POST.get('lesson_id')  # Ensure this name matches your form's input/select name
        solution = request.POST.get('solution')
        lesson = get_object_or_404(Lesson, id=lesson_id)  # Fetch the Lesson instance
        Exercise.objects.create(Lesson=lesson, Description=description, Solution=solution)
        
        return redirect('dash_board')  # This is just an example; replace 'lessons_list' with your actual target
    return render(request, 'add_exercise.html', {'lessons': lessons})


@login_required
def mark_lesson_completed(request, course_id, lesson_id):
    if request.method == "POST":
        user = request.user
        course = get_object_or_404(Course, pk=course_id)
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        
        # Check if the entry already exists to avoid duplicates
        if not UserProgress.objects.filter(User=user, Course=course, Lesson=lesson).exists():
            UserProgress.objects.create(User=user, Course=course, Lesson=lesson, CompletionDate=timezone.now())
            messages.success(request, "Lesson marked as completed.")
        else:
            messages.info(request, "Lesson already marked as completed.")
        # Use the referer from the request to redirect back or use a fallback URL
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            # Redirect to a default URL if the referer is not available
            # Change 'your_fallback_view_name' to the name of your fallback view
            return redirect('course_detail', course_id=course_id)
    else:
        return HttpResponse("Invalid request", status=400)
    
    # Auth __________________________________________________

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()
                    if Profile.objects.filter(user=user).exists():
                        messages.error(request, 'A profile for this user already exists.')
                        return redirect('login')
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    messages.success(request, f'Account created for {user.username}!')
                    return redirect('login')
            except IntegrityError as e:
                messages.error(request, 'An unexpected error occurred. Please try again.')
                print("IntegrityError:", e)  # Debug print
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}. Please try again.')
                print("General Exception:", e)  # Debug print
        else:
            # If forms are not valid, display specific validation errors
            user_errors = user_form.errors.as_text()
            profile_errors = profile_form.errors.as_text()
            print("User Form Errors:", user_errors)  # Debug print
            print("Profile Form Errors:", profile_errors)  # Debug print
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
def login_view(request):
    if request.user.is_authenticated:
        # Redirect to home page (or any other page you designate as home)
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('home')
            else:
                # Return an 'invalid login' error message.
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



# search 
def search_courses(request):
    query = request.GET.get('q', '')  # Get the query parameter 'q', or '' if not present
    if query:
        courses =courses = Course.objects.filter(
            Q(Title__icontains=query) |
            Q(Description__icontains=query) |
            Q(Level__icontains=query) |
            Q(Language__icontains=query) |
            Q(Instructor__username__icontains=query) |  # Assuming the instructor's username is searchable
            Q(Instructor__first_name__icontains=query)  # If you want to search by the instructor's first name
        ) 
    else:
        courses = Course.objects.all()
    return render(request, 'courses/search_courses.html', {'courses': courses, 'query': query})

def courses_by_category(request, category_id):
    course_ids = CourseCategory.objects.filter(Category_id=category_id).values_list('Course_id', flat=True)
    courses = Course.objects.filter(id__in=course_ids)
    return render(request, 'courses/search_courses.html', {'courses': courses, 'category_id': category_id})
