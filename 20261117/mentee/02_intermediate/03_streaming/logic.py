"""Day22 · Streaming과 완료 판정 | PPT 24~31 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args, execute_case, emit
from coursekit.io import write_json
from coursekit.response import get

def receive_event(state, event, clock, started):
    state.events_seen += 1
    kind = get(event,"type")
    if kind == "response.output_text.delta":
        # TODO D22-03-I01: 비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.
        # 입력·완료 기준: clock은 단조 시계입니다. 빈 delta를 첫 표시로 세지 않습니다.
        # BEGIN D22-03-I01
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
        # END D22-03-I01
    elif kind in {"response.completed","response.incomplete","response.failed"}:
        # TODO D22-03-I02: 최종 이벤트의 Response를 보관하세요.
        # 입력·완료 기준: 부분 문자열을 합쳤다고 completed를 직접 만들어서는 안 됩니다.
        # BEGIN D22-03-I02
        # 중복 terminal이면 오류, 아니면 state.final에 event.response 저장
        final_response = get(event, "response")
        # 쉬운 설명: "끝!" 신호가 이미 한 번 왔는데 또 오면 이상한 일이라서 오류로 기록해요.
        # 처음이면 최종 응답을 state.final에 보관해요. 조각을 합쳤다고 해서 내가 마음대로
        # "완료"라고 만들지 않고, 서버가 보낸 최종 응답만 믿어요.
        if state.final is not None:
            state.error = "duplicate_terminal_event"
        state.final = final_response
        # END D22-03-I02
    elif kind == "error":
        state.error="stream_error"

def streaming_choice():
    # TODO D22-03-I03: 실제 스트리밍을 요청하도록 선택값을 반환하세요.
    # 입력·완료 기준: 메시지 UI를 새로 만드는 실습이 아닙니다. 최종 상태·부분 파일·first_text_ms를 확인합니다.
    # BEGIN D22-03-I03
    # 쉬운 설명: 대답을 한꺼번에 받을지(False), 조각조각 실시간으로 받을지(True) 고르는 스위치예요.
    # 이번 실습은 스트리밍을 해 보는 거라서 True로 켜요.
    use_stream = True  # True이면 Responses stream=True
    return use_stream
    # END D22-03-I03

def compare_runs():
    # TODO D22-03-I04: 동일 입력의 비스트리밍과 스트리밍 순서를 지정하세요.
    # 입력·완료 기준: --action compare에서만 2회 호출합니다. 기본 run은 스트리밍1회입니다.
    # BEGIN D22-03-I04
    # 쉬운 설명: 같은 질문을 "한꺼번에 받기(False)"와 "조각조각 받기(True)" 두 방식으로 차례로 해 봐요.
    # 이 순서대로 stream 값이 하나씩 쓰여요. 두 대답의 글자가 똑같을 필요는 없어요.
    modes = [False, True]  # 두 경우만 비교하며 출력 문장 일치를 강요하지 않습니다.
    return modes
    # END D22-03-I04

def timing_view(result):
    # TODO D22-03-I05: 첫 표시 시간과 전체 요청 시간을 분리해 요약하세요.
    # 입력·완료 기준: 미표시인 None과 실제 관측0은 다릅니다. 시뮬레이션 시간을 실제 LLM 속도로 해석하지 않습니다.
    # BEGIN D22-03-I05
    # 쉬운 설명: "첫 글자가 화면에 보이기까지 걸린 시간(first_text_ms)"과
    # "대답이 전부 끝나기까지 걸린 시간(request_ms)"은 서로 다른 시간이라서 따로 적어요.
    # 첫 글자가 안 보였으면 None이에요. 이건 "0ms 만에 보였다"와 완전히 다르니까 0으로 바꾸지 않아요.
    # 모의(simulated) 실행의 시간은 가짜 시계로 만든 값이라 진짜 AI 속도로 읽으면 안 돼요.
    last = result.get("attempts", [])[-1] if result.get("attempts") else {}
    view = {"source_mode": result.get("source_mode"), "run_status": result.get("run_status"),
            "first_text_ms": last.get("first_text_ms"), "request_ms": last.get("request_ms"),
            "measurement_origin": result.get("measurement_origin")}  # 각 값은 result에서 읽고 None을0으로 바꾸지 않습니다.
    return view
    # END D22-03-I05

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    modes=compare_runs() if args.action=="compare" else [streaming_choice()]
    observations=[]
    for use_stream in modes:
        result=execute_case(args,args.case or "H01",stream=use_stream,hooks={"event":receive_event})
        emit(args,result)
        observations.append(timing_view(result))
    write_json(args.output_dir/"timing_comparison.json",observations)
