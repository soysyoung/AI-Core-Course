"""Day21 실습 04: Context 선택·예산. 실행: python main.py"""
from pathlib import Path
import sys
import json

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text, run

# 기준: Day21 PPT 28~36장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def select_context(rows, selected_ids):
    # TODO D21-04-B01: 선택 ID의 순서를 보존해 지식을 골라 JSON으로 직렬화하세요.
    # 입력·대상: knowledge_v1 목록, selected_ids=[102]
    # 완료 기준: 102만 포함한 JSON. 없는 ID는 ValueError. 순서가 바뀌면 문맥도 달라집니다.
    # 핵심: ID 선택과 직렬화일 뿐 의미 검색·RAG를 구현한 것이 아닙니다.
    # BEGIN D21-04-B01
    by_id = {row["id"]:row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError("중복 ID를 확인하세요")
    ids = list(dict.fromkeys(selected_ids))  # 중복 선택은 첫 순서만 남김
    if any(i not in by_id for i in ids):
        raise ValueError("선택한 ID가 없습니다")
    chosen = []
    for knowledge_id in ids:
        chosen.append(None)  # TODO: by_id[knowledge_id]
    context_json = json.dumps([], ensure_ascii=False)  # TODO: chosen
    # [해설-중학생용] 위의 chosen에는 None(빈 자리)만 들어 있고, context_json도 빈 목록이었어요.
    #  - chosen: 고른 번호(ID) 순서대로 진짜 지식 카드(by_id[번호])를 꺼내 담아요.
    #    (도서관에서 책 번호표를 보고, 적힌 순서대로 책을 꺼내 오는 것과 같아요. 순서가 바뀌면 읽는 맥락도 달라져요)
    #  - context_json: 고른 카드들을 글자(JSON)로 바꿔요. ensure_ascii=False는 한글이 깨지지 않게 해줘요.
    #  - 없는 번호는 위에서 이미 ValueError로 막고 있어요.
    #  기존 줄은 지우지 않으려고, 아래에서 값을 다시 덮어썼어요.
    chosen = [by_id[knowledge_id] for knowledge_id in ids]
    context_json = json.dumps(chosen, ensure_ascii=False)
    # [해설] 아래 raise는 "아직 숙제 안 했어요!" 하고 멈추는 경고문이에요. 숙제를 끝냈으니 #으로 잠재웠어요.
    # raise NotImplementedError("D21-04-B01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-B01
    return chosen, context_json

def calculate_budget():
    # TODO D21-04-B02: PPT의 가상 token 예산에서 근거 문맥에 남는 공간을 구하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: available_for_context=4936
    # 핵심: 실제 모델 최대 길이나 측정 결과가 아닙니다. 입력 형식을 포함한 실제 token 측정은 별도입니다.
    # BEGIN D21-04-B02
    parts = {"window":8192,"instructions_question":800,"examples":600,"output_reserve":1600,"margin":256}
    available = 0  # TODO: window에서 지시·질문, 예제, 출력 예약, 여유를 뺍니다.
    result = {"source":"hypothetical_budget_not_model_measurement", "parts":parts, "available_for_context":available}
    # TODO: 결과 4936과 비교. len(text)를 token 수라고 부르지 마세요.
    # [해설-중학생용] available(남는 공간)이 0이라서 "자리가 하나도 없다"고 잘못 말하고 있었어요.
    #  전체 창(window 8192)에서 이미 쓸 자리를 빼야 진짜 남는 자리가 나와요.
    #  용돈 8192원에서 지시·질문 800, 예제 600, 답변 예약 1600, 여유 256을 빼면 4936원이 남는 것과 같아요.
    #  (8192 - 800 - 600 - 1600 - 256 = 4936)
    #  주의: 이건 PPT의 '가상' 숫자예요. 글자 수(len)를 token 수라고 부르면 안 돼요. 그래서 4936과 같은지 assert로 확인해요.
    available = parts["window"] - parts["instructions_question"] - parts["examples"] - parts["output_reserve"] - parts["margin"]
    result = {"source":"hypothetical_budget_not_model_measurement", "parts":parts, "available_for_context":available}
    assert available == 4936
    # [해설] 아래 raise는 멈춤 경고문이라, 숙제를 끝낸 뒤 #으로 잠재웠어요.
    # raise NotImplementedError("D21-04-B02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-B02
    return result

def main():
    rows=read_json(DATA/"knowledge_v1.json")
    chosen, context_json=select_context(rows,[102])
    budget=calculate_budget()
    # TODO D21-04-B03: 포함·제외 ID와 원문·예산을 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 포함 [102], 제외 101·103. 실제 입력 원문을 보존합니다.
    # BEGIN D21-04-B03
    included_ids = []  # TODO: chosen의 id 목록
    excluded = []
    for row in rows:
        if row["id"] not in included_ids:
            excluded.append({"id":row["id"], "reason":""})  # TODO: 제외 이유
    manifest = {"context_version":"knowledge_v1", "included_ids":included_ids, "excluded":excluded, "budget":budget}
    write_text(HERE/"outputs"/"context.json", "")  # TODO: context_json
    write_json(HERE/"outputs"/"context_manifest.json", manifest)
    # [해설-중학생용] 위에서는 included_ids가 빈 목록이고, 제외 이유(reason)도 빈칸이었어요.
    #  - included_ids: 실제로 고른 카드의 id만 모아요. (이번엔 102)
    #  - excluded: 안 고른 카드(101, 103)와 "왜 뺐는지" 이유를 같이 적어요. 이유가 없으면 나중에 헷갈려요.
    #  - context.json에는 모델에게 실제로 줄 원문(context_json)을 그대로 저장해요(원문 보존).
    #  manifest(목록표)는 값이 바뀌었으니 다시 만들어서 덮어써요.
    included_ids = [r["id"] for r in chosen]
    excluded = [{"id":r["id"], "reason":"이번 서버 실행 질문에서 선택하지 않음"} for r in rows if r["id"] not in included_ids]
    manifest = {"context_version":"knowledge_v1", "included_ids":included_ids, "excluded":excluded, "budget":budget}
    write_text(HERE/"outputs"/"context.json", context_json)
    write_json(HERE/"outputs"/"context_manifest.json", manifest)
    # [해설] 아래 raise도 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-04-B03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-B03
    print("[04] Context와 가상 예산 저장 완료. token 실측·검색 결과가 아닙니다.")

if __name__ == "__main__":
    run(main)
