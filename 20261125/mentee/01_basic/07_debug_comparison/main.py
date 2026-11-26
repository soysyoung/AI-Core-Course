"""Day28 실습 07 · 01_basic · 실행 진입점.
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


def score_delta(before: float | None, after: float | None) -> float | None:
    """같은 질문의 Before/After 점수 변화량을 계산하세요. No-answer(None)는 수치 차이를 만들지 않습니다."""
    # TODO D28-07-B01: 같은 질문의 Before/After 점수 변화량을 계산하세요. No-answer(None)는 수치 차이를 만들지 않습니다.
    # 힌트: A/B 비교 전 두 실행의 Dataset 버전과 모드가 같아야 합니다.
    # [추가] None은 "정답이 없는 질문이라 점수를 못 매김"이란 뜻이에요. 0점과 달라요!
    # [추가] 점수가 없는 쪽이 하나라도 있으면 빼기를 할 수 없으니 None을 그대로 돌려줘요.
    if before is None or after is None:
        return None
    # [추가] 변화량 = 나중 점수 - 처음 점수. 양수면 좋아졌고, 음수면 나빠졌어요. (예: 0.5 → 1.0 이면 +0.5)
    return after - before
    raise NotImplementedError("D28-07-B01 TODO를 완성하세요")

def find_problem_stage(run: dict, gold: list[str]) -> str:
    """검색 후보 누락·Reranking 누락·Context 누락·생성 실패 중 어디인지 반환하세요."""
    # TODO D28-07-B02: 검색 후보 누락·Reranking 누락·Context 누락·생성 실패 중 어디인지 반환하세요.
    # 힌트: Candidate에 Gold가 없다면 먼저 Retrieval 단계 문제입니다.
    # [추가] 정답 문서(Gold)가 4개의 문을 차례로 통과하는지 보고, 처음 막힌 문을 범인으로 지목해요.
    # [추가]   문1 검색 후보(candidate_ids) → 문2 재정렬 상위 3개(ranked_ids[:3]) → 문3 Context(included_ids) → 문4 답변 생성(status)
    # [추가] 정답 문서가 없는 질문(No-answer)은 "모른다"고 답해야 정상이에요. 답을 지어냈으면 생성 실패예요.
    if not gold:
        return 'generation_failure' if run['status'] == 'answered' else 'ok_no_answer'
    # [추가] 문1: 정답 문서가 검색 후보에 하나라도 빠졌다면, 시작부터 못 찾은 거예요.
    if not all(g in run['candidate_ids'] for g in gold):
        return 'retrieval_miss'
    # [추가] 문2: 후보에는 있었는데 순위를 다시 매긴 뒤 상위 3등 안에 못 들었어요. (평가 기준 k=3)
    if not all(g in run['ranked_ids'][:3] for g in gold):
        return 'rerank_miss'
    # [추가] 문3: 순위는 좋았지만 LLM에게 실제로 건네준 자료(Context)에 안 들어갔어요.
    if not all(g in run['included_ids'] for g in gold):
        return 'context_miss'
    # [추가] 문4: 자료는 다 받았는데도 답을 못 했다면, 답변을 만드는 단계의 문제예요.
    if run['status'] != 'answered':
        return 'generation_failure'
    # [추가] 4개의 문을 모두 통과했어요. 문제 없음!
    return 'ok'
    raise NotImplementedError("D28-07-B02 TODO를 완성하세요")


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "score_delta":score_delta,
        "find_problem_stage":find_problem_stage
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(7,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':7,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 7 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()
