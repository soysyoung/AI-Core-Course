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
    # BEGIN D26-01-A01
    # TODO D26-01-A01: 다섯 단계의 처리 순서를 반환합니다.
    # 힌트: 검색과 생성 사이에 Context 선택과 Prompt 작성이 필요합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-A01 TODO 미완성")
    # [추가 설명] RAG는 "찾기 -> 고르기 -> 질문지 만들기 -> 답 쓰기 -> 검사하기" 순서로 일합니다.
    # 시험 공부에 비유하면: 교과서에서 관련 쪽을 찾고, 쓸 내용만 고르고, 문제지에 정리하고,
    # 답을 쓰고, 마지막에 채점과 출처 확인을 하는 것과 같아요.
    return [
        "Retriever",  # 1단계: 관련 있는 글 조각을 찾아옵니다.
        "Context Builder",  # 2단계: 답에 쓸 근거만 골라 모읍니다.
        "Prompt",  # 3단계: 규칙+질문+근거를 모델이 읽을 메시지로 만듭니다.
        "Generator",  # 4단계: 모델이 답변을 만듭니다.
        "Validator · Source 연결",  # 5단계: 답을 검사하고 출처 위치를 이어 줍니다.
    ]
    # END D26-01-A01

def evidence_fields(hit: dict) -> dict:
    """출처와 근거 본문을 비교 기록에 넣을 공통 필드로 반환합니다."""
    # BEGIN D26-01-A02
    # TODO D26-01-A02: 입력 Hit의 출처와 본문 필드를 보존합니다.
    # 힌트: 숫자나 예외 문장을 새로 만들지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-A02 TODO 미완성")
    # [추가 설명] hit은 "근거 카드 한 장"입니다. 카드에 적힌 번호·문서·버전·위치·본문을
    # 하나도 고치지 않고 그대로 새 dict에 옮겨 적습니다. (내용을 새로 지어내면 안 돼요!)
    return {
        "citation_id": hit["citation_id"],  # 근거 카드 번호
        "doc_id": hit["doc_id"],  # 문서 이름표
        "source_version": hit["source_version"],  # 문서 버전
        "source_locator": hit["source_locator"],  # 원문 안에서의 위치
        "evidence": hit["body"],  # 근거 본문
    }
    # END D26-01-A02

def attendance_judgment(minutes: int, prior_approval: bool = False) -> str:
    """강의의 가상 사례를 조건문으로 대조합니다. 실제 기관의 출석 판정기가 아닙니다."""
    # BEGIN D26-01-A03
    # TODO D26-01-A03: 15분 경계와 사전 승인 예외를 원문대로 구분합니다.
    # 힌트: 사전 승인이라면 운영실 확인, 그렇지 않은 1~15분은 지각, 15분 초과는 결석입니다. 0분은 비교 대상 밖으로 표시합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-A03 TODO 미완성")
    # [추가 설명] 출석 규칙을 "신호등"처럼 순서대로 확인합니다.
    # 0분 이하는 "아직 수업 전/잘못된 값"이라 비교할 수 없으니 오류로 알려 줍니다.
    if minutes <= 0:
        raise ValueError("minutes는 1 이상이어야 합니다 (0분 이하는 비교 대상 밖)")
    # 사전 승인을 받았다면 우리가 마음대로 정하지 않고, 운영실에 물어보라고 안내합니다.
    # (승인 = 자동으로 출석 인정, 이 아니에요!)
    if prior_approval:
        return "운영실 확인"
    # 15분 "까지"는 지각입니다. 딱 15분도 지각에 포함돼요.
    if minutes <= 15:
        return "지각"
    # 15분을 "초과"(16분부터)하면 결석입니다.
    return "결석"
    # END D26-01-A03

def comparison(hit: dict) -> list[dict]:
    """15분·20분·사전 승인 20분의 세 사례를 같은 원문과 연결합니다."""
    # BEGIN D26-01-A04
    # TODO D26-01-A04: 15분·20분·사전 승인 20분 세 행에 판단과 동일 근거를 묶습니다.
    # 힌트: 앞의 두 함수를 호출하여 각 행을 작성하세요.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-01-A04 TODO 미완성")
    # [추가 설명] 같은 근거 카드 하나로 세 가지 상황을 비교하는 표를 만듭니다.
    # 세 상황: (15분, 승인 없음), (20분, 승인 없음), (20분, 승인 있음)
    # 표의 각 줄은 "상황 + 판단 + 똑같은 근거 정보"로 이루어져 있어요.
    rows = []
    for minutes, approved in [(15, False), (20, False), (20, True)]:
        rows.append({
            "minutes": minutes,  # 늦은 시간(분)
            "prior_approval": approved,  # 사전 승인 여부
            "judgment": attendance_judgment(minutes, approved),  # 위에서 만든 함수로 판단
            **evidence_fields(hit),  # 근거 정보는 세 줄 모두 똑같이 붙입니다.
        })
    return rows
    # END D26-01-A04

def main():
    report = {
        "execution": execution_record("concept_review"),
        "stages": [{"stage": name, **STAGE_CARDS[name]} for name in stage_order()],
        "cases": comparison(example_hit()),
        "observation": "원문의 조건을 Python 조건문으로 대조한 교육용 기록; LLM 호출 아님",
    }
    path = save_json(HERE, "rag_flow.json", report)
    show_success("01 Advanced", path)

if __name__ == "__main__":
    main()
