"""Application entry point for Todo CLI."""

from src.cli.menu import MenuHandler
from src.services.task_manager import TaskManager


def main() -> None:
    """Application entry point.

    Initializes TaskManager and MenuHandler, starts main loop.
    Handles top-level exceptions gracefully.
    """
    try:
        task_manager = TaskManager()
        menu_handler = MenuHandler(task_manager)
        menu_handler.run()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("The application will now exit.")
        raise


if __name__ == "__main__":
    main()
