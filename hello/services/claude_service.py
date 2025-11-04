"""
Service for interacting with Claude API to generate and update educational content
"""
import os
from django.conf import settings
from anthropic import Anthropic
from datetime import datetime


class ClaudeService:
    """Service for Claude API integration"""
    
    def __init__(self):
        api_key = settings.ANTHROPIC_API_KEY
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in settings")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Latest Claude model
    
    def generate_course_content(self, course_title, topic, difficulty="beginner"):
        """Generate course content using Claude"""
        prompt = f"""You are an expert educator creating content for an MCP (Model Context Protocol) server education website.

Create a comprehensive course about: {course_title}
Topic: {topic}
Difficulty Level: {difficulty}

Please provide:
1. A detailed course description (2-3 paragraphs)
2. A short description (1 sentence, max 300 characters)
3. Learning objectives
4. Estimated time in minutes
5. A structured outline with 5-7 lessons

Format your response as JSON with the following structure:
{{
    "description": "detailed course description",
    "short_description": "short one-line description",
    "estimated_time": 60,
    "lessons": [
        {{
            "title": "Lesson title",
            "order": 1,
            "content": "Full lesson content in Markdown format"
        }}
    ]
}}

Focus on practical, hands-on learning with code examples and best practices for MCP servers."""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return None
    
    def generate_lesson_content(self, lesson_title, course_context, previous_lessons=None):
        """Generate lesson content"""
        context_str = ""
        if previous_lessons:
            context_str = f"\nPrevious lessons covered: {', '.join(previous_lessons)}"
        
        prompt = f"""Create a detailed lesson about: {lesson_title}
Course Context: {course_context}
{context_str}

Provide comprehensive content in Markdown format including:
- Clear explanations
- Code examples
- Best practices
- Common pitfalls to avoid
- Exercises or thought questions

Make it engaging and educational for students learning MCP servers."""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return None
    
    def generate_lab_content(self, lab_title, related_lesson=None, difficulty="medium"):
        """Generate lab/exercise content"""
        lesson_context = f"Related to: {related_lesson}" if related_lesson else ""
        
        prompt = f"""Create a hands-on lab exercise about: {lab_title}
Difficulty: {difficulty}
{lesson_context}

Provide:
1. A clear description of what students will build
2. Step-by-step instructions in Markdown
3. Starter code (Python)
4. Expected learning outcomes

Make it practical and engaging, with clear success criteria."""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return None
    
    def update_existing_content(self, content_type, current_content, update_focus):
        """Update existing content with latest information"""
        prompt = f"""Update the following {content_type} content with the latest information and best practices for MCP servers.

Current Content:
{current_content}

Focus Areas for Update:
{update_focus}

Provide the updated content maintaining the same structure and format, but incorporating:
- Latest MCP protocol updates
- Current best practices
- Improved explanations
- Updated code examples

Return only the updated content."""
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return None

