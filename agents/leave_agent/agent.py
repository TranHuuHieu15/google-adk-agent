"""
Leave Agent

Agent responsible for creating leave request forms.
"""

from google.adk.agents.llm_agent import LlmAgent
from typing import Dict, Any
from google.adk.tools.tool_context import ToolContext


def create_leave_form(
    nvid: str,
    employee_name: str,
    leave_type: str,
    reason: str,
    start_date: str,
    end_date: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Tạo form xin nghỉ phép cho nhân viên.
    
    Args:
        nvid: Mã nhân viên
        employee_name: Tên nhân viên
        leave_type: Loại nghỉ phép (sick_leave, annual_leave, personal_leave)
        reason: Lý do xin nghỉ
        start_date: Ngày bắt đầu nghỉ
        end_date: Ngày kết thúc nghỉ
        tool_context: Context để lưu trạng thái
        
    Returns:
        Dict chứa thông tin form nghỉ phép
    """
    print(f"\n----------- LEAVE AGENT DEBUG -----------")
    print(f"Creating leave form for: {employee_name} ({nvid})")
    print(f"Type: {leave_type}, Dates: {start_date} - {end_date}")
    print("-----------------------------------------\n")
    
    # Map leave type to Vietnamese
    leave_type_vn = {
        "sick_leave": "Nghỉ ốm",
        "annual_leave": "Nghỉ phép năm",
        "personal_leave": "Nghỉ việc riêng"
    }.get(leave_type.lower(), leave_type)
    
    form = {
        "form_id": f"LEAVE-{nvid}-{start_date.replace('-', '')}",
        "employee_id": nvid,
        "employee_name": employee_name,
        "leave_type": leave_type_vn,
        "reason": reason,
        "start_date": start_date,
        "end_date": end_date,
        "status": "Pending Approval",
        "created_at": "2025-01-02"
    }
    
    # Save to context
    tool_context.state["leave_form"] = form
    
    return form


root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='Leave_Agent',
    description='Agent tạo form xin nghỉ phép cho nhân viên',
    instruction="""
    Bạn là Leave Agent - Tạo đơn xin nghỉ phép.
    
    HÀNH ĐỘNG BẮT BUỘC:
    Khi nhận được request tạo form nghỉ phép với thông tin (NVID, tên, ngày nghỉ, lý do):
    → NGAY LẬP TỨC gọi tool create_leave_form
    → KHÔNG hỏi lại thông tin
    → Trả về form đã tạo
    
    CÁCH GỌI TOOL:
    create_leave_form(
        nvid="CMD006",
        employee_name="Trần Hữu Hiếu",
        leave_type="sick_leave",  # sick_leave, annual_leave, personal_leave
        reason="bị ốm",
        start_date="10-10-2025",
        end_date="10-10-2025"
    )
    
    QUY TẮC XÁC ĐỊNH leave_type:
    - Lý do: ốm, bệnh, sức khỏe → "sick_leave"
    - Lý do: nghỉ phép, du lịch → "annual_leave"  
    - Lý do: việc riêng, gia đình → "personal_leave"
    
    VÍ DỤ:
    Request: "Tạo form nghỉ phép cho CMD006 - Trần Hữu Hiếu, ngày 10-10-2025, lý do bị ốm"
    → Gọi create_leave_form(nvid="CMD006", employee_name="Trần Hữu Hiếu", leave_type="sick_leave", reason="bị ốm", start_date="10-10-2025", end_date="10-10-2025")
    
    SAU KHI TẠO FORM, trả về markdown:
    
    ## 📋 ĐƠN XIN NGHỈ PHÉP
    | Thông tin | Chi tiết |
    |-----------|----------|
    | Mã đơn | [form_id] |
    | Mã NV | [nvid] |
    | Họ tên | [name] |
    | Loại nghỉ | [type] |
    | Lý do | [reason] |
    | Ngày nghỉ | [date] |
    | Trạng thái | Chờ duyệt |
    
    ✅ Đơn xin nghỉ phép đã được tạo thành công!
    """,
    tools=[create_leave_form],
    output_key="leave_form",
)
