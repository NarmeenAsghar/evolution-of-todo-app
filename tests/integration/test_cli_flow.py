"""Integration tests for CLI flows."""

from io import StringIO
from unittest.mock import patch

import pytest

from src.cli.menu import MenuHandler
from src.services.task_manager import TaskManager


class TestAddTaskFlow:
    """Tests for add task flow."""

    def test_add_task_flow(self):
        """Test complete add task flow."""
        manager = TaskManager()
        menu = MenuHandler(manager)

        inputs = ["1", "Buy groceries", "Milk and eggs", "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()) as output:
                with pytest.raises(SystemExit):
                    menu.run()

        # Verify task was added
        tasks = manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Buy groceries"
        assert tasks[0].description == "Milk and eggs"


class TestViewTasksFlow:
    """Tests for view tasks flow."""

    def test_view_tasks_when_empty(self):
        """Test viewing tasks when list is empty."""
        manager = TaskManager()
        menu = MenuHandler(manager)

        inputs = ["2", "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()) as output:
                with pytest.raises(SystemExit):
                    menu.run()
                result = output.getvalue()

        assert "No tasks yet" in result

    def test_view_tasks_after_adding(self):
        """Test viewing tasks after adding some."""
        manager = TaskManager()
        manager.add_task("Task 1", "Description 1")
        manager.add_task("Task 2", "Description 2")
        menu = MenuHandler(manager)

        inputs = ["2", "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()) as output:
                with pytest.raises(SystemExit):
                    menu.run()
                result = output.getvalue()

        assert "Task 1" in result
        assert "Task 2" in result


class TestUpdateTaskFlow:
    """Tests for update task flow."""

    def test_update_task_flow(self):
        """Test complete update task flow."""
        manager = TaskManager()
        task = manager.add_task("Original Title", "Original Desc")
        menu = MenuHandler(manager)

        inputs = ["3", str(task.id), "Updated Title", "Updated Desc", "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()):
                with pytest.raises(SystemExit):
                    menu.run()

        updated_task = manager.get_task(task.id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Desc"


class TestDeleteTaskFlow:
    """Tests for delete task flow."""

    def test_delete_task_with_confirmation(self):
        """Test deleting task with confirmation."""
        manager = TaskManager()
        task = manager.add_task("To Delete")
        menu = MenuHandler(manager)

        inputs = ["4", str(task.id), "y", "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()):
                with pytest.raises(SystemExit):
                    menu.run()

        assert manager.get_task(task.id) is None

    def test_delete_task_cancellation(self):
        """Test canceling delete operation."""
        manager = TaskManager()
        task = manager.add_task("Keep This")
        menu = MenuHandler(manager)

        inputs = ["4", str(task.id), "n", "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()):
                with pytest.raises(SystemExit):
                    menu.run()

        assert manager.get_task(task.id) is not None


class TestToggleTaskFlow:
    """Tests for toggle task flow."""

    def test_toggle_task_flow(self):
        """Test toggling task completion status."""
        manager = TaskManager()
        task = manager.add_task("Task to Toggle")
        menu = MenuHandler(manager)

        inputs = ["5", str(task.id), "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()):
                with pytest.raises(SystemExit):
                    menu.run()

        toggled_task = manager.get_task(task.id)
        assert toggled_task.completed is True


class TestInvalidInput:
    """Tests for invalid input handling."""

    def test_invalid_menu_choice(self):
        """Test that invalid menu choice shows error."""
        manager = TaskManager()
        menu = MenuHandler(manager)

        inputs = ["99", "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()) as output:
                with pytest.raises(SystemExit):
                    menu.run()
                result = output.getvalue()

        assert "Error:" in result or "Invalid" in result

    def test_invalid_task_id(self):
        """Test that invalid task ID shows error."""
        manager = TaskManager()
        menu = MenuHandler(manager)

        inputs = ["5", "999", "6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()) as output:
                with pytest.raises(SystemExit):
                    menu.run()
                result = output.getvalue()

        assert "not found" in result or "Error" in result


class TestExitFlow:
    """Tests for exit flow."""

    def test_exit_cleanly(self):
        """Test that selecting exit terminates cleanly."""
        manager = TaskManager()
        menu = MenuHandler(manager)

        inputs = ["6"]
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new=StringIO()) as output:
                with pytest.raises(SystemExit):
                    menu.run()
                result = output.getvalue()

        assert "Goodbye" in result
