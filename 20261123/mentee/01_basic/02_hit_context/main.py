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
    # BEGIN D26-02-B01
    # TODO D26-02-B01: [ID] 원문위치, 줄바꿈, 본문 순서로 한 블록을 만듭니다.
    # 힌트: citation_id·source_locator·body를 읽어 f-string으로 연결합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-02-B01 TODO 미완성")
    # [추가 설명] hit은 "근거 카드 한 장"입니다. 이 카드를 읽기 좋은 한 덩어리 글로 바꿉니다.
    # 모양은 이렇습니다: 첫 줄에 [번호] 원문위치, 그 다음 줄에 본문.
    # 예) [201] attendance_v2.md#sec-1
    #     수업 시작 후 15분까지 ...
    # 줄바꿈 기호는 \n 이고, f-string(f"...")은 {} 안에 값을 끼워 넣는 문장 틀이에요.
    return f"[{hit['citation_id']}] {hit['source_locator']}\n{hit['body']}"
    # END D26-02-B01

def make_context(hits: list[dict], max_items: int = 2) -> tuple[str, list[int]]:
    """앞에서 최대 max_items건을 골라 Context와 같은 선택의 ID 목록을 반환합니다."""
    # BEGIN D26-02-B02
    # TODO D26-02-B02: 앞의 최대 2건에서 블록과 ID를 함께 모아 반환합니다.
    # 힌트: 선택한 Hit마다 format_hit을 호출하고, 블록은 줄바꿈 두 개(빈 줄 하나)로 연결합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-02-B02 TODO 미완성")
    # [추가 설명] 카드 묶음(hits)에서 "앞에서부터 max_items장"만 골라 하나의 글(Context)로 합칩니다.
    # 중요한 점: 글에 넣은 카드의 번호만 번호 목록(ids)에도 똑같이 담아야 합니다.
    # (글에는 없는데 목록에만 있으면 거짓 정보가 되니까요!)
    selected = hits[:max_items]  # 앞에서 max_items장만 고름 (원래 목록은 건드리지 않아요)
    blocks = [format_hit(hit) for hit in selected]  # 카드마다 한 덩어리 글로 바꿈
    ids = [hit["citation_id"] for hit in selected]  # 고른 카드의 번호만 모음
    # 덩어리 사이에는 빈 줄이 하나 생기도록 줄바꿈 두 개로 이어 붙입니다.
    # 카드가 하나도 없으면 빈 글 ""과 빈 목록 []이 나오고, 가짜 카드로 채우지 않습니다.
    return "\n\n".join(blocks), ids
    # END D26-02-B02

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
    show_success("02 기본필수", path)

if __name__ == "__main__":
    main()
