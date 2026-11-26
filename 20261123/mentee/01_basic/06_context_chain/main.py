"""실습 06 · Context·출처를 보관하고 Runnable Chain을 실행합니다."""
from pathlib import Path
import argparse
import sys

HERE = Path(__file__).resolve().parent
# 어느 폴더에서 실행해도 이 역할 폴더의 coursekit을 사용합니다.
sys.path.insert(0, str(HERE.parents[1]))

from coursekit.data import load_hits
from coursekit.checkpoints import hits_to_documents, build_context, make_prompt, WireAnswer
from coursekit.llm import create_chat_model
from coursekit.fixtures import fixture_generation
from coursekit.reporting import execution_record, bundle_record
from coursekit.io import save_json, show_success


def prepare_context(documents, question: str, max_items=2, max_chars=600) -> dict:
    """Document 목록 → Context·포함 문서·포함 ID·Prompt 입력. 원문은 바꾸지 않습니다."""
    # BEGIN D26-06-B01
    # TODO D26-06-B01: build_context로 Context와 포함 문서를 얻고, 포함 ID 및 Prompt 입력을 함께 반환합니다.
    # 힌트: 반환 Key는 context, included_docs, provided_ids, inputs입니다. ID는 included_docs에서만 모읍니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-06-B01 TODO 미완성")
    # [추가 설명] 검색으로 찾은 문서가 여러 장이어도, AI에게 보여 줄 "참고 자료집"에는 일부만 들어갈 수 있어요.
    # build_context는 최대 max_items장, 최대 max_chars글자까지만 자료집에 넣어 줍니다.
    # 그리고 두 가지를 돌려줘요.
    #   - context: AI가 읽을 자료집 글 (예: "[201] attendance_v2.md#sec-1\n본문...")
    #   - included_docs: 자료집에 "실제로 들어간" 문서들
    context, included_docs = build_context(documents, max_items=max_items, max_chars=max_chars)
    # AI가 "이 번호를 보고 답했어요"라고 말할 수 있는 번호는 자료집에 실제로 넣은 문서 번호뿐이에요.
    # 그래서 검색 후보 전체(documents)가 아니라 included_docs에서만 번호를 모읍니다.
    # (보여 주지도 않은 문서 번호를 허용하면, AI가 안 본 자료를 봤다고 우겨도 통과돼 버려요.)
    provided_ids = [doc.metadata["citation_id"] for doc in included_docs]
    return {
        "context": context,  # AI에게 보여 줄 자료집 글
        "included_docs": included_docs,  # 자료집에 들어간 문서 (나중에 출처를 연결할 때 사용)
        "provided_ids": provided_ids,  # 답에 인용해도 되는 번호 목록
        # Prompt 문제지의 빈칸 {question}, {context}에 넣을 값 (문자열만 넣어요)
        "inputs": {"question": question, "context": context},
    }
    # END D26-06-B01


def run_generation(prompt, structured_model, inputs: dict):
    """Prompt → Structured Model의 bundle. bundle 검증·승인은 다음 실습입니다."""
    # BEGIN D26-06-B02
    # TODO D26-06-B02: Prompt와 Structured Model을 |로 연결하고 inputs로 실행하여 bundle을 반환합니다.
    # 힌트: Chain의 앞 단계 출력이 뒤 단계 입력입니다. 반환 bundle의 raw·parsed·parsing_error를 그대로 보존합니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-06-B02 TODO 미완성")
    # [추가 설명] 05번에서는 prompt.invoke → chat_model.invoke를 두 줄로 따로 불렀죠?
    # LangChain에서는 | (파이프) 기호로 두 단계를 "컨베이어 벨트"처럼 이어 붙일 수 있어요.
    # 앞 기계(prompt)에서 나온 물건(완성된 문제지)이 자동으로 뒤 기계(structured_model)로 넘어가요.
    generation = prompt | structured_model  # 아직 실행 전! 벨트를 조립만 한 상태예요.
    # invoke를 해야 벨트가 실제로 움직여요. 실제 LLM API 요청은 여기서 일어납니다.
    # 결과(bundle)는 세 칸짜리 dict예요.
    #   - raw: AI가 보낸 원래 답장 그대로
    #   - parsed: 답장을 정해진 양식(status·answer·source_ids·missing_information)으로 정리한 것
    #   - parsing_error: 양식대로 정리하다 실패했을 때의 오류 (성공하면 None)
    # 검사·승인은 다음 실습(07)에서 하므로, 여기서는 손대지 않고 그대로 돌려줍니다.
    return generation.invoke(inputs)
    # END D26-06-B02


def main():
    parser = argparse.ArgumentParser(description="Context → Prompt → Structured Model 관찰")
    parser.add_argument("--offline", action="store_true", help="고정 bundle 예시만 사용; 실제 모델 미실행")
    args = parser.parse_args()
    # 앞 실습의 미완성 코드에 의존하지 않는 제공된 Document 변환 Checkpoint입니다.
    academic_hits = [hit for hit in load_hits() if hit["category"] == "학사"]
    documents = hits_to_documents(academic_hits)
    question = "15분 늦으면 어떻게 기록되나요?"
    prepared = prepare_context(documents, question)
    experiments = {}
    prompt = make_prompt()
    if args.offline:
        # 이 Runnable은 제공된 고정 bundle을 반환합니다. 실제 모델 실행은 아닙니다.
        structured_model = fixture_generation()
    else:
        # 라이브 모델 설정과 Schema를 준비하는 단계입니다. 아직 API를 호출하지 않습니다.
        chat_model = create_chat_model()
        structured_model = chat_model.with_structured_output(
            WireAnswer, method="json_schema", strict=True, include_raw=True)
    bundle = run_generation(prompt, structured_model, prepared["inputs"])
    if bundle is None:
        raise AssertionError("이번 정상 예시의 Context는 비어 있지 않아야 합니다.")
    parsed = bundle.get("parsed")
    cited_ids = list(parsed.source_ids) if parsed is not None else []
    result = {
        "exercise": "06_context_chain",
        "execution": execution_record("offline_fixture" if args.offline else "live", llm=not args.offline),
        "real_model_calls": 0 if args.offline else 1,
        "context": prepared["context"],
        "included_ids": prepared["provided_ids"],
        "included_sources": [dict(doc.metadata) for doc in prepared["included_docs"]],
        "prompt_input": prepared["inputs"],
        "bundle": bundle_record(bundle),
        "observed_source_ids": cited_ids,
        "source_id_membership_only": None if parsed is None else set(cited_ids).issubset(prepared["provided_ids"]),
        "experiments": experiments,
        "human_evidence_review": "pending",
        "review_note": "bundle·포함 ID를 관찰한 기록입니다. 자료형·상태·출처의 승인 검사는 실습07에서 진행합니다.",
    }
    path = save_json(HERE, "context_chain.json", result)
    show_success("06 Context·Runnable 관찰 기록", path)
    print("실제 LLM 실행:", not args.offline, "| 검증 승인 전 bundle 관찰")


if __name__ == "__main__":
    main()
