"""Day22 · AI 지식 답변 생성기 v2 | PPT 60~68 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args, daily_project
from coursekit.io import write_json
from coursekit.metrics import summarize_runs
from coursekit.records import table_rows

def project_cases():
    # TODO D22-08-I01: 최종연동확인질문H01·H02·H03을같은순서로지정하세요.
    # 입력·완료 기준: 이미본질문이므로새holdout의일반화성능이라고부르지않습니다.
    # BEGIN D22-08-I01
    # 쉬운 설명: 마지막 종합 실습에서 물어볼 질문 3개를 H01, H02, H03 순서로 정해요. H01은 스트리밍으로 받아요.
    # 이미 본 질문이라서 "처음 보는 문제에서도 잘한다"는 증거로 쓰면 안 돼요.
    cases = ["H01", "H02", "H03"]  # H01→H02→H03. H01은Streaming입니다.
    return cases
    # END D22-08-I01

def project_rows(runs):
    # TODO D22-08-I02: 각실행의상태·사용량·시간을표행으로연결하세요.
    # 입력·완료 기준: 실패한행도버리지않습니다. 모든질문의예상답을실측답으로채우지않습니다.
    # BEGIN D22-08-I02
    # 쉬운 설명: 실행 결과들을 표(CSV)의 줄로 바꿔요. 실패한 줄도 버리지 않고, 모르는 값은 unknown으로 남겨요.
    # 예상 답을 진짜로 얻은 답처럼 채워 넣지 않아요.
    rows = table_rows(runs)  # table_rows(runs)는unknown과source구분에필요한필드를제공합니다.
    return rows
    # END D22-08-I02

def project_summary(runs):
    # TODO D22-08-I03: 실제·모의·캐시·미실행을분리하여요약하세요.
    # 입력·완료 기준: 소수관찰로P95·SLA·보편적모델우열을주장하지않습니다.
    # BEGIN D22-08-I03
    # 쉬운 설명: 진짜 호출(api_live)·모의(simulated)·캐시(app_cache)·실행 안 함(not_run)을 따로 세어요.
    # 섞으면 모의 결과가 진짜 성능처럼 보여요. 몇 번 안 되는 관찰로 "항상 빠르다" 같은 말은 하지 않아요.
    summary = summarize_runs(runs)  # summarize_runs(runs)
    return summary
    # END D22-08-I03

def check_project(runs):
    # TODO D22-08-I04: 자동검사후사람미평가None을유지하고전송상한을확인하세요.
    # 입력·완료 기준: 사람평가는tools/review.py의별도파일로남깁니다. 새API·DB·RAG는만들지않습니다.
    # BEGIN D22-08-I04
    for run in runs:
        evidence = run.get("evidence_ok")  # 사람평가전None
        sends = run.get("new_api_send_count", 0)
        # 쉬운 설명: (1) 사람이 아직 평가 안 했으니 evidence_ok는 None 그대로여야 해요(컴퓨터가 마음대로 채우면 안 돼요).
        # (2) 새로 API에 보낸 횟수가 4번을 넘지 않아야 해요. 돈이 새는 걸 막는 안전장치예요.
        assert evidence is None, f"사람 평가 전인데 evidence_ok가 채워졌습니다: {evidence}"
        assert sends <= 4, f"새 API 전송이 4번을 넘었습니다: {sends}"
    # END D22-08-I04

def compare_first_and_last(runs):
    # TODO D22-08-I05: 최초시도와마지막시도의상태를분리하여보존하세요.
    # 입력·완료 기준: 첫실패를마지막성공으로덮어쓰지않습니다.
    # BEGIN D22-08-I05
    rows = []
    for run in runs:
        attempts = run.get("attempts", [])
        # first_error·last_status·attempt_count를서로다른필드에보관합니다.
        # 쉬운 설명: 한 질문에 여러 번 시도했다면 "처음 시도에서 난 오류"와 "마지막 결과"를 따로 적어요.
        # 처음에 실패하고 나중에 성공해도 처음 실패 기록을 지우지 않으려는 거예요. attempts가 없으면 None이에요.
        rows.append({"case_id": run.get("case_id"),
                     "first_error": attempts[0].get("error") if attempts else None,
                     "last_status": run.get("run_status"),
                     "attempt_count": len(attempts)})
    return rows
    # END D22-08-I05

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    runs=daily_project(args,prepare_cases=project_cases,make_table=project_rows,finish_summary=project_summary)
    if isinstance(runs,list):
        check_project(runs)
        write_json(args.output_dir/"first_vs_final.json",compare_first_and_last(runs))
