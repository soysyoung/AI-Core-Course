"""Day28 실습 05 · 01_basic · 실행 진입점.
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


def claim_faithfulness(claims: list[dict]) -> float | None:
    """Claim 목록에서 근거가 지지하는 Claim 비율을 계산하세요. Claim이 없으면 None."""
    # TODO D28-05-B01: Claim 목록에서 근거가 지지하는 Claim 비율을 계산하세요. Claim이 없으면 None.
    # 힌트: 모든 Claim의 supported는 교육용 사람 레이블입니다.
    # [추가] Claim = 답변 속 "주장" 한 문장. supported=True면 자료(Context)에 그 내용이 진짜 있다는 뜻이에요.
    # [추가] 주장이 하나도 없으면 0점이 아니라 "채점할 게 없음"이므로 None을 돌려줘요. (0으로 나누기도 막아줘요)
    if not claims:
        return None
    # [추가] 시험 채점처럼 "맞은 개수 ÷ 전체 개수"를 계산해요. 예: 3개 중 2개 맞으면 2/3 ≈ 0.67
    return sum(1 for c in claims if c['supported']) / len(claims)
    raise NotImplementedError("D28-05-B01 TODO를 완성하세요")

def describe_claim_result(claims: list[dict]) -> str:
    """비지원 Claim을 이름과 함께 기록하세요. “모든 Claim 지원”과 “Claim 없음”은 구별합니다."""
    # TODO D28-05-B02: 비지원 Claim을 이름과 함께 기록하세요. “모든 Claim 지원”과 “Claim 없음”은 구별합니다.
    # 힌트: Faithfulness는 Reference Answer와의 비교가 아닙니다.
    # [추가] 경우 1) 주장이 아예 없음 → "다 맞았다"와 헷갈리지 않게 따로 적어요.
    if not claims:
        return 'Claim 없음: 평가할 주장이 없습니다'
    # [추가] 자료로 뒷받침되지 않는(supported=False) 주장의 문장만 골라 모아요.
    unsupported = [c['text'] for c in claims if not c['supported']]
    # [추가] 경우 2) 틀린 주장이 하나도 없음 → 모두 근거가 있다는 뜻이에요.
    if not unsupported:
        return '모든 Claim 지원'
    # [추가] 경우 3) 근거 없는 주장이 있음 → 어떤 문장이 문제인지 이름(문장)을 그대로 보여줘요.
    return '비지원 Claim: ' + ', '.join(unsupported)
    raise NotImplementedError("D28-05-B02 TODO를 완성하세요")


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "claim_faithfulness":claim_faithfulness,
        "describe_claim_result":describe_claim_result
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(5,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':5,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 5 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()
