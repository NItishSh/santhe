import os
import re

def upgrade_dockerfile(path):
    with open(path, 'r') as f:
        content = f.read()

    original_content = content

    # 1. Pin Python versions
    # FROM python:3.11-slim -> FROM python:3.11.8-slim-bookworm
    content = re.sub(r'FROM python:3.11-slim', r'FROM python:3.11.8-slim-bookworm', content)

    # 2. Pin Node versions
    # FROM node:20-alpine -> FROM node:20.11.0-alpine
    content = re.sub(r'FROM node:20-alpine', r'FROM node:20.11.0-alpine', content)
    # Handle the root Dockerfile node:16 case if needed, though simpler to leave if unused, but let's be thorough
    content = re.sub(r'FROM node:16-alpine', r'FROM node:16.20.2-alpine', content)

    # 3. Capitalize AS
    # as builder -> AS builder
    def capitalize_as(match):
        return f"AS {match.group(1)}"
    content = re.sub(r'\s+as\s+(\w+)', capitalize_as, content, flags=re.IGNORECASE)

    # 4. Fix Legacy ENV syntax
    # ENV KEY "value" -> ENV KEY="value"
    # Matches ENV VAR_NAME "value" or ENV VAR_NAME value
    # We need to be careful not to break existing correct ones.
    # Regex look for ENV <SPACE> <WORD> <SPACE> <VALUE> (where value is not starting with =)
    # This is complex to regex purely safely, but looking at the warnings from previous turn:
    # "ENV PORT 3000" in web/Dockerfile
    content = re.sub(r'^ENV\s+(\w+)\s+(?!=\s*)(.+)$', r'ENV \1=\2', content, flags=re.MULTILINE)

    # 5. ARG for Build-time Secrets
    # ENV SECRET_KEY="test_secret" -> ARG SECRET_KEY="test_secret"
    # Only if it looks like a test secret in build stage
    content = content.replace('ENV SECRET_KEY="test_secret"', 'ARG SECRET_KEY="test_secret"')
    content = content.replace("ENV SECRET_KEY='test_secret'", "ARG SECRET_KEY='test_secret'")

    if content != original_content:
        print(f"Upgrading {path}...")
        with open(path, 'w') as f:
            f.write(content)
    else:
        print(f"No changes for {path}")

def main():
    root_dir = "."
    for dirpath, _, filenames in os.walk(root_dir):
        if "Dockerfile" in filenames:
            upgrade_dockerfile(os.path.join(dirpath, "Dockerfile"))

if __name__ == "__main__":
    main()
