# Code Style and Conventions

## Python Style Guidelines
1. **Type Hints**
   - Use type hints for all function parameters and return values
   - Use Optional[] for nullable types
   - Use List[], Dict[] for collection types

2. **Documentation**
   - All public functions and classes must have docstrings
   - Use Google-style docstring format
   - Include parameter descriptions and return value documentation

3. **Naming Conventions**
   - Classes: PascalCase (e.g., `NoteGenerator`)
   - Functions/Methods: snake_case (e.g., `generate_note`)
   - Variables: snake_case (e.g., `video_path`)
   - Constants: UPPER_CASE (e.g., `NOTE_OUTPUT_DIR`)

4. **File Structure**
   - One class per file (when possible)
   - Group related functionality in modules
   - Use `__init__.py` for package-level imports

5. **Error Handling**
   - Use custom exceptions from `app/exceptions`
   - Properly catch and handle expected errors
   - Use atomic operations for file writes

6. **Code Organization**
   - Keep functions focused and single-purpose
   - Use private methods (prefixed with _) for internal logic
   - Group related constants at module level

7. **File Operations**
   - Use atomic writes with .tmp files
   - Always clean up temporary files
   - Use pathlib for path manipulation