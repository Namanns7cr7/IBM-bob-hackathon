# Contributing to DebugSensei

Thank you for your interest in contributing to DebugSensei! 🥋

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Node version)
- Screenshots if applicable

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach
- Any relevant examples

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**: `git commit -m 'Add amazing feature'`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## Development Setup

See [QUICKSTART.md](QUICKSTART.md) for setup instructions.

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small
- Use meaningful variable names

### JavaScript/React (Frontend)
- Use functional components
- Follow React best practices
- Use meaningful component and variable names
- Keep components focused and reusable
- Add comments for complex logic

## Project Structure

```
debugsensei/
├── backend/          # Python FastAPI backend
├── frontend/         # React frontend
├── docs_knowledge/   # Local documentation
└── sample_repos/     # Test repositories
```

## Areas for Contribution

### High Priority
- [ ] Add more language support (Go, Rust, C++, etc.)
- [ ] Expand error pattern database
- [ ] Improve concept detection accuracy
- [ ] Add more documentation files
- [ ] Create comprehensive test suite

### Medium Priority
- [ ] Add dark/light theme toggle
- [ ] Improve UI/UX design
- [ ] Add export functionality (PDF reports)
- [ ] Add progress tracking
- [ ] Implement user preferences

### Low Priority
- [ ] Add animations and transitions
- [ ] Create video tutorials
- [ ] Add internationalization (i18n)
- [ ] Create browser extension
- [ ] Add VS Code extension

## Adding New Language Support

To add support for a new language:

1. **Update `stack_detector.py`**:
   ```python
   language_map = {
       '.go': 'Go',  # Add your extension
       # ...
   }
   ```

2. **Add concept patterns in `concept_detector.py`**:
   ```python
   def _detect_go_concepts(self):
       concept_patterns = {
           'Goroutine': {
               'patterns': [r'\bgo\s+\w+\('],
               'weight': 10,
               # ...
           }
       }
   ```

3. **Create documentation in `docs_knowledge/`**:
   ```
   docs_knowledge/
     go/
       goroutines.md
       channels.md
   ```

4. **Update `docs_retriever.py`** concept map

5. **Test with sample Go project**

## Adding New Error Patterns

To add a new error pattern in `debug_coach.py`:

```python
{
    'name': 'YourErrorName',
    'patterns': [
        r'error pattern regex',
    ],
    'bug_type': 'Error Type',
    'meaning': 'What this error means',
    'likely_causes': [
        'Cause 1',
        'Cause 2',
    ],
    'debugging_steps': [
        'Step 1',
        'Step 2',
    ],
    'possible_fix': 'How to fix it',
    'prevention': 'How to prevent it',
    'concepts_to_learn': ['Concept1', 'Concept2']
}
```

## Testing

### Backend Testing
```bash
cd backend
pytest  # When tests are added
```

### Frontend Testing
```bash
cd frontend
npm test  # When tests are added
```

### Manual Testing
1. Start both backend and frontend
2. Upload various types of codebases
3. Test all tabs and features
4. Try different skill levels and goals
5. Test error debugging with various error logs

## Documentation

When adding features:
- Update README.md if needed
- Add inline code comments
- Update relevant .md files
- Add examples where helpful

## Pull Request Guidelines

### PR Title Format
- `feat: Add new feature`
- `fix: Fix bug description`
- `docs: Update documentation`
- `style: Code style changes`
- `refactor: Code refactoring`
- `test: Add tests`
- `chore: Maintenance tasks`

### PR Description Should Include
- What changes were made
- Why the changes were needed
- How to test the changes
- Screenshots (if UI changes)
- Related issues (if any)

## Code Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Give constructive feedback
- Celebrate successes together

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Read the documentation
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making DebugSensei better! 🥋**