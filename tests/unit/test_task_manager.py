"""Unit tests for the TaskManager service."""

import pytest

from src.models.task import Task
from src.services.task_manager import TaskManager


class TestTaskManagerInitialization:
    """Tests for TaskManager initialization."""

    def test_starts_with_empty_task_list(self):
        """Test that TaskManager initializes with an empty task list."""
        manager = TaskManager()
        assert manager.get_all_tasks() == []
        assert manager.task_count() == 0

    def test_starts_with_next_id_one(self):
        """Test that TaskManager initializes with _next_id = 1."""
        manager = TaskManager()
        task = manager.add_task("First task")
        assert task.id == 1


class TestAddTask:
    """Tests for add_task() method."""

    def test_add_task_with_title_only(self):
        """Test adding a task with title only (description defaults to '')."""
        manager = TaskManager()
        task = manager.add_task("Buy groceries")

        assert task.title == "Buy groceries"
        assert task.description == ""
        assert task.completed is False

    def test_add_task_with_title_and_description(self):
        """Test adding a task with both title and description."""
        manager = TaskManager()
        task = manager.add_task("Review PRs", "Check team pull requests")

        assert task.title == "Review PRs"
        assert task.description == "Check team pull requests"

    def test_auto_increment_ids(self):
        """Test that task IDs auto-increment (1, 2, 3)."""
        manager = TaskManager()
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_reject_empty_title(self):
        """Test that empty title raises ValueError."""
        manager = TaskManager()
        with pytest.raises(ValueError, match="Title cannot be empty"):
            manager.add_task("")

    def test_reject_whitespace_only_title(self):
        """Test that whitespace-only title raises ValueError."""
        manager = TaskManager()
        with pytest.raises(ValueError, match="Title cannot be empty"):
            manager.add_task("   ")

    def test_reject_title_exceeding_200_chars(self):
        """Test that title >200 chars raises ValueError."""
        manager = TaskManager()
        long_title = "a" * 201
        with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
            manager.add_task(long_title)

    def test_reject_description_exceeding_500_chars(self):
        """Test that description >500 chars raises ValueError."""
        manager = TaskManager()
        long_desc = "a" * 501
        with pytest.raises(ValueError, match="Description cannot exceed 500 characters"):
            manager.add_task("Valid title", long_desc)


class TestGetTask:
    """Tests for get_task() method."""

    def test_get_existing_task_returns_task(self):
        """Test that getting an existing task returns the correct Task."""
        manager = TaskManager()
        added = manager.add_task("Test task")
        retrieved = manager.get_task(added.id)

        assert retrieved is not None
        assert retrieved.id == added.id
        assert retrieved.title == "Test task"

    def test_get_nonexistent_task_returns_none(self):
        """Test that getting a non-existent task returns None."""
        manager = TaskManager()
        result = manager.get_task(999)
        assert result is None


class TestGetAllTasks:
    """Tests for get_all_tasks() method."""

    def test_get_all_tasks_when_empty(self):
        """Test that get_all_tasks returns [] when no tasks exist."""
        manager = TaskManager()
        assert manager.get_all_tasks() == []

    def test_get_all_tasks_returns_sorted_by_id(self):
        """Test that get_all_tasks returns tasks sorted by ID."""
        manager = TaskManager()
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        tasks = manager.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_all_tasks_after_deletion(self):
        """Test that get_all_tasks preserves remaining tasks after deletion."""
        manager = TaskManager()
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")

        manager.delete_task(task2.id)

        tasks = manager.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == task1.id
        assert tasks[1].id == task3.id


class TestUpdateTask:
    """Tests for update_task() method."""

    def test_update_title_only(self):
        """Test updating title only (description unchanged)."""
        manager = TaskManager()
        task = manager.add_task("Original", "Description")
        updated = manager.update_task(task.id, title="Updated Title")

        assert updated.title == "Updated Title"
        assert updated.description == "Description"

    def test_update_description_only(self):
        """Test updating description only (title unchanged)."""
        manager = TaskManager()
        task = manager.add_task("Title", "Original")
        updated = manager.update_task(task.id, description="Updated Description")

        assert updated.title == "Title"
        assert updated.description == "Updated Description"

    def test_update_both_title_and_description(self):
        """Test updating both title and description."""
        manager = TaskManager()
        task = manager.add_task("Original Title", "Original Desc")
        updated = manager.update_task(task.id, "New Title", "New Desc")

        assert updated.title == "New Title"
        assert updated.description == "New Desc"

    def test_update_nonexistent_task_raises_error(self):
        """Test that updating non-existent task raises ValueError."""
        manager = TaskManager()
        with pytest.raises(ValueError, match="Task #999 not found"):
            manager.update_task(999, title="New Title")

    def test_update_with_empty_title_raises_error(self):
        """Test that updating with empty title raises ValueError."""
        manager = TaskManager()
        task = manager.add_task("Original")
        with pytest.raises(ValueError, match="Title cannot be empty"):
            manager.update_task(task.id, title="")

    def test_update_with_title_exceeding_200_chars(self):
        """Test that updating with title >200 chars raises ValueError."""
        manager = TaskManager()
        task = manager.add_task("Original")
        long_title = "a" * 201
        with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
            manager.update_task(task.id, title=long_title)

    def test_update_with_description_exceeding_500_chars(self):
        """Test that updating with description >500 chars raises ValueError."""
        manager = TaskManager()
        task = manager.add_task("Title")
        long_desc = "a" * 501
        with pytest.raises(ValueError, match="Description cannot exceed 500 characters"):
            manager.update_task(task.id, description=long_desc)

    def test_id_remains_unchanged_after_update(self):
        """Test that task ID remains unchanged after update."""
        manager = TaskManager()
        task = manager.add_task("Original")
        original_id = task.id
        updated = manager.update_task(original_id, title="Updated")

        assert updated.id == original_id


class TestDeleteTask:
    """Tests for delete_task() method."""

    def test_delete_existing_task(self):
        """Test that deleting an existing task removes it."""
        manager = TaskManager()
        task = manager.add_task("To Delete")
        manager.delete_task(task.id)

        assert manager.get_task(task.id) is None
        assert manager.task_count() == 0

    def test_delete_nonexistent_task_raises_error(self):
        """Test that deleting non-existent task raises ValueError."""
        manager = TaskManager()
        with pytest.raises(ValueError, match="Task #999 not found"):
            manager.delete_task(999)

    def test_subsequent_adds_continue_auto_increment(self):
        """Test that subsequent adds continue auto-increment (no ID reuse)."""
        manager = TaskManager()
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        manager.delete_task(task1.id)
        task3 = manager.add_task("Task 3")

        assert task3.id == 3  # Not 1 (no ID reuse)


class TestToggleTask:
    """Tests for toggle_task() method."""

    def test_toggle_pending_to_completed(self):
        """Test toggling task from pending to completed."""
        manager = TaskManager()
        task = manager.add_task("Task")
        assert task.completed is False

        toggled = manager.toggle_task(task.id)
        assert toggled.completed is True

    def test_toggle_completed_to_pending(self):
        """Test toggling task from completed to pending."""
        manager = TaskManager()
        task = manager.add_task("Task")
        manager.toggle_task(task.id)  # Complete it
        toggled = manager.toggle_task(task.id)  # Toggle back

        assert toggled.completed is False

    def test_toggle_nonexistent_task_raises_error(self):
        """Test that toggling non-existent task raises ValueError."""
        manager = TaskManager()
        with pytest.raises(ValueError, match="Task #999 not found"):
            manager.toggle_task(999)


class TestTaskCount:
    """Tests for task_count() method."""

    def test_count_after_various_operations(self):
        """Test task_count reflects adds and deletes."""
        manager = TaskManager()
        assert manager.task_count() == 0

        task1 = manager.add_task("Task 1")
        assert manager.task_count() == 1

        task2 = manager.add_task("Task 2")
        assert manager.task_count() == 2

        manager.delete_task(task1.id)
        assert manager.task_count() == 1

        manager.delete_task(task2.id)
        assert manager.task_count() == 0
