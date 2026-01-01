"""
Todo Agent - Loop Agent Pattern

This agent manages task planning and execution using a Loop Agent pattern.
It plans tasks, executes them sequentially, and checks completion.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.task_planner import task_planner
from .subagents.task_executor import task_executor
from .subagents.task_checker import task_checker


# Create the Task Execution Loop
# This loop will:
# 1. Execute the current task (TaskExecutor)
# 2. Check if all tasks are complete (TaskChecker) - may call exit_loop
task_execution_loop = LoopAgent(
    name="TaskExecutionLoop",
    max_iterations=10,
    sub_agents=[
        task_executor,   # Execute current task
        task_checker,    # Check completion and decide next step
    ],
    description="Lặp qua từng task trong todo list, thực thi và kiểm tra hoàn thành",
)


# Create the Sequential Pipeline
# 1. First: Plan all tasks (TaskPlanner)
# 2. Then: Execute tasks in a loop (TaskExecutionLoop)
root_agent = SequentialAgent(
    name="TodoAgentPipeline",
    sub_agents=[
        task_planner,         # Step 1: Analyze request and create todo list
        task_execution_loop,  # Step 2: Execute tasks in loop until all done
    ],
    description="Agent phân tích yêu cầu, lên kế hoạch và thực thi từng task tuần tự",
)
