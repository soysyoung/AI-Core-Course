"""Day26 실습 7 · 기본필수. 실행 위치와 무관하게 현재 역할 폴더를 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.io import save_json, show_success
from coursekit.data import example_hit
from coursekit.checkpoints import (
    hits_to_documents, build_context, NO_ANSWER, RagServiceError, receive_bundle,
)
from coursekit.fixtures import fixture_bundle
from coursekit.reporting import execution_record


def common_cases():
    """의도적으로 만든 세 입력입니다. 실제 모델의 응답 로그가 아닙니다."""
    answered = {
        "status": "answered",
        "answer": "일반 기준으로 15분까지는 지각입니다. 사전 승인을 받았다면 운영실에 확인합니다.",
        "source_ids": [201], "missing_information": "",
    }
    insufficient = {
        "status": "insufficient_context", "answer": NO_ANSWER,
        "source_ids": [], "missing_information": "정확한 과제 마감 날짜가 자료에 없습니다.",
    }
    unknown = {**answered, "source_ids": [999]}
    return [
        {"name": "normal", "bundle": fixture_bundle(answered)},
        {"name": "insufficient", "bundle": fixture_bundle(insufficient)},
        {"name": "unknown_source", "bundle": fixture_bundle(unknown)},
    ]


def allowed_source_ids(included_docs):
    """입력: 실제 Context에 포함된 Document 목록 / 출력: set[int]."""
    # BEGIN D26-07-B01
    # TODO D26-07-B01: included_docs의 metadata에서 citation_id를 모아 set으로 반환합니다.
    # 힌트: Document 목록을 순회하고 doc.metadata["citation_id"]를 읽으세요. 검색 후보 목록은 사용하지 않습니다.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-07-B01 TODO 미완성")
    # [추가 설명] "AI가 인용해도 되는 출처 번호 명단"을 만드는 함수예요.
    # 명단에는 자료집(Context)에 실제로 넣어서 AI에게 보여 준 문서의 번호만 들어가야 해요.
    # set(집합)을 쓰는 이유: 같은 번호가 두 번 들어가도 한 번만 남고, "명단에 있나?" 확인이 빨라요.
    # 번호를 201처럼 직접 적지 않고 문서에서 읽어 오기 때문에, 문서가 바뀌어도 올바르게 동작해요.
    # 문서가 하나도 없으면 빈 집합 set()이 됩니다.
    return {doc.metadata["citation_id"] for doc in included_docs}
    # END D26-07-B01


def inspect_case(case, provided_ids):
    """검증 결과를 JSON으로 기록합니다. 원문 의미의 참/거짓은 자동 판정하지 않습니다."""
    # BEGIN D26-07-B02
    # TODO D26-07-B02: receive_bundle로 검사한 결과를 accepted/rejected 형식으로 기록합니다.
    # 힌트: 성공 시 KnowledgeAnswer.model_dump(), RagServiceError 시 str(exc)를 사용합니다. 반환 Key는 docstring 아래 호출부와 expected를 확인하세요.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-07-B02 TODO 미완성")
    # [추가 설명] receive_bundle은 AI 답안을 검사하는 "자동 채점기"예요.
    # 양식이 맞는지, 인용한 번호가 명단(provided_ids)에 있는지 등을 확인해요.
    #   - 통과하면: 정리된 답(KnowledgeAnswer)을 돌려줘요.
    #   - 불합격이면: RagServiceError라는 오류를 던져요. 오류 메시지가 불합격 이유예요.
    # try/except는 "일단 해 보고(try), 오류가 나면 그쪽 길(except)로 간다"는 뜻이에요.
    try:
        answer = receive_bundle(case["bundle"], provided_ids)
    except RagServiceError as exc:
        # 불합격: 이유만 적고 결과는 비워 둡니다.
        # 기계가 이미 거절했으니 사람이 원문과 대조할 필요는 없어요(False).
        return {
            "case": case["name"],
            "outcome": "rejected",
            "error": str(exc),  # 예: "answer_validation_error" (명단에 없는 999를 인용한 경우)
            "result": None,
            "human_review_required": False,
        }
    # 합격: 오류는 없고(None), 정리된 답을 dict로 바꿔 저장합니다.
    # 주의! 기계 검사 합격은 "양식과 번호가 맞다"는 뜻일 뿐, 내용이 원문과 맞는지는 몰라요.
    # 그래서 사람이 원문과 직접 대조해야 한다고 표시합니다(True).
    return {
        "case": case["name"],
        "outcome": "accepted",
        "error": None,
        "result": answer.model_dump(),  # status·answer·source_ids·missing_information 네 칸
        "human_review_required": True,
    }
    # END D26-07-B02


def run():
    documents = hits_to_documents([example_hit()])
    context, included_docs = build_context(documents)
    provided_ids = allowed_source_ids(included_docs)
    cases = common_cases()
    return {
        "source_mode": "validation_fixtures",
        "execution": execution_record("offline"),
        "context": context, "included_ids": sorted(provided_ids),
        "cases": [inspect_case(case, provided_ids) for case in cases],
        "grounding_review": "reports/review.md에서 숫자·조건·예외와 원문 위치를 직접 대조합니다.",
    }


def main():
    report = run()
    path = save_json(HERE, "validation_report.json", report)
    show_success("07 · 고정 입력 검증표 (모델·DB 미실행)", path)
    for row in report["cases"]:
        print(row["case"], row["outcome"], row["error"])
    print("accepted는 기계 검사를 통과했다는 뜻입니다. 원문 대조를 마쳐야 학습이 완료됩니다.")


if __name__ == "__main__":
    main()
