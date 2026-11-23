"""Day22 · 오류와 제한 재시도 | PPT 32~38 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args
from coursekit.errors import classify_error as checkpoint_classify
from coursekit.runner import RetryPolicy
from coursekit.labs import failure_scenarios

def classify(error):
    # TODO D22-04-I01: 401·403은 중단하고, 429의 quota와 일시적 제한을 구분하세요.
    # 입력·완료 기준: 알 수 없는429는 무조건 재시도하지 않습니다. 실제로 제한을 유발하는 호출은 금지합니다.
    # BEGIN D22-04-I01
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
        # 쉬운 설명: 429는 "너무 많이 요청했어요"인데 종류가 나뉘어요.
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
    return result
    # END D22-04-I01

def make_policy():
    # TODO D22-04-I02: 생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.
    # 입력·완료 기준: SDK max_retries=0은 제공 코드에 설정되어 있습니다. 무한 fallback을 추가하지 않습니다.
    # BEGIN D22-04-I02
    # 쉬운 설명: "최대 몇 번까지 다시 해 볼지" 한계를 정해요. 끝없이 반복하면 돈과 시간이 새니까요.
    # max_generations: 답을 새로 만들어 달라고 하는 횟수는 최대 2번
    # max_sends_per_generation: 한 번 만들 때 요청을 보내는 횟수는 최대 2번
    # max_sends_total: 전부 합쳐서 요청은 최대 4번 (2 x 2 = 4)
    limits = {"max_generations": 2, "max_sends_per_generation": 2, "max_sends_total": 4}
    # RetryPolicy(**limits, elapsed_budget_s=60.0)
    return RetryPolicy(**limits, elapsed_budget_s=60.0)  # 60초가 넘으면 더 기다리지 않고 멈춰요.
    # END D22-04-I02

def delay(attempt, retry_after_s, remaining_s, jitter=0.0):
    # TODO D22-04-I03: 헤더 최소 대기와 지수 대기 중 큰 값을 계산하세요.
    # 입력·완료 기준: 함수에 전달되는 헤더값은 이미 검증된 초 단위입니다.
    # BEGIN D22-04-I03
    hinted = 0.0 if retry_after_s is None else retry_after_s
    # 쉬운 설명: 다시 시도하기 전에 얼마나 쉴지 계산해요. 두 후보 중 "더 긴 쪽"을 골라요.
    # (1) 서버가 "n초 뒤에 오세요"라고 알려 준 최소 대기(hinted) - 이보다 짧게 쉬면 안 돼요.
    # (2) 지수 대기: 시도할수록 1, 2, 4, 8초처럼 두 배씩 늘어나는 대기 (최대 8초)
    # jitter는 여러 사람이 동시에 다시 오지 않도록 살짝 더하는 흔들림 시간이에요.
    wait = max(hinted, min(8.0, 2 ** min(attempt - 1, 3))) + jitter  # max(최소 대기, 지수 대기) + jitter
    # END D22-04-I03
    # TODO D22-04-I04: 대기시간이 남은 작업 예산 이상이면 None으로 중단하세요.
    # 입력·완료 기준: 대기 후 실행기는 남은 예산과 횟수를 다시 검사합니다.
    # BEGIN D22-04-I04
    # 쉬운 설명: 기다릴 시간이 남은 시간보다 길거나 같으면 기다리다가 시간이 다 가 버리니까
    # None(= 이번엔 포기)을 돌려줘요. 대기를 억지로 짧게 줄이면 서버가 정한 최소 대기를 어기게 돼요.
    if wait >= remaining_s:
        return None
    return wait  # None / wait 중 선택합니다. min(wait, remaining_s)로당기지 않습니다.
    # END D22-04-I04

def check_attempts(results):
    # TODO D22-04-I05: 각 시도의 번호가 누락되지 않고 총4이하인지 확인하세요.
    # 입력·완료 기준: 실패한 첫 시도도 목록에서 지우지 않습니다.
    # BEGIN D22-04-I05
    for result in results:
        attempts = result["attempts"]
        # 쉬운 설명: 요청을 보낸 기록에 번호표(send_attempt)가 1, 2, 3... 순서대로 빠짐없이 붙었는지,
        # 그리고 전부 합쳐 4번을 넘지 않았는지 확인해요. 첫 번째로 실패한 시도도 지우면 안 돼요.
        numbers = [a["send_attempt"] for a in attempts]
        if numbers != list(range(1, len(attempts) + 1)) or len(attempts) > 4:
            raise ValueError(f"시도 번호가 잘못됐거나 4번을 넘었습니다: {numbers}")
        # 번호는1부터연속, 길이는4이하입니다.
    # END D22-04-I05

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    results=failure_scenarios(args,classifier=classify,delay=delay,policy=make_policy())
    check_attempts(results)
