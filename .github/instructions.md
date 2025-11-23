# GitHub Copilot Instructions for AI_PVSim

This file provides guidelines for GitHub Copilot coding agent and code review when working on this repository.

## About This Project

AI_PVSim is a sandbox project exploring how AI can develop a photovoltaic (PV) simulation system. The goal is to leverage AI capabilities to design and build a comprehensive PV system simulator.

## General Guidelines

### Code Quality
- Write clear, well-documented code with meaningful variable and function names
- Add comments for complex logic or algorithms
- Follow consistent code formatting and style
- Ensure all code is production-ready and maintainable

### Testing
- Include unit tests for new functionality
- Ensure tests are comprehensive and cover edge cases
- Run all tests before submitting changes
- Tests should be clear and well-named to explain what they're testing

### Documentation
- Update README.md when adding major features or changing project structure
- Document all public APIs and functions
- Include usage examples where appropriate
- Keep documentation up-to-date with code changes

### Security
- Never commit secrets, API keys, or credentials
- Validate all user inputs
- Follow security best practices for the technology stack
- Use secure dependencies and keep them updated

### Git Practices
- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Reference issue numbers in commit messages when applicable

## Project-Specific Guidelines

### PV Simulation Focus
- All features should relate to photovoltaic system simulation
- Consider real-world PV system constraints and behaviors
- Use industry-standard formulas and calculations where applicable
- Include physical units in variable names or comments for clarity

### Incremental Development
- Start with simple, working implementations
- Add complexity incrementally
- Validate each step before moving to the next
- Maintain backwards compatibility when possible

## Task Preferences

### Good Tasks for Copilot Agent
- Implementing well-defined features with clear requirements
- Writing tests for existing functionality
- Refactoring code for better organization
- Adding documentation and examples
- Fixing specific bugs with clear reproduction steps
- Updating dependencies

### Tasks Requiring Human Review
- Major architectural decisions
- Complex algorithm implementations requiring domain expertise
- Security-critical code changes
- Breaking API changes

## Communication
- Explain your approach and reasoning
- Ask for clarification when requirements are unclear
- Provide context for decisions made
- Be explicit about assumptions
