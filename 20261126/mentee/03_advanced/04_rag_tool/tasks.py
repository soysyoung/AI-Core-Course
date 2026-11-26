"""04 · 기존 RAG를 rag_search Tool로 · 심화 · 수강생 TODO.

DB: 기존 report_agent_lab / 반드시 SELECT. 실제 Tool은 --live에서 실행됩니다.
"""

def prepare_search(query: str, category: str = 'ALL') -> dict:
    """실제 6개 카테고리만 허용하고 query/category를 반환."""
    # TODO D29-04-A-01: 실제 6개 카테고리만 허용하고 query/category를 반환.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] 검색 전에 질문과 분류를 엄격하게 검사하는 문지기 함수예요. (심화: 서버 정책까지 확인)
    # [쉬운 설명] DB의 reports 표에 실제로 있는 분류 6가지 + 'ALL'만 허용해요.
    allowed = ('ALL', 'EXPERIMENT', 'DAILY_WORK', 'RESEARCH_PLAN', 'DATA_PROCESSING', 'PROMPT', 'MEETING')
    if not isinstance(query, str) or not query.strip():
        raise ValueError('검색어(query)가 비어 있습니다.')
    # [쉬운 설명] 눈에 안 보이는 제어 문자(줄바꿈 제외)는 이상한 입력일 수 있어서 막아요.
    if any(ord(ch) < 32 and ch not in '\n\t' for ch in query):
        raise ValueError('검색어에 허용되지 않는 제어 문자가 있습니다.')
    # [쉬운 설명] 여러 칸 공백을 한 칸으로 정리해요.
    cleaned = ' '.join(query.split())
    if len(cleaned) > 500:
        raise ValueError('검색어는 500자 이하여야 합니다.')
    if category is None:
        category = 'ALL'
    if not isinstance(category, str):
        raise ValueError('category는 문자열이어야 합니다.')
    category = category.strip().upper()
    if category not in allowed:
        raise ValueError(f'허용되지 않는 category입니다: {category}')
    # [쉬운 설명] 심화: .env의 ALLOWED_CATEGORIES(서버 정책)에 없는 분류면 PermissionError로 막아요.
    # [쉬운 설명] 이건 "사람별 권한"이 아니라 "이 서버가 열어 둔 범위"예요. DB에 사용자 권한 표는 없어요.
    if category != 'ALL':
        from coursekit.settings import settings
        if category not in settings().allowed_categories:
            raise PermissionError(f'서버 정책상 허용되지 않은 category입니다: {category}')
    return {'query': cleaned, 'category': category}
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-A-01: 직접 구현하세요')

def invoke_rag(request: dict) -> dict:
    """실제 기존 DB의 pgvector/CUDA RAG를 호출합니다. 가짜 검색 결과 금지."""
    # TODO D29-04-A-02: 실제 기존 DB의 pgvector/CUDA RAG를 호출합니다. 가짜 검색 결과 금지.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] 실제 RAG(문서 검색 + AI 답변)를 실행하는 함수예요. 가짜 결과는 만들지 않아요.
    if not isinstance(request, dict):
        raise ValueError('request는 dict여야 합니다.')
    # [쉬운 설명] query·category 말고 다른 칸(task_id, owner_id 등)이 있으면 거절해요. (Fail Closed: 애매하면 막기)
    extra = set(request) - {'query', 'category'}
    if extra:
        raise ValueError(f'허용되지 않는 요청 항목: {sorted(extra)}')
    checked = prepare_search(request.get('query', ''), request.get('category', 'ALL'))
    # [쉬운 설명] 11/20의 실제 RAG: E5(GPU) 벡터 → pgvector 검색 → Reranker(GPU) → LLM 답변.
    from coursekit.rag import rag_answer
    result = rag_answer(checked['query'], checked['category'])
    # [쉬운 설명] 우리가 아는 상태값이 아니면 믿을 수 없는 결과이니 오류로 알려요.
    if not isinstance(result, dict) or result.get('status') not in ('answered', 'insufficient_context'):
        raise RuntimeError('RAG 결과 상태가 올바르지 않습니다.')
    return result
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-A-02: 직접 구현하세요')


# 추가 구현: 같은 프로젝트의 별도 책임 모듈
from policy_04 import format_evidence, validate_evidence
