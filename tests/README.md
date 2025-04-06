
Run tests

```
uv pip install -e ".[dev]"
docker compose up
pytest -svvl tests/
...
================================================================================== short test summary info ===================================================================================
FAILED tests/test_flow_runs.py::test_get_flow_run_by_id[asyncio] - BaseExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
FAILED tests/test_flow_runs.py::test_get_flow_run_by_id[trio] - BaseExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
FAILED tests/test_flows.py::test_get_flow_run_by_id[asyncio] - BaseExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
FAILED tests/test_flows.py::test_get_flow_run_by_id[trio] - BaseExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
FAILED tests/test_workqueues.py::test_create_and_delete_work_queue[asyncio] - ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
FAILED tests/test_workqueues.py::test_create_and_delete_work_queue[trio] - ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
================================================================================ 6 failed, 28 passed in 3.33s ================================================================================
```