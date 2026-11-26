"""01 · AI Agent vs 고정 RAG/Workflow · 기본필수 · 수강생 TODO.

DB: 기존 report_agent_lab / 반드시 SELECT. 실제 Tool은 --live에서 실행됩니다.
"""

def classify_request(question: str) -> str:
    """질문 성격을 'rag'·'db'·'agent' 중 선택. 규정+상태 복합은 agent. """
    # TODO D29-01-B-01: 질문 성격을 'rag'·'db'·'agent' 중 선택. 규정+상태 복합은 agent.
    # 힌트: Tool 선택 계획과 실제 Agent 판단은 다릅니다. 반환하는 strategy/tools 값을 확인하세요.
    # [쉬운 설명] 질문에 어떤 단어가 들어 있는지 보고 "어디서 답을 찾아야 하는지" 고르는 함수예요.
    # [쉬운 설명] - 문서 내용을 찾아 읽어야 하는 질문 → 'rag' (도서관에서 책을 찾아 읽는 것과 비슷해요)
    # [쉬운 설명] - 보고서의 현재 상태(인덱싱 상태 등)만 묻는 질문 → 'db' (학교 출석부에서 내 이름 옆 표시를 확인하는 것과 비슷해요)
    # [쉬운 설명] - 두 가지를 모두 물어보면 → 'agent' (여러 도구를 골라 차례로 써야 하니까요)
    # [쉬운 설명] 문서 내용을 찾아야 한다는 신호가 되는 단어들이에요.
    rag_keywords = ['근거', '내용', '찾아', '설명', '규정', '문서', '관련', '검색', 'rag', 'RAG']
    # [쉬운 설명] DB에 저장된 "상태"를 물어본다는 신호가 되는 단어들이에요.
    db_keywords = ['상태', '인덱싱', 'index_status', 'ready']
    # [쉬운 설명] any(...)는 "목록 중 하나라도 질문 안에 있으면 True"라는 뜻이에요.
    needs_rag = any(word in question for word in rag_keywords)
    needs_db = any(word in question for word in db_keywords)
    # [쉬운 설명] 문서도 찾고 상태도 확인해야 하면 두 도구를 함께 써야 하므로 'agent'를 골라요.
    if needs_rag and needs_db:
        return 'agent'
    # [쉬운 설명] 상태만 물어보면 DB만 조회하면 되니까 'db'예요.
    if needs_db:
        return 'db'
    # [쉬운 설명] 나머지는 문서 내용을 찾는 질문으로 보고 'rag'를 돌려줘요.
    return 'rag'
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-01-B-01: 직접 구현하세요')

def plan_for_request(question: str) -> dict:
    """처리 전략과 사용할 Tool 목록을 반환. 조건문은 Agent 자체가 아닙니다."""
    # TODO D29-01-B-02: 처리 전략과 사용할 Tool 목록을 반환. 조건문은 Agent 자체가 아닙니다.
    # 힌트: Tool 선택 계획과 실제 Agent 판단은 다릅니다. 반환하는 strategy/tools 값을 확인하세요.
    # [쉬운 설명] 위에서 만든 classify_request로 질문 종류(전략)를 먼저 정해요.
    strategy = classify_request(question)
    # [쉬운 설명] 전략마다 "어떤 도구를 쓸지" 적어 둔 표예요.
    # [쉬운 설명] 'rag_search'는 문서를 검색하는 도구, 'lookup_status'는 DB에서 보고서 상태를 조회하는 도구예요.
    # [쉬운 설명] 이 이름들은 coursekit/agent.py에 실제로 등록된 Tool 이름과 똑같이 맞췄어요.
    tools_by_strategy = {
        'rag': ['rag_search'],
        'db': ['lookup_status'],
        'agent': ['rag_search', 'lookup_status'],
    }
    # [쉬운 설명] 이건 "이런 도구를 쓸 계획이에요"라는 계획표일 뿐이에요.
    # [쉬운 설명] 진짜 Agent는 나중(Chapter 06)에 LLM이 직접 보고 어떤 도구를 부를지 스스로 판단해요.
    return {'strategy': strategy, 'tools': tools_by_strategy[strategy]}
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-01-B-02: 직접 구현하세요')

