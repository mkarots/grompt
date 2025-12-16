# Publishing to PyPI

## Version and Tag Synchronization

To publish a new version to PyPI, follow these steps:

### 1. Update Version in pyproject.toml

Update the `version` field in `pyproject.toml`:

```toml
[project]
version = "0.2.0"  # Update this
```

### 2. Create a Git Tag

Create a tag that matches the version (with optional 'v' prefix):

```bash
# Option 1: Tag with 'v' prefix (recommended)
git tag v0.2.0

# Option 2: Tag without prefix
git tag 0.2.0
```

**Important:** The tag version must match the version in `pyproject.toml` exactly (the workflow will verify this).

### 3. Push the Tag

```bash
git push origin v0.2.0
```

This will trigger the GitHub Actions workflow that:
- Verifies the tag matches `pyproject.toml` version
- Builds the package
- Publishes to PyPI

### 4. Verify Publication

Check PyPI: https://pypi.org/project/grompt/

## Workflow Details

The `.github/workflows/publish.yml` workflow:
- Triggers on tags matching `v*` pattern
- Extracts version from tag (removes 'v' prefix if present)
- Verifies version matches `pyproject.toml`
- Builds using `make build`
- Publishes using `make publish` with credentials from GitHub secrets

## GitHub Secrets Required

- `PYPI_USERNAME`: Your PyPI username
- `PYPI_PASSWORD`: Your PyPI password or API token

## Best Practices

1. **Always update `pyproject.toml` first** before creating the tag
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Use 'v' prefix** for tags (e.g., `v0.2.0`) for consistency
4. **Test locally first** with `make build` and `make publish-test` (TestPyPI)
5. **Create a release** on GitHub after successful publication

