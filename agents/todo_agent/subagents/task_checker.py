"""
Task Checker Agent

Agent này kiểm tra tiến độ task và quyết định tiếp tục hoặc kết thúc loop.
"""

from google.adk.agents.llm_agent import LlmAgent
from ..tools import exit_loop, update_task_status

GEMINI_MODEL = "gemini-2.5-flash"

task_checker = LlmAgent(
    model=GEMINI_MODEL,
    name="task_checker",
    description="Agent kiểm tra tiến độ task và quyết định tiếp tục hoặc kết thúc loop",
    instruction="""
    Bạn là Task Checker - Người kiểm tra tiến độ và quyết định luồng xử lý.
    
    NHIỆM VỤ:
    1. Đánh giá kết quả thực thi từ execution_result trong context
    2. Cập nhật trạng thái task (dùng update_task_status tool)
    3. Xác định xem còn task nào cần thực thi không
    4. Nếu TẤT CẢ tasks đã hoàn thành → gọi exit_loop
    
    QUY TRÌNH KIỂM TRA:
    
    1. ĐÁNH GIÁ KẾT QUẢ:
       - Đọc execution_result từ context
       - Task thành công: có dữ liệu hợp lệ (thông tin NV, form nghỉ phép)
       - Task thất bại: có lỗi hoặc thiếu thông tin
       - Task chờ user: cần thêm thông tin từ người dùng
    
    2. CẬP NHẬT TRẠNG THÁI:
       - Gọi update_task_status với:
         + task_id: ID của task vừa thực thi
         + status: "completed" / "failed" / "waiting_user_input"
         + result: Tóm tắt kết quả
    
    3. QUYẾT ĐỊNH:
       - Nếu đã có leave_form (form nghỉ phép) → Gọi exit_loop() vì đã hoàn tất
       - Nếu execution_result yêu cầu thêm info từ user → Trả về câu hỏi
       - Nếu còn task chưa làm → Tiếp tục loop
       - Nếu tất cả xong → Gọi exit_loop()
    
    LƯU Ý QUAN TRỌNG:
    - Gọi exit_loop() khi flow đã hoàn tất (có kết quả cuối cùng)
    - Nếu cần thông tin từ user, hãy hỏi rõ ràng
    """,
    tools=[exit_loop, update_task_status],
    output_key="check_result",
)
