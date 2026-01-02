"""
Công cụ cho Todo Agent

Cung cấp các tiện ích để quản lý tác vụ và điều khiển vòng lặp.
"""

from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext


def exit_loop(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Chỉ gọi hàm này khi TẤT CẢ các tác vụ trong danh sách todo đã được hoàn thành.
    Điều này báo hiệu rằng quá trình lặp nên kết thúc.

    Args:
        tool_context: Ngữ cảnh để thực thi công cụ

    Returns:
        Từ điển (dict) phản hồi trạng thái hoàn thành
    """

    tool_context.actions.escalate = True
    return {"status": "completed", "message": "Tất cả tác vụ đã hoàn thành. Thoát vòng lặp."}


def update_task_status(
    task_id: str,
    status: str,
    result: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Cập nhật trạng thái của một tác vụ cụ thể trong danh sách todo.

    Args:
        task_id: ID của tác vụ cần cập nhật
        status: Trạng thái mới ('pending', 'in_progress', 'completed', 'failed')
        result: Kết quả hoặc đầu ra của tác vụ
        tool_context: Ngữ cảnh để truy cập và cập nhật trạng thái phiên (session)

    Returns:
        Dict xác nhận việc cập nhật
    """

    # Cập nhật state
    if "task_results" not in tool_context.state:
        tool_context.state["task_results"] = {}

    tool_context.state["task_results"][task_id] = {
        "status": status,
        "result": result
    }

    return {
        "task_id": task_id,
        "status": status,
        "message": f"Tác vụ {task_id} đã được cập nhật sang trạng thái {status}"
    }


def get_current_task(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Lấy tác vụ đang chờ tiếp theo từ danh sách todo.

    Args:
        tool_context: Ngữ cảnh để truy cập trạng thái phiên (session)

    Returns:
        Dict chứa thông tin tác vụ hiện tại hoặc trạng thái hoàn thành
    """
    todo_list = tool_context.state.get("todo_list", [])
    task_results = tool_context.state.get("task_results", {})

    for task in todo_list:
        task_id = task.get("task_id")
        if task_id not in task_results or task_results[task_id].get("status") != "completed":
            return {
                "has_pending": True,
                "current_task": task,
                "message": f"Tác vụ tiếp theo: {task.get('task_title')}"
            }

    return {
        "has_pending": False,
        "current_task": None,
        "message": "Tất cả tác vụ đã hoàn thành!"
    }
