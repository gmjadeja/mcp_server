"""
Script to create initial sample data for the MCP Education website
Run with: python manage.py shell < create_initial_data.py
Or: python create_initial_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_site.settings')
django.setup()

from hello.models import MCPProvider, Course, Lesson, Lab, LearningPath
from django.contrib.auth.models import User

print("Creating initial data...")

# Create MCP Providers
print("Creating MCP Providers...")
anthropic, created = MCPProvider.objects.get_or_create(
    name="Anthropic Claude",
    defaults={
        'description': "Official Anthropic Claude AI platform with native MCP support",
        'official_url': "https://www.anthropic.com",
        'is_active': True
    }
)
print(f"  - {anthropic.name} {'created' if created else 'already exists'}")

openai, created = MCPProvider.objects.get_or_create(
    name="OpenAI",
    defaults={
        'description': "OpenAI platform with MCP server integration capabilities",
        'official_url': "https://openai.com",
        'is_active': True
    }
)
print(f"  - {openai.name} {'created' if created else 'already exists'}")

# Create Learning Paths
print("\nCreating Learning Paths...")
claude_path, created = LearningPath.objects.get_or_create(
    slug="claude-supported-mcp",
    defaults={
        'name': "Claude-Supported MCP Servers",
        'description': "Learn to create and use MCP servers with Claude's native support. Perfect for beginners who want to leverage Claude's built-in MCP capabilities.",
        'provider': anthropic,
        'icon': 'fas fa-robot',
        'is_featured': True,
        'order': 1
    }
)
print(f"  - {claude_path.name} {'created' if created else 'already exists'}")

custom_path, created = LearningPath.objects.get_or_create(
    slug="custom-mcp-servers",
    defaults={
        'name': "Custom MCP Servers",
        'description': "Build your own custom MCP servers from scratch. Learn the protocol, tools, and best practices for creating specialized MCP servers.",
        'provider': None,
        'icon': 'fas fa-code',
        'is_featured': True,
        'order': 2
    }
)
print(f"  - {custom_path.name} {'created' if created else 'already exists'}")

# Create Course
print("\nCreating Courses...")
intro_course, created = Course.objects.get_or_create(
    slug="introduction-to-mcp-servers",
    defaults={
        'title': "Introduction to MCP Servers",
        'description': "A comprehensive introduction to Model Context Protocol (MCP) servers. Learn what MCP is, how it works, and why it's important for AI applications. This course covers the fundamentals, architecture, and use cases of MCP servers.",
        'short_description': "Learn the fundamentals of MCP servers and how they enhance AI applications",
        'difficulty_level': 'beginner',
        'estimated_time': 120,
        'order': 1,
        'is_published': True
    }
)
print(f"  - {intro_course.title} {'created' if created else 'already exists'}")

# Add course to learning paths
claude_path.courses.add(intro_course)
custom_path.courses.add(intro_course)

# Create Lessons
print("\nCreating Lessons...")
lesson1, created = Lesson.objects.get_or_create(
    course=intro_course,
    slug="what-is-mcp",
    defaults={
        'title': "What is MCP?",
        'content': """# What is MCP?

The Model Context Protocol (MCP) is a standardized protocol that enables AI assistants to securely access external tools and data sources.

## Key Concepts

- **Protocol**: A standardized way for AI models to interact with external systems
- **Context**: External information that enhances AI responses
- **Security**: Secure, controlled access to tools and data

## Why MCP Matters

MCP servers allow AI assistants to:
- Access real-time data
- Use external tools
- Maintain context across sessions
- Integrate with various services

## Next Steps

In the next lesson, we'll explore the architecture of MCP servers and how they work.
""",
        'order': 1,
        'is_published': True
    }
)
print(f"  - {lesson1.title} {'created' if created else 'already exists'}")

lesson2, created = Lesson.objects.get_or_create(
    course=intro_course,
    slug="mcp-architecture",
    defaults={
        'title': "MCP Architecture",
        'content': """# MCP Architecture

Understanding how MCP servers are structured and how they communicate.

## Components

1. **MCP Server**: The service that provides tools and resources
2. **MCP Client**: The AI assistant that uses the server
3. **Protocol Layer**: Standardized communication protocol

## Communication Flow

```
AI Assistant → MCP Client → MCP Protocol → MCP Server → External Resources
```

## Key Features

- **Bidirectional**: Both client and server can initiate communication
- **Asynchronous**: Non-blocking operations
- **Extensible**: Easy to add new tools and resources

## Best Practices

- Keep server responses efficient
- Handle errors gracefully
- Document all available tools
""",
        'order': 2,
        'is_published': True
    }
)
print(f"  - {lesson2.title} {'created' if created else 'already exists'}")

lesson3, created = Lesson.objects.get_or_create(
    course=intro_course,
    slug="creating-your-first-mcp-server",
    defaults={
        'title': "Creating Your First MCP Server",
        'content': """# Creating Your First MCP Server

A step-by-step guide to building your first MCP server.

## Prerequisites

- Python 3.10+
- Basic Python knowledge
- Understanding of APIs

## Step 1: Setup

Create a new Python project:
```bash
mkdir my-mcp-server
cd my-mcp-server
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install mcp
```

## Step 2: Create Server

Create a `server.py` file:

```python
from mcp.server import Server
from mcp.types import Tool

app = Server("my-server")

@app.tool()
def hello_world(name: str) -> str:
    \"\"\"Greet someone\"\"\"
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run()
```

## Step 3: Test

Run your server:
```bash
python server.py
```

## Next Steps

Try the lab exercise to build a more complex server!
""",
        'order': 3,
        'is_published': True
    }
)
print(f"  - {lesson3.title} {'created' if created else 'already exists'}")

# Create Lab
print("\nCreating Labs...")
lab1, created = Lab.objects.get_or_create(
    slug="hello-world-mcp-server",
    defaults={
        'title': "Hello World MCP Server",
        'description': "Build your first MCP server that greets users and performs basic operations.",
        'instructions': """# Hello World MCP Server Lab

## Objective
Create a simple MCP server that can greet users and perform basic string operations.

## Tasks

1. **Setup**: Create a new Python project with MCP dependencies
2. **Greeting Tool**: Create a tool that takes a name and returns a greeting
3. **String Reversal**: Add a tool that reverses a string
4. **Test**: Test both tools to ensure they work correctly

## Success Criteria

- Server starts without errors
- Both tools are accessible
- Tools return correct results
- Code is clean and well-documented

## Hints

- Start with the starter code provided
- Test each tool individually
- Check the MCP documentation for examples
""",
        'starter_code': """from mcp.server import Server
from mcp.types import Tool

app = Server("hello-world-server")

# TODO: Add your tools here
# Example:
# @app.tool()
# def greet(name: str) -> str:
#     return f"Hello, {name}!"

if __name__ == "__main__":
    app.run()
""",
        'difficulty': 'easy',
        'estimated_time': 30,
        'course': intro_course,
        'lesson': lesson3,
        'order': 1,
        'is_published': True
    }
)
print(f"  - {lab1.title} {'created' if created else 'already exists'}")

print("\n✅ Initial data creation complete!")
print("\nYou can now:")
print("  1. Visit http://127.0.0.1:8000/ to see the homepage")
print("  2. Visit http://127.0.0.1:8000/admin/ to manage content")
print("  3. View courses at http://127.0.0.1:8000/courses/")

