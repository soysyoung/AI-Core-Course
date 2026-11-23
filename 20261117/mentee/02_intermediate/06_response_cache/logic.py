"""Day22 · 승인 응답 캐시 | PPT 47~52 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from copy import deepcopy
from coursekit.support import parse_args, cache_lab
from coursekit.io import write_json, digest
from coursekit.request import build_request as checkpoint_request
from coursekit.cache import read_cache as checkpoint_cache

def key_of(request, scope, validator_version="day21-v1"):
    # TODO D22-06-I01: 질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.
    # 입력·완료 기준: API키는포함하지않습니다. 전체본문이키에들어가야같은ID의내용변경도감지합니다.
    # BEGIN D22-06-I01
    # 쉬운 설명: 캐시 키는 "보관함 열쇠 번호"예요. 질문이 같아도 모델, 요청 전체, 답변 양식(Schema),
    # 검증 규칙 버전, 사용 범위(scope) 중 하나라도 다르면 다른 번호가 나와야 옛날 답을 엉뚱하게 재사용하지 않아요.
    # (API 키는 비밀이라 넣지 않아요.)
    basis = {"scope": scope, "model": request["model"], "request": request,
             "format": request.get("text", {}).get("format"), "validator_version": validator_version}
    key = digest(basis)  # digest(basis): 정렬된JSON의SHA-256
    return key
    # END D22-06-I01

def approved_cache(cache, key, now, provided_ids, *, expected_source, scope):
    # TODO D22-06-I02: 현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.
    # 입력·완료 기준: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    # BEGIN D22-06-I02
    # 쉬운 설명: 보관함에서 옛날 답을 꺼내도 되는지 "안전 검사"를 거쳐요. 유효기간, 사람의 승인, 범위(scope),
    # 진짜/모의 출처가 하나라도 안 맞으면 None(= 미스)이 나와요. 이때 답을 지어내면 안 돼요.
    cached = checkpoint_cache(cache, key, now, provided_ids, expected_source=expected_source, scope=scope)  # checkpoint_cache(..., expected_source=expected_source, scope=scope)
    # None은미스입니다. 새답변을가짜로만들지않습니다.
    return cached
    # END D22-06-I02

def compare_context_keys():
    # TODO D22-06-I03: 같은ID의본문변경이캐시키를바꾸는지확인하세요.
    # 입력·완료 기준: 이키비교는전송0회의모의검사입니다. 실제재사용은먼저생성·사람승인후reuse명령으로확인합니다.
    # BEGIN D22-06-I03
    from coursekit.io import input_parts
    from coursekit.config import load_settings
    case, selected, instructions = input_parts("H01")
    model = load_settings("simulated").models["fast"]
    first = checkpoint_request(model, instructions, case["question"], selected)
    changed = deepcopy(selected)  # 원본JSON파일은바꾸지않습니다.
    # 쉬운 설명: 자료의 id는 그대로 두고 내용(content)만 살짝 바꾸면 열쇠 번호가 달라지는지 시험해요.
    # 안 달라지면 "바뀐 자료인데 옛날 답을 재사용"하는 사고가 나요. 실제 호출은 안 해요(전송 0회).
    changed[0]["content"] += " 실행 환경도 함께 적습니다."
    second = checkpoint_request(model, instructions, case["question"], changed)
    scope = load_settings("simulated").scope
    first_key = key_of(first, scope)
    changed_key = key_of(second, scope)
    return {"case_id": "H01", "changed_id": changed[0]["id"], "first_key": first_key,
            "changed_key": changed_key, "key_changed": first_key != changed_key, "send_count": 0}
    # END D22-06-I03

def model_key_check():
    # TODO D22-06-I04: 모델선택만바뀌어도다른키가되는지확인하세요.
    # 입력·완료 기준: 스트리밍여부는출력전달방식이며요청내생성설정은같게유지합니다.
    # BEGIN D22-06-I04
    # 동일질문·문맥으로fast/quality요청을만들어key를비교합니다. 전송하지않습니다.
    # 쉬운 설명: 질문과 자료는 똑같고 "모델 이름"만 다르게 해서 열쇠 번호를 만들어 비교해요.
    # 모델이 다르면 답도 다를 수 있으니 번호도 달라야 해요. (스트리밍 여부 같은 다른 설정은 그대로 둬요.)
    from coursekit.io import input_parts
    from coursekit.config import load_settings
    case, selected, instructions = input_parts("H01")
    settings = load_settings("simulated")
    fast = settings.models["fast"]
    quality = settings.models.get("quality") or fast + "-quality-sample"  # quality 미설정이면 이름만 다른 예시 모델(전송 안 함)
    key_fast = key_of(checkpoint_request(fast, instructions, case["question"], selected), settings.scope)
    key_quality = key_of(checkpoint_request(quality, instructions, case["question"], selected), settings.scope)
    if key_fast == key_quality:
        raise ValueError("모델이 달라도 캐시 키가 같습니다")
    return {"fast_key": key_fast, "quality_key": key_quality, "key_changed": True, "send_count": 0}
    # END D22-06-I04

def ttl_check():
    # TODO D22-06-I05: 만료시간에같거나지난캐시가재사용되지않는지검사하세요.
    # 입력·완료 기준: TTL을읽을때마다연장하지않습니다.
    # BEGIN D22-06-I05
    fake = {"k": {"expires_at":10.0, "human_approved":True}}
    # now=10.0이면None입니다.
    # 쉬운 설명: 보관함 물건에는 유효기간(expires_at)이 있어요. 지금 시각이 유효기간과 "같거나 지났으면"
    # 못 꺼내야 해요(None). 꺼낼 때마다 기간을 늘려 주지도 않아요.
    for now in (10.0, 11.0):
        if checkpoint_cache(fake, "k", now, [], expected_source="simulated", scope="s") is not None:
            raise ValueError(f"만료된 캐시가 재사용됐습니다: now={now}")
    if fake["k"]["expires_at"] != 10.0:
        raise ValueError("읽었더니 만료시간이 바뀌었습니다")
    # END D22-06-I05

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    write_json(args.output_dir/"cache_key_checks.json",compare_context_keys())
    model_key_check()
    ttl_check()
    result=cache_lab(args,key_builder=key_of,cache_reader=approved_cache)
