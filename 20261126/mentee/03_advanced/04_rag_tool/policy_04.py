"""경계값·오류/권한 정책: Advanced · Day29."""

def format_evidence(result: dict) -> dict:
    """RAG 답변·실제 Context 출처·상태를 구분해 결과로 반환."""
    # TODO D29-04-A-03: RAG 답변·실제 Context 출처·상태를 구분해 결과로 반환.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] RAG 결과를 "상태", "AI 답변", "근거 출처" 칸으로 나눠 정리하는 함수예요.
    # [쉬운 설명] 숙제할 때 "내 답"과 "참고한 책 목록"을 따로 적는 것과 같아요.
    if not isinstance(result, dict):
        raise ValueError('result는 dict여야 합니다.')
    status = result.get('status', 'unknown')
    # [쉬운 설명] 근거마다 꼭 필요한 정보(출처 ID, 번호, 제목, 위치)만 골라 담아요.
    evidence = []
    for source in result.get('sources') or []:
        if isinstance(source, dict):
            evidence.append({
                'source_id': source.get('source_id'),
                'report_id': source.get('report_id'),
                'title': source.get('title'),
                'source_locator': source.get('source_locator'),
            })
    # [쉬운 설명] 근거 부족 상태에서는 출처를 비워요. "모른다"면서 출처를 붙이면 앞뒤가 안 맞으니까요.
    if status in ('insufficient_context', 'not_found'):
        evidence = []
    return {
        'status': status,
        'answer': result.get('answer', ''),
        'evidence': evidence,
        'evidence_count': len(evidence),
        'retrieval': result.get('retrieval', {}),
        # [쉬운 설명] 심화: 출처 검증 결과도 함께 적어서, 읽는 사람이 믿어도 되는 결과인지 바로 알 수 있게 해요.
        'evidence_valid': validate_evidence(result),
    }
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-A-03: 직접 구현하세요')

def validate_evidence(result: dict) -> bool:
    """선택된 Context 내 출처만 인정하고 No-answer 출처를 거절합니다."""
    # TODO D29-04-A-04: 선택된 Context 내 출처만 인정하고 No-answer 출처를 거절합니다.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] AI가 붙인 출처가 "진짜로 읽은 보고서"인지 검사하는 함수예요. 하나라도 이상하면 False예요.
    # [쉬운 설명] 책을 안 읽고 "이 책에 나와요"라고 쓰면 안 되는 것처럼, 실제로 읽은 Context의 출처만 인정해요.
    import re
    if not isinstance(result, dict):
        return False
    status = result.get('status')
    sources = result.get('sources', [])
    if not isinstance(sources, list):
        return False
    # [쉬운 설명] 규칙 1: "근거가 부족해요(No-answer)"라고 했으면 출처가 하나도 없어야 해요.
    if status in ('insufficient_context', 'not_found'):
        return len(sources) == 0
    # [쉬운 설명] 규칙 2: 답했다고 하면 출처가 최소 하나는 있어야 해요.
    if status != 'answered' or not sources:
        return False
    # [쉬운 설명] included_ids는 검색 후 실제로 Context에 넣은(AI가 읽은) 보고서 번호 목록이에요.
    included = set((result.get('retrieval') or {}).get('included_ids') or [])
    seen = set()
    for source in sources:
        if not isinstance(source, dict):
            return False
        source_id = source.get('source_id')
        report_id = source.get('report_id')
        # [쉬운 설명] 규칙 3: 출처 ID는 'RPT-숫자' 모양이고, 그 숫자가 report_id와 같아야 해요.
        if not isinstance(source_id, str) or not re.fullmatch(r'RPT-\d+', source_id):
            return False
        if source_id != f'RPT-{report_id}':
            return False
        # [쉬운 설명] 규칙 4: 같은 출처를 두 번 쓰면 안 돼요.
        if source_id in seen:
            return False
        seen.add(source_id)
        # [쉬운 설명] 규칙 5: 실제로 읽은 Context(included_ids) 안에 있는 보고서여야 해요.
        if report_id not in included:
            return False
    return True
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-A-04: 직접 구현하세요')

