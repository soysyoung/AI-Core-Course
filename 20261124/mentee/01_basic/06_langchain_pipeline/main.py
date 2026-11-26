"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def prepare_pipeline_request(case):
    """원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다."""
    # BEGIN D27-06-B01
    # TODO D27-06-B01: 원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    # [쉬운 설명] 학생이 한 질문을 "그대로" 담아 보냅니다. 여기서 고쳐 쓰지 않아요.
    # [쉬운 설명] 검색하기 좋은 문장(search_query)은 나중에 Chain 안에서 따로 만들기 때문에,
    # [쉬운 설명] 원래 질문과 고친 질문을 둘 다 남겨서 나중에 비교할 수 있습니다.
    return {
        'query': case['question'],     # [쉬운 설명] 원래 질문 (원본 그대로)
        'history': case['history'],    # [쉬운 설명] 앞에서 나눈 대화 기록 ("그거"가 뭔지 알아낼 때 사용)
        'category': case['category'],  # [쉬운 설명] 어떤 종류의 질문인지 (학사/시설/지원)
        # [쉬운 설명] candidate_k, context_k, use_rewrite 같은 나머지 설정은 쓰지 않으면 기본값이 자동으로 들어갑니다.
    }
    # [쉬운 설명] 위에서 항상 return 하므로 아래 줄은 실행되지 않습니다.
    raise NotImplementedError("D27-06-B01 미완성")
    # END D27-06-B01


def wire_langchain_pipeline(dependencies, offline):
    """LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다."""
    # BEGIN D27-06-B02
    # TODO D27-06-B02: LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    # [쉬운 설명] 이미 만들어진 조립 함수(create_rag_pipeline)를 가져다 씁니다.
    from coursekit.pipeline import create_rag_pipeline
    # [쉬운 설명] dependencies에는 (질문 고치기, 검색, 순위 정하기, 답변 만들기) 4개 부품이 순서대로 들어 있습니다.
    # [쉬운 설명] *를 붙이면 묶음을 풀어서 4개를 차례로 넘겨 줍니다.
    # [쉬운 설명] 여기서는 컨베이어 벨트를 "설치만" 하고 돌리지는 않아요.
    # [쉬운 설명] 실제로 벨트가 움직이는 건 나중에 chain.invoke(요청)을 부를 때입니다.
    return create_rag_pipeline(*dependencies, offline=offline)
    # [쉬운 설명] 위에서 항상 return 하므로 아래 줄은 실행되지 않습니다.
    raise NotImplementedError("D27-06-B02 미완성")
    # END D27-06-B02


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 06 · 06_langchain_pipeline')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[6](args.offline,[prepare_pipeline_request,wire_langchain_pipeline])
    path=save_report(HERE,'day27_06_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 06 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
