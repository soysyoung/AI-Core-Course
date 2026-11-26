"""용도별 추가 검증: Intermediate · Day29."""

def validate_message_pair(call: dict, message: dict) -> bool:
    """두 메시지에 같은 호출 ID·Tool 이름이 들어 있는지 확인."""
    # TODO D29-02-I-03: 두 메시지에 같은 호출 ID·Tool 이름이 들어 있는지 확인.
    # 힌트: name, args, id가 요청값이고 tool_call_id가 결과의 연결 키입니다.
    # [쉬운 설명] 주문서(call)와 영수증(message)이 정말 같은 주문의 짝인지 확인하는 함수예요.
    # [쉬운 설명] 둘 중 하나라도 dict 모양이 아니면 비교할 수 없으니 False예요.
    if not isinstance(call, dict) or not isinstance(message, dict):
        return False
    # [쉬운 설명] 주문 번호가 비어 있으면 "번호 없음 == 번호 없음"으로 잘못 맞다고 할 수 있어서 먼저 막아요.
    if not call.get('id'):
        return False
    # [쉬운 설명] 1) 주문서 id와 영수증 tool_call_id가 같은지
    same_id = call.get('id') == message.get('tool_call_id')
    # [쉬운 설명] 2) 주문한 도구 이름과 결과를 만든 도구 이름이 같은지
    same_name = call.get('name') == message.get('name')
    # [쉬운 설명] 두 가지가 모두 같아야 진짜 짝이에요.
    return same_id and same_name
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-02-I-03: 직접 구현하세요')

