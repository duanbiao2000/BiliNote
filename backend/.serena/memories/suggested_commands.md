# Essential Commands for BiliNote Development

## Development Server
```bash
# Start development server
python main.py

# Alternative with uvicorn (with hot reload)
uvicorn app:create_app --reload
```

## Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
```

## Building
```bash
# Windows build
build.bat

# Linux/macOS build
./build.sh
```

## Development Tools
```bash
# Format code
black .
isort .

# Run tests
pytest

# Check types
mypy .
```

## Common Git Operations (Windows/WSL)
```bash
# Check status
git status

# Create new branch
git checkout -b feature/name

# Commit changes
git add .
git commit -m "description"

# Push changes
git push origin branch-name
```

## Utility Commands (Windows/WSL)
```bash
# List directories
ls -la

# Search in files
grep -r "pattern" .

# Find files
find . -name "pattern"

# Navigate directories
cd path/to/directory
```