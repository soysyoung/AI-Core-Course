"""02 · AIMessage.tool_calls / ToolMessage · 기본필수 · 수강생 TODO.

DB: 기존 report_agent_lab / 반드시 SELECT. 실제 Tool은 --live에서 실행됩니다.
"""

def make_request(tool_name: str, args: dict, call_id: str) -> dict:
    """AIMessage.tool_calls의 항목 형태. 실제로 도구를 실행하지는 않습니다."""
    # TODO D29-02-B-01: AIMessage.tool_calls의 항목 형태. 실제로 도구를 실행하지는 않습니다.
    # 힌트: name, args, id가 요청값이고 tool_call_id가 결과의 연결 키입니다.
    # [쉬운 설명] 이 함수는 AI가 "이 도구 좀 써 줘!"라고 적어 내는 주문서를 만들어요.
    # [쉬운 설명] 식당 주문서처럼 "어떤 메뉴(name)", "옵션(args)", "주문 번호(id)" 세 가지를 적어요.
    # [쉬운 설명] 주문서만 쓰는 거라서 실제로 DB를 조회하지는 않아요. 요리는 다음 단계에서 해요.
    # [쉬운 설명] 도구 이름이 비어 있으면 어떤 도구를 써야 할지 모르니까 오류를 내요.
    if not isinstance(tool_name, str) or not tool_name.strip():
        raise ValueError('도구 이름(tool_name)이 비어 있습니다.')
    # [쉬운 설명] args는 {'report_id': 63}처럼 "이름: 값" 모양(dict)이어야 해요.
    if not isinstance(args, dict):
        raise ValueError('args는 dict여야 합니다.')
    # [쉬운 설명] 주문 번호(id)가 없으면 나중에 결과가 어느 주문의 것인지 짝을 맞출 수 없어요.
    if not isinstance(call_id, str) or not call_id.strip():
        raise ValueError('call_id가 비어 있습니다.')
    # [쉬운 설명] dict(args)로 복사해 두면, 바깥에서 원래 args를 바꿔도 주문서 내용은 그대로 남아요.
    return {'name': tool_name, 'args': dict(args), 'id': call_id}
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-02-B-01: 직접 구현하세요')

def match_result(call: dict, result: dict) -> dict:
    """실제로 DB Tool을 호출한 뒤 결과를 같은 tool_call_id에 묶습니다."""
    # TODO D29-02-B-02: 실제로 DB Tool을 호출한 뒤 결과를 같은 tool_call_id에 묶습니다.
    # 힌트: name, args, id가 요청값이고 tool_call_id가 결과의 연결 키입니다.
    # [쉬운 설명] 이 함수는 도구를 실제로 실행해서 나온 결과(result)를 주문서(call)와 짝지어 주는 영수증을 만들어요.
    # [쉬운 설명] 영수증에 주문 번호(tool_call_id)를 똑같이 적어야 AI가 "아, 이건 내 그 주문의 결과구나" 하고 알아봐요.
    # [쉬운 설명] 주문서에 번호가 없으면 짝을 맞출 수 없으니 오류를 내요.
    if not isinstance(call, dict) or not call.get('id'):
        raise ValueError('Tool Call ID(id)가 없습니다.')
    # [쉬운 설명] DB에서 받은 결과도 dict 모양이어야 해요. 아니면 뭔가 잘못된 거예요.
    if not isinstance(result, dict):
        raise ValueError('Tool 결과(result)는 dict여야 합니다.')
    # [쉬운 설명] 'type'은 "이건 도구 실행 결과 메시지예요"라는 이름표예요.
    # [쉬운 설명] 'tool_call_id'에는 주문서의 id를 그대로 옮겨 적어서 둘을 연결해요.
    # [쉬운 설명] 'name'은 어떤 도구가 만든 결과인지, 'content'는 DB가 돌려준 실제 내용이에요.
    return {
        'type': 'ToolMessage',
        'tool_call_id': call['id'],
        'name': call.get('name'),
        'content': result,
    }
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-02-B-02: 직접 구현하세요')

