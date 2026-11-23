"""Day21 실습 08: AI 지식 답변 생성기 v1. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, run
from coursekit.prompting import make_bundle

# 기준: Day21 PPT 64~72장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.experiments import prepare_experiment, review_experiment, summarize, write_summary
from coursekit.retry import run_fixture_scenarios
from coursekit.io import check_name

def choose_bundle(bundle_path=None):
    # TODO D21-08-B01: 05에서 고정한 A/B 입력을 재사용하고 실행에 사용할 버전을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 05 outputs/dev_01/frozen_bundle.json을 선택적으로 지정. 원문을 바꾸지 않습니다.
    # 핵심: 마지막 프로젝트는 기존 흐름을 다시 연결합니다. 새 API·DB·벡터 검색을 만들지 않습니다.
    # BEGIN D21-08-B01
    if bundle_path is None:
        bundle = make_bundle()  # 앞 교시 미완성자를 위한 제공 체크포인트
        print("[독립 시작점] 실제 D 실험을 개선한 결과가 아닙니다.")
    else:
        bundle = {}  # TODO: read_json(bundle_path)
    # TODO: context_version, schema_version, A/B 버전의 존재를 확인
    # H 결과를 보고 이 파일을 덮어쓰지 마세요.
    # [해설-중학생용] 위의 else에서는 bundle이 {}(빈 상자)로 남아 있어서 05에서 만든 A/B 묶음을 가져오지 못했어요.
    #  - bundle_path(파일 경로)를 받았다면 그 파일을 읽어서 써요. 05에서 고정(frozen)해 둔 입력을 '그대로' 재사용하는 거예요.
    #    (친구가 만들어 둔 시험지 묶음을 베끼지 않고 원본 그대로 가져다 쓰는 것과 같아요. 내용을 바꾸지 않아요.)
    #  - 경로가 없으면 위에서 이미 제공된 시작점(make_bundle())을 쓰고, 그 사실을 화면에 알려 줘요.
    #  - 가져온 묶음이 맞는지 확인해요: 문맥 버전은 knowledge_v1, 출력 약속 버전은 answer_schema_v1, A와 B 두 가지가 다 있어야 해요.
    #    하나라도 다르면 엉뚱한 묶음이라서 ValueError로 바로 멈춰요.
    #  기존 줄은 지우지 않으려고, 아래에서 값을 다시 덮어썼어요.
    if bundle_path is not None:
        bundle = read_json(bundle_path)
    if bundle["context_version"] != "knowledge_v1" or bundle["schema_version"] != "answer_schema_v1":
        raise ValueError("수업의 문맥·출력 계약 버전을 확인하세요")
    assert set(bundle["variants"]) == {"A", "B"}
    # [해설] 아래 raise는 "아직 숙제 안 했어요!" 하고 멈추는 경고문이에요. 숙제를 끝냈으니 #으로 잠재웠어요.
    # raise NotImplementedError("D21-08-B01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-B01
    return bundle

def choose_cases():
    # TODO D21-08-B02: 최종 확인용 H01~H03만 골라 세 질문의 A/B 계획을 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: A/B 각 3질문, 첫 응답 총 6개. H03의 세 근거를 임의로 줄이지 않습니다.
    # BEGIN D21-08-B02
    cases = read_json(DATA/"holdout_v1.json")
    expected_ids = []  # TODO: H01, H02, H03
    # TODO: 세 질문과 선택 ID를 확인. expected_behavior를 Prompt에 넣지 않습니다.
    # [해설-중학생용] 마지막 확인용(holdout) 질문 H01, H02, H03 세 개만 써요. 3질문 × A/B 2가지 = 첫 응답 6개예요.
    #  05번 때 쓴 연습 문제(D01~D03)와 다른 '진짜 시험 문제'라서, 시험 전에 문제를 미리 보고 고치면 안 돼요.
    #  - expected_ids는 "쓰기로 한 번호표"이고, 실제 파일의 번호와 assert로 맞춰 봐요.
    #  - 각 질문이 참고할 자료 번호(selected_ids)도 확인해요: H01은 103, H02는 102(비밀번호 자료는 없어요),
    #    H03은 101·102·103 세 개 모두예요. H03의 근거 세 개를 마음대로 줄이면 안 돼요.
    #  - '이렇게 답해야 한다'는 정답 힌트(expected_behavior)는 질문 글에 넣지 않아요. 시험지에 정답을 적어 두는 것과 같아요.
    expected_ids = ["H01", "H02", "H03"]
    assert [c["case_id"] for c in cases] == expected_ids
    assert cases[0]["selected_ids"] == [103]
    assert cases[1]["selected_ids"] == [102]
    assert cases[2]["selected_ids"] == [101, 102, 103]
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-08-B02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-B02
    return cases

def make_report(rows):
    # TODO D21-08-B03: 검증과 사람 평가를 합치되 미실행·미평가 상태를 그대로 남기세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상·부족·형식 실패·참조 실패·사람 평가를 구분하고 B의 승리를 강요하지 않습니다.
    # BEGIN D21-08-B03
    report = summarize(rows)
    first = []  # TODO: attempt == 1만 선택
    report["project"] = {
        "name":"AI 지식 답변 생성기 v1", "first_target":len(first),
        "not_run":0,         # TODO: 미실행 수
        "human_pending":0,   # TODO: evidence_ok가 None인 수
        "max_attempt":0,     # TODO: 최대 attempt
        "completion":"실제 관찰과 근거 대조 필요",
    }
    # TODO: max_attempt <= 2 확인. 샘플 통과를 모델 우수성으로 적지 마세요.
    # [해설-중학생용] 위의 first는 비어 있었고 숫자들도 전부 0이어서, 아직 안 한 것도 "0점 완료"처럼 보일 수 있었어요. 제대로 세요.
    #  - first: '첫 번째 시도(attempt==1)'만 골라요. 고쳐서 다시 낸 답이 섞이면 첫 점수가 부풀려져요.
    #  - not_run: 아직 안 한 칸 수 / human_pending: 사람이 아직 안 본 칸 수(evidence_ok가 None)
    #    "아직 모름(None)"과 "틀림(False)"은 달라서, 모르는 걸 0점으로 바꾸지 않아요.
    #  - max_attempt: 가장 많이 시도한 횟수예요. 규칙상 최대 2번이라서 assert로 2 이하인지 확인해요.
    #  - completion: "자동 만점"이나 "B가 이겼다" 같은 말을 미리 적지 않아요. 직접 관찰하고 근거를 대조해야 해요.
    #  주의: 실행이 되었다고 모델이 훌륭하다는 뜻은 아니에요. (이 코드는 응답을 직접 받아 넣기 전에는 전부 미실행이에요.)
    first = [r for r in rows if r["attempt"] == 1]
    report["project"].update({
        "first_target":len(first),
        "not_run":sum(r["execution_state"] == "not_run" for r in first),
        "human_pending":sum(r.get("evidence_ok") is None for r in first),
        "max_attempt":max((r["attempt"] for r in rows), default=0),
        "completion":"실제 관찰·근거 대조 결과를 확인하세요. 자동 만점/승자 없음",
    })
    assert report["project"]["max_attempt"] <= 2
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-08-B03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-B03
    return report

def choose_repeats():
    return 1

def main():
    import argparse
    parser=argparse.ArgumentParser(description="모델 호출 없이 Prompt 준비 또는 실제 수동 응답 검토")
    parser.add_argument("command",choices=["prepare","review","fixtures"],nargs="?",default="prepare")
    parser.add_argument("--run",default="holdout_01",help="영문 실험 폴더명; 기존 실험 덮어쓰기 금지")
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
