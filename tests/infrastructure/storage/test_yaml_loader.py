"""
Unit tests for the YAMLLoader.
"""

import yaml
import pytest
from grompt.core.prompt import Prompt
from grompt.infrastructure.storage.yaml_loader import YAMLLoader


class TestYAMLLoader:
    """Test cases for the YAMLLoader class."""

    @pytest.fixture
    def prompts_dir(self, tmp_path):
        """Create a temporary prompts directory."""
        d = tmp_path / "prompts"
        d.mkdir()
        return d

    @pytest.fixture
    def loader(self, prompts_dir):
        """Create a loader instance."""
        return YAMLLoader(prompts_dir)

    def test_save_prompt(self, loader, prompts_dir):
        """Test saving a prompt to disk."""
        prompt = Prompt(
            id="saved-prompt", version=1, template="Content", parameters={"model": "gpt-4"}
        )

        path = loader.save(prompt)

        assert path.exists()
        assert path == prompts_dir / "saved-prompt.yaml"

        with open(path) as f:
            data = yaml.safe_load(f)
            assert data["id"] == "saved-prompt"
            assert data["template"] == "Content"
            assert data["parameters"]["model"] == "gpt-4"

    def test_save_prompt_custom_filename(self, loader, prompts_dir):
        """Test saving with a custom filename/path."""
        prompt = Prompt(id="p1", version=1, template="t", parameters={"model": "m"})

        # Save as a nested path
        path = loader.save(prompt, prompt_id="nested/custom-name")

        assert path.exists()
        assert path == prompts_dir / "nested/custom-name.yaml"

        with open(path) as f:
            data = yaml.safe_load(f)
            assert data["id"] == "p1"  # ID in file matches prompt object

    def test_load_prompt_by_id(self, loader, prompts_dir):
        """Test loading a prompt by ID."""
        # Create file manually
        p_file = prompts_dir / "my-prompt.yaml"
        with open(p_file, "w") as f:
            yaml.dump(
                {
                    "id": "my-prompt",
                    "version": 2,
                    "parameters": {"model": "gpt-3.5"},
                    "template": "Hello",
                },
                f,
            )

        prompt = loader.load_prompt("my-prompt")

        assert isinstance(prompt, Prompt)
        assert prompt.id == "my-prompt"
        assert prompt.version == 2
        assert prompt.template == "Hello"
        assert prompt.model == "gpt-3.5"

    def test_load_prompt_by_absolute_path(self, loader, tmp_path):
        """Test loading a prompt by absolute file path."""
        # Create a file outside the standard prompts dir
        external_file = tmp_path / "external.yaml"
        with open(external_file, "w") as f:
            yaml.dump(
                {
                    "id": "ext-prompt",
                    "version": 1,
                    "model": "gpt-4",  # legacy format test
                    "template": "External",
                },
                f,
            )

        prompt = loader.load_prompt(str(external_file))

        assert prompt.id == "ext-prompt"
        assert prompt.template == "External"
        assert prompt.model == "gpt-4"  # should be migrated to parameters

    def test_load_prompt_not_found(self, loader):
        """Test loading a non-existent prompt raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            loader.load_prompt("missing-prompt")

    def test_load_invalid_yaml(self, loader, prompts_dir):
        """Test loading invalid YAML raises error."""
        p_file = prompts_dir / "bad.yaml"
        with open(p_file, "w") as f:
            f.write("id: test\n  indentation_error: true")  # Invalid YAML

        with pytest.raises(yaml.YAMLError):
            loader.load_prompt("bad")

    def test_exists(self, loader, prompts_dir):
        """Test checking if a prompt exists."""
        (prompts_dir / "exists.yaml").touch()

        assert loader.exists("exists") is True
        assert loader.exists("missing") is False

    def test_list_prompts(self, loader, prompts_dir):
        """Test listing available prompts."""
        (prompts_dir / "p1.yaml").touch()
        (prompts_dir / "subdir").mkdir()
        (prompts_dir / "subdir/p2.yaml").touch()

        prompts = loader.list_prompts()

        assert "p1" in prompts
        assert "p2" in prompts
        assert len(prompts) == 2
