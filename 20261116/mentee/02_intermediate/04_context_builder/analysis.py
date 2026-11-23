"""Day21 실습 04: Context 선택·예산. 실행: python main.py"""
from pathlib import Path
import sys
import json

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text

# 기준: Day21 PPT 28~36장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def select_context(rows, selected_ids):
    # TODO D21-04-I01: 선택 ID의 순서를 보존해 지식을 골라 JSON으로 직렬화하세요.
    # 입력·대상: knowledge_v1 목록, selected_ids=[102]
    # 완료 기준: 102만 포함한 JSON. 없는 ID는 ValueError. 순서가 바뀌면 문맥도 달라집니다.
    # 핵심: ID 선택과 직렬화일 뿐 의미 검색·RAG를 구현한 것이 아닙니다.
    # BEGIN D21-04-I01
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
    # raise NotImplementedError("D21-04-I01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-I01
    return chosen, context_json

def calculate_budget():
    # TODO D21-04-I02: PPT의 가상 token 예산에서 근거 문맥에 남는 공간을 구하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: available_for_context=4936
    # 핵심: 실제 모델 최대 길이나 측정 결과가 아닙니다. 입력 형식을 포함한 실제 token 측정은 별도입니다.
    # BEGIN D21-04-I02
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
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-04-I02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-I02
    return result

def main():
    rows=read_json(DATA/"knowledge_v1.json")
    chosen, context_json=select_context(rows,[102])
    budget=calculate_budget()
    # TODO D21-04-I03: 포함·제외 ID와 원문·예산을 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 포함 [102], 제외 101·103. 실제 입력 원문을 보존합니다.
    # BEGIN D21-04-I03
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
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-04-I03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-I03
    # TODO D21-04-I04: 중복 선택은 제거하고, 스냅샷 중복 ID와 없는 ID는 오류인지 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 중복 선택과 잘못된 원본 ID를 구분합니다.
    # BEGIN D21-04-I04
    dedup, _ = select_context(rows, [102,102,101])
    errors = []
    # TODO: [102,101]인지 확인하고 [999]·스냅샷 중복을 각각 try/except ValueError로 검사
    # 실패를 무시한 채 조용히 지식을 누락시키지 마세요.
    # [해설-중학생용] 두 종류의 "이상한 입력"을 서로 다르게 다뤄요.
    #  - 같은 번호를 두 번 고른 경우([102,102,101]): 오류가 아니에요. 중복만 빼고 [102,101]로 정리해요.
    #  - 원본 자료에 같은 번호가 두 장 있거나, 없는 번호(999)를 고른 경우: 진짜 문제라서 ValueError(오류)가 나야 해요.
    #  각각 try/except로 시험해서 "오류가 제대로 났는지(True)"를 기록해요. 오류를 조용히 넘기면 지식이 몰래 빠질 수 있어요.
    #  (rows+[rows[0]]는 첫 카드를 한 장 더 붙여서 일부러 '번호 중복' 상황을 만든 것이에요.)
    assert [r["id"] for r in dedup] == [102, 101]
    for records, ids in [(rows, [999]), (rows + [rows[0]], [101])]:
        try:
            select_context(records, ids)
        except ValueError:
            errors.append(True)
        else:
            errors.append(False)
    assert all(errors)
    write_json(HERE/"outputs"/"selection_checks.json", {"dedup_ids":[r["id"] for r in dedup], "errors_detected":errors})
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-04-I04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-I04
    # TODO D21-04-I05: 허용·유효성·관련성 검토를 선택 이유와 함께 적으세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 이 기록만으로 권한 통제가 구현된 것은 아닙니다. 자료 선정 정책을 설명하는 활동입니다.
    # BEGIN D21-04-I05
    policy = {"permissions":"", "validity":"", "relevance":"", "order":"", "excluded_when_over_budget":""}
    # TODO: 가상 자료의 허용·유효성·관련성·순서 정책 작성 후 저장
    # [해설-중학생용] 어떤 자료를 왜 골랐는지 '규칙'을 글로 남겨요. 위의 policy 빈칸을 채워요.
    #  - permissions(허용): 써도 되는 자료인가? / validity(유효성): 최신·올바른 버전인가?
    #  - relevance(관련성): 질문과 관계가 있는가? / order(순서): 어떤 순서로 넣을까?
    #  - excluded_when_over_budget: 자리가 모자라면 무엇부터 뺄까?
    #  주의: 이건 '설명 글'일 뿐이에요. 이렇게 적었다고 실제로 권한 통제 기능이 만들어진 건 아니에요.
    policy.update({"permissions":"수업용 가상 지식만 사용","validity":"knowledge_v1 고정","relevance":"서버 실행 위치는 102",
                   "order":"요청한 selected_ids의 첫 순서","excluded_when_over_budget":"중복·무관 정보부터 검토, 실제 tokenizer로 재측정 필요"})
    write_json(HERE/"outputs"/"context_policy.json", policy)
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-04-I05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-I05
    print("[04] Context와 가상 예산 저장 완료. token 실측·검색 결과가 아닙니다.")
