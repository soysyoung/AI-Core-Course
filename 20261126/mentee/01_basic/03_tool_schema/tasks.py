"""03 · @tool·Pydantic·JSON Schema · 기본필수 · 수강생 TODO.

DB: 기존 report_agent_lab / 반드시 SELECT. 실제 Tool은 --live에서 실행됩니다.
"""

def validate_id(report_id: int) -> int:
    """실제 reports.report_id인 양의 정수만 허용합니다."""
    # TODO D29-03-B-01: 실제 reports.report_id인 양의 정수만 허용합니다.
    # 힌트: @tool 함수의 docstring, report_id:int, args_schema를 읽어보세요.
    # [쉬운 설명] 보고서 번호(report_id)가 "1 이상의 정수"인지 검사하는 문지기 함수예요.
    # [쉬운 설명] 파이썬에서는 True/False도 몰래 1/0 숫자처럼 취급돼요. 그래서 bool은 먼저 따로 막아요.
    if isinstance(report_id, bool) or not isinstance(report_id, int):
        raise ValueError('report_id는 정수여야 합니다.')
    # [쉬운 설명] 보고서 번호는 1번부터 시작해요. 0이나 -1 같은 번호는 있을 수 없어요.
    if report_id < 1:
        raise ValueError('report_id는 1 이상의 양의 정수여야 합니다.')
    # [쉬운 설명] 여기서는 "모양"만 검사해요. 그 번호의 보고서가 DB에 진짜 있는지는
    # [쉬운 설명] 다음 함수의 Tool이 실제 DB를 SELECT로 조회해서 알려줘요. (없으면 status가 'ok'가 아니에요)
    return report_id
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-03-B-01: 직접 구현하세요')

def register_status_tool():
    """@tool을 사용해 실제 DB 상태 조회 함수를 등록하고 반환합니다."""
    # TODO D29-03-B-02: @tool을 사용해 실제 DB 상태 조회 함수를 등록하고 반환합니다.
    # 힌트: @tool 함수의 docstring, report_id:int, args_schema를 읽어보세요.
    # [쉬운 설명] 평범한 파이썬 함수를 AI가 쓸 수 있는 "도구(Tool)"로 등록하는 함수예요.
    # [쉬운 설명] import를 함수 안에 둔 이유: --check처럼 DB 없이 실행할 때는 이 무거운 도구들을 불러오지 않아도 되거든요.
    import json
    from langchain.tools import tool
    from pydantic import BaseModel, Field, ConfigDict
    from coursekit.db import fetch_report_status

    # [쉬운 설명] StatusInput은 도구의 "입력 신청서 양식"이에요. (Pydantic 모델)
    # [쉬운 설명] AI는 이 양식(JSON Schema)을 보고 "report_id에 양의 정수를 넣어야 하는구나" 하고 배워요.
    class StatusInput(BaseModel):
        # [쉬운 설명] extra='forbid'는 양식에 없는 칸(task_id, owner_id 등)을 적으면 거절한다는 뜻이에요.
        model_config = ConfigDict(extra='forbid')
        # [쉬운 설명] gt=0은 "0보다 커야 한다(greater than 0)"는 규칙이에요. description은 AI가 읽는 설명이에요.
        report_id: int = Field(gt=0, description='기존 reports.report_id (task_id 아님)')

    # [쉬운 설명] @tool(...)을 함수 위에 붙이면 그 함수가 도구로 변신해요.
    # [쉬운 설명] 'lookup_status'는 도구 이름이고, args_schema=StatusInput은 위에서 만든 입력 양식을 쓰겠다는 뜻이에요.
    @tool('lookup_status', args_schema=StatusInput)
    def lookup_status(report_id: int) -> str:
        """기존 reports.report_id의 인덱싱 상태(index_status)·revision을 읽기 전용으로 조회합니다. 과제 제출 상태가 아닙니다."""
        # [쉬운 설명] 바로 위 큰따옴표 세 개 문장(docstring)은 AI가 읽는 "도구 사용 설명서"예요. 그래서 꼭 적어야 해요.
        # [쉬운 설명] 한 번 더 validate_id로 번호를 검사한 뒤, 실제 DB에서 SELECT로 상태를 읽어 와요.
        value = fetch_report_status(validate_id(report_id))
        # [쉬운 설명] 결과를 JSON 글자로 바꿔서 돌려줘요. ensure_ascii=False는 한글이 깨지지 않게 해 줘요.
        return json.dumps(value, ensure_ascii=False, default=str)

    # [쉬운 설명] 완성된 도구를 돌려줘요. main.py에서 .name, .args_schema, .invoke()로 사용해요.
    return lookup_status
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-03-B-02: 직접 구현하세요')

