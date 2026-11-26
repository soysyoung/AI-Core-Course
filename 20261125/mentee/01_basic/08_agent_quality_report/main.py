"""Day28 실습 08 · 01_basic · 실행 진입점.
수강생은 TODO의 요구사항을 해결하고 예상 출력과 비교합니다.
강사용 코드에는 데이터 계약, 단계별 처리 의도와 예외를 주석으로 설명합니다.
"""
from pathlib import Path
import argparse
import sys

ROLE_ROOT = Path(__file__).resolve().parents[2]
if str(ROLE_ROOT) not in sys.path:
    sys.path.insert(0,str(ROLE_ROOT))

from coursekit.eval_workshops import execute
from coursekit.eval_report import write_json


def evaluate_one(example: dict, run: dict, gold: list[str], grades: dict) -> dict:
    """질문 ID로 Target 출력과 Gold를 결합해 평가 레코드를 반환하세요."""
    # TODO D28-08-B01: 질문 ID로 Target 출력과 Gold를 결합해 평가 레코드를 반환하세요.
    # 힌트: Trace 필드가 빠졌다면 빈 리스트로 바꾸지 말고 오류로 보고합니다.
    # [추가] 이미 있는 채점 도구(evaluate_retrieval)를 빌려 써요. 새로 만들 필요가 없어요.
    from coursekit.eval_metrics import evaluate_retrieval
    # [추가] 검사 1) 1번 문제의 답안지에 2번 답이 적혀 있으면 안 되니, 질문 ID가 같은지 확인해요.
    if run.get('question_id') != example['question_id']:
        raise ValueError(f"질문 ID 불일치: {example['question_id']} / {run.get('question_id')}")
    # [추가] 검사 2) Trace(어떤 문서를 찾고 골랐는지 남긴 기록)가 빠졌으면 []로 덮지 않고 바로 오류를 내요.
    # [추가]        빈 칸을 []로 채우면 "검색 결과 0개"로 착각해서 점수가 거짓으로 낮아지기 때문이에요.
    missing = [key for key in ('candidate_ids', 'ranked_ids', 'included_ids') if key not in run]
    if missing:
        raise KeyError(f"{example['question_id']} Trace 필드 누락: {missing}")
    # [추가] 이제 정답(Gold)과 Target 결과를 한 장의 성적표로 합쳐요.
    return {'question_id': example['question_id'],
            'mode': run['mode'],                 # [추가] 실제 실행(live)인지 연습용 고정 데이터인지
            'status': run['status'],             # [추가] 답변 상태 (answered / insufficient_context)
            'source_count': len(run.get('sources', [])),  # [추가] 답변에 붙은 출처 개수
            **evaluate_retrieval(run['ranked_ids'], gold, grades, 3)}  # [추가] Recall@3 같은 검색 점수들
    raise NotImplementedError("D28-08-B01 TODO를 완성하세요")

def summarize_all(rows: list[dict]) -> dict:
    """개별 질문 결과의 평균(유효 Gold만)과 오류·출처 상태를 집계하세요."""
    # TODO D28-08-B02: 개별 질문 결과의 평균(유효 Gold만)과 오류·출처 상태를 집계하세요.
    # 힌트: No-answer 질문은 Retrieval 평균에서 제외하고 별도 개수로 기록합니다.
    # [추가] 반 평균을 낼 때 결석생을 0점으로 넣지 않는 것처럼, 점수가 None인 No-answer 질문은 평균에서 빼요.
    # [추가] 이미 있는 summarize_retrieval이 평균 계산 + 제외한 개수(no_answer_excluded)까지 해줘요.
    from collections import Counter
    from coursekit.eval_metrics import summarize_retrieval
    summary = summarize_retrieval(rows)
    # [추가] 상태별로 몇 개인지 세요. 예: {'answered': 6, 'insufficient_context': 2}
    summary['status_counts'] = dict(Counter(row['status'] for row in rows))
    # [추가] 실행 모드별 개수예요. 연습용(offline_fixture) 결과를 실제 성능으로 착각하지 않게 해줘요.
    summary['mode_counts'] = dict(Counter(row['mode'] for row in rows))
    # [추가] "답했다"면서 출처가 0개인 질문 수예요. 근거 없이 답했을 수 있어 따로 살펴봐야 해요.
    summary['answered_without_source'] = sum(1 for row in rows if row['status'] == 'answered' and row['source_count'] == 0)
    summary['total_questions'] = len(rows)
    return summary
    raise NotImplementedError("D28-08-B02 TODO를 완성하세요")


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "evaluate_one":evaluate_one,
        "summarize_all":summarize_all
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(8,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':8,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 8 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()
