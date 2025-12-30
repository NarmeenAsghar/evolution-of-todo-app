# Implementation Plan: In-Memory Todo CLI Application

**Branch**: `001-todo-cli` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-todo-cli/spec.md`

## Summary

Build a professional command-line todo application with clean three-layer architecture (Model → Service → CLI). The application provides complete CRUD operations for tasks with auto-incrementing IDs, status tracking, and product-quality UX. All data stored in-memory using Python standard library only. Focus on deterministic behavior, comprehensive input validation, and responsive performance (<100ms startup, <50ms operations).

**Technical Approach**: Pure Python dataclasses for Task model, centralized TaskManager service for business logic, modular CLI components for user interaction. Main loop delegates all operations to TaskManager, ensuring clean separation and testability.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (dataclasses, typing, sys)
**Storage**: In-memory (dictionary for O(1) lookups by ID, no persistence)
**Testing**: pytest with coverage ≥90%
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single application (command-line tool)
**Performance Goals**:
- <100ms application startup
- <50ms per operation (add, view, update, delete, toggle)
- O(n) or better for all task operations
- Handle 100+ tasks without degradation

**Constraints**:
- Python standard library only (no third-party packages except pytest for testing)
- In-memory storage (no files, databases, or network)
- Single-threaded synchronous execution
- UTF-8 terminal support required for visual indicators
- Maximum function length: 20 lines
- Maximum class length: 200 lines
- No global mutable state

**Scale/Scope**: Small single-user application (100+ tasks in memory, 5 user operations, ~500 lines of source code)

## Constitution Check

*GATE: Must pass before implementation. All items verified against `.specify/memory/constitution.md`*

### Core Principles Compliance

✓ **Spec-Driven Development**: Plan derived from approved specification (specs/001-todo-cli/spec.md)
✓ **No Manual Coding**: Implementation will be generated via Claude Code following this plan
✓ **Clean Architecture**: Three distinct layers with unidirectional dependencies (CLI → Service → Model)
✓ **Deterministic Behavior**: Auto-increment IDs via counter, no randomness, pure functions where possible
✓ **Product-Quality CLI UX**: Detailed UX design included in this plan
✓ **Test-First Development**: Test strategy defined before implementation

### Code Standards Compliance

✓ **Naming Conventions**: PascalCase classes, snake_case functions/variables
✓ **Code Quality**: Max 20-line functions, max 200-line classes, 100-char line limit
✓ **Documentation**: Google-style docstrings, type hints on all signatures
✓ **Dependencies**: Python 3.13+ standard library only (pytest for testing)

### Testing Standards Compliance

✓ **Test Coverage**: Target ≥90% coverage, 100% of public APIs
✓ **Test Organization**: Mirror source structure in tests/ directory
✓ **Test Quality**: Independent tests, fixtures for setup, one assertion per test

### Security Standards Compliance

✓ **Input Validation**: All user inputs validated (numeric IDs, string lengths, empty checks)
✓ **Error Handling**: No stack traces to users, friendly error messages
✓ **No Code Execution**: No eval/exec usage

### Performance Standards Compliance

✓ **In-Memory Storage**: Dictionary-based storage for O(1) lookups
✓ **Efficiency**: No unnecessary copies, efficient data structures
✓ **Response Times**: Startup <100ms, operations <50ms

**Constitution Violations**: None

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (architectural plan)
├── tasks.md             # Implementation tasks (created by /sp.tasks)
└── checklists/
    └── requirements.md  # Spec quality validation (completed)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   └── task.py          # Task dataclass with validation
├── services/
│   ├── __init__.py
│   └── task_manager.py  # TaskManager service (business logic)
├── cli/
│   ├── __init__.py
│   ├── menu.py          # Menu display and input handling
│   └── formatters.py    # Output formatting utilities
├── __init__.py
└── main.py              # Application entry point

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task.py           # Task model tests
│   ├── test_task_manager.py   # TaskManager service tests
│   └── test_formatters.py     # Formatter utility tests
└── integration/
    ├── __init__.py
    └── test_cli_flow.py        # End-to-end CLI flow tests

pyproject.toml           # Project metadata and dependencies
main.py                  # Entry point (imports from src.main)
README.md                # Usage instructions
```

**Structure Decision**: Selected **Option 1: Single project** structure because this is a standalone CLI application with no frontend/backend split or mobile components. Clean layered architecture with models/ (data), services/ (logic), cli/ (interface) matches constitutional requirement for clean architecture with unidirectional dependencies.

## Complexity Tracking

No constitutional violations - complexity tracking not required.

---

## Architecture Design

### Layer Overview

```
┌─────────────────────────────────────┐
│     CLI Layer (User Interface)      │
│  - menu.py: Menu display & input    │
│  - formatters.py: Output formatting │
└──────────────┬──────────────────────┘
               │ (delegates to)
               ↓
┌─────────────────────────────────────┐
│   Service Layer (Business Logic)    │
│  - task_manager.py: CRUD operations │
│  - Input validation & ID generation │
└──────────────┬──────────────────────┘
               │ (operates on)
               ↓
┌─────────────────────────────────────┐
│      Model Layer (Data)             │
│  - task.py: Task dataclass          │
│  - Immutable after creation (IDs)   │
└─────────────────────────────────────┘
```

**Dependency Flow**: CLI → Service → Model (never reversed)

**Key Principles**:
- CLI never directly mutates task data
- Service layer owns all business logic and validation
- Model layer is pure data (no logic)
- Each layer can be tested independently

### Module Specifications

#### 1. Model Layer: `src/models/task.py`

**Purpose**: Define Task data structure with validation

**Exports**:
```python
@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique numeric identifier (immutable)
        title: Task title (1-200 characters, required)
        description: Detailed notes (0-500 characters, optional)
        completed: Completion status (boolean, default False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
```

**Responsibilities**:
- Data structure definition
- Attribute type definitions
- Default values for optional fields

**Not Responsible For**:
- ID generation (handled by TaskManager)
- Validation logic (handled by TaskManager)
- Formatting/display (handled by CLI formatters)

**Testability**: Can instantiate Task objects directly in tests to verify structure

---

#### 2. Service Layer: `src/services/task_manager.py`

**Purpose**: Centralized business logic for task operations

**Exports**:
```python
class TaskManager:
    """Manages task lifecycle and business operations.

    Handles task creation, retrieval, updates, deletion, and status toggling.
    Maintains auto-incrementing ID counter and task storage.
    """

    def __init__(self) -> None:
        """Initialize with empty task storage and ID counter at 1."""

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

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task if found, None otherwise
        """

    def get_all_tasks(self) -> list[Task]:
        """Retrieve all tasks ordered by ID.

        Returns:
            List of tasks sorted by ID (ascending)
        """

    def update_task(self, task_id: int, title: str | None = None,
                    description: str | None = None) -> Task:
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

    def delete_task(self, task_id: int) -> None:
        """Delete task by ID.

        Args:
            task_id: Task identifier

        Raises:
            ValueError: If task not found
        """

    def toggle_task(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: Task identifier

        Returns:
            Updated Task object

        Raises:
            ValueError: If task not found
        """

    def task_count(self) -> int:
        """Get total number of tasks."""
```

**Internal State**:
```python
_tasks: dict[int, Task]  # Dictionary for O(1) lookups
_next_id: int            # Auto-increment counter (starts at 1)
```

**Validation Rules** (enforced in add_task and update_task):
- Title: Non-empty after strip(), 1-200 characters
- Description: 0-500 characters
- Raise ValueError with clear message on validation failure

**Responsibilities**:
- CRUD operations (Create, Read, Update, Delete)
- ID auto-generation and uniqueness
- Input validation and sanitization
- Status toggling logic
- Task storage management

**Not Responsible For**:
- User input/output
- Error message formatting
- Display formatting

**Testability**: Can instantiate TaskManager and verify operations without CLI

---

#### 3. CLI Layer: `src/cli/formatters.py`

**Purpose**: Output formatting utilities

**Exports**:
```python
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

def format_empty_state() -> str:
    """Return friendly empty state message.

    Returns:
        "No tasks yet. Add one to get started!"
    """

def format_success(message: str) -> str:
    """Format success message with checkmark.

    Args:
        message: Success message text

    Returns:
        "✓ {message}"
    """

def format_error(message: str) -> str:
    """Format error message with X indicator.

    Args:
        message: Error message text

    Returns:
        "✗ Error: {message}"
    """

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
```

**Formatting Standards**:
- Use UTF-8 characters: ✓ (completed), ✗ (error), [ ] (pending)
- Table alignment with consistent column widths
- Description preview: Show first 50 chars + "..." if longer
- Consistent indentation (2 spaces)
- Empty lines between sections for readability

**Responsibilities**:
- Visual presentation of tasks
- Table formatting and alignment
- Success/error message styling
- Empty state handling

**Not Responsible For**:
- Business logic
- Data validation
- User input handling

**Testability**: Pure functions - pass Task objects, verify string output

---

#### 4. CLI Layer: `src/cli/menu.py`

**Purpose**: Menu display and user input handling

**Exports**:
```python
class MenuHandler:
    """Handles CLI menu display and user interactions.

    Manages main menu loop, delegates operations to TaskManager,
    and displays formatted output to user.
    """

    def __init__(self, task_manager: TaskManager) -> None:
        """Initialize with TaskManager dependency."""

    def run(self) -> None:
        """Run main menu loop until user exits.

        Displays menu, handles user input, executes operations,
        and shows results. Catches KeyboardInterrupt for clean exit.
        """

    def display_menu(self) -> None:
        """Display numbered menu options."""

    def handle_add_task(self) -> None:
        """Handle add task flow: prompt for title/description, create task."""

    def handle_view_tasks(self) -> None:
        """Handle view tasks: fetch all tasks, display formatted list."""

    def handle_update_task(self) -> None:
        """Handle update flow: prompt for ID, fields to update."""

    def handle_delete_task(self) -> None:
        """Handle delete flow: prompt for ID, confirm, delete."""

    def handle_toggle_task(self) -> None:
        """Handle toggle flow: prompt for ID, toggle status."""

    def _get_input(self, prompt: str) -> str:
        """Get user input with prompt."""

    def _get_int_input(self, prompt: str) -> int | None:
        """Get integer input, return None on invalid input."""

    def _confirm(self, message: str) -> bool:
        """Show confirmation prompt, return True if user confirms."""
```

**Menu Structure**:
```
========================================
         TODO CLI APPLICATION
========================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

> [user input]
```

**Input Handling**:
- Validate numeric input for menu choices and task IDs
- Strip whitespace from string inputs
- Handle empty inputs gracefully
- Catch ValueError exceptions from TaskManager and display formatted errors
- Catch KeyboardInterrupt (Ctrl+C) for clean exit

**Flow After Each Operation**:
1. Execute operation via TaskManager
2. Display success message or error
3. Wait for user to press Enter
4. Clear screen (optional) and redisplay menu

**Responsibilities**:
- Menu display
- User input collection and parsing
- Operation delegation to TaskManager
- Output display via formatters
- Error handling and user feedback

**Not Responsible For**:
- Business logic (delegated to TaskManager)
- Formatting logic (delegated to formatters)

**Testability**: Can mock TaskManager and verify menu behavior

---

#### 5. Entry Point: `src/main.py`

**Purpose**: Application initialization and startup

**Exports**:
```python
def main() -> None:
    """Application entry point.

    Initializes TaskManager and MenuHandler, starts main loop.
    Handles top-level exceptions gracefully.
    """
```

**Responsibilities**:
- Initialize TaskManager
- Initialize MenuHandler with TaskManager
- Start menu loop
- Catch and log any unhandled exceptions
- Provide clean exit

**Entry Point**: `main.py` at repository root imports and calls `src.main.main()`

---

### Data Flow Examples

#### Example 1: Add Task Flow

```
User: Selects "1. Add Task"
  ↓
MenuHandler.handle_add_task():
  - Prompts for title: "Buy groceries"
  - Prompts for description: "Milk and eggs"
  ↓
TaskManager.add_task("Buy groceries", "Milk and eggs"):
  - Validates title (non-empty, ≤200 chars) ✓
  - Validates description (≤500 chars) ✓
  - Creates Task(id=1, title="Buy groceries", description="Milk and eggs", completed=False)
  - Stores in _tasks[1]
  - Increments _next_id to 2
  - Returns Task object
  ↓
MenuHandler:
  - Formats success message: "✓ Task #1 added successfully!"
  - Displays to user
  - Returns to main menu
```

#### Example 2: View Tasks Flow

```
User: Selects "2. View Tasks"
  ↓
MenuHandler.handle_view_tasks():
  ↓
TaskManager.get_all_tasks():
  - Returns list[Task] sorted by ID
  ↓
MenuHandler:
  - If empty: formatters.format_empty_state()
  - Else: formatters.format_task_list(tasks)
  - Displays formatted output
  - Returns to main menu
```

#### Example 3: Toggle Task Flow

```
User: Selects "5. Toggle Task Status"
  ↓
MenuHandler.handle_toggle_task():
  - Prompts for task ID: "1"
  - Parses to int(1)
  ↓
TaskManager.toggle_task(1):
  - Fetches task from _tasks[1]
  - If not found: raise ValueError("Task #1 not found")
  - Toggles task.completed (False → True)
  - Returns updated Task
  ↓
MenuHandler:
  - Catches ValueError if raised → format_error()
  - Else: format_success("Task #1 marked as completed")
  - Displays result
  - Returns to main menu
```

---

## Error Handling Strategy

### Input Validation (TaskManager)

**Title Validation**:
- Check: `title.strip() == ""` → ValueError("Title cannot be empty")
- Check: `len(title) > 200` → ValueError("Title cannot exceed 200 characters")

**Description Validation**:
- Check: `len(description) > 500` → ValueError("Description cannot exceed 500 characters")

**ID Validation**:
- Check: `task_id not in _tasks` → ValueError(f"Task #{task_id} not found")

### Input Parsing (MenuHandler)

**Menu Choice**:
- Non-numeric input → Display: "✗ Error: Please enter a number between 1 and 6"
- Out of range (< 1 or > 6) → Display: "✗ Error: Invalid choice. Please select 1-6"

**Task ID Input**:
- Non-numeric input → Display: "✗ Error: Please enter a valid task ID number"
- Negative number → Display: "✗ Error: Task ID must be a positive number"

### Exception Handling Flow

```python
# In MenuHandler methods:
try:
    # Operation via TaskManager
    result = self.task_manager.some_operation(...)
    print(format_success("Operation successful!"))
except ValueError as e:
    # Business logic errors from TaskManager
    print(format_error(str(e)))
except KeyboardInterrupt:
    # User pressed Ctrl+C
    print("\n✓ Goodbye!")
    sys.exit(0)
```

**Never Expose**:
- Stack traces to end users
- Internal implementation details
- Python exception types

**Always Provide**:
- Clear description of what went wrong
- Suggested corrective action when possible
- Consistent error formatting with ✗ prefix

---

## UX Design Specification

### Visual Design

**Main Menu**:
```
========================================
         TODO CLI APPLICATION
========================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Task Status
6. Exit

> _
```

**Task List Display**:
```
========================================
              YOUR TASKS
========================================

ID | Status | Title                      | Description
---|--------|----------------------------|---------------------------
1  | [✓]    | Buy groceries              | Milk, eggs, bread...
2  | [ ]    | Review pull requests       | Check team code...
3  | [ ]    | Write documentation        | Update README and...

Total: 3 tasks (1 completed, 2 pending)
```

**Empty State**:
```
========================================
              YOUR TASKS
========================================

No tasks yet. Add one to get started!
```

**Success Messages**:
```
✓ Task #1 added successfully!
✓ Task #2 updated successfully!
✓ Task #3 deleted successfully!
✓ Task #4 marked as completed!
```

**Error Messages**:
```
✗ Error: Title cannot be empty
✗ Error: Task #999 not found
✗ Error: Please enter a valid task ID number
```

**Confirmation Prompts**:
```
Are you sure you want to delete Task #3? (y/n): _
```

### Interaction Patterns

**Add Task Flow**:
```
Enter task title: Buy groceries
Enter task description (optional, press Enter to skip): Milk and eggs

✓ Task #1 added successfully!

Press Enter to continue...
[Main menu redisplays]
```

**Update Task Flow**:
```
Enter task ID to update: 1
Current title: Buy groceries
Enter new title (or press Enter to keep current): Buy groceries and bread
Current description: Milk and eggs
Enter new description (or press Enter to keep current):

✓ Task #1 updated successfully!

Press Enter to continue...
```

**Delete Task Flow**:
```
Enter task ID to delete: 3
Task #3: Write documentation
Are you sure you want to delete this task? (y/n): y

✓ Task #3 deleted successfully!

Press Enter to continue...
```

**Toggle Task Flow**:
```
Enter task ID to toggle: 1

✓ Task #1 marked as completed!

Press Enter to continue...
```

**Exit Flow**:
```
User selects: 6

✓ Goodbye!
[Application terminates]
```

### UX Principles

1. **Consistency**: All success messages use ✓ prefix, all errors use ✗ prefix
2. **Feedback**: Every action produces immediate confirmation or error message
3. **Forgiveness**: Confirmation prompts for destructive operations (delete)
4. **Clarity**: Numbered menu options, clear prompts, structured output
5. **Efficiency**: Menu redisplays after each action for quick multiple operations
6. **Resilience**: Invalid inputs handled gracefully without crashing
7. **Guidance**: Empty states provide helpful next steps
8. **Polish**: Aligned tables, consistent spacing, professional appearance

---

## Performance Considerations

### Data Structure Choices

**Task Storage**: `dict[int, Task]`
- **Why**: O(1) lookup by ID (get, update, delete, toggle)
- **Alternative Rejected**: List requires O(n) search by ID
- **Trade-off**: Dictionary overhead acceptable for 100+ tasks

**Task Listing**: `sorted(_tasks.values())`
- **Complexity**: O(n log n) for sorting by ID
- **Justification**: View operation, not performance-critical
- **Optimization**: Can memoize if needed, but premature for initial implementation

### Performance Targets

| Operation | Target | Strategy |
|-----------|--------|----------|
| Startup | <100ms | No I/O, minimal initialization |
| Add Task | <50ms | O(1) dictionary insert |
| Get Task | <50ms | O(1) dictionary lookup |
| Update Task | <50ms | O(1) dictionary lookup + update |
| Delete Task | <50ms | O(1) dictionary deletion |
| Toggle Task | <50ms | O(1) dictionary lookup + update |
| View All Tasks | <50ms | O(n) iteration + O(n log n) sort, acceptable for n<1000 |

### Memory Considerations

**Per-Task Overhead**:
- Task object: ~200 bytes (4 fields + Python overhead)
- Dictionary entry: ~100 bytes (key + pointer + overhead)
- Total: ~300 bytes per task

**100 Tasks**: ~30 KB
**1000 Tasks**: ~300 KB

**Conclusion**: Memory usage negligible, no optimization needed

### Scalability Notes

**Current Design Scales To**:
- 1000+ tasks without performance issues
- Python dict handles 10k+ entries efficiently
- Sorting 1000 items: ~10ms on modern hardware

**Future Optimizations** (if needed):
- Maintain sorted list alongside dict (trade memory for speed)
- Index by status for filtered views
- Pagination for display (current design shows all tasks)

**Not Needed for Phase 1**: Current design meets all requirements

---

## Testing Strategy

### Test Organization

```
tests/
├── unit/
│   ├── test_task.py           # Task model tests
│   ├── test_task_manager.py   # TaskManager service tests
│   └── test_formatters.py     # Formatter utility tests
└── integration/
    └── test_cli_flow.py        # End-to-end CLI tests
```

### Unit Test Coverage

#### test_task.py
- Test Task instantiation with all fields
- Test Task instantiation with defaults (description="", completed=False)
- Test Task immutability of ID
- Test Task field types

#### test_task_manager.py
**Initialization**:
- Test TaskManager starts with empty task list
- Test TaskManager starts with _next_id = 1

**add_task()**:
- Test add task with title only (description defaults to "")
- Test add task with title and description
- Test auto-increment ID (add 3 tasks, verify IDs 1, 2, 3)
- Test reject empty title (ValueError)
- Test reject whitespace-only title (ValueError)
- Test reject title >200 chars (ValueError)
- Test reject description >500 chars (ValueError)

**get_task()**:
- Test get existing task returns correct Task
- Test get non-existent task returns None

**get_all_tasks()**:
- Test get all tasks when empty returns []
- Test get all tasks returns sorted by ID
- Test get all tasks after deletion preserves remaining tasks

**update_task()**:
- Test update title only (description unchanged)
- Test update description only (title unchanged)
- Test update both title and description
- Test update non-existent task raises ValueError
- Test update with empty title raises ValueError
- Test update with title >200 chars raises ValueError
- Test update with description >500 chars raises ValueError
- Test ID remains unchanged after update

**delete_task()**:
- Test delete existing task removes it
- Test delete non-existent task raises ValueError
- Test subsequent adds continue auto-increment (no ID reuse)

**toggle_task()**:
- Test toggle pending → completed
- Test toggle completed → pending
- Test toggle non-existent task raises ValueError

**task_count()**:
- Test count after various operations

#### test_formatters.py
- Test format_task_list with empty list returns empty state
- Test format_task_list with one task formats correctly
- Test format_task_list with multiple tasks shows table
- Test format_task_list shows [✓] for completed, [ ] for pending
- Test format_task_list truncates long descriptions with "..."
- Test format_empty_state returns expected message
- Test format_success adds ✓ prefix
- Test format_error adds ✗ Error: prefix
- Test format_task_detail shows full task information

### Integration Test Coverage

#### test_cli_flow.py
**Approach**: Mock stdin/stdout, verify end-to-end flows

**Test Scenarios**:
- Test add task flow (menu choice 1 → title → description → success)
- Test view tasks when empty shows empty state
- Test view tasks after adding shows formatted list
- Test update task flow (menu choice 3 → ID → new title → success)
- Test delete task with confirmation (menu choice 4 → ID → y → success)
- Test delete task cancellation (menu choice 4 → ID → n → cancel)
- Test toggle task flow (menu choice 5 → ID → success)
- Test invalid menu choice shows error and redisplays menu
- Test invalid task ID shows error
- Test exit cleanly (menu choice 6 → goodbye)

### Test Fixtures

```python
@pytest.fixture
def task_manager():
    """Provide fresh TaskManager instance."""
    return TaskManager()

@pytest.fixture
def sample_tasks(task_manager):
    """Provide TaskManager with 3 sample tasks."""
    task_manager.add_task("Task 1", "Description 1")
    task_manager.add_task("Task 2", "Description 2")
    task_manager.add_task("Task 3", "Description 3")
    return task_manager
```

### Coverage Target

- **Minimum**: 90% overall coverage
- **Target**: 100% of public API methods
- **Exclude**: main.py entry point (tested via integration tests)

---

## Development Order

**Phase 1: Model Layer** (Testable foundation)
1. Create `src/models/task.py` with Task dataclass
2. Write `tests/unit/test_task.py`
3. Verify tests pass

**Phase 2: Service Layer** (Core business logic)
1. Create `src/services/task_manager.py` with TaskManager class
2. Write `tests/unit/test_task_manager.py` (all 20+ test cases)
3. Run tests (RED - they should fail)
4. Implement TaskManager methods to pass tests (GREEN)
5. Refactor for code quality (REFACTOR)

**Phase 3: CLI Formatters** (Output utilities)
1. Create `src/cli/formatters.py` with formatting functions
2. Write `tests/unit/test_formatters.py`
3. Implement formatters to pass tests

**Phase 4: CLI Menu** (User interface)
1. Create `src/cli/menu.py` with MenuHandler class
2. Write `tests/integration/test_cli_flow.py`
3. Implement MenuHandler to pass tests
4. Manual testing for UX polish

**Phase 5: Application Entry** (Integration)
1. Create `src/main.py` with main() function
2. Create `main.py` at root (imports src.main)
3. Manual end-to-end testing
4. Verify all success criteria from spec

**Phase 6: Documentation & Polish**
1. Write README.md with usage instructions
2. Add module-level docstrings
3. Final coverage check (≥90%)
4. Final UX verification against spec

---

## Risk Analysis & Mitigation

### Risk 1: UTF-8 Characters Not Displaying

**Problem**: Terminal doesn't support UTF-8 (✓, ✗ characters)
**Likelihood**: Low (most modern terminals support UTF-8)
**Impact**: Medium (UX degradation)
**Mitigation**:
- Document UTF-8 requirement in README
- Test on Windows Command Prompt, PowerShell, Unix terminals
- Fallback: Could use ASCII alternatives ([X], [_]) if needed
**Decision**: Accept risk for Phase 1, UTF-8 is standard

### Risk 2: Performance with 1000+ Tasks

**Problem**: Sorting 1000+ tasks on every view might be slow
**Likelihood**: Low (spec targets 100 tasks)
**Impact**: Low (still within <50ms target on modern hardware)
**Mitigation**:
- Current O(n log n) sort is acceptable for n<1000
- If needed: Maintain pre-sorted list alongside dict
**Decision**: Accept risk, optimize only if measured performance issue

### Risk 3: Input Validation Edge Cases

**Problem**: Unexpected input combinations (e.g., Unicode, control characters)
**Likelihood**: Medium (users might paste unusual content)
**Impact**: Low (Python str handles Unicode well)
**Mitigation**:
- Rely on Python's robust str handling
- Length validation prevents most issues
- Test with edge cases during development
**Decision**: Standard validation sufficient, handle edge cases as bugs if found

### Risk 4: Test Coverage <90%

**Problem**: Difficult-to-test code paths (e.g., KeyboardInterrupt handling)
**Likelihood**: Low (well-defined architecture)
**Impact**: Medium (constitutional violation)
**Mitigation**:
- Design for testability (dependency injection, small functions)
- Use pytest coverage tools to identify gaps
- Add tests incrementally during development
**Decision**: Follow TDD rigorously, coverage should naturally reach ≥90%

---

## Definition of Done

**This feature is complete when**:

1. ✓ All 5 user stories from spec have passing tests
2. ✓ All 20 functional requirements (FR-001 to FR-020) are implemented
3. ✓ All 10 success criteria (SC-001 to SC-010) are verified
4. ✓ Test coverage ≥90% (pytest --cov report)
5. ✓ All tests pass (pytest exit code 0)
6. ✓ Application starts in <100ms (manual verification)
7. ✓ Operations respond in <50ms (manual verification with 100 tasks)
8. ✓ Manual testing confirms UX matches specification
9. ✓ README.md documents installation and usage
10. ✓ Code adheres to constitutional standards (max function length, naming, etc.)
11. ✓ No stack traces shown to users for any invalid input
12. ✓ Clean exit on Ctrl+C verified

**Acceptance Process**:
1. Run full test suite: `pytest tests/ --cov=src --cov-report=term-missing`
2. Verify coverage ≥90%
3. Manual testing of complete CRUD flow
4. Performance check with 100 tasks
5. UX review against spec requirements
6. Constitutional compliance review

---

## Next Steps

**Immediate**:
1. Run `/sp.tasks` to generate implementation tasks from this plan
2. Review and approve generated tasks
3. Begin Phase 1 (Model Layer) implementation

**After Implementation**:
1. Create ADR if significant decisions made during development
2. Update this plan if architecture changes
3. Create PHR documenting implementation completion

**Future Phases** (out of current scope):
- Phase II: Add file persistence
- Phase III: Add task priorities and tags
- Phase IV: Add search and filter capabilities

---

**Plan Status**: Ready for task generation
**Constitutional Compliance**: ✓ All principles satisfied
**Risk Level**: Low (well-understood problem, proven patterns)
**Estimated Implementation**: 5-8 tasks following TDD workflow
