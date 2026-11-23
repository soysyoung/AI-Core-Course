"""Day22 · 사용량·시간·비용 | PPT 39~46 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from decimal import Decimal as D
from coursekit.support import parse_args, guarded
from coursekit.io import read_json
from coursekit.response import get
from coursekit.metrics import estimate_cost as checkpoint_cost
from coursekit.labs import usage_lab

def usage_of(response):
    # TODO D22-05-B01: 사용량이 없으면 None, 있으면 입력·출력과부분 상세를 읽으세요.
    # 입력·완료 기준: 없는 값에 or0을 쓰지 않습니다. delta 개수를출력 Token 수로쓰지 않습니다.
    # BEGIN D22-05-B01
    u = get(response, "usage")
    # 쉬운 설명: AI가 "이번에 글자 조각(Token)을 얼마나 썼는지" 적어 준 영수증(usage)을 읽는 곳이에요.
    # 영수증이 아예 없으면 "모르겠음"이라는 뜻으로 None을 돌려줘요. 0이라고 적으면
    # "공짜였다"는 뜻이 되어 틀리니까, 없는 값에 or 0을 쓰면 안 돼요.
    if u is None:
        return None
    values = {"input_tokens": get(u, "input_tokens"), "output_tokens": get(u, "output_tokens"),
              # cached_tokens: 입력 중 "전에 본 적 있어서 싸게 계산되는" 부분 (input_tokens_details 안에 있어요)
              "cached_tokens": get(get(u, "input_tokens_details"), "cached_tokens"),
              # reasoning_tokens: 출력 중 AI가 속으로 생각하는 데 쓴 부분 (output_tokens_details 안에 있어요)
              "reasoning_tokens": get(get(u, "output_tokens_details"), "reasoning_tokens"),
              "total_tokens": get(u, "total_tokens")}
    # u가없으면None. 상세는 get(get(u,"..._details"),"..._tokens")
    return values  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-05-B01

def calculate(usage, model, *, service_tier="default"):
    checked=checkpoint_cost(usage,model,service_tier=service_tier)
    if checked["estimated_usd"] is None:
        return checked
    from coursekit.io import ROOT
    price=read_json(ROOT/"config"/"prices.json")["models"][model]
    # TODO D22-05-B02: 캐시를제외한 입력·캐시입력·출력 비용을 Decimal로 계산하세요.
    # 입력·완료 기준: 가격은 USD/100만Token입니다. reasoning을출력에다시더하지 않습니다. unknown과0구분.
    # BEGIN D22-05-B02
    i = usage["input_tokens"]
    c = usage["cached_tokens"]
    o = usage["output_tokens"]
    # 쉬운 설명: 영수증의 Token 수에 가격표를 곱해서 대략 얼마인지(USD) 계산해요.
    # 입력은 두 종류예요. 캐시(전에 본 것)는 싸고, 캐시가 아닌 것은 보통 가격이에요.
    # 그래서 "입력 전체 - 캐시 입력"이 캐시 아닌 입력이에요.
    # 가격표는 "100만 Token당 가격"이라서 마지막에 1,000,000으로 나눠요.
    # float(소수)로 계산하면 0.1 같은 값이 살짝 틀어질 수 있어서, 정확한 Decimal(D)을 써요.
    # reasoning(속으로 생각한 Token)은 이미 output 안에 들어 있으니까 또 더하지 않아요.
    uncached = i - c  # 입력 전체 - 캐시 입력
    amount = (uncached * D(price["input_per_million"]) + c * D(price["cached_input_per_million"])
              + o * D(price["output_per_million"])) / D(1000000)  # 각 token수×해당단가의 합 / D(1000000)
    # 반환은 dict(checked, estimated_usd=str(amount))
    return dict(checked, estimated_usd=str(amount))  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-05-B02

def make_row(result, attempt, cost):
    # TODO D22-05-B03: 시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.
    # 입력·완료 기준: 이 도구는 기존 run.json을 읽습니다. 측정을 위해 필요없는유료재호출은하지 않습니다.
    # BEGIN D22-05-B03
    row = {"run_id": result["run_id"], "source_mode": result["source_mode"]}
    # 쉬운 설명: 표의 "한 줄"을 만들어요. 몇 번째 시도인지, 진짜/모의 중 뭐였는지,
    # 걸린 시간, 쓴 Token 수, 비용을 한 줄에 같이 적어 두면 나중에 비교하기 쉬워요.
    # 이미 저장된 run.json 기록을 읽기만 하고, 돈이 드는 AI 호출은 새로 하지 않아요.
    # 값이 없으면 .get()이 None을 돌려줘서, 모르는 값을 0으로 속이지 않아요.
    row.update(send_attempt=attempt.get("send_attempt"), request_ms=attempt.get("request_ms"),
               first_text_ms=attempt.get("first_text_ms"), usage=attempt.get("usage"), **cost)
    # attempt에서 send_attempt·request_ms·first_text_ms·usage를읽고 cost와합칩니다.
    return row  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-05-B03

def main():
    args=parse_args(HERE)
    usage_lab(args,usage_reader=usage_of,calculator=calculate,row_builder=make_row)

if __name__=="__main__":
    guarded(main)
