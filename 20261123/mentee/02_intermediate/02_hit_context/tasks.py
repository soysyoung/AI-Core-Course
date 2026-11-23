"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record

def format_hit(hit: dict) -> str:
    """Hit 한 건의 ID·위치·본문을 한 문자열 블록으로 반환합니다."""
    # BEGIN D26-02-I01
    # TODO D26-02-I01: [ID] 원문위치, 줄바꿈, 본문 순서로 한 블록을 만듭니다.
    # 힌트: citation_id·source_locator·body를 읽어 f-string으로 연결합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-02-I01 TODO 미완성")
    # [추가 설명] hit은 "근거 카드 한 장"입니다. 이 카드를 읽기 좋은 한 덩어리 글로 바꿉니다.
    # 모양: 첫 줄에 [번호] 원문위치, 그 다음 줄에 본문.
    # 예) [201] attendance_v2.md#sec-1
    #     수업 시작 후 15분까지 ...
    # 줄바꿈 기호는 \n 이고, f-string(f"...")은 {} 안에 값을 끼워 넣는 문장 틀이에요.
    return f"[{hit['citation_id']}] {hit['source_locator']}\n{hit['body']}"
    # END D26-02-I01

def select_hits(hits: list[dict], max_items: int = 2) -> list[dict]:
    """입력 순서를 유지해 앞의 최대 max_items건만 고릅니다."""
    # BEGIN D26-02-I02
    # TODO D26-02-I02: 입력 순서대로 앞의 최대 max_items건을 선택합니다.
    # 힌트: 목록 슬라이스를 사용합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-02-I02 TODO 미완성")
    # [추가 설명] 카드 묶음에서 "앞에서부터 max_items장"만 뽑습니다.
    # hits[:max_items]는 "처음부터 max_items번째 앞까지 잘라 줘"라는 뜻이에요. (슬라이스)
    # 새 목록이 만들어지니 원래 목록은 그대로이고, 카드가 모자라면 있는 만큼만 나옵니다.
    return hits[:max_items]
    # END D26-02-I02

def make_context(hits: list[dict], max_items: int = 2) -> tuple[str, list[int]]:
    """선택한 목록에서 Context와 포함 ID를 동시에 만듭니다."""
    # BEGIN D26-02-I03
    # TODO D26-02-I03: 선택 결과를 문자열로 연결하고 같은 Hit의 citation_id 목록을 반환합니다.
    # 힌트: 본문과 ID 수집을 같은 for 반복문 안에 둡니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-02-I03 TODO 미완성")
    # [추가 설명] 글(Context)과 번호 목록(ids)을 "같은 반복문 안에서 동시에" 만듭니다.
    # 같은 카드를 보면서 글과 번호를 함께 챙겨야, 글에 없는 번호가 목록에 끼는 실수가 없어요.
    blocks = []  # 카드별 글 덩어리를 담을 빈 상자
    ids = []  # 고른 카드의 번호를 담을 빈 상자
    for hit in select_hits(hits, max_items):  # 앞에서 만든 함수로 카드를 고름
        blocks.append(format_hit(hit))  # 이 카드의 글 덩어리 추가
        ids.append(hit["citation_id"])  # 같은 카드의 번호 추가
    # 덩어리 사이는 빈 줄 하나(\n\n)로 이어 붙입니다. 카드가 없으면 빈 글 ""과 빈 목록 []이 됩니다.
    return "\n\n".join(blocks), ids
    # END D26-02-I03

def main():
    hit = example_hit()
    context, included_ids = make_context([hit])
    report = {
        "execution": execution_record("local_python"),
        "context": context,
        "included_ids": included_ids,
        "input_source": "lecture_fixture",
        "character_count": len(context),
    }
    path = save_json(HERE, "hit_context.json", report)
    show_success("02 응용", path)

if __name__ == "__main__":
    main()
