"""
HR Agent

Agent responsible for managing employee information.
"""

from google.adk.agents.llm_agent import LlmAgent

mock_employee_db = [
    {
        "NVID": "CMD001",
        "username": "Nguyễn Văn An",
        "position": "Senior Developer",
        "leave_day": 12
    },
    {
        "NVID": "CMD002",
        "username": "Trần Thị Bích",
        "position": "HR Manager",
        "leave_day": 5
    },
    {
        "NVID": "CMD003",
        "username": "Lê Hoàng Nam",
        "position": "Solution Architect",
        "leave_day": 15
    },
    {
        "NVID": "CMD004",
        "username": "Phạm Minh Tâm",
        "position": "Tester",
        "leave_day": 8
    },
    {
        "NVID": "CMD005",
        "username": "Hoàng Thùy Linh",
        "position": "BrSE",
        "leave_day": 10
    },
    {
        "NVID": "CMD006",
        "username": "Trần Hữu Hiếu",
        "position": "Backend Developer",
        "leave_day": 7
    }
]

def get_employee_info(keyword: str) -> str:
    """
    Tra cứu thông tin nhân viên từ cơ sở dữ liệu dựa trên mã nhân viên.
    
    Args:
        keyword (str): Mã nhân viên cần tìm (ví dụ: "CMD001").
        
    Returns:
        str: Thông tin chi tiết của nhân viên nếu tìm thấy, hoặc thông báo không tìm thấy.
    """
    keyword = keyword.upper().strip()
    
    print(f"\n----------- HR AGENT DEBUG -----------")
    print(f"Searching for employee: {keyword}")
    print("--------------------------------------\n")
    
    for emp in mock_employee_db:
        if keyword == emp["NVID"]:
            result = {
                "found": True,
                "NVID": emp["NVID"],
                "username": emp["username"],
                "position": emp["position"],
                "leave_day": emp["leave_day"]
            }
            return f"""
Tìm thấy thông tin nhân viên:
- Mã NV: {emp['NVID']}
- Họ tên: {emp['username']}
- Chức vụ: {emp['position']}
- Số ngày phép còn lại: {emp['leave_day']} ngày
"""
    
    return f"Không tìm thấy nhân viên nào với mã '{keyword}' trong hệ thống."


root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='HR_Agent',
    description='Agent quản lý thông tin nhân sự - tra cứu thông tin nhân viên theo NVID',
    instruction="""
    Bạn là HR Agent - Trợ lý tra cứu thông tin nhân sự.
    
    HÀNH ĐỘNG BẮT BUỘC:
    Khi nhận được request có chứa NVID (mã nhân viên như CMD001, CMD006, etc.):
    → NGAY LẬP TỨC gọi tool get_employee_info với NVID đó
    → KHÔNG hỏi lại, KHÔNG giới thiệu bản thân
    → Chỉ trả về kết quả tra cứu
    
    VÍ DỤ:
    Request: "Tra cứu thông tin nhân viên CMD006"
    → Gọi: get_employee_info("CMD006")
    → Trả về kết quả
    
    Request: "Lấy thông tin nhân viên với NVID: CMD001"
    → Gọi: get_employee_info("CMD001")
    → Trả về kết quả
    
    KHÔNG ĐƯỢC:
    - Hỏi lại NVID khi đã có trong request
    - Tự giới thiệu thay vì thực hiện tra cứu
    - Trả lời mà không gọi tool
    """,
    tools=[get_employee_info],
    output_key="employee_info",
)
