"""용도별 추가 검증: Intermediate · Day29."""

def needs_two_sources(plan: dict) -> bool:
    """문서 검색 Tool과 DB Tool이 모두 필요한 계획인지 확인."""
    # TODO D29-01-I-03: 문서 검색 Tool과 DB Tool이 모두 필요한 계획인지 확인.
    # 힌트: Tool 선택 계획과 실제 Agent 판단은 다릅니다. 반환하는 strategy/tools 값을 확인하세요.
    # [쉬운 설명] 계획표(plan)에 "문서 검색 도구"와 "DB 상태 도구"가 둘 다 들어 있는지 확인하는 함수예요.
    # [쉬운 설명] 계획표 모양이 이상하면(dict가 아니면) 두 도구가 있을 수 없으니 False예요.
    if not isinstance(plan, dict):
        return False
    # [쉬운 설명] get('tools', [])는 'tools'가 없으면 빈 목록을 쓰라는 뜻이에요. 그래서 오류 없이 넘어가요.
    tools = plan.get('tools', [])
    # [쉬운 설명] 두 도구 이름이 모두 목록 안에 있어야 True예요. (and는 "둘 다"라는 뜻)
    return 'rag_search' in tools and 'lookup_status' in tools
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-01-I-03: 직접 구현하세요')

