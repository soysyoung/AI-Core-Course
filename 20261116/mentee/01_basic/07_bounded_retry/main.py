"""Day21 실습 07: 실패 분류·최대 2회. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, sha_text, run

# 기준: Day21 PPT 56~63장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.retry import run_fixture_scenarios

def repair_prompt(original, error):
    # TODO D21-07-B01: 허용한 형식 오류만 안전한 한 문장 요약으로 수정 요청을 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: unknown_source는 자동 형식 수정 요청을 만들지 않습니다.
    # BEGIN D21-07-B01
    safe = {
        "json_error":"",    # TODO: JSON 문법/코드 블록 관련 짧은 안내
        "schema_error":"",  # TODO: 필수 필드·자료형·길이 안내
    }
    if error not in safe:
        raise ValueError("형식 오류만 수정 요청을 만듭니다")
    repaired = original + "\n[수정 요청] " + ""  # TODO: safe[error], 같은 질문·지식·계약 유지
    # 이전 원문 전체, traceback, 비밀 값은 붙이지 않습니다.
    # [해설-중학생용] 위 safe의 안내 문장이 ""(빈칸)이라, 수정 요청에 "무엇을 고쳐라"는 말이 하나도 없었어요. 빈칸을 채워요.
    #  - json_error(글이 깨짐): "JSON 객체 하나를 코드 블록 없이 출력하세요."
    #  - schema_error(양식이 틀림): "필수 필드·자료형·길이를 지키세요." 라고 짧게 알려 줘요.
    #  안전 규칙: AI의 이전 답 전체, 오류 로그(traceback), 비밀 값은 붙이지 않아요. 한 문장 요약만 줘요.
    #  (선생님이 틀린 시험지를 돌려줄 때 "답안지 전체를 복사해 줄게"가 아니라 "형식을 지켜서 다시 써 봐"라고 짧게 말하는 것과 같아요.)
    #  또 '자료에 없는 번호를 댄 경우(unknown_source)'는 형식 문제가 아니라서, 위의 if error not in safe 에서 ValueError로 막혀요.
    #  기존 줄은 지우지 않으려고, 아래에서 값을 다시 덮어썼어요.
    safe["json_error"] = "JSON 객체 하나를 코드 블록 없이 출력하세요."
    safe["schema_error"] = "필수 필드·자료형·길이를 지키세요. source_ids는 양의 정수 목록입니다."
    repaired = original + "\n[수정 요청] 같은 질문·지식·계약을 유지하세요. " + safe[error] + " 부족한 사실은 만들지 마세요."
    # [해설] 아래 raise는 "아직 숙제 안 했어요!" 하고 멈추는 경고문이에요. 숙제를 끝냈으니 #으로 잠재웠어요.
    # raise NotImplementedError("D21-07-B01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-B01
    return repaired

def run_with_retry(generate, prompt, validate):
    # TODO D21-07-B02: 최초 1회+수정 1회까지만 반복하고 통과하지 못하면 None을 반환하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 호출 수가 최대 2. 정상 정보 부족도 1회에 종료.
    # 핵심: 성공 반환은 자동 구조·참조 통과일 뿐입니다. 근거를 맞게 읽었는지 사람 검토가 남습니다.
    # BEGIN D21-07-B02
    history = []
    for attempt in (1,2):
        raw = generate(prompt)
        obj, error = validate(raw)
        history.append({"attempt":attempt,"error":error,"raw_text":raw,"prompt_sha256":sha_text(prompt)})
        # [해설-중학생용] 아래 원래 if False는 "항상 거짓"이라 성공해도 멈추지 않고 계속 돌아요. 그 앞에 진짜 조건을 넣어요.
        #  오류가 없으면(error is None) 합격이에요! 바로 결과(obj)와 기록(history)을 돌려주고 끝내요.
        #  '자료 부족'이라고 정상적으로 답한 것도 합격이라 1번만에 끝나요(굳이 다시 묻지 않아요).
        if error is None:
            return obj, history
        if False:  # TODO: error is None일 때 즉시 obj, history 반환
            return obj, history
        # [해설-중학생용] 다시 시도해도 되는 경우는 '형식 오류(json_error, schema_error)'이면서 아직 1번째일 때뿐이에요.
        #  - 가짜 출처 같은 '규칙 위반'은 다시 해도 안 고쳐지니 바로 멈춰요(break).
        #  - 이미 2번째(attempt==2)면 더 하지 않고 멈춰요. "최초 1번 + 수정 1번", 최대 2번만 부탁해요(무한 반복 방지).
        #  (숙제 검사에서 "한 번 고쳐 올 기회"는 주지만 끝없이 다시 내게 하지는 않는 것과 같아요.)
        if error not in {"json_error", "schema_error"} or attempt == 2:
            break
        if False:  # TODO: 형식 오류가 아니거나 2회째라면 break
            break
        # TODO: 다음 시도 전에만 repair_prompt를 호출
        prompt = prompt
        # [해설-중학생용] 위의 prompt = prompt는 "나한테 나를 대입"이라 아무것도 안 바꿔요. 다시 부탁할 땐 수정 요청이 붙은 새 부탁 글을 써요.
        #  repair_prompt는 '다음 시도 직전'에만 불러요. 위에서 성공·중단으로 이미 빠져나갔다면 여기까지 오지 않아요.
        prompt = repair_prompt(prompt, error)
    # TODO: 끝까지 실패하면 None, history를 반환. 아래 raise는 완성 후 삭제합니다.
    # [해설-중학생용] 끝까지 합격하지 못했으면 결과는 None(없음)이고, 어떤 시도를 했는지 기록(history)만 돌려줘요.
    #  주의: 합격(obj가 있음)은 '양식과 출처 번호가 맞다'는 뜻일 뿐이에요. 답이 근거를 맞게 읽었는지는 사람이 따로 봐야 해요.
    return None, history
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-07-B02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-B02

def main():
    fixtures=read_json(DATA/"validation_fixtures.json")
    # TODO D21-07-B03: 네 fixture 순서의 호출 수 2·2·1·1을 확인하고 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 복구 성공·연속 실패·규칙 중단·부족 정상 종료 네 경우.
    # BEGIN D21-07-B03
    results = run_fixture_scenarios(fixtures, runner=run_with_retry)
    calls = []  # TODO: results의 calls 목록
    # TODO: [2,2,1,1]과 비교
    write_json(HERE/"outputs"/"retry_results.json", {"source_mode":"fixture","results":[]})  # TODO: results
    # [해설-중학생용] 위의 calls는 빈 목록이고, 저장한 results도 빈 목록이었어요. 진짜 값으로 채워요.
    #  연습용 시나리오 4개의 'AI에게 부탁한 횟수'는 순서대로 2·2·1·1이 되어야 해요.
    #   ① 고쳐서 성공: 2번 ② 두 번 다 실패: 2번 ③ 규칙 위반이라 바로 중단: 1번 ④ 자료 부족을 정상 답변: 1번
    #  assert로 [2,2,1,1]인지 확인하고, 결과를 파일에 저장해요(덮어쓰기).
    #  주의: 진짜 AI가 아니라 선생님이 만든 가짜 답으로 '흐름'만 확인한 거예요. 실제 AI가 얼마나 잘 고치는지는 몰라요.
    calls = [x["calls"] for x in results]
    assert calls == [2, 2, 1, 1]
    write_json(HERE/"outputs"/"retry_results.json", {"source_mode":"fixture","results":results})
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-07-B03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-07-B03
    print("[07] 제어 흐름만 검증했습니다. 실제 모델 복구율은 측정하지 않았습니다.")

if __name__ == "__main__":
    run(main)
