# Contributing to Grompt

Thank you for your interest in contributing to Grompt! 🎉

## Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/grompt.git
   cd grompt
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests**
   ```bash
   pytest
   ```

## Code Style

- **Formatting**: Use Black (line length: 100)
  ```bash
   black grompt/ tests/
   ```

- **Linting**: Use Ruff
  ```bash
   ruff check grompt/ tests/
   ```

- **Type Checking**: Use MyPy
  ```bash
   mypy grompt/
   ```

- **Type Hints**: Required for all new code

## Testing

- Write tests for all new features
- Ensure all tests pass: `pytest`
- Aim for high coverage: `pytest --cov=grompt --cov-report=html`
- Tests should be in `tests/` directory, mirroring the source structure

## Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes**
   - Write code following the style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Run checks**
   ```bash
   # Format code
   black grompt/ tests/
   
   # Lint
   ruff check grompt/ tests/
   
   # Type check
   mypy grompt/
   
   # Run tests
   pytest
   ```

4. **Commit your changes**
   - Use clear, descriptive commit messages
   - Follow conventional commits format (see below)

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

## Commit Messages

Use clear, descriptive commit messages following conventional commits:

- `feat: Add hash-based change detection`
- `fix: Correct version increment logic`
- `docs: Update README with examples`
- `test: Add validator tests`
- `refactor: Simplify commit command`
- `chore: Update dependencies`

## Project Structure

```
grompt/
├── grompt/
│   ├── core/           # Core domain logic
│   ├── application/    # Application layer (CLI)
│   └── infrastructure/ # Infrastructure (storage, etc.)
├── tests/              # Test files
├── docs/               # Documentation
└── examples/           # Example applications
```

## Areas for Contribution

- **Bug fixes**: Check open issues
- **Documentation**: Improve clarity and examples
- **Tests**: Increase coverage
- **Features**: Discuss in issues first
- **Examples**: Add real-world use cases

## Questions?

- Open an issue for questions or discussions
- Check existing issues before creating new ones
- Be respectful and constructive in discussions

Thank you for contributing! 🙏

