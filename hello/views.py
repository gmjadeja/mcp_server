from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Course, Lesson, Lab, LearningPath, MCPProvider
import markdown


def home(request):
    """Homepage with featured learning paths and courses"""
    featured_paths = LearningPath.objects.filter(is_featured=True, courses__is_published=True).distinct()
    featured_courses = Course.objects.filter(is_published=True)[:6]
    providers = MCPProvider.objects.filter(is_active=True)
    
    context = {
        'featured_paths': featured_paths,
        'featured_courses': featured_courses,
        'providers': providers,
    }
    return render(request, 'hello/home.html', context)


def course_list(request):
    """List all courses"""
    courses = Course.objects.filter(is_published=True)
    difficulty = request.GET.get('difficulty')
    if difficulty:
        courses = courses.filter(difficulty_level=difficulty)
    
    context = {
        'courses': courses,
        'difficulty_filter': difficulty,
    }
    return render(request, 'hello/course_list.html', context)


def course_detail(request, slug):
    """Course detail page"""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.filter(is_published=True)
    labs = course.labs.filter(is_published=True)
    
    context = {
        'course': course,
        'lessons': lessons,
        'labs': labs,
    }
    return render(request, 'hello/course_detail.html', context)


def lesson_detail(request, course_slug, lesson_slug):
    """Lesson detail page"""
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, is_published=True)
    
    # Convert markdown to HTML
    lesson.content_html = markdown.markdown(lesson.content)
    
    # Get next and previous lessons
    lessons = list(course.lessons.filter(is_published=True).order_by('order'))
    try:
        lesson_index = lessons.index(lesson)
        next_lesson = lessons[lesson_index + 1] if lesson_index + 1 < len(lessons) else None
        prev_lesson = lessons[lesson_index - 1] if lesson_index > 0 else None
    except ValueError:
        next_lesson = None
        prev_lesson = None
    
    context = {
        'course': course,
        'lesson': lesson,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
    }
    return render(request, 'hello/lesson_detail.html', context)


def lab_list(request):
    """List all labs"""
    labs = Lab.objects.filter(is_published=True)
    difficulty = request.GET.get('difficulty')
    if difficulty:
        labs = labs.filter(difficulty=difficulty)
    
    context = {
        'labs': labs,
        'difficulty_filter': difficulty,
    }
    return render(request, 'hello/lab_list.html', context)


def lab_detail(request, slug):
    """Lab detail page"""
    lab = get_object_or_404(Lab, slug=slug, is_published=True)
    
    # Convert markdown to HTML
    lab.instructions_html = markdown.markdown(lab.instructions)
    lab.description_html = markdown.markdown(lab.description)
    
    context = {
        'lab': lab,
    }
    return render(request, 'hello/lab_detail.html', context)


def learning_path_list(request):
    """List all learning paths"""
    paths = LearningPath.objects.all()
    context = {
        'paths': paths,
    }
    return render(request, 'hello/learning_path_list.html', context)


def learning_path_detail(request, slug):
    """Learning path detail page"""
    path = get_object_or_404(LearningPath, slug=slug)
    courses = path.courses.filter(is_published=True)
    
    context = {
        'path': path,
        'courses': courses,
    }
    return render(request, 'hello/learning_path_detail.html', context)
