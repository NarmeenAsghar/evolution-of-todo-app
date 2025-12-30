"""TaskManager service for task business logic."""

from src.models.task import Task


class TaskManager:
    """Manages task lifecycle and business operations.

    Handles task creation, retrieval, updates, deletion, and status toggling.
    Maintains auto-incrementing ID counter and in-memory task storage.
    """

    def __init__(self) -> None:
        """Initialize with empty task storage and ID counter at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create new task with auto-generated ID.

        Args:
            title: Task title (1-200 chars, required)
            description: Task description (0-500 chars, optional)

        Returns:
            Created Task object

        Raises:
            ValueError: If title is empty/whitespace or exceeds length limits
        """
        # Validate title
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

        # Validate description
        if len(description) > 500:
            raise ValueError("Description cannot exceed 500 characters")

        # Create and store task
        task = Task(
            id=self._next_id, title=title, description=description, completed=False
        )
        self._tasks[self._next_id] = task
        self._next_id += 1

        return task

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks ordered by ID.

        Returns:
            List of tasks sorted by ID (ascending)
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def update_task(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> Task:
        """Update task title and/or description.

        Args:
            task_id: Task identifier
            title: New title (if provided, 1-200 chars)
            description: New description (if provided, 0-500 chars)

        Returns:
            Updated Task object

        Raises:
            ValueError: If task not found or validation fails
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        # Validate and update title if provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            if len(title) > 200:
                raise ValueError("Title cannot exceed 200 characters")
            task.title = title

        # Validate and update description if provided
        if description is not None:
            if len(description) > 500:
                raise ValueError("Description cannot exceed 500 characters")
            task.description = description

        return task

    def delete_task(self, task_id: int) -> None:
        """Delete task by ID.

        Args:
            task_id: Task identifier

        Raises:
            ValueError: If task not found
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task #{task_id} not found")
        del self._tasks[task_id]

    def toggle_task(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: Task identifier

        Returns:
            Updated Task object

        Raises:
            ValueError: If task not found
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        task.completed = not task.completed
        return task

    def task_count(self) -> int:
        """Get total number of tasks.

        Returns:
            Number of tasks currently stored
        """
        return len(self._tasks)
