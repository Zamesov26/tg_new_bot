# Contribution Guidelines

Thank you for your interest in contributing to wonderland! This document provides guidelines and best practices for contributing to the project.

## How to Contribute

### Reporting Issues

Before creating a new issue, please check if a similar issue already exists in the issue tracker.

When reporting an issue, please include:

1. **Clear Description**: A concise description of the problem
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment Details**: 
   - Operating system
   - Python version
   - Database version
   - Any other relevant environment information
6. **Logs**: Relevant log output if applicable

### Feature Requests

To request a new feature:

1. Check if the feature has already been requested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Any implementation ideas (optional)
   - Priority level (low/medium/high)

### Code Contributions

#### Development Setup

1. Fork the repository
2. Clone your fork
3. Set up the development environment (see [Development Guide](development.md))
4. Create a feature branch for your changes

#### Making Changes

1. **Branch Naming**: Use descriptive branch names like `feature/user-authentication` or `bugfix/database-connection`
2. **Commit Messages**: Write clear, concise commit messages
   - Use present tense ("Add feature" not "Added feature")
   - Use imperative mood ("Fix bug" not "Fixes bug")
   - Include issue number if applicable ("Fix #123: Resolve database connection issue")
3. **Code Style**: Follow the project's coding standards (see [Development Guide](development.md))
4. **Documentation**: Update relevant documentation
5. **Tests**: Add or update tests for your changes

#### Pull Request Process

1. **Before Submitting**:
   - Ensure all tests pass
   - Run code quality checks
   - Update documentation
   - Squash commits if necessary

2. **Pull Request Description**:
   - Reference any related issues
   - Describe the changes made
   - Explain the approach taken
   - Include any relevant context

3. **Review Process**:
   - All PRs require review from maintainers
   - Address all review comments
   - Make requested changes or provide justification for not doing so

4. **Merging**:
   - PRs are merged by maintainers after approval
   - Maintain a clean commit history
   - Use squash merge for small changes, merge commit for significant features

## Code Standards

### Python Standards

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep line length to 80 characters
- Use meaningful variable and function names

### Testing

- Write unit tests for new functionality
- Maintain or improve code coverage
- Write integration tests for complex interactions
- Follow the testing patterns described in [Testing Guide](testing.md)

### Documentation

- Update README.md if adding new features
- Add or update docstrings for code changes
- Update relevant documentation in the docs/ directory
- Keep documentation up to date with code changes

## Development Workflow

### Setting Up Development Environment

See [Development Guide](development.md) for detailed instructions.

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app

# Run specific test module
pytest tests/unit/test_module.py
```

### Code Quality Checks

```bash
# Check code style
ruff check .

# Format code
ruff format .
```

### Database Migrations

When making database changes:

1. Create migration: `alembic revision --autogenerate -m "Description"`
2. Review generated migration
3. Apply migration: `alembic upgrade head`
4. Test migration in development environment

## Communication

### Getting Help

- Check existing documentation
- Search issue tracker for similar questions
- Ask in issue comments if appropriate

### Discussions

For architectural discussions or major feature proposals:

1. Create an issue to discuss the proposal
2. Gather feedback from maintainers and community
3. Refine the proposal based on feedback
4. Proceed with implementation once agreed

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as a physical or electronic address, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address, posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4, available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/