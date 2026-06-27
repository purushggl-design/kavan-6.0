# KAVAN v6.0 — Contributing Guidelines

Thank you for contributing to KAVAN! To maintain the highest engineering standards and code quality, please adhere to the following workflow and guidelines.

---

## 1. Branch Naming Conventions

- **Features**: `feature/<issue-id>-short-description` (e.g., `feature/102-oauth2-setup`)
- **Bug Fixes**: `bugfix/<issue-id>-short-description` (e.g., `bugfix/45-redis-timeout`)
- **Hotfixes**: `hotfix/<issue-id>-short-description` (e.g., `hotfix/12-cors-fail`)
- **Chore / Docs**: `chore/<short-description>` or `docs/<short-description>`

---

## 2. Commit Message Conventions

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat: add rate limiting foundation` (New feature for the user)
- `fix: resolve pg_dump connection failure` (Bug fix)
- `docs: update deployment instructions` (Documentation changes)
- `style: format imports using isort` (Formatting, white-space, etc. - no code changes)
- `refactor: extract metrics collectors to registry` (Refactoring production code)
- `test: add unit test for system health endpoint` (Adding/correcting tests)
- `chore: update packages in requirements.txt` (Build process, dependencies, auxiliary tools)

---

## 3. Pull Request Workflow

1. **Create a local branch** following the branch naming conventions.
2. **Implement changes** adhering to code style requirements.
3. **Verify locally**:
   - Run tests: `pytest tests/`
   - Run static analysis: `ruff check .` && `mypy .`
   - Test pre-commit: `pre-commit run --all-files`
4. **Push your branch** and open a Pull Request (PR) against `develop` (never directly to `main`).
5. **Ensure CI/CD passes**: Every PR triggers the automated test, build, and security scans.
6. **Obtain Approval**: At least one senior developer review and approval is required.
