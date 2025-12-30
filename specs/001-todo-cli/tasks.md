---
description: "Implementation tasks for In-Memory Todo CLI Application"
---

# Tasks: In-Memory Todo CLI Application

**Input**: Design documents from `specs/001-todo-cli/`
**Prerequisites**: plan.md (completed), spec.md (completed)

**Tests**: Tests are REQUIRED per constitution. All tasks follow TDD workflow: Write tests → RED → Implement → GREEN → Refactor

**Organization**: Tasks are grouped by development phase following the plan's layered architecture approach. Each phase builds on the previous, with clear checkpoints for validation.

## Format: `[ID] [P?] [Phase] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Phase]**: Which development phase this task belongs to (Setup, Model, Service, Formatters, Menu, Integration, Polish)
- Include exact file paths in descriptions

## Path Conventions

Single project structure (per plan.md):
- Source: `src/` at repository root
- Tests: `tests/` at repository root
- Entry point: `main.py` at repository root

---

## Phase 1: Project Setup

**Purpose**: Initialize project structure and dependencies

**Goal**: Create foundational project files and directory structure per plan.md specifications

- [ ] T001 [P] [Setup] Create project directory structure: `src/models/`, `src/services/`, `src/cli/`, `tests/unit/`, `tests/integration/`
- [ ] T002 [P] [Setup] Create all `__init__.py` files in `src/`, `src/models/`, `src/services/`, `src/cli/`, `tests/`, `tests/unit/`, `tests/integration/`
- [ ] T003 [Setup] Create `pyproject.toml` with Python 3.13+ requirement and pytest dev dependency

**Checkpoint**: Directory structure matches plan.md, project can be initialized

---

## Phase 2: Model Layer - Task Entity

**Purpose**: Implement Task data model with tests (TDD: RED → GREEN → REFACTOR)

**Goal**: Create Task dataclass that serves as foundation for all operations

**User Stories Supported**: All (US1-US5) - Task is the core entity

**Independent Test**: Can instantiate Task objects and verify attributes

### Tests for Task Model (Write FIRST - must FAIL before implementation)

- [ ] T004 [P] [Model-Test] Write test for Task instantiation with all fields in `tests/unit/test_task.py`
- [ ] T005 [P] [Model-Test] Write test for Task instantiation with defaults (description="", completed=False) in `tests/unit/test_task.py`
- [ ] T006 [P] [Model-Test] Write test for Task field types (id:int, title:str, description:str, completed:bool) in `tests/unit/test_task.py`

### Implementation for Task Model

- [ ] T007 [Model-Impl] Run tests → verify RED (tests fail)
- [ ] T008 [Model-Impl] Create Task dataclass in `src/models/task.py` with attributes: id (int), title (str), description (str, default=""), completed (bool, default=False)
- [ ] T009 [Model-Impl] Add type hints and Google-style docstring to Task class in `src/models/task.py`
- [ ] T010 [Model-Impl] Run tests → verify GREEN (all tests pass)

**Checkpoint**: Task model complete, all tests passing, ready for service layer

---

## Phase 3: Service Layer - TaskManager

**Purpose**: Implement TaskManager business logic with comprehensive tests (TDD: RED → GREEN → REFACTOR)

**Goal**: Create TaskManager service that handles all CRUD operations, validation, and ID generation

**User Stories Supported**: All (US1-US5) - TaskManager is central business logic

**Independent Test**: Can instantiate TaskManager and perform operations without CLI

### Tests for TaskManager (Write FIRST - must FAIL before implementation)

**Initialization Tests**:
- [ ] T011 [P] [Service-Test] Write test: TaskManager starts with empty task list in `tests/unit/test_task_manager.py`
- [ ] T012 [P] [Service-Test] Write test: TaskManager starts with `_next_id = 1` in `tests/unit/test_task_manager.py`

**add_task() Tests**:
- [ ] T013 [P] [Service-Test] Write test: add task with title only (description defaults to "") in `tests/unit/test_task_manager.py`
- [ ] T014 [P] [Service-Test] Write test: add task with title and description in `tests/unit/test_task_manager.py`
- [ ] T015 [P] [Service-Test] Write test: auto-increment ID (add 3 tasks, verify IDs 1, 2, 3) in `tests/unit/test_task_manager.py`
- [ ] T016 [P] [Service-Test] Write test: reject empty title (ValueError) in `tests/unit/test_task_manager.py`
- [ ] T017 [P] [Service-Test] Write test: reject whitespace-only title (ValueError) in `tests/unit/test_task_manager.py`
- [ ] T018 [P] [Service-Test] Write test: reject title >200 chars (ValueError) in `tests/unit/test_task_manager.py`
- [ ] T019 [P] [Service-Test] Write test: reject description >500 chars (ValueError) in `tests/unit/test_task_manager.py`

**get_task() Tests**:
- [ ] T020 [P] [Service-Test] Write test: get existing task returns correct Task in `tests/unit/test_task_manager.py`
- [ ] T021 [P] [Service-Test] Write test: get non-existent task returns None in `tests/unit/test_task_manager.py`

**get_all_tasks() Tests**:
- [ ] T022 [P] [Service-Test] Write test: get all tasks when empty returns [] in `tests/unit/test_task_manager.py`
- [ ] T023 [P] [Service-Test] Write test: get all tasks returns sorted by ID in `tests/unit/test_task_manager.py`
- [ ] T024 [P] [Service-Test] Write test: get all tasks after deletion preserves remaining tasks in `tests/unit/test_task_manager.py`

**update_task() Tests**:
- [ ] T025 [P] [Service-Test] Write test: update title only (description unchanged) in `tests/unit/test_task_manager.py`
- [ ] T026 [P] [Service-Test] Write test: update description only (title unchanged) in `tests/unit/test_task_manager.py`
- [ ] T027 [P] [Service-Test] Write test: update both title and description in `tests/unit/test_task_manager.py`
- [ ] T028 [P] [Service-Test] Write test: update non-existent task raises ValueError in `tests/unit/test_task_manager.py`
- [ ] T029 [P] [Service-Test] Write test: update with empty title raises ValueError in `tests/unit/test_task_manager.py`
- [ ] T030 [P] [Service-Test] Write test: update with title >200 chars raises ValueError in `tests/unit/test_task_manager.py`
- [ ] T031 [P] [Service-Test] Write test: update with description >500 chars raises ValueError in `tests/unit/test_task_manager.py`
- [ ] T032 [P] [Service-Test] Write test: ID remains unchanged after update in `tests/unit/test_task_manager.py`

**delete_task() Tests**:
- [ ] T033 [P] [Service-Test] Write test: delete existing task removes it in `tests/unit/test_task_manager.py`
- [ ] T034 [P] [Service-Test] Write test: delete non-existent task raises ValueError in `tests/unit/test_task_manager.py`
- [ ] T035 [P] [Service-Test] Write test: subsequent adds continue auto-increment (no ID reuse) in `tests/unit/test_task_manager.py`

**toggle_task() Tests**:
- [ ] T036 [P] [Service-Test] Write test: toggle pending → completed in `tests/unit/test_task_manager.py`
- [ ] T037 [P] [Service-Test] Write test: toggle completed → pending in `tests/unit/test_task_manager.py`
- [ ] T038 [P] [Service-Test] Write test: toggle non-existent task raises ValueError in `tests/unit/test_task_manager.py`

**task_count() Tests**:
- [ ] T039 [P] [Service-Test] Write test: count after various operations in `tests/unit/test_task_manager.py`

### Implementation for TaskManager (RED → GREEN → REFACTOR)

- [ ] T040 [Service-Impl] Run tests → verify RED (all 29 tests fail)
- [ ] T041 [Service-Impl] Create TaskManager class skeleton with `__init__`, `_tasks: dict[int, Task]`, `_next_id: int` in `src/services/task_manager.py`
- [ ] T042 [Service-Impl] Implement `add_task(title: str, description: str = "") -> Task` with validation in `src/services/task_manager.py`
- [ ] T043 [Service-Impl] Implement `get_task(task_id: int) -> Task | None` in `src/services/task_manager.py`
- [ ] T044 [Service-Impl] Implement `get_all_tasks() -> list[Task]` with sorting in `src/services/task_manager.py`
- [ ] T045 [Service-Impl] Implement `update_task(task_id: int, title: str | None, description: str | None) -> Task` with validation in `src/services/task_manager.py`
- [ ] T046 [Service-Impl] Implement `delete_task(task_id: int) -> None` with error handling in `src/services/task_manager.py`
- [ ] T047 [Service-Impl] Implement `toggle_task(task_id: int) -> Task` with error handling in `src/services/task_manager.py`
- [ ] T048 [Service-Impl] Implement `task_count() -> int` in `src/services/task_manager.py`
- [ ] T049 [Service-Impl] Add type hints and Google-style docstrings to all TaskManager methods in `src/services/task_manager.py`
- [ ] T050 [Service-Impl] Run tests → verify GREEN (all 29 tests pass)
- [ ] T051 [Service-Refactor] Refactor TaskManager for code quality: max 20 lines per method, DRY validation logic

**Checkpoint**: TaskManager complete with 100% test coverage, all tests passing

---

## Phase 4: CLI Layer - Formatters

**Purpose**: Implement output formatting utilities with tests (TDD: RED → GREEN → REFACTOR)

**Goal**: Create pure formatting functions for task display and messages

**User Stories Supported**: All (US1-US5) - Formatters handle all output presentation

**Independent Test**: Can call formatting functions with Task objects and verify string output

### Tests for Formatters (Write FIRST - must FAIL before implementation)

- [ ] T052 [P] [Formatter-Test] Write test: format_task_list with empty list returns empty state message in `tests/unit/test_formatters.py`
- [ ] T053 [P] [Formatter-Test] Write test: format_task_list with one task formats correctly in `tests/unit/test_formatters.py`
- [ ] T054 [P] [Formatter-Test] Write test: format_task_list with multiple tasks shows table in `tests/unit/test_formatters.py`
- [ ] T055 [P] [Formatter-Test] Write test: format_task_list shows [✓] for completed, [ ] for pending in `tests/unit/test_formatters.py`
- [ ] T056 [P] [Formatter-Test] Write test: format_task_list truncates long descriptions with "..." in `tests/unit/test_formatters.py`
- [ ] T057 [P] [Formatter-Test] Write test: format_empty_state returns expected message in `tests/unit/test_formatters.py`
- [ ] T058 [P] [Formatter-Test] Write test: format_success adds ✓ prefix in `tests/unit/test_formatters.py`
- [ ] T059 [P] [Formatter-Test] Write test: format_error adds ✗ Error: prefix in `tests/unit/test_formatters.py`
- [ ] T060 [P] [Formatter-Test] Write test: format_task_detail shows full task information in `tests/unit/test_formatters.py`

### Implementation for Formatters (RED → GREEN → REFACTOR)

- [ ] T061 [Formatter-Impl] Run tests → verify RED (all 9 tests fail)
- [ ] T062 [Formatter-Impl] Implement `format_task_list(tasks: list[Task]) -> str` with table formatting in `src/cli/formatters.py`
- [ ] T063 [Formatter-Impl] Implement `format_empty_state() -> str` in `src/cli/formatters.py`
- [ ] T064 [Formatter-Impl] Implement `format_success(message: str) -> str` in `src/cli/formatters.py`
- [ ] T065 [Formatter-Impl] Implement `format_error(message: str) -> str` in `src/cli/formatters.py`
- [ ] T066 [Formatter-Impl] Implement `format_task_detail(task: Task) -> str` in `src/cli/formatters.py`
- [ ] T067 [Formatter-Impl] Add type hints and Google-style docstrings to all formatter functions in `src/cli/formatters.py`
- [ ] T068 [Formatter-Impl] Run tests → verify GREEN (all 9 tests pass)
- [ ] T069 [Formatter-Refactor] Refactor formatters for code quality: consistent spacing, alignment, max 20 lines per function

**Checkpoint**: Formatters complete with 100% test coverage, all tests passing

---

## Phase 5: CLI Layer - MenuHandler

**Purpose**: Implement menu system and user interaction with integration tests

**Goal**: Create MenuHandler that orchestrates user input, delegates to TaskManager, and displays formatted output

**User Stories Supported**: All (US1-US5) - MenuHandler implements complete user interface

**Independent Test**: Can mock TaskManager and stdin/stdout to verify menu behavior

### Tests for MenuHandler (Write FIRST - must FAIL before implementation)

**Integration Tests** (End-to-End Flows):
- [ ] T070 [P] [Menu-Test] Write test: add task flow (menu choice 1 → title → description → success) in `tests/integration/test_cli_flow.py`
- [ ] T071 [P] [Menu-Test] Write test: view tasks when empty shows empty state in `tests/integration/test_cli_flow.py`
- [ ] T072 [P] [Menu-Test] Write test: view tasks after adding shows formatted list in `tests/integration/test_cli_flow.py`
- [ ] T073 [P] [Menu-Test] Write test: update task flow (menu choice 3 → ID → new title → success) in `tests/integration/test_cli_flow.py`
- [ ] T074 [P] [Menu-Test] Write test: delete task with confirmation (menu choice 4 → ID → y → success) in `tests/integration/test_cli_flow.py`
- [ ] T075 [P] [Menu-Test] Write test: delete task cancellation (menu choice 4 → ID → n → cancel) in `tests/integration/test_cli_flow.py`
- [ ] T076 [P] [Menu-Test] Write test: toggle task flow (menu choice 5 → ID → success) in `tests/integration/test_cli_flow.py`
- [ ] T077 [P] [Menu-Test] Write test: invalid menu choice shows error and redisplays menu in `tests/integration/test_cli_flow.py`
- [ ] T078 [P] [Menu-Test] Write test: invalid task ID shows error in `tests/integration/test_cli_flow.py`
- [ ] T079 [P] [Menu-Test] Write test: exit cleanly (menu choice 6 → goodbye) in `tests/integration/test_cli_flow.py`

### Implementation for MenuHandler (RED → GREEN → REFACTOR)

- [ ] T080 [Menu-Impl] Run tests → verify RED (all 10 integration tests fail)
- [ ] T081 [Menu-Impl] Create MenuHandler class skeleton with `__init__(task_manager: TaskManager)` in `src/cli/menu.py`
- [ ] T082 [Menu-Impl] Implement `display_menu() -> None` with formatted menu options in `src/cli/menu.py`
- [ ] T083 [Menu-Impl] Implement `_get_input(prompt: str) -> str` helper in `src/cli/menu.py`
- [ ] T084 [Menu-Impl] Implement `_get_int_input(prompt: str) -> int | None` with validation in `src/cli/menu.py`
- [ ] T085 [Menu-Impl] Implement `_confirm(message: str) -> bool` for confirmations in `src/cli/menu.py`
- [ ] T086 [Menu-Impl] Implement `handle_add_task() -> None` with input prompts and TaskManager delegation in `src/cli/menu.py`
- [ ] T087 [Menu-Impl] Implement `handle_view_tasks() -> None` with TaskManager fetch and formatter display in `src/cli/menu.py`
- [ ] T088 [Menu-Impl] Implement `handle_update_task() -> None` with ID prompt, field updates, TaskManager delegation in `src/cli/menu.py`
- [ ] T089 [Menu-Impl] Implement `handle_delete_task() -> None` with ID prompt, confirmation, TaskManager delegation in `src/cli/menu.py`
- [ ] T090 [Menu-Impl] Implement `handle_toggle_task() -> None` with ID prompt, TaskManager delegation in `src/cli/menu.py`
- [ ] T091 [Menu-Impl] Implement `run() -> None` main loop with menu display, input handling, operation routing, KeyboardInterrupt handling in `src/cli/menu.py`
- [ ] T092 [Menu-Impl] Add error handling: catch ValueError from TaskManager, display with format_error() in `src/cli/menu.py`
- [ ] T093 [Menu-Impl] Add type hints and Google-style docstrings to all MenuHandler methods in `src/cli/menu.py`
- [ ] T094 [Menu-Impl] Run tests → verify GREEN (all 10 integration tests pass)
- [ ] T095 [Menu-Refactor] Refactor MenuHandler for code quality: max 20 lines per method, DRY error handling

**Checkpoint**: MenuHandler complete, all integration tests passing, end-to-end flows verified

---

## Phase 6: Application Integration

**Purpose**: Wire up application entry point and enable end-to-end execution

**Goal**: Create main.py entry point that initializes components and starts application

**User Stories Supported**: All (US1-US5) - Entry point enables complete application

**Independent Test**: Can launch application and perform all operations manually

### Implementation for Application Entry

- [ ] T096 [Integration] Create `main() -> None` function in `src/main.py` that initializes TaskManager and MenuHandler
- [ ] T097 [Integration] Add top-level exception handling in `main()` for graceful error reporting in `src/main.py`
- [ ] T098 [Integration] Add type hints and Google-style docstring to `main()` in `src/main.py`
- [ ] T099 [Integration] Create entry point `main.py` at repository root that imports and calls `src.main.main()`
- [ ] T100 [Integration] Add shebang `#!/usr/bin/env python3` to root `main.py` for Unix compatibility

**Checkpoint**: Application can be launched with `python main.py`, all user flows executable

---

## Phase 7: UX Polish & Documentation

**Purpose**: Refine user experience and document usage

**Goal**: Ensure product-quality CLI experience matching specification UX standards

**User Stories Supported**: All (US1-US5) - Polish affects entire user experience

### UX Refinement

- [ ] T101 [Polish] Add ASCII headers to menu display (========== separators) in `src/cli/menu.py`
- [ ] T102 [Polish] Add application title "TODO CLI APPLICATION" to menu header in `src/cli/menu.py`
- [ ] T103 [Polish] Verify table alignment in formatters: columns for ID, Status, Title, Description in `src/cli/formatters.py`
- [ ] T104 [Polish] Add "Press Enter to continue..." prompts after operations in `src/cli/menu.py`
- [ ] T105 [Polish] Verify success messages use ✓ prefix consistently in all operations
- [ ] T106 [Polish] Verify error messages use ✗ Error: prefix consistently in all operations
- [ ] T107 [Polish] Add "Total: X tasks (Y completed, Z pending)" footer to task list display in `src/cli/formatters.py`
- [ ] T108 [Polish] Test UTF-8 characters (✓, ✗, [ ], [✓]) display correctly on Windows/Linux/macOS

### Documentation

- [ ] T109 [P] [Polish] Create `README.md` at repository root with installation instructions (Python 3.13+ requirement)
- [ ] T110 [P] [Polish] Add usage examples to `README.md`: how to run, available commands
- [ ] T111 [P] [Polish] Add module-level docstrings to all files: `src/models/task.py`, `src/services/task_manager.py`, `src/cli/formatters.py`, `src/cli/menu.py`, `src/main.py`
- [ ] T112 [P] [Polish] Document UTF-8 terminal requirement in `README.md`

**Checkpoint**: UX matches spec standards, application is documented and ready for use

---

## Phase 8: Quality Assurance & Verification

**Purpose**: Verify all requirements, success criteria, and constitutional compliance

**Goal**: Confirm application meets all specifications before completion

**User Stories Supported**: All (US1-US5) - Final verification of complete feature

### Test Coverage & Quality

- [ ] T113 [QA] Run full test suite: `pytest tests/ -v` and verify all tests pass
- [ ] T114 [QA] Run coverage report: `pytest tests/ --cov=src --cov-report=term-missing` and verify ≥90% coverage
- [ ] T115 [QA] Review coverage report and add tests for any uncovered code paths
- [ ] T116 [QA] Verify test organization mirrors source structure (tests/unit/, tests/integration/)

### Manual Verification (Against Spec Success Criteria)

- [ ] T117 [QA] **SC-001**: Manually test complete CRUD lifecycle (add, view, update, delete, toggle) via numbered menu
- [ ] T118 [QA] **SC-002**: Measure startup time with `time python main.py` (target: <100ms)
- [ ] T119 [QA] **SC-003**: Test operation response time with 100 tasks (target: <50ms per operation)
- [ ] T120 [QA] **SC-004**: Test invalid inputs (empty title, invalid ID, non-numeric menu choice) - verify no crashes or stack traces
- [ ] T121 [QA] **SC-005**: Verify all invalid inputs produce clear, actionable error messages with ✗ prefix
- [ ] T122 [QA] **SC-006**: Verify [✓] and [ ] indicators clearly distinguish completed vs pending tasks
- [ ] T123 [QA] **SC-007**: Verify main menu returns after every operation without extra user input
- [ ] T124 [QA] **SC-008**: Test with 100+ tasks, verify no performance degradation
- [ ] T125 [QA] **SC-009**: Test exit via menu option 6 and Ctrl+C, verify clean shutdown
- [ ] T126 [QA] **SC-010**: Verify menu is self-evident (numbered options, clear prompts, no external docs needed)

### Functional Requirements Verification

- [ ] T127 [QA] **FR-001 to FR-020**: Manually verify all 20 functional requirements from spec.md are implemented
- [ ] T128 [QA] Verify task IDs auto-increment starting from 1 and are never reused after deletion
- [ ] T129 [QA] Verify title validation: reject empty, accept 1-200 chars
- [ ] T130 [QA] Verify description validation: accept 0-500 chars
- [ ] T131 [QA] Verify confirmation prompt appears before delete operation

### Constitutional Compliance

- [ ] T132 [QA] Verify max function length ≤20 lines (excluding docstrings) across all files
- [ ] T133 [QA] Verify max class length ≤200 lines across all files
- [ ] T134 [QA] Verify max line length ≤100 characters across all files
- [ ] T135 [QA] Verify all public functions have Google-style docstrings
- [ ] T136 [QA] Verify all public functions have type hints
- [ ] T137 [QA] Verify naming conventions: PascalCase classes, snake_case functions/variables
- [ ] T138 [QA] Verify no third-party dependencies in source (except pytest for testing)
- [ ] T139 [QA] Verify clean architecture: no UI logic in service layer, no business logic in UI layer

**Checkpoint**: All requirements verified, application ready for delivery

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Model)**: Depends on Phase 1 (directory structure)
- **Phase 3 (Service)**: Depends on Phase 2 (Task model)
- **Phase 4 (Formatters)**: Depends on Phase 2 (Task model) - can run parallel with Phase 3
- **Phase 5 (Menu)**: Depends on Phase 3 (TaskManager) and Phase 4 (Formatters)
- **Phase 6 (Integration)**: Depends on Phase 5 (MenuHandler)
- **Phase 7 (Polish)**: Depends on Phase 6 (working application)
- **Phase 8 (QA)**: Depends on Phase 7 (polished application)

### TDD Workflow (Phases 2-5)

**Critical**: Tests MUST be written FIRST and FAIL before implementation

1. Write all tests for the phase (marked with `-Test` suffix)
2. Run tests → verify RED (all fail)
3. Implement code (marked with `-Impl` suffix)
4. Run tests → verify GREEN (all pass)
5. Refactor (marked with `-Refactor` suffix)
6. Run tests → verify still GREEN

### Parallel Opportunities

**Phase 1**: All 3 setup tasks marked [P] can run in parallel

**Phase 2**: All 3 model tests marked [P] can be written in parallel

**Phase 3**: All service tests (T011-T039) marked [P] can be written in parallel within their test categories

**Phase 4**: All formatter tests (T052-T060) marked [P] can be written in parallel

**Phase 5**: All menu integration tests (T070-T079) marked [P] can be written in parallel

**Phase 7**: Documentation tasks (T109-T112) marked [P] can run in parallel

**Phase 8**: Manual verification tasks can be divided among team members

### Within Each Phase

- Tests before implementation (RED before GREEN)
- Implementation in logical order (initialization → methods)
- Refactoring after GREEN
- Never move to next phase until checkpoint verified

---

## Implementation Strategy

### Test-First Approach (Constitutional Requirement)

**For Every Phase with Tests**:
1. Write ALL tests for the phase
2. Run tests → Must see RED (failures)
3. Implement code to pass tests
4. Run tests → Must see GREEN (success)
5. Refactor for quality
6. Run tests → Must stay GREEN
7. Verify checkpoint before proceeding

### Incremental Validation

**After Each Phase**:
- Phase 2: Task model complete → can create Task objects
- Phase 3: TaskManager complete → can perform CRUD operations programmatically
- Phase 4: Formatters complete → can format task output
- Phase 5: MenuHandler complete → can interact via CLI
- Phase 6: Integration complete → full application works
- Phase 7: Polish complete → professional UX
- Phase 8: QA complete → all requirements verified

### Development Order Rationale

1. **Setup first**: Foundation for all code
2. **Model second**: Data structure needed by everything
3. **Service third**: Business logic depends on model
4. **Formatters fourth**: Output utilities (parallel-safe with service)
5. **Menu fifth**: UI layer ties everything together
6. **Integration sixth**: Wire up entry point
7. **Polish seventh**: Refine UX after functionality works
8. **QA eighth**: Comprehensive verification at the end

---

## Notes

- **[P]** = Parallel-safe (different files, no dependencies)
- **Phase Labels**: Setup, Model-Test, Model-Impl, Service-Test, Service-Impl, Formatter-Test, Formatter-Impl, Menu-Test, Menu-Impl, Integration, Polish, QA
- **TDD Workflow**: Mandatory for Phases 2-5 (Model, Service, Formatters, Menu)
- **Checkpoints**: Validate phase completion before proceeding
- **Test Count**: 51 test tasks (3 model + 29 service + 9 formatter + 10 integration)
- **Implementation Count**: 88 implementation/verification tasks
- **Total Tasks**: 139 tasks organized in 8 phases
- **Commit Strategy**: Commit after each phase checkpoint
- **Coverage Target**: ≥90% (verified in Phase 8)
- **Constitutional Compliance**: Verified in Phase 8 QA tasks

---

## Task Summary by Phase

| Phase | Test Tasks | Implementation Tasks | Total |
|-------|-----------|---------------------|-------|
| 1. Setup | 0 | 3 | 3 |
| 2. Model | 3 | 7 | 10 |
| 3. Service | 29 | 12 | 41 |
| 4. Formatters | 9 | 9 | 18 |
| 5. Menu | 10 | 16 | 26 |
| 6. Integration | 0 | 5 | 5 |
| 7. Polish | 0 | 12 | 12 |
| 8. QA | 0 | 24 | 24 |
| **Total** | **51** | **88** | **139** |

**Estimated Completion**: Following TDD workflow, expect 2-3 tasks per hour = 40-70 hours for complete implementation and verification

---
