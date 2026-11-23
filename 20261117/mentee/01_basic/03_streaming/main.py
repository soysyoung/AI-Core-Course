"""Day22 · Streaming과 완료 판정 | PPT 24~31 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded, execute_case, emit
from coursekit.response import get

def receive_event(state, event, clock, started):
    state.events_seen += 1
    kind = get(event,"type")
    if kind == "response.output_text.delta":
        # TODO D22-03-B01: 비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.
        # 입력·완료 기준: clock은 단조 시계입니다. 빈 delta를 첫 표시로 세지 않습니다.
        # BEGIN D22-03-B01
        delta = get(event, "delta", "")
        # 쉬운 설명: AI의 대답은 글자 조각(delta)들이 하나씩 도착해요. 그 조각을 모아 둬요.
        # 처음으로 "내용이 있는" 조각이 온 순간까지 걸린 시간을 재요. (빈 조각은 세지 않아요)
        # clock()은 지금 시각, started는 요청을 보낸 시각이라서 둘을 빼면 걸린 시간이에요.
        # 1000을 곱하면 초가 밀리초(ms)로 바뀌어요.
        if delta and state.first_text_ms is None:
            state.first_text_ms = (clock() - started) * 1000  # (clock() - started) * 1000
        # state.parts.append(...)로 누적. delta 개수는 Token 수가 아닙니다.
        if isinstance(delta, str):
            state.parts.append(delta)
        # END D22-03-B01
    elif kind in {"response.completed","response.incomplete","response.failed"}:
        # TODO D22-03-B02: 최종 이벤트의 Response를 보관하세요.
        # 입력·완료 기준: 부분 문자열을 합쳤다고 completed를 직접 만들어서는 안 됩니다.
        # BEGIN D22-03-B02
        # 중복 terminal이면 오류, 아니면 state.final에 event.response 저장
        final_response = get(event, "response")
        # 쉬운 설명: "끝!" 신호가 이미 한 번 왔는데 또 오면 이상한 일이라서 오류로 기록해요.
        # 처음이면 최종 응답을 state.final에 보관해요. 조각을 합쳤다고 해서 내가 마음대로
        # "완료"라고 만들지 않고, 서버가 보낸 최종 응답만 믿어요.
        if state.final is not None:
            state.error = "duplicate_terminal_event"
        state.final = final_response
        # END D22-03-B02
    elif kind == "error":
        state.error="stream_error"

def streaming_choice():
    # TODO D22-03-B03: 실제 스트리밍을 요청하도록 선택값을 반환하세요.
    # 입력·완료 기준: 메시지 UI를 새로 만드는 실습이 아닙니다. 최종 상태·부분 파일·first_text_ms를 확인합니다.
    # BEGIN D22-03-B03
    # 쉬운 설명: 대답을 한꺼번에 받을지(False), 조각조각 실시간으로 받을지(True) 고르는 스위치예요.
    # 이번 실습은 스트리밍을 해 보는 거라서 True로 켜요.
    use_stream = True  # True이면 Responses stream=True
    return use_stream  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-03-B03

def main():
    args=parse_args(HERE)
    modes=[streaming_choice()]
    observations=[]
    for use_stream in modes:
        result=execute_case(args,args.case or "H01",stream=use_stream,hooks={"event":receive_event})
        emit(args,result)

if __name__=="__main__":
    guarded(main)
