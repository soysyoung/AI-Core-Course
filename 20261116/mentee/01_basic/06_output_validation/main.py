"""Day21 실습 06: JSON·Schema·참조 검증. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, run

# 기준: Day21 PPT 46~55장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from coursekit.contracts import strict_json, INSUFFICIENT

def make_model():
    # TODO D21-06-B01: PPT 50장의 엄격한 네 필드 계약을 선언하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 문자열 ID "101", bool true, 추가 필드, 501자 답을 거부합니다.
    # 핵심: 모델 정의는 로컬 검증입니다. 실제 LLM의 생성 형식을 자동 제약하는 API 설정은 아닙니다.
    # BEGIN D21-06-B01
    SourceID = Annotated[int, Field(strict=True, gt=0)]
    class KnowledgeAnswer(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        status: Literal["answered", "insufficient_context"]
        answer: str = Field(min_length=1, max_length=1)  # TODO: 최대 500
        source_ids: list[SourceID] = Field(max_length=1) # TODO: 최대 3
        missing_information: str = Field(max_length=1) # TODO: 최대 200
    # 기본값을 추가하지 마세요. 네 필드 모두 필수입니다.
    # [해설-중학생용] 위 KnowledgeAnswer의 한도(max_length)가 1이라 "답은 1글자, 출처는 1개"만 허용하는 엉터리 규칙이었어요.
    #  진짜 계약(규칙표)대로 다시 선언해요. 같은 이름으로 다시 만들면 아래 것이 위 것을 대신해요(기존 코드는 그대로 둬요).
    #  - answer: 1~500자 (빈 답도, 너무 긴 답도 안 돼요)
    #  - source_ids: 양의 정수만, 최대 3개. strict=True라서 "101"(글자)이나 true(참/거짓)를 숫자로 몰래 바꿔 주지 않아요.
    #  - missing_information: 최대 200자
    #  - extra="forbid": 약속에 없는 필드가 하나라도 더 있으면 거부해요. 네 필드 모두 필수예요(기본값 없음).
    #  (학교 제출 양식에 칸 수와 글자 수 제한이 있고, 어기면 접수를 안 해 주는 것과 같아요.)
    #  주의: 이건 우리 컴퓨터 안의 검사예요. 진짜 AI가 이 모양으로만 쓰게 강제하는 설정은 아니에요.
    class KnowledgeAnswer(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        status: Literal["answered", "insufficient_context"]
        answer: str = Field(min_length=1, max_length=500)
        source_ids: list[SourceID] = Field(max_length=3)
        missing_information: str = Field(max_length=200)
    # [해설] 아래 raise는 "아직 숙제 안 했어요!" 하고 멈추는 경고문이에요. 숙제를 끝냈으니 #으로 잠재웠어요.
    # raise NotImplementedError("D21-06-B01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-B01
    return KnowledgeAnswer

def parse_answer(raw):
    Model=make_model()
    # TODO D21-06-B02: JSON 문법 실패와 Pydantic Schema 실패를 분리하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 깨진 JSON→json_error, {} 또는 문자열 출처→schema_error.
    # 핵심: 형변환을 허용해 잘못된 출처를 억지로 정수로 만들지 않습니다.
    # BEGIN D21-06-B02
    try:
        data = strict_json(raw)  # 크기·중복 키 보호는 제공 함수
    except (ValueError, RecursionError):
        # [해설-중학생용] 아래 원래 줄은 오류 이름이 ""(빈칸)이라 "오류 없음"으로 착각해 버려요. 그래서 그 앞에서 먼저 제대로 돌려보내요.
        #  JSON '문법'이 깨진 경우(괄호 빠짐 등)는 "json_error"예요. (글을 읽을 수조차 없는 상태)
        return None, "json_error"
        return None, ""         # TODO: json_error
    try:
        obj = None              # TODO: Model.model_validate(data)
        # [해설-중학생용] 위의 obj = None은 "검사 안 하고 비워 둔" 상태예요. 진짜로 규칙표(Model)에 대 보며 검사해요.
        #  글은 읽을 수 있어도 모양이 틀리면(필드 빠짐, "101" 같은 글자 출처 등) 여기서 ValidationError가 나요.
        obj = Model.model_validate(data)
    except ValidationError:
        # [해설-중학생용] 글은 읽혔지만 규칙표에 안 맞는 경우는 "schema_error"예요. 위 json_error와 이름을 나눠야 원인을 알 수 있어요.
        #  (편지가 찢어져서 못 읽는 것 vs 읽었는데 양식이 틀린 것은 다른 문제예요.)
        return None, "schema_error"
        return None, ""         # TODO: schema_error
    # [해설] 두 검사를 모두 통과하면 아래 return obj,None(문제 없음)으로 이어져요. 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-06-B02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-B02
    return obj,None

def check_rules(obj, provided_ids):
    # TODO D21-06-B03: 이번 문맥의 출처 범위와 상태별 조합을 확인하세요.
    # 입력·대상: obj 및 실제 전달된 provided_ids
    # 완료 기준: [999]→unknown_source; 부족 응답은 고정문·빈 출처·부족 정보명 조합.
    # 핵심: ID 포함 검사는 근거 문장의 의미적 뒷받침을 증명하지 않습니다.
    # BEGIN D21-06-B03
    ids = obj.source_ids
    if len(ids) != len(set(ids)):
        return "duplicate_source"
    # [해설-중학생용] 아래 원래 if False는 "항상 거짓"이라 아무것도 막지 못해요. 그 앞에 진짜 검사를 먼저 넣어요.
    #  출처 번호는 '이번에 실제로 준 자료의 번호(provided_ids)' 안에 있어야 해요. 없는 번호(예: 999)를 내세우면 가짜 출처예요.
    #  (set(ids) <= set(provided_ids)는 "내가 댄 출처가 전부 받은 자료 안에 있다"는 뜻이에요.)
    if not set(ids) <= set(provided_ids):
        return "unknown_source"
    if False:  # TODO: ids가 provided_ids의 부분집합이 아닌가?
        return "unknown_source"
    if obj.status == "answered":
        # [해설-중학생용] "답했다(answered)"고 말하려면 출처가 꼭 있어야 하고, 부족한 정보 칸은 비어 있어야 해요.
        #  출처가 없거나, 답했다면서 "부족한 정보"를 적어 놓으면 말이 안 맞아요(status_rule 위반).
        if not ids or obj.missing_information != "":
            return "status_rule"
        if False:  # TODO: 출처가 없거나 missing_information이 빈 문자열이 아닌가?
            return "status_rule"
    else:
        # [해설-중학생용] "자료 부족(insufficient_context)"이라고 말하면 출처는 비어 있어야 하고, '무엇이 부족한지'는 적혀 있어야 해요.
        #  출처를 대면서 모른다고 하거나, 뭐가 부족한지 안 적으면 말이 안 맞아요(status_rule 위반).
        if ids or not obj.missing_information.strip():
            return "status_rule"
        if False:  # TODO: 출처가 있거나 부족한 정보명이 없는가?
            return "status_rule"
    if not obj.answer.strip():
        return "blank_answer"
    if obj.status == "insufficient_context" and obj.answer != INSUFFICIENT:
        return "status_rule"
    # [해설] 모든 규칙을 통과하면 아래 return None(오류 없음)으로 가요. 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    #  주의: 이 검사는 '출처 번호가 맞는가'만 봐요. 그 출처가 답을 정말 뒷받침하는지(내용)는 사람이 따로 봐야 해요.
    # raise NotImplementedError("D21-06-B03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-B03
    return None

def validate_answer(raw, provided_ids):
    obj,error=parse_answer(raw)
    if error:
        return None,error
    error=check_rules(obj,provided_ids)
    return (None,error) if error else (obj,None)

def main():
    fixtures=read_json(DATA/"validation_fixtures.json")
    # TODO D21-06-B04: 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 26개 fixture가 기대 오류와 일치. semantic_counterexample은 자동 통과하지만 사람 검토 필요.
    # BEGIN D21-06-B04
    results = []
    for item in fixtures:
        obj, error = validate_answer(item["raw_text"], item["provided_ids"])
        results.append({"fixture_id":item["fixture_id"],"source_mode":"fixture",
                        "error":error,"expected_error":item["expected_error"],
                        "matches_expected":False,  # TODO: error와 expected_error 비교
                        "evidence_ok":None})
    # TODO: 각 행의 matches_expected가 True인지 확인
    write_json(HERE/"outputs"/"fixture_results.json", results)
    write_json(HERE/"outputs"/"answer_schema.json", {})  # TODO: model_json_schema()
    # [해설-중학생용] 위 matches_expected는 전부 False(틀림)로 적혀 있었고, 스키마 파일도 빈 {}였어요.
    #  - 기대한 오류(expected_error)와 실제로 나온 오류(error)가 같으면 True로 고쳐요(정답 맞춰 보기).
    #  - 26개 모두 맞는지 assert로 확인해요. 하나라도 다르면 바로 알려 줘요.
    #  - 규칙표(모델)에서 스키마(양식 설명서)를 뽑아 answer_schema.json에 저장해요. 두 파일은 진짜 내용으로 덮어써요.
    #  주의: semantic_counterexample(그럴듯하지만 근거가 엉뚱한 답)은 이 검사를 '통과'해 버려요. 사람이 따로 봐야 해요.
    for r in results:
        r["matches_expected"] = r["error"] == r["expected_error"]
    assert all(r["matches_expected"] for r in results)
    write_json(HERE/"outputs"/"fixture_results.json", results)
    write_json(HERE/"outputs"/"answer_schema.json", make_model().model_json_schema())
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-06-B04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-B04
    print("[06] 로컬 검증 완료. 구조·참조 검사와 실제 근거 평가는 다릅니다.")

if __name__ == "__main__":
    run(main)
