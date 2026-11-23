"""Day22 · 승인 응답 캐시 | PPT 47~52 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from copy import deepcopy
from coursekit.support import parse_args, guarded, cache_lab
from coursekit.io import write_json, digest
from coursekit.request import build_request as checkpoint_request
from coursekit.cache import read_cache as checkpoint_cache

def key_of(request, scope, validator_version="day21-v1"):
    # TODO D22-06-B01: 질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.
    # 입력·완료 기준: API키는포함하지않습니다. 전체본문이키에들어가야같은ID의내용변경도감지합니다.
    # BEGIN D22-06-B01
    # 쉬운 설명: 캐시 키는 "보관함 열쇠 번호"예요. 질문이 같아도 모델, 요청 전체, 답변 양식(Schema),
    # 검증 규칙 버전, 사용 범위(scope) 중 하나라도 다르면 다른 번호가 나와야 해요.
    # 안 그러면 옛날 답을 엉뚱하게 재사용할 수 있어요. (API 키는 넣지 않아요. 비밀이니까요.)
    # request 전체가 들어가서 같은 id의 자료 내용이 바뀌어도 번호가 바뀌어요.
    basis = {"scope": scope, "model": request["model"], "request": request,
             "format": request.get("text", {}).get("format"), "validator_version": validator_version}
    key = digest(basis)  # digest(basis): 정렬된JSON의SHA-256
    return key  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-06-B01

def approved_cache(cache, key, now, provided_ids, *, expected_source, scope):
    # TODO D22-06-B02: 현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.
    # 입력·완료 기준: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    # BEGIN D22-06-B02
    # 쉬운 설명: 보관함에서 옛날 답을 꺼내도 되는지 "안전 검사"를 거쳐요. 이미 만들어진 검사 함수가
    # 유효기간, 사람의 승인 여부, 범위(scope), 진짜/모의 출처, 현재 자료와의 일치를 한꺼번에 확인해요.
    # 하나라도 안 맞으면 None(= 미스)이 나와요. 이때 내가 답을 대충 지어내면 안 돼요.
    cached = checkpoint_cache(cache, key, now, provided_ids, expected_source=expected_source, scope=scope)  # checkpoint_cache(..., expected_source=expected_source, scope=scope)
    # None은미스입니다. 새답변을가짜로만들지않습니다.
    return cached  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-06-B02

def compare_context_keys():
    # TODO D22-06-B03: 같은ID의본문변경이캐시키를바꾸는지확인하세요.
    # 입력·완료 기준: 이키비교는전송0회의모의검사입니다. 실제재사용은먼저생성·사람승인후reuse명령으로확인합니다.
    # BEGIN D22-06-B03
    from coursekit.io import input_parts
    from coursekit.config import load_settings
    case, selected, instructions = input_parts("H01")
    model = load_settings("simulated").models["fast"]
    first = checkpoint_request(model, instructions, case["question"], selected)
    changed = deepcopy(selected)  # 원본JSON파일은바꾸지않습니다.
    # 쉬운 설명: 자료의 id는 그대로 두고 내용(content)만 살짝 바꾸면 열쇠 번호가 달라지는지 시험해요.
    # 번호가 안 바뀌면 "바뀐 자료인데 옛날 답을 재사용"하는 사고가 나요. 실제 호출은 하지 않아요(전송 0회).
    # 원본 파일은 deepcopy로 복사한 것만 바꿔서 건드리지 않아요.
    changed[0]["content"] += " 실행 환경도 함께 적습니다."
    second = checkpoint_request(model, instructions, case["question"], changed)
    scope = load_settings("simulated").scope
    first_key = key_of(first, scope)
    changed_key = key_of(second, scope)
    return {"case_id": "H01", "changed_id": changed[0]["id"], "first_key": first_key,
            "changed_key": changed_key, "key_changed": first_key != changed_key, "send_count": 0}
    # changed[0]["content"]수정 → 두번째request → key비교
    # END D22-06-B03

def main():
    args=parse_args(HERE)
    write_json(args.output_dir/"cache_key_checks.json",compare_context_keys())
    result=cache_lab(args,key_builder=key_of,cache_reader=approved_cache)

if __name__=="__main__":
    guarded(main)
