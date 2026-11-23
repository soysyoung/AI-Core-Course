"""Day22 · AI 지식 답변 생성기 v2 | PPT 60~68 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded, daily_project
from coursekit.metrics import summarize_runs
from coursekit.records import table_rows

def project_cases():
    # TODO D22-08-B01: 최종연동확인질문H01·H02·H03을같은순서로지정하세요.
    # 입력·완료 기준: 이미본질문이므로새holdout의일반화성능이라고부르지않습니다.
    # BEGIN D22-08-B01
    # 쉬운 설명: 마지막 종합 실습에서 물어볼 질문 3개를 H01, H02, H03 순서로 정해요. H01은 스트리밍으로 받아요.
    # 이미 본 질문이라서 "처음 보는 문제에서도 잘한다"는 증거로 쓰면 안 돼요.
    cases = ["H01", "H02", "H03"]  # H01→H02→H03. H01은Streaming입니다.
    return cases  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-08-B01

def project_rows(runs):
    # TODO D22-08-B02: 각실행의상태·사용량·시간을표행으로연결하세요.
    # 입력·완료 기준: 실패한행도버리지않습니다. 모든질문의예상답을실측답으로채우지않습니다.
    # BEGIN D22-08-B02
    # 쉬운 설명: 실행 결과들을 표(CSV)의 줄로 바꿔요. 실패한 줄도 버리지 않고, 모르는 값은 unknown으로 남겨요.
    # 예상 답을 진짜로 얻은 답처럼 채워 넣지 않아요. 이미 만들어진 table_rows가 이걸 해 줘요.
    rows = table_rows(runs)  # table_rows(runs)는unknown과source구분에필요한필드를제공합니다.
    return rows  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-08-B02

def project_summary(runs):
    # TODO D22-08-B03: 실제·모의·캐시·미실행을분리하여요약하세요.
    # 입력·완료 기준: 소수관찰로P95·SLA·보편적모델우열을주장하지않습니다.
    # BEGIN D22-08-B03
    # 쉬운 설명: 진짜 호출(api_live)·모의(simulated)·캐시(app_cache)·실행 안 함(not_run)을 따로따로 세어요.
    # 섞어서 합치면 모의 결과가 진짜 성능처럼 보여요. 몇 번 안 되는 관찰로 "항상 빠르다" 같은 말은 하지 않아요.
    summary = summarize_runs(runs)  # summarize_runs(runs)
    return summary  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-08-B03

def check_project(runs):
    # TODO D22-08-B04: 자동검사후사람미평가None을유지하고전송상한을확인하세요.
    # 입력·완료 기준: 사람평가는tools/review.py의별도파일로남깁니다. 새API·DB·RAG는만들지않습니다.
    # BEGIN D22-08-B04
    for run in runs:
        evidence = run.get("evidence_ok")  # 사람평가전None
        sends = run.get("new_api_send_count", 0)
        # 쉬운 설명: 두 가지를 확인해요. (1) 사람이 아직 평가 안 했으니 evidence_ok는 None 그대로여야 해요(컴퓨터가 마음대로 True로 채우면 안 돼요).
        # (2) 새로 API에 보낸 횟수가 4번을 넘지 않아야 해요. 돈이 새는 걸 막는 안전장치예요.
        assert evidence is None, f"사람 평가 전인데 evidence_ok가 채워졌습니다: {evidence}"
        assert sends <= 4, f"새 API 전송이 4번을 넘었습니다: {sends}"
    # END D22-08-B04

def main():
    args=parse_args(HERE)
    runs=daily_project(args,prepare_cases=project_cases,make_table=project_rows,finish_summary=project_summary)
    if isinstance(runs,list):
        check_project(runs)

if __name__=="__main__":
    guarded(main)
