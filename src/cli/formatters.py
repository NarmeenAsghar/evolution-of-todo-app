"""Output formatting utilities for the CLI."""

from src.models.task import Task


def format_task_list(tasks: list[Task]) -> str:
    """Format tasks as aligned table with headers.

    Output format:
        ID | Status | Title                | Description
        ---|--------|----------------------|------------------
        1  | [✓]    | Buy groceries        | Milk, eggs...
        2  | [ ]    | Review PRs           | Check team...

    Args:
        tasks: List of Task objects to format

    Returns:
        Formatted string ready for display
    """
    if not tasks:
        return format_empty_state()

    lines = []
    lines.append("=" * 80)
    lines.append("                              YOUR TASKS")
    lines.append("=" * 80)
    lines.append("")

    # Header
    lines.append(f"{'ID':<4} | {'Status':<7} | {'Title':<25} | {'Description'}")
    lines.append(f"{'-'*4}-|-{'-'*7}-|-{'-'*25}-|-{'-'*25}")

    # Tasks
    for task in tasks:
        status = "[✓]" if task.completed else "[ ]"
        desc_preview = (
            task.description[:47] + "..."
            if len(task.description) > 50
            else task.description
        )
        lines.append(
            f"{task.id:<4} | {status:<7} | {task.title[:25]:<25} | {desc_preview}"
        )

    # Summary
    completed_count = sum(1 for t in tasks if t.completed)
    pending_count = len(tasks) - completed_count
    lines.append("")
    lines.append(
        f"Total: {len(tasks)} tasks ({completed_count} completed, {pending_count} pending)"
    )

    return "\n".join(lines)


def format_empty_state() -> str:
    """Return friendly empty state message.

    Returns:
        Empty state message string
    """
    lines = []
    lines.append("=" * 80)
    lines.append("                              YOUR TASKS")
    lines.append("=" * 80)
    lines.append("")
    lines.append("No tasks yet. Add one to get started!")
    return "\n".join(lines)


def format_success(message: str) -> str:
    """Format success message with checkmark.

    Args:
        message: Success message text

    Returns:
        Formatted success message with ✓ prefix
    """
    return f"✓ {message}"


def format_error(message: str) -> str:
    """Format error message with X indicator.

    Args:
        message: Error message text

    Returns:
        Formatted error message with ✗ Error: prefix
    """
    return f"✗ Error: {message}"


def format_task_detail(task: Task) -> str:
    """Format single task with full details.

    Output format:
        Task #1 [✓]
        Title: Buy groceries
        Description: Milk, eggs, bread, cheese

    Args:
        task: Task object to format

    Returns:
        Formatted multi-line string
    """
    status = "[✓]" if task.completed else "[ ]"
    lines = []
    lines.append(f"Task #{task.id} {status}")
    lines.append(f"Title: {task.title}")
    if task.description:
        lines.append(f"Description: {task.description}")
    return "\n".join(lines)
