"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def diagnose_stage(case):
    """어떤 문제가 먼저 발생했는지 위에서부터 조건을 검사합니다."""
    # BEGIN D27-01-B01
    # TODO D27-01-B01: 어떤 문제가 먼저 발생했는지 위에서부터 조건을 검사합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    # [쉬운 설명] 건강검진처럼 위에서부터 하나씩 확인하고, 처음 걸리는 문제를 바로 답합니다.
    # [쉬운 설명] 1) 문서를 볼 권한이 없으면, 검색을 아무리 잘해도 소용없으니 가장 먼저 봅니다.
    if not case['authorized']:
        return 'authorization_filter'
    # [쉬운 설명] 2) 문서가 옛날 버전이면 최신 문서만 찾도록 걸러야 합니다.
    if not case['current']:
        return 'version_filter'
    # [쉬운 설명] 3) 검색용 목록(색인)이 아직 준비 안 됐으면 찾을 수가 없습니다.
    if not case['ready']:
        return 'index_not_ready'
    # [쉬운 설명] 4) "그거 어떻게 해?"처럼 질문이 애매하면, 질문부터 또렷하게 고쳐 써야 합니다.
    if case['ambiguous']:
        return 'rewrite'
    # [쉬운 설명] 5) 정답 문서가 후보 목록에 아예 없으면 '찾기(검색)' 단계 문제입니다.
    if not case['gold_in_candidates']:
        return 'retrieval'
    # [쉬운 설명] 6) 후보에는 있는데 최종 자료에 못 들어갔으면 '순서 정하기(재정렬)' 문제입니다.
    if not case['gold_in_context']:
        return 'reranking'
    # [쉬운 설명] 7) 자료는 잘 들어갔는데 출처가 틀렸으면 '검증' 단계 문제입니다.
    if case['valid_source'] is False:
        return 'validation'
    # [쉬운 설명] 8) 아무 문제도 안 걸렸으면 정상입니다.
    return 'healthy'
    # [쉬운 설명] 위에서 항상 return 하므로 아래 줄은 실행되지 않습니다.
    raise NotImplementedError("D27-01-B01 미완성")
    # END D27-01-B01


def recommend_action(stage):
    """문제 단계에 맞는 개선 방법을 반환합니다. Reranker는 누락된 후보를 새로 찾지 않습니다."""
    # BEGIN D27-01-B02
    # TODO D27-01-B02: 문제 단계에 맞는 개선 방법을 반환합니다. Reranker는 누락된 후보를 새로 찾지 않습니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    # [쉬운 설명] 사전처럼 "문제 이름 → 고치는 방법"을 짝지어 두고, 받은 이름으로 찾아 돌려줍니다.
    # [쉬운 설명] 모르는 이름이 오면 KeyError가 나서, 실수를 조용히 넘기지 않습니다.
    return {
        'authorization_filter': '서버에서 접근 권한을 검사합니다.',
        'version_filter': '현재 유효한 문서만 검색합니다.',
        'index_not_ready': 'Indexing 공개 상태를 확인합니다.',
        'rewrite': 'History에서 명확한 대상만 복원합니다.',
        'retrieval': '검색 대상·필터·Top-k를 점검합니다.',
        # [쉬운 설명] Reranker는 이미 찾은 후보의 순서만 바꿀 뿐, 없는 문서를 새로 찾아오지 못합니다.
        'reranking': '후보 문서의 관련성 순위를 다시 평가합니다.',
        'validation': '답변과 실제 근거를 대조합니다.',
        'healthy': '정상 흐름을 유지합니다.',
    }[stage]
    # [쉬운 설명] 위에서 항상 return 하므로 아래 줄은 실행되지 않습니다.
    raise NotImplementedError("D27-01-B02 미완성")
    # END D27-01-B02


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 01 · 01_failure_diagnosis')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[1](args.offline,[diagnose_stage,recommend_action])
    path=save_report(HERE,'day27_01_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 01 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
