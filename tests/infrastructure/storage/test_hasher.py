"""
Unit tests for the PromptHasher.
"""

from grompt.core.prompt import Prompt
from grompt.infrastructure.storage.hasher import PromptHasher


class TestPromptHasher:
    """Test cases for the PromptHasher class."""

    def test_generate_hash_consistency(self):
        """Test that hashing produces consistent results for same input."""
        prompt = Prompt(
            id="test",
            version=1,
            template="Hello {{ name }}",
            parameters={"model": "gpt-4"},
            system="System",
        )

        hash1 = PromptHasher.generate_hash(prompt)
        hash2 = PromptHasher.generate_hash(prompt)

        assert hash1 == hash2
        assert len(hash1) == 12  # Git-like short hash length

    def test_generate_hash_changes_with_content(self):
        """Test that changing content changes the hash."""
        prompt1 = Prompt(
            id="test", version=1, template="Hello {{ name }}", parameters={"model": "gpt-4"}
        )

        prompt2 = Prompt(
            id="test",
            version=1,
            template="Hello {{ name }}!",  # Changed template
            parameters={"model": "gpt-4"},
        )

        hash1 = PromptHasher.generate_hash(prompt1)
        hash2 = PromptHasher.generate_hash(prompt2)

        assert hash1 != hash2

    def test_generate_hash_ignores_volatile_fields(self):
        """Test that hash ignores fields like hash itself or unrelated metadata."""
        prompt1 = Prompt(id="p", version=1, template="t", parameters={"model": "m"})
        hash1 = PromptHasher.generate_hash(prompt1)

        # Add the hash to the object
        prompt1.hash = "some_old_hash"
        hash2 = PromptHasher.generate_hash(prompt1)

        assert hash1 == hash2

    def test_verify_hash_valid(self):
        """Test verify_hash returns True for matching hash."""
        prompt = Prompt(id="p", version=1, template="t", parameters={"model": "m"})
        valid_hash = PromptHasher.generate_hash(prompt)
        prompt.hash = valid_hash

        assert PromptHasher.verify_hash(prompt) is True

    def test_verify_hash_invalid(self):
        """Test verify_hash returns False for mismatch."""
        prompt = Prompt(id="p", version=1, template="t", parameters={"model": "m"})
        prompt.hash = "invalid_hash"

        assert PromptHasher.verify_hash(prompt) is False
