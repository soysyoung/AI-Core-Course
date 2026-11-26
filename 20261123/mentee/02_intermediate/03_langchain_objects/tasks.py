"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record

COMPONENT_INPUTS = {
    "Document": "page_content와 metadata를 담아 생성",
    "Retriever": "query·category·candidate_k가 있는 dict",
    "Prompt": "question·context가 있는 dict",
    "Chat Model": "ChatPromptValue 또는 메시지 목록",
}

def component_outputs() -> dict[str, str]:
    """강의에서 다룬 네 구성요소의 출력 자료형을 대응시킵니다."""
    # BEGIN D26-03-I01
    # TODO D26-03-I01: 네 구성요소의 반환값을 구분해 dict로 반환합니다.
    # 힌트: Prompt는 ChatPromptValue, Chat Model은 AIMessage입니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-03-I01 TODO 미완성")
    # [추가 설명] 각 부품이 "무엇을 돌려주는지"를 표로 정리합니다.
    # 요리에 비유하면: Document는 재료 카드, Retriever는 재료를 찾아오는 사람(카드 목록을 돌려줌),
    # Prompt는 주문서를 만드는 사람(ChatPromptValue), Chat Model은 요리사(AIMessage 답변)예요.
    # Prompt와 Chat Model의 결과는 이름이 비슷해 헷갈리기 쉬우니 꼭 구분합니다.
    return {
        "Document": "본문·출처를 보관하는 데이터 객체",  # 실행하지 않고 담아 두는 그릇
        "Retriever": "list[Document]",  # 찾아온 Document 여러 장
        "Prompt": "ChatPromptValue",  # 모델에 보낼 메시지 묶음
        "Chat Model": "AIMessage",  # 모델이 만든 답변 메시지
    }
    # END D26-03-I01

def access_kinds() -> dict[str, str]:
    """데이터를 읽는 경우와 invoke로 작업을 실행하는 경우를 구분합니다."""
    # BEGIN D26-03-I02
    # TODO D26-03-I02: Document는 data, 실행 구성요소는 invoke로 표시합니다.
    # 힌트: 값 읽기와 실행을 구분합니다. 여기서는 실제 API 호출을 하지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-03-I02 TODO 미완성")
    # [추가 설명] "읽기만 하는 것"과 "일을 시키는 것"을 나눕니다.
    # Document는 공책처럼 펼쳐서 읽기만 하면 되니 data,
    # 나머지 셋은 .invoke(입력)으로 일을 시켜야 결과가 나오니 invoke입니다.
    # 여기서는 표만 만들 뿐, 실제로 invoke를 호출하지는 않아요.
    return {
        "Document": "data",
        "Retriever": "invoke",
        "Prompt": "invoke",
        "Chat Model": "invoke",
    }
    # END D26-03-I02

def repair_swapped_returns(swapped: dict[str, str]) -> dict[str, str]:
    """입력 표를 복사하고 Prompt와 Chat Model의 잘못된 출력만 고칩니다."""
    # BEGIN D26-03-I03
    # TODO D26-03-I03: 잘못된 표를 복사해 Prompt·Chat Model의 출력 두 곳을 고칩니다.
    # 힌트: component_outputs에서 올바른 값을 읽고 원본 dict는 유지합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-03-I03 TODO 미완성")
    # [추가 설명] 틀린 표를 "복사본"에서 고칩니다. 원본은 비교용으로 그대로 남겨야 해요.
    # {**swapped}는 같은 내용의 새 dict를 만드는 문법이라, 복사본을 고쳐도 원본은 안 바뀝니다.
    # 바꿔 적힌 두 칸(Prompt·Chat Model)만 올바른 표(component_outputs)의 값으로 덮어씁니다.
    correct = component_outputs()
    repaired = {**swapped}  # 원본 보존용 복사
    repaired["Prompt"] = correct["Prompt"]
    repaired["Chat Model"] = correct["Chat Model"]
    return repaired
    # END D26-03-I03

def main():
    outputs = component_outputs()
    access = access_kinds()
    report = {
        "execution": execution_record("concept_review"),
        "components": [{"component": name, "input": value,
                        "output": outputs[name], "access": access[name]}
                       for name, value in COMPONENT_INPUTS.items()],
        "observation": "입력·출력 대응표; Prompt·모델 invoke는 실행하지 않음",
    }
    before = {**outputs, "Prompt": "AIMessage", "Chat Model": "ChatPromptValue"}
    report["before"] = before
    report["after"] = repair_swapped_returns(before)
    path = save_json(HERE, "object_contracts.json", report)
    show_success("03 응용", path)

if __name__ == "__main__":
    main()
