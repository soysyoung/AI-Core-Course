"""04 · 기존 RAG를 rag_search Tool로 · 기본필수 · 수강생 TODO.

DB: 기존 report_agent_lab / 반드시 SELECT. 실제 Tool은 --live에서 실행됩니다.
"""

def prepare_search(query: str, category: str = 'ALL') -> dict:
    """실제 6개 카테고리만 허용하고 query/category를 반환."""
    # TODO D29-04-B-01: 실제 6개 카테고리만 허용하고 query/category를 반환.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] 검색하기 전에 "질문"과 "분류(category)"가 올바른지 먼저 확인하는 함수예요.
    # [쉬운 설명] DB의 reports 표에 실제로 있는 분류 6가지예요. 'ALL'은 "전부에서 찾아 줘"라는 뜻이에요.
    allowed = ('ALL', 'EXPERIMENT', 'DAILY_WORK', 'RESEARCH_PLAN', 'DATA_PROCESSING', 'PROMPT', 'MEETING')
    # [쉬운 설명] 질문이 글자가 아니거나, 공백만 있으면 검색할 게 없으니 오류를 내요.
    if not isinstance(query, str) or not query.strip():
        raise ValueError('검색어(query)가 비어 있습니다.')
    # [쉬운 설명] 너무 긴 질문(500자 초과)도 막아요. 검색 도구가 받을 수 있는 길이에 한계가 있어요.
    if len(query.strip()) > 500:
        raise ValueError('검색어는 500자 이하여야 합니다.')
    # [쉬운 설명] 분류도 글자여야 해요. upper()는 소문자를 대문자로 바꿔서 'research_plan'도 받아 줘요.
    if not isinstance(category, str):
        raise ValueError('category는 문자열이어야 합니다.')
    category = category.strip().upper()
    # [쉬운 설명] 목록에 없는 분류(예: 'TASK')는 DB에 없으니 거절해요.
    if category not in allowed:
        raise ValueError(f'허용되지 않는 category입니다: {category}')
    # [쉬운 설명] 깨끗하게 정리한 질문과 분류를 dict로 돌려줘요. strip()은 앞뒤 공백을 지워 줘요.
    return {'query': query.strip(), 'category': category}
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-B-01: 직접 구현하세요')

def invoke_rag(request: dict) -> dict:
    """실제 기존 DB의 pgvector/CUDA RAG를 호출합니다. 가짜 검색 결과 금지."""
    # TODO D29-04-B-02: 실제 기존 DB의 pgvector/CUDA RAG를 호출합니다. 가짜 검색 결과 금지.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] 실제 RAG(문서 검색 + AI 답변)를 실행하는 함수예요. 가짜 답을 만들지 않고 진짜 시스템을 불러요.
    # [쉬운 설명] 요청이 dict가 아니면 질문을 꺼낼 수 없으니 오류를 내요.
    if not isinstance(request, dict):
        raise ValueError('request는 dict여야 합니다.')
    # [쉬운 설명] 혹시 prepare_search를 거치지 않은 요청이 와도 안전하도록 한 번 더 검사해요.
    checked = prepare_search(request.get('query', ''), request.get('category', 'ALL'))
    # [쉬운 설명] rag_answer는 11/20에 만든 실제 RAG예요. 순서는 이래요:
    # [쉬운 설명] 1) E5 모델(GPU)로 질문을 숫자 벡터로 바꾸고 2) pgvector로 비슷한 보고서를 DB에서 찾고
    # [쉬운 설명] 3) Reranker(GPU)로 순서를 다시 매기고 4) LLM이 찾은 보고서만 읽고 답을 써요.
    from coursekit.rag import rag_answer
    # [쉬운 설명] GPU가 없거나 DB에 벡터가 없으면 여기서 오류가 나요. 그건 "가짜 성공"을 막기 위한 정상 동작이에요.
    return rag_answer(checked['query'], checked['category'])
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-B-02: 직접 구현하세요')

