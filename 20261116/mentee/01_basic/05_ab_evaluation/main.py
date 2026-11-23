"""Day21 실습 05: 개선용 질문 A/B 비교. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, run
from coursekit.prompting import BASE_RULE, ADDED_RULE, make_bundle

# 기준: Day21 PPT 37~45장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.experiments import prepare_experiment, review_experiment, summarize, write_summary
from coursekit.retry import run_fixture_scenarios
from coursekit.io import check_name

def choose_bundle(bundle_path=None):
    if bundle_path is not None:
        raise ValueError("05는 새 A/B를 설계합니다. --bundle은 08에서 사용하세요.")
    # TODO D21-05-B01: A의 규칙을 유지하면서 B에 근거 부족 규칙 한 개만 추가하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 질문·문맥·계약·예제는 같고 B의 근거 규칙 1개만 다릅니다.
    # 핵심: 02의 예제 교체 실험과 05의 근거 규칙 실험을 한 비교로 섞지 않습니다.
    # BEGIN D21-05-B01
    rule_a = BASE_RULE
    rule_b = rule_a + "\n" + ""  # TODO: ADDED_RULE 추가
    # 이번 A/B의 예제 유무는 둘 다 동일합니다(여기서는 0개).
    bundle = make_bundle(rule_a=rule_a, rule_b=rule_b, examples=[])
    # [해설-중학생용] 위의 rule_b는 "\n" 뒤에 ""(빈 글)을 붙여서 A와 똑같은 규칙이었어요. 그러면 A/B가 같아서 비교가 안 돼요.
    #  A/B 비교는 "딱 하나만 다르게" 해야 원인을 알 수 있어요(달리기에서 신발만 바꿔 신고 기록을 재는 것과 같아요).
    #  그래서 B에만 '근거가 부족하면 모른다고 답하라'는 규칙(ADDED_RULE) 한 개를 더하고, 질문·예제·출력 모양은 그대로 둬요.
    #  예제 바꾸기 실험(02번)과 섞지 않으려고 예제는 둘 다 0개로 같아요.
    rule_b = rule_a + "\n" + ADDED_RULE
    bundle = make_bundle(rule_a=rule_a, rule_b=rule_b, examples=[])
    # [해설] 아래 raise는 "아직 숙제 안 했어요!" 하고 멈추는 경고문이에요. 숙제를 끝냈으니 #으로 잠재웠어요.
    # raise NotImplementedError("D21-05-B01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-05-B01
    return bundle

def choose_cases():
    # TODO D21-05-B02: 개선용 D01~D03 세 질문만 선택하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기본필수 3질문 × A/B = 첫 응답 6개. 예상 행동을 Prompt에 넣지 않습니다.
    # BEGIN D21-05-B02
    cases = read_json(DATA/"dev_v1.json")
    expected_ids = []  # TODO: D01, D02, D03
    # TODO: cases의 case_id 목록과 expected_ids 대조. H는 아직 실행하지 않습니다.
    # [해설-중학생용] 개선용(dev) 질문 D01~D03 세 개만 쓰기로 정했어요. 질문 3개 × A/B 2가지 = 첫 응답 6개예요.
    #  expected_ids는 "우리가 쓰겠다고 정한 번호표"이고, 실제 파일의 번호(case_id)와 맞는지 assert로 대조해요.
    #  다르면 바로 멈춰서, 엉뚱한 질문(예: 나중에 쓸 H 질문)이 섞여 들어오는 걸 막아요.
    #  주의: 질문에 '정답 힌트(예상 행동)'를 넣지 않아요. 넣으면 시험지에 답을 적어 두는 것과 같아요.
    expected_ids = ["D01", "D02", "D03"]
    assert [c["case_id"] for c in cases] == expected_ids
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-05-B02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-05-B02
    return cases

def make_report(rows):
    # TODO D21-05-B03: 첫 응답만 골라 통과·미실행·미평가 개수를 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 재시도 응답은 첫 응답 점수에 섞이지 않습니다. 실패를 분모에서 빼지 않습니다.
    # 핵심: None과 False는 다릅니다. 미평가를 0점으로 대체하지 않습니다.
    # BEGIN D21-05-B03
    first = [r for r in rows if False]  # TODO: attempt == 1
    counts = {}
    for variant in ("A","B"):
        subset = []  # TODO: first에서 이 variant 선택
        counts[variant] = {
            "N":len(subset), "json_passed":0,  # TODO: json_ok is True의 수
            "not_run":0,                      # TODO: execution_state == 'not_run'
            "human_pending":0,                # TODO: evidence_ok is None
        }
    report = summarize(rows)  # 세부 지표·분모는 제공된 집계기
    report["learner_first_counts"] = counts
    # [해설-중학생용] 위의 first는 조건이 항상 False라 하나도 못 골랐고, 숫자(counts)도 전부 0이었어요. 제대로 세요.
    #  - first: '첫 번째 시도(attempt==1)'만 골라요. 다시 시도해서 고친 답이 섞이면 첫 점수가 부풀려져요.
    #  - A와 B를 따로 세요: N(전체 칸 수), json_passed(형식 통과), not_run(아직 안 한 것), human_pending(사람이 아직 안 본 것).
    #  - json_ok is True 로 세는 이유: None(아직 모름)과 False(틀림)는 달라요. 아직 모르는 걸 0점으로 치면 안 돼요.
    #  - 실패도 N(분모)에서 빼지 않아요. 못한 시험지도 시험지 수에 들어가요.
    first = [r for r in rows if r["attempt"] == 1]
    counts = {}
    for variant in ("A", "B"):
        subset = [r for r in first if r["variant"] == variant]
        counts[variant] = {
            "N":len(subset), "json_passed":sum(r["json_ok"] is True for r in subset),
            "not_run":sum(r["execution_state"] == "not_run" for r in subset),
            "human_pending":sum(r["evidence_ok"] is None for r in subset),
        }
    report = summarize(rows)
    report["learner_first_counts"] = counts
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-05-B03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-05-B03
    return report

def choose_repeats():
    return 1

def main():
    import argparse
    parser=argparse.ArgumentParser(description="모델 호출 없이 Prompt 준비 또는 실제 수동 응답 검토")
    parser.add_argument("command",choices=["prepare","review","fixtures"],nargs="?",default="prepare")
    parser.add_argument("--run",default="dev_01",help="영문 실험 폴더명; 기존 실험 덮어쓰기 금지")
    parser.add_argument("--bundle",type=Path,help="05에서 고정한 frozen_bundle.json. 미지정 시 제공 독립 시작점 사용")
    args=parser.parse_args()
    check_name(args.run)
    folder=HERE/"outputs"/args.run
    if args.command=="prepare":
        bundle=choose_bundle(args.bundle)
        cases=choose_cases()
        repeats=choose_repeats()
        prepare_experiment(folder,bundle,cases,repeats=repeats)
        print("[준비]",folder)
        print("prompts의 원문을 각각 새 대화에 입력하세요. 아직 실제 응답은 0개입니다.")
    elif args.command=="review":
        rows=review_experiment(folder)
        report=make_report(rows)
        write_summary(folder,report)
        print("[검토]",folder/"summary.md")
        print("raw가 없는 항목은 미실행, 사람 평가 null은 미평가입니다.")
    else:
        results=run_fixture_scenarios(read_json(DATA/"validation_fixtures.json"))
        write_json(HERE/"outputs"/"fixture_checks.json",{"source_mode":"fixture","results":results})
        print("[샘플 검사] 호출 수 2·2·1·1. 모델의 실제 복구율이 아닙니다.")

if __name__ == "__main__":
    run(main)
