from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [   
    path('home/', views.course_list, name='home'), 
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # 
    path('', views.course_list, name='courses_list'),
    path('add-course/', views.add_course_view, name='add_course_view'),
    path('add-category/', views.add_category_view, name='add_category_view'),
    path('add-lession/', views.add_lession_view, name='add_lession_view'),
    path('add-exercise/', views.add_exercise_view, name='add_exercise_view'),
    path('courses/', views.course_list, name='courses_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    # path('add_course/', views.AddCourseView, name='add_course'),
    path('add_course_submit/', views.add_course, name='add_course_submit'),
    path('dash-board/', views.dash_board, name='dash_board'),
    path('dash_board/add_category', views.add_category, name='add_category'),
    path('add-lesson/', views.add_lesson, name='add_lesson'),
    path('courses/<int:course_id>/lessons/', views.lessons_list_by_course, name='course_lessons_list'),
    path('lesson_detail/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('add_exercise/', views.add_exercise, name='add_exercise'),
    # path('load_template/', views.load_template, name='load_template'),
    path('category/update/<int:category_id>/', views.update_category, name='update_category'),  
    path('course/update/<int:course_id>/', views.update_course, name='update_course'),
    path('lessons/update/<int:lesson_id>/', views.update_lesson, name='update_lesson'),
    path('exercises/update/<int:exercise_id>/', views.update_exercise, name='update_exercise'),
    path('search/', views.search_courses, name='search_courses'),
    path('courses/category/<int:category_id>/', views.courses_by_category, name='courses_by_category'),

    path('courses/<int:course_id>/lessons/<int:lesson_id>/complete/', views.mark_lesson_completed, name='mark_lesson_completed'),


]