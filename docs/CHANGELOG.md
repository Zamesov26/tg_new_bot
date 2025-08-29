# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation suite including:
  - API documentation
  - Deployment guide
  - User guide
  - Development guide
  - Testing guide
- Updated README.md with current project structure
- Enhanced ADR documentation with architecture overview
- Enhanced DR documentation with prioritization guidelines

### Changed
- Updated ADR README with project architecture overview
- Updated DR README with project context and prioritization guidelines
- Improved documentation structure and navigation

### Deprecated
- None

### Removed
- None

### Fixed
- Documentation references (fixed tdr -> dr in README)
- Inconsistent documentation links

### Security
- None

## [0.1.0] - 2025-08-29

### Added
- Initial project structure
- Telegram bot engine with aiohttp
- Django admin panel
- PostgreSQL database integration with SQLAlchemy
- Alembic for database migrations
- Core domain models:
  - Users
  - Programs
  - Media
  - Promotions
  - Questionnaires
  - FSM (Finite State Machine)
- Telegram API accessor with polling mechanism
- Basic bot functionality:
  - Interactive menu navigation
  - Program browsing
  - Booking system
  - FAQ section
  - Promotional materials
- Admin panel with CRUD operations for all entities
- Configuration management
- Architecture Decision Records (ADRs)
- Document Records (DRs) for technical debt
- Basic project documentation in README.md

### Changed
- None

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- None

## Project Development Phases

### Phase 1: Foundation (Completed)
- Basic project structure
- Core architecture decisions
- Database schema design
- Telegram bot implementation
- Admin panel setup

### Phase 2: Documentation (In Progress)
- Comprehensive documentation suite
- API documentation
- Deployment guide
- User guide
- Development guide
- Testing guide

### Phase 3: Quality Improvements (Planned)
- Implementation of test suite
- Code quality improvements
- Performance optimizations
- Security enhancements

### Phase 4: Advanced Features (Planned)
- Webhook support for Telegram
- Caching implementation
- Notification system
- Multilingual support
- Advanced analytics

## Technical Debt Items

The following technical debt items are documented in the DR system and planned for future resolution:

### High Priority
- DR-0001: SSL certificate verification disabled
- DR-0002: Hardcoded secrets in code
- DR-0004: Monolithic TgApiAccessor class
- DR-0006: Insufficient exception handling

### Medium Priority
- DR-0005: Lack of automated tests
- DR-0007: Potential database performance issues
- DR-0009: Insufficient documentation and comments
- DR-0010: Insufficient typing
- DR-0012: Code inconsistencies and potential bugs

### Lower Priority
- DR-0003: Unclosed file descriptors
- DR-0008: URL building code duplication
- DR-0011: Unused dependencies and potentially unnecessary components
- DR-0013: Multiple unfinished tasks (TODO comments)

## Future Release Planning

### v0.2.0 (Planned)
- Implementation of basic test suite
- Code quality improvements
- Performance optimizations
- Security enhancements

### v0.3.0 (Planned)
- Webhook support for Telegram
- Caching implementation
- Notification system

### v1.0.0 (Planned)
- Full test coverage
- Production-ready security
- Comprehensive documentation
- Performance benchmarks