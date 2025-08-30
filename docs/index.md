# wonderland Documentation

Welcome to the comprehensive documentation for wonderland, a Telegram bot application built with Python, aiohttp, and Django.

## Project Overview

wonderland is a Telegram bot application designed for managing programs, handling user bookings, and interacting with users through Telegram. It features both a Telegram bot interface for end users and a Django admin panel for content management.

Key features include:
- Interactive Telegram bot with menu navigation
- Program management and information display
- Booking system for user participation
- FAQ and promotional materials
- User management with role-based access control
- Django admin panel for content management

## Documentation Sections

### 📚 Getting Started

- [**README.md**](../README.md) - Project overview and quick start guide
- [**User Guide**](user_guide.md) - Instructions for end users and administrators
- [**Deployment Guide**](deployment.md) - Instructions for deploying to production

### 👨‍💻 Development

- [**Development Guide**](development.md) - Information for developers
- [**API Documentation**](api.md) - Detailed API specifications
- [**Testing Guide**](testing.md) - Testing strategy and practices
- [**CONTRIBUTING.md**](CONTRIBUTING.md) - Contribution guidelines

### 🏗️ Architecture & Design

- [**Architecture Decision Records (ADR)**](adr/) - Key architectural decisions
- [**Document Records (DR)**](dr/) - Technical debt and problem documentation
- [**Analysis Documents**](analysis/) - In-depth analysis and research

### 📋 Project Management

- [**CHANGELOG.md**](CHANGELOG.md) - Release history and changes
- [**backlog.md**](backlog.md) - Future features and improvements

## Quick Links

### For End Users
- [User Guide](user_guide.md) - How to use the Telegram bot
- [FAQ Section](user_guide.md#faq-section) - Common questions and answers

### For Administrators
- [Admin Panel Guide](user_guide.md#for-administrators-admin-panel) - Using the Django admin interface
- [Deployment Guide](deployment.md) - Installing and running the application

### For Developers
- [Development Setup](development.md#development-environment-setup) - Setting up your development environment
- [Coding Standards](development.md#coding-standards) - Code style and best practices
- [API Documentation](api.md) - Detailed API specifications
- [Testing Guide](testing.md) - Writing and running tests

### For Contributors
- [Contribution Guidelines](CONTRIBUTING.md) - How to contribute to the project
- [Issue Reporting](CONTRIBUTING.md#reporting-issues) - How to report bugs and request features
- [Code Review Process](CONTRIBUTING.md#pull-request-process) - Pull request and review process

## Project Structure

```
.
├── app/                    # Main aiohttp application
│   ├── bot_engine/        # Telegram bot engine
│   ├── tg_api/            # Telegram API accessor
│   ├── database/          # Database configuration
│   ├── store/             # Component store and accessors
│   └── ...                # Other modules
├── admin_panel/           # Django admin panel
├── docs/                  # Documentation (you are here)
│   ├── adr/               # Architecture Decision Records
│   ├── dr/                # Document Records
│   ├── analysis/          # Analysis and research
│   └── ...                # Other documentation files
├── migrations/            # Database migrations
├── etc/                   # Configuration files
└── tests/                 # Test files (TODO)
```

## Support

For technical support, please:
1. Check the [User Guide](user_guide.md) and [FAQ](user_guide.md#faq-section)
2. Review existing issues in the issue tracker
3. Create a new issue if your problem is not addressed elsewhere

## License

TODO: Add license information

## Authors

- Oleg Zamesov (@Zamesov) - Lead Developer

---

*This documentation is a living document and is updated regularly with improvements and additions.*