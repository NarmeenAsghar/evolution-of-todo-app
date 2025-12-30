"""Unit tests for CLI formatter functions."""

import pytest

from src.cli.formatters import (
    format_empty_state,
    format_error,
    format_success,
    format_task_detail,
    format_task_list,
)
from src.models.task import Task


class TestFormatTaskList:
    """Tests for format_task_list() function."""

    def test_format_empty_list_returns_empty_state(self):
        """Test that empty task list shows empty state message."""
        result = format_task_list([])
        assert "No tasks yet" in result
        assert "Add one to get started" in result

    def test_format_one_task(self):
        """Test formatting a single task."""
        task = Task(id=1, title="Buy groceries", description="Milk and eggs", completed=False)
        result = format_task_list([task])

        assert "1" in result
        assert "Buy groceries" in result
        assert "[ ]" in result

    def test_format_multiple_tasks_shows_table(self):
        """Test that multiple tasks are formatted as a table."""
        tasks = [
            Task(id=1, title="Task 1", description="Desc 1", completed=False),
            Task(id=2, title="Task 2", description="Desc 2", completed=True),
            Task(id=3, title="Task 3", description="Desc 3", completed=False),
        ]
        result = format_task_list(tasks)

        assert "ID" in result
        assert "Status" in result
        assert "Title" in result
        assert "Description" in result
        assert "Task 1" in result
        assert "Task 2" in result
        assert "Task 3" in result

    def test_format_shows_completed_and_pending_indicators(self):
        """Test that completed tasks show [✓] and pending show [ ]."""
        tasks = [
            Task(id=1, title="Completed Task", description="", completed=True),
            Task(id=2, title="Pending Task", description="", completed=False),
        ]
        result = format_task_list(tasks)

        assert "[✓]" in result
        assert "[ ]" in result

    def test_format_truncates_long_descriptions(self):
        """Test that long descriptions are truncated with '...'."""
        long_desc = "a" * 100
        task = Task(id=1, title="Task", description=long_desc, completed=False)
        result = format_task_list([task])

        assert "..." in result


class TestFormatEmptyState:
    """Tests for format_empty_state() function."""

    def test_returns_expected_message(self):
        """Test that format_empty_state returns correct message."""
        result = format_empty_state()
        assert "No tasks yet" in result
        assert "Add one to get started" in result


class TestFormatSuccess:
    """Tests for format_success() function."""

    def test_adds_checkmark_prefix(self):
        """Test that success message includes ✓ prefix."""
        result = format_success("Task added successfully")
        assert "✓" in result
        assert "Task added successfully" in result


class TestFormatError:
    """Tests for format_error() function."""

    def test_adds_error_prefix(self):
        """Test that error message includes ✗ Error: prefix."""
        result = format_error("Task not found")
        assert "✗" in result
        assert "Error:" in result
        assert "Task not found" in result


class TestFormatTaskDetail:
    """Tests for format_task_detail() function."""

    def test_shows_full_task_information(self):
        """Test that task detail shows all task information."""
        task = Task(
            id=5,
            title="Review pull requests",
            description="Check team code for quality",
            completed=True,
        )
        result = format_task_detail(task)

        assert "Task #5" in result
        assert "[✓]" in result
        assert "Review pull requests" in result
        assert "Check team code for quality" in result
