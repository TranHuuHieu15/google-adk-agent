"""
Tools for Todo Agent

Provides utilities for task management and loop control.
"""

from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext


def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Call this function ONLY when ALL tasks in the todo list have been completed.
    This signals the iterative process should end.

    Args:
        tool_context: Context for tool execution

    Returns:
        Empty dictionary
    """
    print("\n=========== EXIT LOOP TRIGGERED ===========")
    print("All tasks completed successfully!")
    print("Loop will exit now")
    print("============================================\n")

    tool_context.actions.escalate = True
    return {"status": "completed", "message": "All tasks have been completed. Exiting loop."}


def update_task_status(
    task_id: str, 
    status: str, 
    result: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Update the status of a specific task in the todo list.

    Args:
        task_id: The ID of the task to update
        status: New status ('pending', 'in_progress', 'completed', 'failed')
        result: The result or output of the task
        tool_context: Context for accessing and updating session state

    Returns:
        Dict with update confirmation
    """
    print(f"\n----------- TASK UPDATE -----------")
    print(f"Task {task_id}: {status}")
    print(f"Result: {result[:100]}..." if len(result) > 100 else f"Result: {result}")
    print("-----------------------------------\n")

    # Update state
    if "task_results" not in tool_context.state:
        tool_context.state["task_results"] = {}
    
    tool_context.state["task_results"][task_id] = {
        "status": status,
        "result": result
    }
    
    return {
        "task_id": task_id,
        "status": status,
        "message": f"Task {task_id} updated to {status}"
    }


def get_current_task(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Get the next pending task from the todo list.

    Args:
        tool_context: Context for accessing session state

    Returns:
        Dict with current task info or completion status
    """
    todo_list = tool_context.state.get("todo_list", [])
    task_results = tool_context.state.get("task_results", {})
    
    for task in todo_list:
        task_id = task.get("task_id")
        if task_id not in task_results or task_results[task_id].get("status") != "completed":
            return {
                "has_pending": True,
                "current_task": task,
                "message": f"Next task: {task.get('task_title')}"
            }
    
    return {
        "has_pending": False,
        "current_task": None,
        "message": "All tasks completed!"
    }
