"""Day22 · 명시적 모델 선택 | PPT 53~59 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded
from coursekit.config import choose_model as checkpoint_choose
from coursekit.labs import routing_lab

def route(mode, models):
    # TODO D22-07-B01: fast·quality만허용하고실제모델과선택이유를반환하세요.
    # 입력·완료 기준: 알수없는모드를fast로조용히바꾸지않습니다. quality권한없으면not_run입니다.
    # BEGIN D22-07-B01
    allowed = {"fast", "quality"}
    # 쉬운 설명: "빠른 모델(fast)"과 "품질 좋은 모델(quality)" 중 사용자가 직접 고른 것만 써요.
    # 이상한 이름이 오면 몰래 fast로 바꾸지 않고 오류를 내요. quality 모델이 설정 안 됐을 때도
    # 다른 모델로 슬쩍 바꾸지 않고 멈춰요(= not_run). 미리 만들어진 checkpoint_choose가 이 검사를 다 해 줘요.
    model, reason = checkpoint_choose(mode, models)  # reason은 "explicit_mode:fast" 같은 선택 이유예요.
    return (model, reason)  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-07-B01

def record_view(result):
    # TODO D22-07-B02: 어떤모델이든동일한결과필드로비교하세요.
    # 입력·완료 기준: 고가모델이항상더좋다는결론을미리넣지않습니다.
    # BEGIN D22-07-B02
    fields = ["case_id", "source_mode", "model", "route_reason", "run_status",
              "answer_object", "evidence_ok", "usage", "request_ms", "estimated_usd"]
    # 쉬운 설명: 어떤 모델로 실행했든 똑같은 칸(fields)으로 한 줄 요약을 만들어요. 그래야 공평하게 비교돼요.
    # 값이 없으면 .get()이 None을 줘서 모르는 값을 0으로 속이지 않아요. "비싼 모델이 더 좋다"는 결론은 미리 넣지 않아요.
    row = {key: result.get(key) for key in fields}
    return row  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-07-B02

def comparison_modes():
    # TODO D22-07-B03: 명시적비교에서만fast·quality를한번씩선택하세요.
    # 입력·완료 기준: 기본run은한모델만호출합니다. compare는계정권한·예산확인후선택합니다.
    # BEGIN D22-07-B03
    # 쉬운 설명: 비교할 때만 fast와 quality를 딱 한 번씩 써요. 실패했다고 반복(while)하거나 자동으로 다른 모델로 넘기지 않아요.
    modes = ["fast", "quality"]  # fast와quality각한번, while fallback금지
    return modes  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-07-B03

def main():
    args=parse_args(HERE)
    routing_lab(args,router=route,record_view=record_view,compare_modes=comparison_modes)

if __name__=="__main__":
    guarded(main)
