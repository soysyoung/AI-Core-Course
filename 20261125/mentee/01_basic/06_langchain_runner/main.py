"""Day28 실습 06 · 01_basic · 실행 진입점.
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


def safe_target_input(example: dict) -> dict:
    """question_id·question·category·history만 새 dict로 복사하고 Gold·Reference를 제외하세요."""
    # TODO D28-06-B01: question_id·question·category·history만 새 dict로 복사하고 Gold·Reference를 제외하세요.
    # 힌트: Target Runner는 정답을 모르는 상태에서 실행해야 공정합니다.
    # [추가] 시험 볼 때 문제지만 주고 정답지는 안 주는 것과 같아요.
    # [추가] 허락된 4개 칸만 골라 "새" dict에 담아요. reference_answer 같은 정답 정보는 자연히 빠져요.
    # [추가] 원본 example을 고치지 않고 새로 만들기 때문에, 나중에 채점할 때 원본은 그대로 쓸 수 있어요.
    return {key: example[key] for key in ('question_id', 'question', 'category', 'history')}
    raise NotImplementedError("D28-06-B01 TODO를 완성하세요")

def invoke_target(target, request: dict) -> dict:
    """실제 Runnable.invoke(request)를 호출하고 결과가 dict이며 질문 ID가 같은지 확인하세요."""
    # TODO D28-06-B02: 실제 Runnable.invoke(request)를 호출하고 결과가 dict이며 질문 ID가 같은지 확인하세요.
    # 힌트: 단순 함수 직접 호출 대신 RunnableLambda를 감싼 객체의 invoke()입니다.
    # [추가] target은 LangChain의 "실행 상자"예요. 상자에 질문을 넣고 .invoke() 버튼을 누르면 답이 나와요.
    result = target.invoke(request)
    # [추가] 검사 1) 답이 dict(이름표가 붙은 상자) 모양이 아니면, 다음 단계가 읽을 수 없으니 바로 멈춰요.
    if not isinstance(result, dict):
        raise TypeError(f'Target 결과는 dict여야 합니다: {type(result).__name__}')
    # [추가] 검사 2) 1번 문제를 냈는데 2번 문제의 답이 오면 채점이 엉망이 되니, 질문 ID가 같은지 확인해요.
    if result.get('question_id') != request['question_id']:
        raise ValueError(f"질문 ID 불일치: 요청 {request['question_id']} / 결과 {result.get('question_id')}")
    return result
    raise NotImplementedError("D28-06-B02 TODO를 완성하세요")


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "safe_target_input":safe_target_input,
        "invoke_target":invoke_target
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(6,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':6,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 6 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()
