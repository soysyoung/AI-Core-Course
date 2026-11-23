"""Day22 · 메시지와 출력 계약 | PPT 14~23 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

import json
from coursekit.support import parse_args, guarded, execute_case, emit
from coursekit.request import OUTPUT_FORMAT, build_request as checkpoint_request
from coursekit.response import get, output_text

def make_request(model, instructions, question, selected, *, structured=True):
    # TODO D22-02-B01: 질문과 선택 지식만 user input으로 직렬화하세요.
    # 입력·완료 기준: selected_ids가 아닌 선택된 지식의 id·title·content·category를 보냅니다. expected_behavior는 넣지 않습니다.
    # BEGIN D22-02-B01
    # 쉬운 설명: AI에게 보낼 "질문 + 참고 자료"를 하나의 글자(JSON)로 포장하는 곳이에요.
    # 참고 자료(knowledge)에는 id·title·content·category 4가지만 넣어요.
    # (정답 힌트가 담긴 expected_behavior 같은 다른 항목은 AI에게 보여주면 안 되니까 빼요.)
    payload = {"question": question,
               "knowledge": [{k: row[k] for k in ("id", "title", "content", "category")}
                             for row in selected]}  # 이번 selected를 넣습니다.
    # json.dumps는 파이썬 데이터를 글자로 바꿔 줘요. ensure_ascii=False는 한글이 깨지지 않게 해요.
    serialized = json.dumps(payload, ensure_ascii=False)  # json.dumps(..., ensure_ascii=False)
    # END D22-02-B01
    # TODO D22-02-B02: 공급자용 Schema를 요청의 text.format으로 연결하세요.
    # 입력·완료 기준: response_format이 아니라 Responses의 text.format입니다. Wire와 로컬 KnowledgeAnswer는 다릅니다.
    # BEGIN D22-02-B02
    request = checkpoint_request(model, instructions, question, selected, structured=False)
    # 쉬운 설명: 위에서 포장한 글자를 "사용자(user)가 보낸 메시지"로 넣고,
    # "대답은 정해진 양식(JSON Schema)대로 써 줘"라는 부탁을 text.format에 적어요.
    # (response_format이 아니라 Responses API에서는 text.format이라는 이름을 써요.)
    request["input"] = [{"role": "user", "content": serialized}]  # role="user", content=serialized
    request["text"] = {"format": OUTPUT_FORMAT}   # {"format": OUTPUT_FORMAT}
    return request  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-02-B02

def response_gate(response):
    # TODO D22-02-B03: 거절 콘텐츠와 미완료 상태를 먼저 구분하세요.
    # 입력·완료 기준: API status와 answer JSON의 status는 다릅니다. 거절을 형식 오류로 바꾸지 않습니다.
    # BEGIN D22-02-B03
    for item in get(response, "output", []) or []:
        if get(item, "type") == "message":
            for part in get(item, "content", []) or []:
                # 쉬운 설명: AI가 "그건 답할 수 없어요"라고 거절했는지 먼저 확인해요.
                # 거절은 '형식이 틀린 것'이 아니라 따로 구분해야 해서 "refused"라고 알려 줘요.
                if get(part, "type") == "refusal":
                    return None, "refused"  # refusal이면 None, "refused" 반환
    status = get(response, "status")  # completed가 아니면 오류 반환
    # 쉬운 설명: 대답이 끝까지 잘 완성됐는지(completed) 확인해요. 중간에 끊겼거나 실패했으면
    # 그 상태 이름을 돌려주고, 처음 보는 상태면 "response_error"라고 해요.
    if status != "completed":
        return None, status if status in {"incomplete", "failed", "cancelled", "queued", "in_progress"} else "response_error"
    # END D22-02-B03
    # TODO D22-02-B04: 완료 응답에서도 빈 본문을 검사한 뒤 원문을 반환하세요.
    # 입력·완료 기준: 원문을 수정해 유효한 JSON처럼 만들지 않습니다. 로컬 검증기는 다음 단계에서 실행됩니다.
    # BEGIN D22-02-B04
    raw = output_text(response)
    # 쉬운 설명: 끝났다고 해도 글자가 하나도 없는 "빈 대답"일 수 있어요. 그래서 한 번 더 확인해요.
    # strip()은 앞뒤 빈칸을 없애 줘요. 비었으면 오류 이름을, 아니면 원문을 고치지 않고 그대로 돌려줘요.
    if not raw.strip():
        return None, "empty_output"
    # 힌트: 공백을 제거한 결과가 비어 있으면 (None, "empty_output")
    return raw, None  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-02-B04

def main():
    args=parse_args(HERE)
    cases=["D02"]
    for case_id in ([args.case] if args.case else cases):
        result=execute_case(args,case_id,request_builder=make_request,hooks={"gate":response_gate})
        emit(args,result)
        if result["run_status"] in {"auth_error","quota_error","permission_error","not_run"}:
            break

if __name__=="__main__":
    guarded(main)
