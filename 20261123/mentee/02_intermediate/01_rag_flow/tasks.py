"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record

# 입력·출력 설명은 제공됩니다. TODO에서는 올바른 처리 순서를 연결합니다.
STAGE_CARDS = {
    "Generator": {"input": "모델 입력", "output": "생성된 답변"},
    "Prompt": {"input": "규칙·질문·Context", "output": "모델이 읽을 메시지"},
    "Retriever": {"input": "질문·검색 조건", "output": "관련 청크 후보"},
    "Validator · Source 연결": {"input": "생성 결과·허용 ID", "output": "검증 결과·원문 위치"},
    "Context Builder": {"input": "후보 목록", "output": "선택한 근거·포함 ID"},
}

def stage_order() -> list[str]:
    """STAGE_CARDS의 이름 다섯 개를 처리 순서대로 반환합니다."""
    # BEGIN D26-01-I01
    # TODO D26-01-I01: 다섯 단계의 처리 순서를 반환합니다.
    # 힌트: STAGE_CARDS의 이름을 사용합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-I01 TODO 미완성")
    # [추가 설명] RAG는 "찾기 -> 고르기 -> 질문지 만들기 -> 답 쓰기 -> 검사하기" 순서로 일합니다.
    # 시험 공부에 비유하면: 교과서에서 관련 쪽을 찾고, 쓸 내용만 고르고, 문제지에 정리하고,
    # 답을 쓰고, 마지막에 채점과 출처 확인을 하는 것과 같아요.
    # STAGE_CARDS 안에 이름이 이미 있지만 순서가 섞여 있어서, 올바른 순서로 직접 나열해 돌려줍니다.
    return [
        "Retriever",  # 1단계: 관련 있는 글 조각을 찾아옵니다.
        "Context Builder",  # 2단계: 답에 쓸 근거만 골라 모읍니다.
        "Prompt",  # 3단계: 규칙+질문+근거를 모델이 읽을 메시지로 만듭니다.
        "Generator",  # 4단계: 모델이 답변을 만듭니다.
        "Validator · Source 연결",  # 5단계: 답을 검사하고 출처 위치를 이어 줍니다.
    ]
    # END D26-01-I01

def find_hit(hits: list[dict], doc_id: str) -> dict:
    """주어진 예시 목록에서 문서 ID가 같은 Hit 한 건을 선택합니다."""
    # BEGIN D26-01-I02
    # TODO D26-01-I02: 목록에서 요청한 doc_id의 Hit를 반환하고 없으면 LookupError를 발생시킵니다.
    # 힌트: 각 Hit의 doc_id를 순서대로 비교합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-I02 TODO 미완성")
    # [추가 설명] hits는 "근거 카드 묶음", doc_id는 찾고 싶은 문서의 이름표입니다.
    # 카드를 한 장씩 넘겨 보며 이름표가 같은 카드를 발견하면 바로 그 카드를 돌려줍니다.
    for hit in hits:
        if hit["doc_id"] == doc_id:
            return hit
    # 끝까지 봐도 없으면, 비슷해 보이는 다른 문서를 대신 주면 안 됩니다. "없다"고 오류로 알려 줍니다.
    raise LookupError(f"문서를 찾을 수 없습니다: {doc_id}")
    # END D26-01-I02

def deadline_note(hit: dict) -> dict:
    """과제 문서의 존재와 정확한 마감 날짜의 존재를 구분해 기록합니다."""
    # BEGIN D26-01-I03
    # TODO D26-01-I03: 문서 발견 여부와 정확한 날짜의 유무를 나누어 기대 판단을 작성합니다.
    # 힌트: “담당자가 공지한 날짜”는 실제 날짜 값이 아닙니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-I03 TODO 미완성")
    # [추가 설명] "문서가 있다"와 "정확한 날짜가 적혀 있다"는 서로 다른 이야기입니다.
    # 예를 들어 "숙제는 선생님이 말해 준 날까지"라는 쪽지는 있어도, 몇 월 며칠인지는 알 수 없죠.
    # 그래서 문서는 찾았지만(True) 날짜는 알 수 없다(False)고 따로따로 적고,
    # 근거가 부족하니 날짜를 지어내지 말고 "정보 부족" 상태로 기록합니다.
    # hit 카드의 값은 고치지 않고 그대로 옮겨 적습니다.
    return {
        "question": "내 과제의 정확한 마감 날짜는?",  # 확인하려는 질문
        "citation_id": hit["citation_id"],  # 근거 카드 번호 그대로
        "doc_id": hit["doc_id"],  # 문서 이름표 그대로
        "source_version": hit["source_version"],  # 문서 버전 그대로
        "source_locator": hit["source_locator"],  # 원문 위치 그대로
        "evidence": hit["body"],  # 근거 본문 그대로
        "document_found": True,  # 과제 문서는 찾았습니다.
        "exact_date_available": False,  # 하지만 정확한 날짜 값은 없습니다.
        "expected_status": "insufficient_context",  # 근거가 모자란 상태 (서버 고장과는 다릅니다)
        "reason": "문서는 담당자가 공지한 날짜를 따르라고만 안내하며 정확한 날짜는 제공하지 않습니다.",
    }
    # END D26-01-I03

def main():
    hit = find_hit(load_hits(), "DOC-ASSIGN")
    report = {
        "execution": execution_record("concept_review"),
        "stages": [{"stage": name, **STAGE_CARDS[name]} for name in stage_order()],
        "case": deadline_note(hit),
        "observation": "예시 문서 선택과 사람이 작성한 정보 부족 판단",
    }
    path = save_json(HERE, "rag_flow.json", report)
    show_success("01 Intermediate", path)

if __name__ == "__main__":
    main()
