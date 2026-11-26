"""04 · 기존 RAG를 rag_search Tool로 · 응용 · 수강생 TODO.

DB: 기존 report_agent_lab / 반드시 SELECT. 실제 Tool은 --live에서 실행됩니다.
"""

def prepare_search(query: str, category: str = 'ALL') -> dict:
    """실제 6개 카테고리만 허용하고 query/category를 반환."""
    # TODO D29-04-I-01: 실제 6개 카테고리만 허용하고 query/category를 반환.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] 검색하기 전에 "질문"과 "분류(category)"가 올바른지 먼저 확인하는 함수예요.
    # [쉬운 설명] DB의 reports 표에 실제로 있는 분류 6가지 + 'ALL'(전부에서 찾기)만 허용해요.
    allowed = ('ALL', 'EXPERIMENT', 'DAILY_WORK', 'RESEARCH_PLAN', 'DATA_PROCESSING', 'PROMPT', 'MEETING')
    # [쉬운 설명] 질문이 글자가 아니거나 공백만 있으면 오류예요.
    if not isinstance(query, str) or not query.strip():
        raise ValueError('검색어(query)가 비어 있습니다.')
    # [쉬운 설명] split()으로 잘랐다가 ' '.join()으로 붙이면 "여러 칸 공백"이 "한 칸"으로 정리돼요.
    cleaned = ' '.join(query.split())
    # [쉬운 설명] 500자보다 길면 검색 도구가 받지 않으니 막아요.
    if len(cleaned) > 500:
        raise ValueError('검색어는 500자 이하여야 합니다.')
    # [쉬운 설명] 분류가 None으로 오면 기본값 'ALL'로 생각해요.
    if category is None:
        category = 'ALL'
    if not isinstance(category, str):
        raise ValueError('category는 문자열이어야 합니다.')
    # [쉬운 설명] 대문자로 통일해서 'meeting'도 'MEETING'으로 받아 줘요.
    category = category.strip().upper()
    if category not in allowed:
        raise ValueError(f'허용되지 않는 category입니다: {category}')
    return {'query': cleaned, 'category': category}
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-I-01: 직접 구현하세요')

def invoke_rag(request: dict) -> dict:
    """실제 기존 DB의 pgvector/CUDA RAG를 호출합니다. 가짜 검색 결과 금지."""
    # TODO D29-04-I-02: 실제 기존 DB의 pgvector/CUDA RAG를 호출합니다. 가짜 검색 결과 금지.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] 실제 RAG(문서 검색 + AI 답변)를 실행하는 함수예요. 가짜 결과는 절대 만들지 않아요.
    if not isinstance(request, dict):
        raise ValueError('request는 dict여야 합니다.')
    # [쉬운 설명] 요청에 엉뚱한 칸(task_id 등)이 섞여 있으면 거절해요. query와 category만 받아요.
    extra = set(request) - {'query', 'category'}
    if extra:
        raise ValueError(f'허용되지 않는 요청 항목: {sorted(extra)}')
    # [쉬운 설명] prepare_search를 거치지 않은 요청이어도 안전하도록 한 번 더 검사해요.
    checked = prepare_search(request.get('query', ''), request.get('category', 'ALL'))
    # [쉬운 설명] 11/20의 실제 RAG를 불러요: E5(GPU) 벡터 → pgvector 검색 → Reranker(GPU) → LLM 답변.
    from coursekit.rag import rag_answer
    result = rag_answer(checked['query'], checked['category'])
    # [쉬운 설명] 결과가 예상한 모양(dict + status)이 아니면 믿을 수 없으니 오류로 알려요.
    if not isinstance(result, dict) or 'status' not in result:
        raise RuntimeError('RAG 결과 형식이 올바르지 않습니다.')
    return result
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-I-02: 직접 구현하세요')


# 추가 구현: 같은 프로젝트의 별도 책임 모듈
from validation_04 import format_evidence
