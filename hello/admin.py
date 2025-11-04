from django.contrib import admin
from .models import MCPProvider, Course, Lesson, Lab, LearningPath, ContentUpdate
import markdown


@admin.register(MCPProvider)
class MCPProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty_level', 'order', 'is_published', 'last_ai_update']
    list_filter = ['difficulty_level', 'is_published', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'last_ai_update']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'is_published', 'last_ai_update']
    list_filter = ['is_published', 'course', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'last_ai_update']
    raw_id_fields = ['course']


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'difficulty', 'order', 'is_published', 'last_ai_update']
    list_filter = ['difficulty', 'is_published', 'course', 'created_at']
    search_fields = ['title', 'description', 'instructions']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'last_ai_update']
    raw_id_fields = ['course', 'lesson']


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'is_featured', 'order']
    list_filter = ['is_featured', 'provider']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['courses']
    raw_id_fields = ['provider']


@admin.register(ContentUpdate)
class ContentUpdateAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'content_id', 'status', 'created_at', 'applied_at']
    list_filter = ['status', 'content_type', 'created_at']
    search_fields = ['prompt_used', 'ai_response']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
