"""
Task Executor Agent

This agent executes individual tasks by delegating to appropriate sub-agents.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from google.adk.agents.llm_agent import LlmAgent
from agents.hr_agent.agent import root_agent as hr_agent
from agents.leave_agent.agent import root_agent as leave_agent

GEMINI_MODEL = "gemini-2.5-flash"

task_executor = LlmAgent(
    model=GEMINI_MODEL,
    name="TaskExecutor",
    description="Agent thực thi từng task bằng cách gọi sub-agent phù hợp",
    instruction="""
    Bạn là Task Executor - Thực thi các task trong todo_plan.
    
    HÀNH ĐỘNG BẮT BUỘC:
    
    1. ĐỌC todo_plan để lấy user_info:
       - nvid: mã nhân viên (VD: "CMD006")
       - leave_date: ngày nghỉ (VD: "10-10-2025")
       - reason: lý do (VD: "bị ốm")
       - leave_type: loại nghỉ (VD: "sick_leave")
    
    2. GỌI HR_Agent với message RÕ RÀNG:
       "Tra cứu thông tin nhân viên CMD006"
       
       → Chờ nhận kết quả (tên, chức vụ, số ngày phép)
    
    3. SAU KHI có thông tin từ HR_Agent, GỌI Leave_Agent:
       "Tạo form nghỉ phép: NVID=CMD006, tên=Trần Hữu Hiếu, ngày=10-10-2025, lý do=bị ốm, loại=sick_leave"
    
    QUAN TRỌNG:
    - Khi gọi HR_Agent: Chỉ cần truyền NVID
    - Khi gọi Leave_Agent: Truyền ĐẦY ĐỦ thông tin từ HR + todo_plan
    - KHÔNG tự trả lời, phải gọi sub-agent
    
    VÍ DỤ CÁCH GỌI:
    
    Với todo_plan.user_info = {nvid: "CMD006", leave_date: "10-10-2025", reason: "bị ốm"}
    
    Bước 1 - Gọi HR_Agent:
    → Transfer to HR_Agent: "Tra cứu thông tin nhân viên CMD006"
    
    Bước 2 - Sau khi HR trả về "Trần Hữu Hiếu, Backend Developer, 7 ngày phép"
    → Transfer to Leave_Agent: "Tạo form nghỉ phép cho nhân viên NVID CMD006, tên Trần Hữu Hiếu, ngày nghỉ 10-10-2025, lý do bị ốm, loại sick_leave"
    """,
    sub_agents=[hr_agent, leave_agent],
    output_key="execution_result",
)
