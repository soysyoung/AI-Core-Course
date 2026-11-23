"""Day22 · 첫 실제 응답 | PPT 6~13 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded, execute_case, emit
from coursekit.io import write_json

def make_first_request(model, instructions, question, selected, *, structured=False):
    # TODO D22-01-B01: 첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.
    # 입력·완료 기준: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.
    # BEGIN D22-01-B01
    # 쉬운 설명: AI에게 보낼 "주문서"를 만드는 곳이에요. 빈칸(None)을 알맞은 값으로 채웠어요.
    # model: 어떤 AI를 쓸지 → 함수가 받은 model 값을 그대로 써요 (내 맘대로 정하지 않아요)
    # input: AI에게 할 질문 → 받은 question 이에요
    # max_output_tokens: AI가 대답할 수 있는 최대 길이(글자 조각 수) → 1200으로 제한해요
    # store: 대답을 서버에 저장할지 → False라서 저장하지 않아요
    request = {"model": model, "instructions": instructions, "input": question,
               "reasoning": {"effort": "none"}, "max_output_tokens": 1200,
               "store": False, "service_tier": "default"}
    # model은 전달값, input은 question, 출력 상한1200, store=False
    return request  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-01-B01

def create_response(client, request, stream=False):
    # TODO D22-01-B02: Responses API를 한 번 호출하고 반환값을 돌려주세요.
    # 입력·완료 기준: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # BEGIN D22-01-B02
    options = dict(request)  # 힌트: 이미 만든 요청 딕셔너리
    # 쉬운 설명: 앞에서 만든 "주문서"를 실제로 AI에게 보내고, 돌아온 대답을 받아요.
    # **options는 딕셔너리 안의 값들을 하나씩 풀어서 넣어 주는 문법이에요.
    # create를 딱 한 번만 부르니까 요청도 한 번만 나가요.
    response = client.responses.create(**options, stream=stream)  # 힌트: client.responses.create(**options, stream=stream)
    return response  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-01-B02

def make_view(result):
    # TODO D22-01-B03: 키 없이 source·model·종료 상태·응답 ID를 요약하세요.
    # 입력·완료 기준: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    # BEGIN D22-01-B03
    last = result.get("attempts", [])[-1] if result.get("attempts") else {}
    # 쉬운 설명: 결과에서 중요한 4가지만 뽑아 "한 줄 요약표"를 만들어요. (비밀 키는 들어가지 않아요)
    # source_mode: 진짜 호출인지 가짜(모의) 호출인지 / model: 쓴 AI 이름
    # run_status: 끝난 상태 / response_id: 대답의 번호표
    # .get()을 쓰면 값이 없을 때 에러 대신 None이 나와요. 실행을 안 했으면 번호표도 없으니 None이 맞아요.
    summary = {"source_mode": result.get("source_mode"), "model": result.get("model"),
               "run_status": result.get("run_status"), "response_id": last.get("response_id")}
    # 힌트: result와 last에서 같은 필드명을 읽습니다.
    return summary  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-01-B03

def main():
    args=parse_args(HERE)
    result=execute_case(args,"FIRST",request_builder=make_first_request,hooks={"create":create_response})
    emit(args,result)
    view=make_view(result)
    write_json(args.output_dir/"connection_view.json",view)

if __name__=="__main__":
    guarded(main)
