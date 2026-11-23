"""Day21 실습 02: Zero/Few-shot·버전. 실행: python main.py"""
from pathlib import Path
import sys
import json

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text, save_version
from coursekit.prompting import make_bundle

# 기준: Day21 PPT 14~20장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.prompting import render_prompt

def build_examples():
    # TODO D21-02-I01: 예제 ID 901을 사용해 정상 답과 정보 부족 답을 완성하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상·부족 예제 2개. 평가 질문 D/H를 Few-shot에 사용하지 않습니다.
    # 핵심: 입력 예제를 늘려도 모델 가중치가 바뀌는 것은 아닙니다.
    # BEGIN D21-02-I01
    example_context = [{"id":901,"content":"대여 장소는 안내 데스크입니다."}]
    examples = [
        {"question":"어디서 대여하나요?","context":example_context,
         "answer":{"status":"", "answer":"", "source_ids":[], "missing_information":""}},
        {"question":"대여료는 얼마인가요?","context":example_context,
         "answer":{"status":"", "answer":"", "source_ids":[], "missing_information":""}},
    ]
    # TODO: 정상 답에는 [901], 정보 부족에는 []와 부족한 사실 이름을 사용합니다.
    # [해설-중학생용] 위의 빈칸("")은 시험지의 빈 답칸과 같아요. 아래에서 답을 채워 넣었어요.
    #  - 첫 질문(어디서 대여?)은 자료 901번에 답이 있으니 status="answered", source_ids=[901] (출처 번호)
    #  - 둘째 질문(대여료?)은 자료에 가격이 없으니 "모르겠다"가 정답: "insufficient_context"(자료 부족),
    #    source_ids=[](근거 없음), 부족한 정보는 "대여료"라고 적어요.
    #  기존 줄은 지우지 않으려고, 빈칸 위에 값을 다시 덮어썼어요.
    examples[0]["answer"] = {"status":"answered","answer":"안내 데스크에서 대여합니다.","source_ids":[901],"missing_information":""}
    examples[1]["answer"] = {"status":"insufficient_context","answer":"제공된 지식으로는 답할 수 없습니다.","source_ids":[],"missing_information":"대여료"}
    # [해설] 아래 raise는 "아직 숙제 안 했어요!" 하고 멈추는 경고문이에요. 숙제를 끝냈으니 #으로 잠재웠어요.
    # raise NotImplementedError("D21-02-I01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-I01
    return examples

def main():
    examples=build_examples()
    # TODO D21-02-I02: 같은 질문에 Zero-shot과 Few-shot Prompt를 각각 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 두 Prompt가 생성됩니다. 이는 05의 근거 규칙 A/B와 별도 설계 실험입니다.
    # BEGIN D21-02-I02
    case = read_json(DATA/"dev_v1.json")[0]
    zero_bundle = make_bundle(examples=[])     # 예제 없는 입력
    few_bundle = make_bundle(examples=[])      # TODO: examples 사용
    zero_prompt, _ = render_prompt(zero_bundle, case, "A")
    few_prompt, _ = render_prompt(few_bundle, case, "A")
    # TODO: 예제 ID 901의 포함 여부를 확인
    # [해설-중학생용] 위의 few_bundle은 예제를 빈 상자([])로 만들어서 Zero-shot과 똑같아져 버렸어요.
    #  Few-shot은 "예제를 보여주는" 방식이니, 예제가 든 상자로 다시 만들고 프롬프트도 다시 만들어요.
    few_bundle = make_bundle(examples=examples)
    few_prompt, _ = render_prompt(few_bundle, case, "A")
    # 확인(assert): 예제 없는 쪽엔 901이 없고, 예제 있는 쪽엔 901이 있어야 정상이에요. 아니면 바로 알려줘요.
    assert "901" not in zero_prompt and "901" in few_prompt
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-02-I02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-I02
    # TODO D21-02-I03: 변경점·가설·고정 조건과 두 Prompt를 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 가설을 실제 성능 결과처럼 기록하지 않습니다.
    # BEGIN D21-02-I03
    experiment = {
        "experiment":"examples_design_only", "base_version":"examples_zero_v1", "new_version":"examples_few_v1",
        "changed":"", "hypothesis":"", "fixed":[], "source_mode":"design_only"
    }
    # TODO: 예제 유무를 바꿨다는 기록과 고정 조건을 작성
    write_json(HERE/"outputs"/"examples.json", [])  # TODO: examples
    write_json(HERE/"outputs"/"experiment.json", experiment)
    write_text(HERE/"outputs"/"zero_prompt.txt", "")  # TODO: zero_prompt
    write_text(HERE/"outputs"/"few_prompt.txt", "")   # TODO: few_prompt
    # [해설-중학생용] 위에서는 빈 내용으로 파일을 먼저 만들었어요. 이제 진짜 내용으로 다시 저장해요(덮어쓰기).
    #  실험 기록은 "무엇을 바꿨나(예제 유무)", "어떻게 될 거라 예상하나(가설)", "그대로 둔 것(고정 조건)"을 적어요.
    #  가설은 '예상'일 뿐 실제 성능 결과가 아니라서 "관찰한다"라고만 써요.
    experiment.update({"changed":"예제 유무","hypothesis":"정상과 정보 부족의 출력 조합을 잘 따를지 관찰한다.",
                       "fixed":["질문","knowledge_v1","answer_schema_v1","근거 규칙"]})
    write_json(HERE/"outputs"/"examples.json", examples)
    write_json(HERE/"outputs"/"experiment.json", experiment)
    write_text(HERE/"outputs"/"zero_prompt.txt", zero_prompt)
    write_text(HERE/"outputs"/"few_prompt.txt", few_prompt)
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-02-I03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-I03
    # TODO D21-02-I04: 예제 하나의 질문 표현만 바꾸고 새 버전으로 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기존 examples를 변경하지 않고 새 파일로 저장합니다.
    # BEGIN D21-02-I04
    replaced = json.loads(json.dumps(examples,ensure_ascii=False))
    # TODO: replaced[0]["question"]만 바꾸고 새 버전·이유 기록
    record = {"version":"examples_few_v2","changed":"","hypothesis":"","examples":replaced}
    # TODO: save_version 사용. 05 A/B에 이 변경을 함께 섞지 마세요.
    # [해설-중학생용] 예제 하나의 '질문 말투'만 살짝 바꿔서 새 버전(v2)으로 기록해요. 딱 하나만 바꾸는 게 핵심이에요.
    #  - replaced는 원본(examples)을 통째로 복사한 거라, 여기를 바꿔도 원본은 그대로예요(복사본에 낙서하는 것과 같아요).
    #  - 질문 뜻은 같고 표현만 달라요: "어디서 대여하나요?" -> "대여 장소를 알려 주세요."
    #  - save_version은 같은 이름 파일의 내용이 다르면 덮어쓰기를 막아 줘요. 그래서 기록이 몰래 바뀌지 않아요.
    #  - 05번 A/B 실험에는 이 변경을 섞지 않아요(한 번에 하나만 바꿔야 원인을 알 수 있어서예요).
    replaced[0]["question"] = "대여 장소를 알려 주세요."
    record.update({"changed":"정상 예제 질문 표현 1개","hypothesis":"의미가 같은 표현에도 출력 계약을 유지하는지 관찰",
                   "examples":replaced,"fixed_context":"knowledge_v1","fixed_schema":"answer_schema_v1"})
    save_version(HERE/"outputs"/"examples_few_v2.json", record)
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-02-I04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-I04
    print("[02] 예제·버전 설계 완료. 05는 예제 고정, 근거 규칙만 비교합니다.")
