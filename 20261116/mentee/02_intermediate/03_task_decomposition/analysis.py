"""Day21 실습 03: 작업 분해와 정보 부족. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text

# 기준: Day21 PPT 21~27장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def analyze_card(card):
    # TODO D21-03-I01: 질문이 요구하는 사실과, 제공 자료가 지원하는 사실을 구분하세요.
    # 입력·대상: 교사가 작성한 required/supported/conflicts 카드
    # 완료 기준: C01 missing=[], C02 missing=[보관 기간]
    # 핵심: 이 코드는 자유로운 질문의 의미를 자동 이해하지 않습니다. 명시된 판단 카드를 처리합니다.
    # BEGIN D21-03-I01
    required = []   # TODO: card["required"]
    supported = {}   # TODO: card["supported"]
    missing = []
    for fact in required:
        if False:    # TODO: supported에 없는 fact인지
            missing.append(fact)
    conflicts = []   # TODO: card["conflicts"]
    # [해설-중학생용] 위의 빈 칸들은 "빈 시험지"예요. 카드(card)에 적힌 진짜 내용으로 다시 채워요.
    #  - required: 질문에 답하려면 꼭 알아야 하는 사실 목록 (예: 보관 기간)
    #  - supported: 우리가 가진 자료가 실제로 뒷받침하는 사실 목록 (사실 이름 -> 출처 번호)
    #  - missing: required에는 있는데 supported에는 없는 것 = "자료에 없어서 모르는 것"
    #    (친구 숙제 목록과 내 준비물을 비교해서 빠진 걸 찾는 것과 같아요)
    #  - conflicts: 자료끼리 서로 말이 다른 사실 (예: 보관 위치가 두 군데로 적힘)
    #  기존 줄은 지우지 않으려고, 빈 칸 아래에서 값을 다시 덮어썼어요.
    required = list(card["required"])
    supported = card["supported"]
    missing = [fact for fact in required if fact not in supported]
    conflicts = list(card["conflicts"])
    # [해설] 아래 raise는 "아직 숙제 안 했어요!" 하고 멈추는 경고문이에요. 숙제를 끝냈으니 #으로 잠재웠어요.
    # raise NotImplementedError("D21-03-I01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-I01
    # TODO D21-03-I02: 하나라도 근거가 부족하면 수업의 정보 부족 상태를 선택하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 오늘 계약은 부분 답변을 새 상태로 추가하지 않습니다. 충분한 근거가 없으면 명시적으로 멈춥니다.
    # BEGIN D21-03-I02
    status = ""  # TODO: missing 또는 conflicts가 있으면 부족, 아니면 answered
    source_ids = []
    if status == "answered":
        for fact in required:
            source_ids.extend([])  # TODO: supported[fact]
    result = {"case_id":card["case_id"],"required":required,
              "missing":missing,"conflicts":conflicts,"status":status,"source_ids":source_ids,
              "basis":"teacher_authored_fact_card"}
    # [해설-중학생용] 위에서는 status가 ""(빈칸)이라 판단이 안 된 상태였어요. 여기서 제대로 정해요.
    #  규칙: 모르는 것(missing)이나 말이 엇갈리는 것(conflicts)이 "하나라도" 있으면
    #        추측해서 답하지 않고 "insufficient_context"(자료 부족)로 멈춰요. 둘 다 없을 때만 "answered".
    #        (시험에서 모르는 문제를 찍지 않고 "모르겠다"고 쓰는 것과 같아요)
    #  source_ids(출처 번호)는 답할 수 있을 때만 모으고, 같은 번호가 겹치면 한 번만 남겨요(dict.fromkeys).
    status = "insufficient_context" if missing or conflicts else "answered"
    source_ids = []
    if status == "answered":
        for fact in required:
            source_ids.extend(supported[fact])
    source_ids = list(dict.fromkeys(source_ids))
    result = {"case_id":card["case_id"],"required":required,"supported_facts":list(supported),
              "missing":missing,"conflicts":conflicts,"status":status,"source_ids":source_ids,
              "basis":"teacher_authored_fact_card"}
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-03-I02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-I02
    return result

def main():
    cards=read_json(DATA/"decomposition_cards.json")
    # TODO D21-03-I03: 정상·정보 부족의 판단과 최종 출력 지시를 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 2개 결과와 작업 지시를 저장합니다. 모델 추론 관찰 기록이 아닙니다.
    # BEGIN D21-03-I03
    results = []
    for card in cards[:2]:
        results.append(None)  # TODO: analyze_card(card)
    instruction = ""  # TODO: 사실 대조·부족 처리·최종 JSON 요구(긴 내부 사고 요구 X)
    write_json(HERE/"outputs"/"task_cards.json", results)
    write_text(HERE/"outputs"/"task_instruction.txt", instruction)
    # [해설-중학생용] 위에서는 results에 None(아무것도 없음)을, instruction에 빈 글을 저장했어요.
    #  이제 진짜로 카드 2장을 분석해서 결과를 채우고, 모델에게 줄 지시문을 써서 다시 저장해요(덮어쓰기).
    #  지시문 3가지: ① 질문이 요구하는 사실과 근거를 맞춰 보기 ② 부족하면 추측 말고 필요한 정보 적기
    #  ③ 길게 생각한 과정은 쓰지 말고 최종 JSON만 내기.
    results = [analyze_card(c) for c in cards[:2]]
    instruction = "질문이 요구하는 사실과 근거를 대조하세요. 부족하면 추측하지 말고 필요한 정보를 적으세요. 내부 사고 기록 대신 최종 JSON만 반환하세요."
    # 확인(assert): 첫 카드는 답할 수 있고, 둘째 카드는 자료 부족이어야 정상이에요. 아니면 바로 알려줘요.
    assert results[0]["status"] == "answered" and results[1]["status"] == "insufficient_context"
    write_json(HERE/"outputs"/"task_cards.json", results)
    write_text(HERE/"outputs"/"task_instruction.txt", instruction)
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-03-I03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-I03
    # TODO D21-03-I04: 위치와 기간을 함께 묻는 질문에서 빠진 사실을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 없는 보관 기간을 위치 정보로 추측하지 않습니다.
    # BEGIN D21-03-I04
    compound = analyze_card(cards[2])
    # TODO: 위치는 있지만 기간은 없음. 부분 answered로 바꾸지 않는지 검사
    # TODO: compound_case.json에 저장
    # [해설-중학생용] 세 번째 카드는 "어디에, 몇 년 보관하나요?"처럼 질문이 두 개가 합쳐져 있어요.
    #  자료에는 '위치(101번)'만 있고 '기간'은 없어요. 이럴 때 "위치만이라도 답할게요" 하고 반쯤 답하면 안 돼요.
    #  (오늘 규칙에는 '부분 답변'이라는 상태가 없어서, 하나라도 모르면 통째로 "자료 부족"이에요.)
    #  assert로 확인해요: 빠진 건 "보관 기간"뿐이고, 상태는 insufficient_context, 출처 번호는 비어 있어야 해요.
    #  그리고 없는 기간을 위치 정보로 짐작해서 만들어 내지 않았다는 증거로 compound_case.json에 저장해요.
    assert compound["missing"] == ["보관 기간"]
    assert compound["status"] == "insufficient_context" and compound["source_ids"] == []
    write_json(HERE/"outputs"/"compound_case.json", compound)
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-03-I04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-03-I04
    print("[03] 판단 카드 완료. 근거 대조는 사람의 판단이 포함됩니다.")
