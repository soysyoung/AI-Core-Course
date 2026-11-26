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
    # BEGIN D26-05-B01
    # TODO D26-05-B01: 질문과 Context를 각각 question·context Key로 묶어 반환합니다.
    # 힌트: Dictionary의 두 Key 이름은 Prompt의 변수 이름과 같아야 합니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-05-B01 TODO 미완성")
    # [추가 설명] Prompt는 빈칸이 뚫린 "문제지 양식"이에요. 양식에는 {question}과 {context}라는 빈칸이 있어요.
    # 빈칸을 채우려면 "빈칸 이름표: 채울 내용" 형태의 dict를 넘겨야 해요.
    # 이름표가 양식의 빈칸 이름과 한 글자라도 다르면 "빈칸을 못 찾았다"는 오류가 나요.
    return {
        "question": question,  # 학생이 물어본 질문
        "context": context,  # 질문에 답할 때 참고할 근거 글(출처 번호 포함)
    }
    # END D26-05-B01


def invoke_pair(prompt, chat_model, inputs: dict):
    """dict → ChatPromptValue → AIMessage. 반환: (prompt_value, message)."""
    # BEGIN D26-05-B02
    # TODO D26-05-B02: Prompt를 먼저 실행하고 그 반환값을 Chat Model에 전달한 뒤 두 반환값을 함께 반환합니다.
    # 힌트: 첫 invoke의 반환값이 둘째 invoke의 입력입니다. 반환 순서는 (prompt_value, message)입니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-05-B02 TODO 미완성")
    # [추가 설명] 이 함수는 두 단계를 차례로 실행해요.
    #   1단계: 문제지 양식(prompt)에 질문·근거를 채워 "완성된 문제지"(ChatPromptValue)를 만든다.
    #          이때는 아직 AI에게 아무것도 보내지 않아요. 종이만 준비한 상태예요.
    #   2단계: 완성된 문제지를 AI(chat_model)에게 건네고 "답안지"(AIMessage)를 받는다.
    #          실제 LLM API 요청은 바로 이 2단계에서 일어나요.
    # 1단계의 결과물이 2단계의 입력이 되는 "릴레이 달리기"라고 생각하면 돼요.
    prompt_value = prompt.invoke(inputs)  # 1단계: 문제지 완성
    message = chat_model.invoke(prompt_value)  # 2단계: AI에게 문제지를 주고 답안 받기
    # 무엇을 보냈는지(문제지)와 무엇을 받았는지(답안)를 둘 다 기록하려고 함께 돌려줍니다.
    # 순서는 (문제지, 답안) 입니다.
    return prompt_value, message
    # END D26-05-B02


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
    # 모델 생성·호출 전에 로컬 TODO와 입력을 먼저 확인합니다.
    prepared = [(case_id, make_inputs(question, context_of(hit)), hit)
                for case_id, question, hit in cases]
    observations = {}
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
