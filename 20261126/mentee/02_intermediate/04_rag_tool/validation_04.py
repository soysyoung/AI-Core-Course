"""용도별 추가 검증: Intermediate · Day29."""

def format_evidence(result: dict) -> dict:
    """RAG 답변·실제 Context 출처·상태를 구분해 결과로 반환."""
    # TODO D29-04-I-03: RAG 답변·실제 Context 출처·상태를 구분해 결과로 반환.
    # 힌트: 실제 query/category 검증 후 coursekit.rag의 live 연결을 호출하세요.
    # [쉬운 설명] RAG 결과를 "상태", "AI 답변", "근거 출처" 세 칸으로 나눠서 보기 쉽게 정리하는 함수예요.
    # [쉬운 설명] 숙제할 때 "내 답"과 "참고한 책 목록"을 따로 적는 것과 같아요.
    if not isinstance(result, dict):
        raise ValueError('result는 dict여야 합니다.')
    # [쉬운 설명] status는 'answered'(답함) 또는 'insufficient_context'(근거 부족) 같은 상태예요.
    status = result.get('status', 'unknown')
    # [쉬운 설명] 근거 목록에서 꼭 필요한 정보(출처 ID, 보고서 번호, 제목, 위치)만 골라 담아요.
    evidence = []
    for source in result.get('sources') or []:
        if isinstance(source, dict):
            evidence.append({
                'source_id': source.get('source_id'),
                'report_id': source.get('report_id'),
                'title': source.get('title'),
                'source_locator': source.get('source_locator'),
            })
    # [쉬운 설명] 근거가 부족하다는 상태인데 출처가 붙어 있으면 앞뒤가 안 맞아요. 그래서 출처를 비워요.
    if status in ('insufficient_context', 'not_found'):
        evidence = []
    return {
        'status': status,
        'answer': result.get('answer', ''),
        'evidence': evidence,
        'evidence_count': len(evidence),
        # [쉬운 설명] retrieval은 "어떤 보고서들이 후보였고 몇 개가 실제로 쓰였는지" 기록이에요.
        'retrieval': result.get('retrieval', {}),
    }
    # [쉬운 설명] 아래 줄은 원래 있던 코드라 지우지 않고 남겨 두었어요. 위에서 return으로 이미 끝나서 실행되지 않아요.
    raise NotImplementedError('D29-04-I-03: 직접 구현하세요')

