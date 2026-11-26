"""단계별 역할 분리: checks.py / 독립 실행은 main.py. """

def validate_trace(result):
    """원 질문·검색용 질문·후보·Context ID를 각각 확인합니다."""
    # BEGIN D27-06-I03
    # TODO D27-06-I03: 원 질문·검색용 질문·후보·Context ID를 각각 확인합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    # [쉬운 설명] trace는 파이프라인이 일하면서 남긴 "작업 일지"입니다. 일지를 한 줄씩 검사해요.
    t = result['trace']
    # [쉬운 설명] 출처로 쓴 문서 번호들을 모아 둡니다.
    source_ids = [s['chunk_id'] for s in result['sources']]
    return {
        # [쉬운 설명] 원래 질문과 검색용 질문이 둘 다 비어 있지 않게 따로 적혀 있는지
        'questions_separate': bool(t['original_question'] and t['search_query']),
        # [쉬운 설명] 후보 문서 번호와 Context에 넣은 문서 번호가 목록(list)으로 기록됐는지
        'ids_recorded': isinstance(t['candidate_ids'], list) and isinstance(t['included_ids'], list),
        # [쉬운 설명] Context에 넣은 문서는 반드시 후보 중에서 골랐는지 (없던 문서가 끼어들면 안 돼요)
        'included_from_candidates': set(t['included_ids']).issubset(t['candidate_ids']),
        # [쉬운 설명] 출처로 쓴 문서는 반드시 Context에 넣은 것인지 (안 읽은 책을 출처로 쓰면 안 되는 것과 같아요)
        'sources_from_context': set(source_ids).issubset(t['included_ids']),
    }
    # [쉬운 설명] 위에서 항상 return 하므로 아래 줄은 실행되지 않습니다.
    raise NotImplementedError("D27-06-I03 미완성")
    # END D27-06-I03
