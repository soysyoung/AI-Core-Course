"""01 · AI Agent vs 고정 RAG/Workflow · 응용 · 수강생 TODO.

DB: 기존 report_agent_lab / 반드시 SELECT. 실제 Tool은 --live에서 실행됩니다.
"""

def classify_request(question: str) -> str:
    """질문 성격을 'rag'·'db'·'agent' 중 선택. 규정+상태 복합은 agent. """
    # TODO D29-01-I-01: 질문 성격을 'rag'·'db'·'agent' 중 선택. 규정+상태 복합은 agent.
    # 힌트: Tool 선택 계획과 실제 Agent 판단은 다릅니다. 반환하는 strategy/tools 값을 확인하세요.
    # [쉬운 설명] 질문에 들어 있는 단어를 보고 "어디서 답을 찾아야 하는지" 고르는 함수예요.
    # [쉬운 설명] - 문서 내용을 찾아 읽어야 하면 → 'rag' (도서관에서 책을 찾아 읽기)
    # [쉬운 설명] - 보고서의 현재 상태만 물으면 → 'db' (출석부에서 표시 확인하기)
    # [쉬운 설명] - 둘 다 물으면 → 'agent' (여러 도구를 골라 차례로 써야 해요)
    # [쉬운 설명] 질문이 비어 있으면 무엇을 해야 할지 알 수 없으니 오류를 내요.
    if not isinstance(question, str) or not question.strip():
        raise ValueError('질문(question)이 비어 있습니다.')
    # [쉬운 설명] lower()로 영어를 모두 소문자로 바꿔요. 그러면 'RAG'와 'rag'를 같은 단어로 볼 수 있어요.
    text = question.lower()
    # [쉬운 설명] 문서 내용을 찾아야 한다는 신호 단어들이에요. (규정·근거·설명 등)
    rag_keywords = ['근거', '내용', '찾아', '설명', '규정', '문서', '관련', '검색', '요약', 'rag']
    # [쉬운 설명] DB에 저장된 "상태"를 묻는다는 신호 단어들이에요.
    db_keywords = ['상태', '인덱싱', 'index_status', 'ready', 'pending', 'failed']
    # [쉬운 설명] any(...)는 "목록 중 하나라도 질문 안에 있으면 True"라는 뜻이에요.
    needs_rag = any(word in text for word in rag_keywords)
    needs_db = any(word in text for word in db_keywords)
    # [쉬운 설명] 문서와 상태를 둘 다 알아야 하면 도구 두 개가 필요하니 'agent'예요.
    if needs_rag and needs_db:
        return 'agent'
    # [쉬운 설명] 상태만 물으면 DB 조회 하나로 충분해서 'db'예요.
    if needs_db:
        return 'db'
    # [쉬운 설명] 그 밖의 질문은 문서 내용을 찾는 질문으로 보고 'rag'를 돌려줘요.
    return 'rag'
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-01-I-01: 직접 구현하세요')

def plan_for_request(question: str) -> dict:
    """처리 전략과 사용할 Tool 목록을 반환. 조건문은 Agent 자체가 아닙니다."""
    # TODO D29-01-I-02: 처리 전략과 사용할 Tool 목록을 반환. 조건문은 Agent 자체가 아닙니다.
    # 힌트: Tool 선택 계획과 실제 Agent 판단은 다릅니다. 반환하는 strategy/tools 값을 확인하세요.
    # [쉬운 설명] 먼저 classify_request로 질문 종류(전략)를 정해요.
    strategy = classify_request(question)
    # [쉬운 설명] 전략마다 쓸 도구를 적어 둔 표예요.
    # [쉬운 설명] 'rag_search'는 문서 검색 도구, 'lookup_status'는 DB에서 보고서 상태를 조회하는 도구예요.
    # [쉬운 설명] 이 이름들은 coursekit/agent.py에 실제로 등록된 Tool 이름과 똑같이 맞췄어요.
    tools_by_strategy = {
        'rag': ['rag_search'],
        'db': ['lookup_status'],
        'agent': ['rag_search', 'lookup_status'],
    }
    # [쉬운 설명] 이건 "이 도구들을 쓸 계획이에요"라는 계획표일 뿐, 진짜 Agent가 아니에요.
    # [쉬운 설명] 진짜 Agent는 나중(Chapter 06)에 LLM이 스스로 어떤 도구를 부를지 판단해요.
    # [쉬운 설명] list(...)로 새 목록을 만들어 돌려줘서, 밖에서 목록을 바꿔도 위의 표는 안 바뀌어요.
    return {'strategy': strategy, 'tools': list(tools_by_strategy[strategy])}
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-01-I-02: 직접 구현하세요')


# 추가 구현: 같은 프로젝트의 별도 책임 모듈
from validation_01 import needs_two_sources
