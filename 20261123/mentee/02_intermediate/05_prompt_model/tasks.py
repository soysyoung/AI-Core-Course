"""실습 05 · Prompt 구성과 Chat Model 호출을 구분합니다."""
from pathlib import Path
import argparse
import sys

HERE = Path(__file__).resolve().parent
# 어느 폴더에서 실행해도 이 역할 폴더의 coursekit을 사용합니다.
sys.path.insert(0, str(HERE.parents[1]))

from coursekit.data import example_hit, load_hits
from coursekit.checkpoints import make_prompt
from coursekit.llm import create_chat_model
from coursekit.fixtures import fixture_chat_model, fixture_generation
from coursekit.reporting import execution_record, message_record
from coursekit.io import save_json, show_success


def make_inputs(question: str, context: str) -> dict:
    """입력: 질문·근거 문자열 / 출력: question, context 두 Key를 가진 dict."""
    # BEGIN D26-05-I01
    # TODO D26-05-I01: 질문과 Context를 각각 question·context Key로 묶어 반환합니다.
    # 힌트: Dictionary의 두 Key 이름은 Prompt의 변수 이름과 같아야 합니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-05-I01 TODO 미완성")
    # [추가 설명] Prompt 틀에는 {question}, {context}라는 빈칸이 있어요.
    # 빈칸 이름과 똑같은 Key로 값을 담아야 Prompt가 제자리에 끼워 넣을 수 있습니다.
    return {"question": question, "context": context}
    # END D26-05-I01


def invoke_pair(prompt, chat_model, inputs: dict):
    """dict → ChatPromptValue → AIMessage. 반환: (prompt_value, message)."""
    # BEGIN D26-05-I02
    # TODO D26-05-I02: Prompt를 먼저 실행하고 그 반환값을 Chat Model에 전달한 뒤 두 반환값을 함께 반환합니다.
    # 힌트: 첫 invoke의 반환값이 둘째 invoke의 입력입니다. 반환 순서는 (prompt_value, message)입니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-05-I02 TODO 미완성")
    # [추가 설명] 두 단계 릴레이입니다.
    # 1) Prompt에 dict를 주면 모델이 읽을 메시지 묶음(ChatPromptValue)이 나오고,
    # 2) 그 결과를 그대로 Chat Model에 넘기면 답변(AIMessage)이 나옵니다.
    # Prompt 단계에서 오류가 나면 2단계로 가지 않으므로 모델은 호출되지 않아요.
    prompt_value = prompt.invoke(inputs)
    message = chat_model.invoke(prompt_value)
    return prompt_value, message
    # END D26-05-I02


def inspect_missing_context(prompt) -> dict:
    """의도적으로 빠진 입력을 검사합니다. 모델 API는 이 함수에 등장하지 않습니다."""
    # BEGIN D26-05-I03
    # TODO D26-05-I03: context Key를 뺀 입력을 Prompt에 전달하여 발생한 KeyError의 단계를 기록합니다.
    # 힌트: try/except KeyError를 사용합니다. 이 함수에서는 Chat Model을 호출하지 않습니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-05-I03 TODO 미완성")
    # [추가 설명] 일부러 context 빈칸을 비워서 Prompt에 넣어 봅니다.
    # 빈칸을 채울 값이 없으니 Prompt 단계에서 KeyError가 나고, 모델까지는 가지 않습니다.
    # try/except는 "해 보고, 이 오류가 나면 잡아서 기록하자"라는 문법이에요.
    try:
        prompt.invoke({"question": "15분 늦으면 어떻게 기록되나요?"})
    except KeyError as error:
        return {"stage": "prompt_input", "exception_type": type(error).__name__, "model_invoked": False}
    raise AssertionError("context가 없는데 Prompt가 KeyError를 내지 않았습니다.")
    # END D26-05-I03


def context_of(hit: dict) -> str:
    """앞 장에서 배운 출처 포함 블록 형식입니다. 이번 실습의 제공 코드입니다."""
    return f'[{hit["citation_id"]}] {hit["source_locator"]}\n{hit["body"]}'


def main():
    parser = argparse.ArgumentParser(description="Prompt → Chat Model 입력·출력 관찰")
    parser.add_argument("--offline", action="store_true", help="고정 응답 예시만 사용; 실제 모델 미실행")
    args = parser.parse_args()
    attendance = example_hit()
    prompt = make_prompt()
    cases = [("attendance_15", "15분 늦으면 어떻게 기록되나요?", attendance)]
    assignment = next(hit for hit in load_hits() if hit["doc_id"] == "DOC-ASSIGN")
    cases.append(("assignment_deadline", "내 과제의 정확한 마감 날짜는?", assignment))
    # 모델 생성·호출 전에 로컬 TODO와 입력을 먼저 확인합니다.
    prepared = [(case_id, make_inputs(question, context_of(hit)), hit)
                for case_id, question, hit in cases]
    observations = {}
    observations["missing_context"] = inspect_missing_context(prompt)
    # 기본 경로는 실제 모델입니다. 환경 문제가 있어도 자동으로 예시로 전환하지 않습니다.
    chat_model = fixture_chat_model() if args.offline else create_chat_model()
    records = []
    for case_id, inputs, hit in prepared:
        prompt_value, message = invoke_pair(prompt, chat_model, inputs)
        records.append({
            "case_id": case_id,
            "question": inputs["question"],
            "context": inputs["context"],
            "prompt_value_type": type(prompt_value).__name__,
            "prompt_messages": [{"type": m.type, "content": m.content}
                                for m in prompt_value.to_messages()],
            "response": message_record(message),
            "evidence": {"citation_id": hit["citation_id"],
                         "doc_id": hit["doc_id"], "source_locator": hit["source_locator"],
                         "body": hit["body"]},
            "human_evidence_review": "pending",
        })
    result = {
        "exercise": "05_prompt_model",
        "execution": execution_record("offline_fixture" if args.offline else "live", llm=not args.offline),
        "real_model_calls": 0 if args.offline else len(records),
        "fixed_example_calls": len(records) if args.offline else 0,
        "observations": observations,
        "cases": records,
        "review_note": "문장·출처의 정답 여부는 자동 판정하지 않았습니다. reports/review.md에 원문 대조를 기록하세요.",
    }
    path = save_json(HERE, "prompt_model.json", result)
    show_success("05 Prompt·Chat Model 관찰 기록", path)
    print("실제 LLM 실행:", not args.offline, "| 원문 대조: 수강생 확인 필요")


if __name__ == "__main__":
    main()
