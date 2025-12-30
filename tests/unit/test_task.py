"""Unit tests for the Task model."""

import pytest

from src.models.task import Task


class TestTaskInstantiation:
    """Tests for Task instantiation."""

    def test_task_instantiation_with_all_fields(self):
        """Test creating a Task with all fields specified."""
        task = Task(id=1, title="Buy groceries", description="Milk and eggs", completed=True)

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk and eggs"
        assert task.completed is True

    def test_task_instantiation_with_defaults(self):
        """Test creating a Task with default values for description and completed."""
        task = Task(id=2, title="Review PRs")

        assert task.id == 2
        assert task.title == "Review PRs"
        assert task.description == ""
        assert task.completed is False

    def test_task_field_types(self):
        """Test that Task fields have correct types."""
        task = Task(id=3, title="Write tests", description="Unit tests", completed=False)

        assert isinstance(task.id, int)
        assert isinstance(task.title, str)
        assert isinstance(task.description, str)
        assert isinstance(task.completed, bool)
