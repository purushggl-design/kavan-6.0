# KAVAN v6.0 — Code Style Guide

KAVAN prioritizes clean, readable, and highly maintainable code. We enforce strict styling standards.

---

## 1. Automated Code Formatting

We use **Black** for code styling, **isort** for import sorting, and **Ruff** for linting.

- **Line Length**: Set to exactly `88` characters.
- **Quotes**: Double quotes (`"`) for strings unless single quotes are needed to avoid escaping.
- **Imports**: Group imports by standard library, third-party libraries, and local modules, sorted alphabetically inside each group.

To auto-format code:
```bash
black .
isort .
ruff check --fix .
```

---

## 2. Type Annotations

Type annotations are **mandatory** for all new Python functions, methods, and classes:

- Always specify parameter types and the return type.
- Example:
  ```python
  def get_by_id(self, pk: Any, raise_404: bool = True) -> Optional[ModelType]:
      ...
  ```
- Make sure mypy type checks pass with zero errors (`mypy .`).

---

## 3. Comments and Documentation

- Use docstrings for all modules, classes, and public methods.
- Document assumptions, parameters, return types, and exceptions raised.
- Keep comments up-to-date. Remove stale code comments and print statements.
