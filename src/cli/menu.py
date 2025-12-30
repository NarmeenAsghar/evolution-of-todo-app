"""MenuHandler for CLI user interaction."""

import sys

from src.cli.formatters import (
    format_error,
    format_success,
    format_task_detail,
    format_task_list,
)
from src.services.task_manager import TaskManager


class MenuHandler:
    """Handles CLI menu display and user interactions.

    Manages main menu loop, delegates operations to TaskManager,
    and displays formatted output to user.
    """

    def __init__(self, task_manager: TaskManager) -> None:
        """Initialize with TaskManager dependency.

        Args:
            task_manager: TaskManager instance for business operations
        """
        self.task_manager = task_manager

    def run(self) -> None:
        """Run main menu loop until user exits.

        Displays menu, handles user input, executes operations,
        and shows results. Catches KeyboardInterrupt for clean exit.
        """
        try:
            while True:
                self.display_menu()
                choice = self._get_input("\n> ")

                if choice == "1":
                    self.handle_add_task()
                elif choice == "2":
                    self.handle_view_tasks()
                elif choice == "3":
                    self.handle_update_task()
                elif choice == "4":
                    self.handle_delete_task()
                elif choice == "5":
                    self.handle_toggle_task()
                elif choice == "6":
                    print("\n✓ Goodbye!")
                    sys.exit(0)
                else:
                    print(format_error("Invalid choice. Please select 1-6"))
                    self._pause()

        except KeyboardInterrupt:
            print("\n\n✓ Goodbye!")
            sys.exit(0)

    def display_menu(self) -> None:
        """Display numbered menu options."""
        print("\n" + "=" * 80)
        print("                         TODO CLI APPLICATION")
        print("=" * 80)
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Status")
        print("6. Exit")

    def handle_add_task(self) -> None:
        """Handle add task flow: prompt for title/description, create task."""
        print("\n--- Add New Task ---")
        title = self._get_input("Enter task title: ")
        description = self._get_input("Enter task description (optional, press Enter to skip): ")

        try:
            task = self.task_manager.add_task(title, description)
            print(format_success(f"Task #{task.id} added successfully!"))
        except ValueError as e:
            print(format_error(str(e)))

        self._pause()

    def handle_view_tasks(self) -> None:
        """Handle view tasks: fetch all tasks, display formatted list."""
        print()
        tasks = self.task_manager.get_all_tasks()
        print(format_task_list(tasks))
        self._pause()

    def handle_update_task(self) -> None:
        """Handle update flow: prompt for ID, fields to update."""
        print("\n--- Update Task ---")
        task_id = self._get_int_input("Enter task ID to update: ")
        if task_id is None:
            print(format_error("Please enter a valid task ID number"))
            self._pause()
            return

        # Show current task
        task = self.task_manager.get_task(task_id)
        if task is None:
            print(format_error(f"Task #{task_id} not found"))
            self._pause()
            return

        print(f"\nCurrent title: {task.title}")
        new_title = self._get_input("Enter new title (or press Enter to keep current): ")

        print(f"Current description: {task.description}")
        new_desc = self._get_input("Enter new description (or press Enter to keep current): ")

        try:
            # Only update if user provided new values
            title_update = new_title if new_title.strip() else None
            desc_update = new_desc if new_desc else None

            if title_update or desc_update is not None:
                self.task_manager.update_task(task_id, title_update, desc_update)
                print(format_success(f"Task #{task_id} updated successfully!"))
            else:
                print("No changes made.")
        except ValueError as e:
            print(format_error(str(e)))

        self._pause()

    def handle_delete_task(self) -> None:
        """Handle delete flow: prompt for ID, confirm, delete."""
        print("\n--- Delete Task ---")
        task_id = self._get_int_input("Enter task ID to delete: ")
        if task_id is None:
            print(format_error("Please enter a valid task ID number"))
            self._pause()
            return

        # Show task details before confirmation
        task = self.task_manager.get_task(task_id)
        if task is None:
            print(format_error(f"Task #{task_id} not found"))
            self._pause()
            return

        print()
        print(format_task_detail(task))
        if self._confirm("\nAre you sure you want to delete this task? (y/n): "):
            try:
                self.task_manager.delete_task(task_id)
                print(format_success(f"Task #{task_id} deleted successfully!"))
            except ValueError as e:
                print(format_error(str(e)))
        else:
            print("Delete cancelled.")

        self._pause()

    def handle_toggle_task(self) -> None:
        """Handle toggle flow: prompt for ID, toggle status."""
        print("\n--- Toggle Task Status ---")
        task_id = self._get_int_input("Enter task ID to toggle: ")
        if task_id is None:
            print(format_error("Please enter a valid task ID number"))
            self._pause()
            return

        try:
            task = self.task_manager.toggle_task(task_id)
            status = "completed" if task.completed else "pending"
            print(format_success(f"Task #{task_id} marked as {status}!"))
        except ValueError as e:
            print(format_error(str(e)))

        self._pause()

    def _get_input(self, prompt: str) -> str:
        """Get user input with prompt.

        Args:
            prompt: Prompt string to display

        Returns:
            User input string
        """
        return input(prompt)

    def _get_int_input(self, prompt: str) -> int | None:
        """Get integer input, return None on invalid input.

        Args:
            prompt: Prompt string to display

        Returns:
            Integer value if valid, None otherwise
        """
        try:
            value = input(prompt)
            return int(value)
        except ValueError:
            return None

    def _confirm(self, message: str) -> bool:
        """Show confirmation prompt, return True if user confirms.

        Args:
            message: Confirmation prompt message

        Returns:
            True if user enters 'y' or 'Y', False otherwise
        """
        response = input(message).strip().lower()
        return response == "y"

    def _pause(self) -> None:
        """Pause and wait for user to press Enter."""
        input("\nPress Enter to continue...")
