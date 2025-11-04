"""
Management command to auto-update content using Claude API
Usage: python manage.py update_content --type course --id 1
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from hello.models import Course, Lesson, Lab, ContentUpdate
from hello.services.claude_service import ClaudeService
import json
import re


class Command(BaseCommand):
    help = 'Update educational content using Claude API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['course', 'lesson', 'lab'],
            help='Type of content to update',
        )
        parser.add_argument(
            '--id',
            type=int,
            help='ID of the content to update',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all content that needs updating',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Update content older than X days (default: 7)',
        )

    def handle(self, *args, **options):
        try:
            claude_service = ClaudeService()
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Claude API not configured: {e}'))
            return

        content_type = options.get('type')
        content_id = options.get('id')
        update_all = options.get('all')
        days_threshold = options.get('days')

        if update_all:
            self.update_all_content(claude_service, days_threshold)
        elif content_type and content_id:
            self.update_specific_content(claude_service, content_type, content_id)
        else:
            self.stdout.write(self.style.ERROR('Please specify --type and --id, or use --all'))

    def update_specific_content(self, claude_service, content_type, content_id):
        """Update a specific piece of content"""
        if content_type == 'course':
            obj = Course.objects.get(id=content_id)
            self.update_course(claude_service, obj)
        elif content_type == 'lesson':
            obj = Lesson.objects.get(id=content_id)
            self.update_lesson(claude_service, obj)
        elif content_type == 'lab':
            obj = Lab.objects.get(id=content_id)
            self.update_lab(claude_service, obj)

    def update_all_content(self, claude_service, days_threshold):
        """Update all content that hasn't been updated recently"""
        cutoff_date = timezone.now() - timezone.timedelta(days=days_threshold)
        
        # Update courses
        courses = Course.objects.filter(
            is_published=True,
        ).filter(
            models.Q(last_ai_update__isnull=True) | models.Q(last_ai_update__lt=cutoff_date)
        )
        
        for course in courses:
            self.stdout.write(f'Updating course: {course.title}')
            self.update_course(claude_service, course)
        
        # Update lessons
        lessons = Lesson.objects.filter(
            is_published=True,
        ).filter(
            models.Q(last_ai_update__isnull=True) | models.Q(last_ai_update__lt=cutoff_date)
        )
        
        for lesson in lessons:
            self.stdout.write(f'Updating lesson: {lesson.title}')
            self.update_lesson(claude_service, lesson)
        
        # Update labs
        labs = Lab.objects.filter(
            is_published=True,
        ).filter(
            models.Q(last_ai_update__isnull=True) | models.Q(last_ai_update__lt=cutoff_date)
        )
        
        for lab in labs:
            self.stdout.write(f'Updating lab: {lab.title}')
            self.update_lab(claude_service, lab)

    def update_course(self, claude_service, course):
        """Update course content"""
        try:
            update_focus = f"Update course '{course.title}' with latest MCP server information and best practices"
            current_content = f"Title: {course.title}\nDescription: {course.description}"
            
            updated_content = claude_service.update_existing_content(
                'course',
                current_content,
                update_focus
            )
            
            if updated_content:
                # Create content update record
                ContentUpdate.objects.create(
                    content_type='course',
                    content_id=course.id,
                    prompt_used=update_focus,
                    ai_response=updated_content,
                    status='pending'
                )
                
                # For now, we'll create the update record but not auto-apply
                # Admin can review and approve
                self.stdout.write(
                    self.style.SUCCESS(f'Course update generated for: {course.title}')
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating course: {e}'))

    def update_lesson(self, claude_service, lesson):
        """Update lesson content"""
        try:
            update_focus = f"Update lesson '{lesson.title}' with latest information"
            current_content = lesson.content
            
            updated_content = claude_service.update_existing_content(
                'lesson',
                current_content,
                update_focus
            )
            
            if updated_content:
                ContentUpdate.objects.create(
                    content_type='lesson',
                    content_id=lesson.id,
                    prompt_used=update_focus,
                    ai_response=updated_content,
                    status='pending'
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Lesson update generated for: {lesson.title}')
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating lesson: {e}'))

    def update_lab(self, claude_service, lab):
        """Update lab content"""
        try:
            update_focus = f"Update lab '{lab.title}' with latest best practices"
            current_content = f"{lab.description}\n\n{lab.instructions}"
            
            updated_content = claude_service.update_existing_content(
                'lab',
                current_content,
                update_focus
            )
            
            if updated_content:
                ContentUpdate.objects.create(
                    content_type='lab',
                    content_id=lab.id,
                    prompt_used=update_focus,
                    ai_response=updated_content,
                    status='pending'
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Lab update generated for: {lab.title}')
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating lab: {e}'))

