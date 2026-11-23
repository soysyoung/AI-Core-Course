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
    # BEGIN D26-03-B01
    # TODO D26-03-B01: 네 구성요소의 반환값을 구분해 dict로 반환합니다.
    # 힌트: Prompt는 ChatPromptValue, Chat Model은 AIMessage입니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-03-B01 TODO 미완성")
    # [추가 설명] 네 가지 도구가 "일을 마치고 무엇을 돌려주는지"를 짝지어 적는 표입니다.
    # 자판기에 비유하면: 돈(입력)을 넣고 나오는 물건(출력)이 도구마다 다르다는 뜻이에요.
    return {
        "Document": "본문·출처를 보관하는 데이터 객체",  # 글과 출처를 담아 두는 "메모 카드"
        "Retriever": "list[Document]",  # 질문에 맞는 메모 카드들을 찾아 "목록"으로 돌려줍니다.
        "Prompt": "ChatPromptValue",  # 질문+근거를 "모델에게 보낼 편지"로 만든 결과입니다.
        "Chat Model": "AIMessage",  # 모델이 편지를 읽고 쓴 "답장"입니다. (편지와 답장은 다른 물건!)
    }
    # END D26-03-B01

def access_kinds() -> dict[str, str]:
    """데이터를 읽는 경우와 invoke로 작업을 실행하는 경우를 구분합니다."""
    # BEGIN D26-03-B02
    # TODO D26-03-B02: Document는 data, 실행 구성요소는 invoke로 표시합니다.
    # 힌트: 값 읽기와 실행을 구분합니다. 여기서는 실제 API 호출을 하지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-03-B02 TODO 미완성")
    # [추가 설명] "그냥 읽는 것(data)"과 "일을 시키는 것(invoke)"을 구분합니다.
    # Document는 적힌 내용을 읽기만 하는 메모장이라 data입니다.
    # 나머지 셋은 invoke("실행해 줘!")라고 시켜야 일을 하는 도구라서 invoke입니다.
    # 여기서는 표시만 하고, 실제로 실행(API 호출)은 하지 않아요.
    return {
        "Document": "data",  # 읽기만 하는 데이터
        "Retriever": "invoke",  # 실행해서 검색 결과를 받음
        "Prompt": "invoke",  # 실행해서 메시지를 만듦
        "Chat Model": "invoke",  # 실행해서 답을 받음
    }
    # END D26-03-B02

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
    path = save_json(HERE, "object_contracts.json", report)
    show_success("03 기본필수", path)

if __name__ == "__main__":
    main()
