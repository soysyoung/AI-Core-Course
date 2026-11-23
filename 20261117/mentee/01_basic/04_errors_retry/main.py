"""Day22 · 오류와 제한 재시도 | PPT 32~38 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded
from coursekit.errors import classify_error as checkpoint_classify, retry_delay as checkpoint_delay
from coursekit.runner import RetryPolicy
from coursekit.labs import failure_scenarios

def classify(error):
    # TODO D22-04-B01: 401·403은 중단하고, 429의 quota와 일시적 제한을 구분하세요.
    # 입력·완료 기준: 알 수 없는429는 무조건 재시도하지 않습니다. 실제로 제한을 유발하는 호출은 금지합니다.
    # BEGIN D22-04-B01
    status = error.status
    codes = {error.code, error.error_type}
    # 쉬운 설명: 에러 번호(status)를 보고 "다시 해 볼까, 그만둘까"를 정해요. retryable은 "다시 시도해도 되나?"예요.
    # 401(열쇠가 틀림)은 아무리 기다려도 열쇠가 저절로 바뀌지 않으니까 False(재시도 안 함)예요.
    # 403(권한 없음)도 기다린다고 권한이 생기지 않으니까 똑같이 중단해요.
    if status == 401:
        result = {"kind": "auth_error", "retryable": False}  # 기다려도 키는 바뀌지 않습니다.
    elif status == 403:
        result = {"kind": "permission_error", "retryable": False}
    elif status == 429:
        # 쉬운 설명: 429는 "너무 많이 요청했어요"인데 두 종류가 있어요.
        # (1) quota: 돈/사용량 한도가 다 찬 것 → 기다려도 안 풀리니까 중단
        # (2) rate_limit: 잠깐 몰려서 막힌 것 → 조금 기다리면 되니까 재시도
        # (3) 이유를 모르는 429: 함부로 계속 시도하면 안 되니까 재시도하지 않아요.
        if codes & {"insufficient_quota", "billing_hard_limit_reached", "billing_not_active", "usage_limit_reached"}:
            result = {"kind": "quota_error", "retryable": False}  # quota이면중단, rate_limit_exceeded면제한 재시도
        elif codes & {"rate_limit_exceeded", "rate_limit_error", "requests", "tokens"}:
            result = {"kind": "rate_limit", "retryable": True}
        else:
            result = {"kind": "unknown_429", "retryable": False}
    else:
        # 쉬운 설명: 나머지 에러(서버 오류 등)는 이미 만들어진 분류 함수에게 맡겨요.
        result = checkpoint_classify(error)
    # 그 외는 checkpoint_classify(error)를 이용합니다.
    return result  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-04-B01

def make_policy():
    # TODO D22-04-B02: 생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.
    # 입력·완료 기준: SDK max_retries=0은 제공 코드에 설정되어 있습니다. 무한 fallback을 추가하지 않습니다.
    # BEGIN D22-04-B02
    # 쉬운 설명: "최대 몇 번까지 다시 해 볼지" 한계를 정해요. 끝없이 반복하면 돈과 시간이 새니까요.
    # max_generations: 답을 새로 만들어 달라고 하는 횟수는 최대 2번
    # max_sends_per_generation: 한 번 만들 때 요청을 보내는 횟수는 최대 2번
    # max_sends_total: 전부 합쳐서 요청은 최대 4번 (2 x 2 = 4)
    limits = {"max_generations": 2, "max_sends_per_generation": 2, "max_sends_total": 4}
    # RetryPolicy(**limits, elapsed_budget_s=60.0)
    return RetryPolicy(**limits, elapsed_budget_s=60.0)  # 60초가 넘으면 더 기다리지 않고 멈춰요.
    # END D22-04-B02

def delay(attempt, retry_after_s, remaining_s, jitter=0.0):
    # TODO D22-04-B03: 제공된 대기 함수에 남은 예산을 전달하고 반환값을 유지하세요.
    # 입력·완료 기준: 서버의 최소 대기를 짧게 줄이지 않습니다.
    # BEGIN D22-04-B03
    # 쉬운 설명: 다시 시도하기 전에 "얼마나 쉬었다 갈지"를 계산해요. 이미 있는 계산 함수에
    # 남은 시간(remaining_s)을 같이 넘겨요. 서버가 "n초 뒤에 오세요"라고 하면(retry_after_s)
    # 그보다 짧게 줄이지 않아요. 남은 시간 안에 못 기다리면 None이 나오는데,
    # None은 "이번엔 포기"라는 뜻이라서 0으로 바꾸면 안 돼요.
    wait = checkpoint_delay(attempt, retry_after_s, remaining_s, jitter)  # checkpoint_delay(attempt, retry_after_s, remaining_s, jitter)
    # None은 이번 실행을중단한다는 뜻입니다. 0으로 바꾸지 않습니다.
    return wait  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-04-B03

def main():
    args=parse_args(HERE)
    results=failure_scenarios(args,classifier=classify,delay=delay,policy=make_policy())

if __name__=="__main__":
    guarded(main)
