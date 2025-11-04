from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class MCPProvider(models.Model):
    """MCP Server Providers (Claude, OpenAI, etc.)"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    official_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='providers/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Course(models.Model):
    """Main course structure"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    estimated_time = models.IntegerField(help_text="Estimated time in minutes", default=60)
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_ai_update = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})


class Lesson(models.Model):
    """Individual lessons within a course"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField(help_text="Markdown supported")
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_ai_update = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'title']
        unique_together = ['course', 'slug']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('lesson_detail', kwargs={'course_slug': self.course.slug, 'lesson_slug': self.slug})


class Lab(models.Model):
    """Hands-on labs and exercises"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='labs', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='labs', null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    instructions = models.TextField(help_text="Markdown supported")
    starter_code = models.TextField(blank=True, help_text="Initial code for students")
    solution_code = models.TextField(blank=True, help_text="Solution code (hidden from students)")
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    estimated_time = models.IntegerField(default=30)
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_ai_update = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('lab_detail', kwargs={'slug': self.slug})


class LearningPath(models.Model):
    """Different learning paths (Claude-supported vs Custom)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    provider = models.ForeignKey(MCPProvider, on_delete=models.SET_NULL, null=True, blank=True)
    courses = models.ManyToManyField(Course, related_name='learning_paths')
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name (e.g., 'fa-code')")
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('learning_path_detail', kwargs={'slug': self.slug})


class ContentUpdate(models.Model):
    """Track AI-generated content updates"""
    content_type = models.CharField(
        max_length=20,
        choices=[
            ('course', 'Course'),
            ('lesson', 'Lesson'),
            ('lab', 'Lab'),
        ]
    )
    content_id = models.IntegerField()
    prompt_used = models.TextField()
    ai_response = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.content_type} #{self.content_id} - {self.status}"
