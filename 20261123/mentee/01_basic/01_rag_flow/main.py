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
    # BEGIN D26-01-B01
    # TODO D26-01-B01: 다섯 단계의 이름을 처리 순서대로 반환합니다.
    # 힌트: 검색 → 근거 선택 → 메시지 작성 → 생성 → 확인 순서입니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-B01 TODO 미완성")
    # [추가 설명] RAG는 "찾기 -> 고르기 -> 질문지 만들기 -> 답 쓰기 -> 검사하기" 순서로 일합니다.
    # 시험 공부에 비유하면: 교과서에서 관련 쪽을 찾고(Retriever), 그중 쓸 내용만 고르고(Context Builder),
    # 문제지에 정리해서(Prompt), 답을 쓰고(Generator), 마지막에 채점·출처 확인(Validator)을 하는 것과 같아요.
    # 이 순서대로 이름(문자열) 다섯 개를 리스트에 담아 돌려주면 됩니다.
    return [
        "Retriever",  # 1단계: 질문과 관련 있는 글 조각을 찾아옵니다.
        "Context Builder",  # 2단계: 찾은 것 중 답에 쓸 근거만 골라 모읍니다.
        "Prompt",  # 3단계: 규칙+질문+근거를 모델이 읽을 메시지로 만듭니다.
        "Generator",  # 4단계: 모델이 그 메시지를 읽고 답변을 만듭니다.
        "Validator · Source 연결",  # 5단계: 답이 맞는지, 출처가 어디인지 확인합니다.
    ]
    # END D26-01-B01

def evidence_note(hit: dict) -> dict:
    """출석 문서와 사람이 읽은 판단을 함께 기록합니다. 모델 호출 결과가 아닙니다."""
    # BEGIN D26-01-B02
    # TODO D26-01-B02: 입력 Hit의 출처·본문과 15분 질문의 판단·예외를 한 dict로 묶습니다.
    # 힌트: source_locator와 body를 그대로 읽고, 문서의 “까지”와 사전 승인 조건을 확인하세요.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-B02 TODO 미완성")
    # [추가 설명] hit은 "검색으로 찾은 글 조각 한 장의 카드"라고 생각하세요.
    # 카드에는 번호(citation_id), 문서 이름(doc_id), 버전, 원문 위치, 본문이 적혀 있어요.
    # 이 카드의 내용을 "고치지 않고 그대로" 복사해서 새 확인표(dict)에 옮겨 적습니다.
    # 거기에 사람이 읽고 내린 판단(지각)과 확인할 예외(사전 승인)를 덧붙입니다.
    return {
        "citation_id": hit["citation_id"],  # 근거 카드 번호 그대로
        "doc_id": hit["doc_id"],  # 어느 문서에서 왔는지 그대로
        "source_version": hit["source_version"],  # 문서 버전(v2) 그대로
        "source_locator": hit["source_locator"],  # 원문에서의 정확한 위치 그대로
        "evidence": hit["body"],  # 근거가 되는 본문 그대로 (바꾸지 않기!)
        "question": "15분 늦으면 어떻게 기록되나요?",  # 우리가 확인하려는 질문
        # 본문에 "15분까지 입실하면 지각"이라고 적혀 있어서, 딱 15분 늦은 건 지각입니다.
        # ("15분을 초과"해야 결석이므로 15분 정각은 결석이 아니에요.)
        "judgment": "지각",
        # 본문 마지막 문장: 사전 승인을 받았다면 운영실에 따로 물어봐야 합니다.
        "exception_to_check": "사전 승인을 받은 경우 운영실 확인",
    }
    # END D26-01-B02

def main():
    order = stage_order()
    report = {
        "execution": execution_record("concept_review"),
        "stages": [{"stage": name, **STAGE_CARDS[name]} for name in order],
        "case": evidence_note(example_hit()),
        "observation": "사람이 강의 원문을 읽고 작성한 역할·근거 확인표",
    }
    path = save_json(HERE, "rag_flow.json", report)
    show_success("01 Basic", path)

if __name__ == "__main__":
    main()
