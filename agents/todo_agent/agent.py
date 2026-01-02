"""
Todo Agent - Mẫu Agent Vòng lặp (Loop Agent)

Agent này quản lý việc lập kế hoạch và thực thi công việc bằng mẫu Agent Vòng lặp.
Nó lập kế hoạch các task, thực thi chúng theo thứ tự và kiểm tra trạng thái hoàn thành.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.task_planner import task_planner
from .subagents.task_executor import task_executor
from .subagents.task_checker import task_checker


# Tạo vòng lặp thực thi task
# Vòng lặp này sẽ:
# 1. Thực thi task hiện tại (TaskExecutor)
# 2. Kiểm tra xem tất cả task đã hoàn thành chưa (TaskChecker) - có thể gọi exit_loop
task_execution_loop = LoopAgent(
    name="TaskExecutionLoop",
    max_iterations=10,
    sub_agents=[
        task_executor,   # Thực thi task hiện tại
        task_checker,    # Kiểm tra hoàn thành và quyết định bước tiếp theo
    ],
    description="Lặp qua từng task trong todo list, thực thi và kiểm tra hoàn thành",
)


# Tạo pipeline tuần tự
# 1. Đầu tiên: Lên kế hoạch tất cả task (TaskPlanner)
# 2. Sau đó: Thực thi các task theo vòng lặp (TaskExecutionLoop)
root_agent = SequentialAgent(
    name="TodoAgentPipeline",
    sub_agents=[
        task_planner,         # Bước 1: Phân tích yêu cầu và tạo todo list
        task_execution_loop,  # Bước 2: Thực thi task trong vòng lặp cho đến khi xong hết
    ],
    description="Agent phân tích yêu cầu, lên kế hoạch và thực thi từng task tuần tự",
)
