"""Day21 실습 01: Prompt 구조와 요구사항. 실행: python main.py"""
from pathlib import Path
import sys
import json
from string import Template

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text
from coursekit.prompting import CONTRACT_TEXT

# 기준: Day21 PPT 7~13장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def build_requirements():
    # TODO D21-01-I01: 역할·작업·입력·제약·실패·출력 여섯 칸을 완성하세요.
    # 입력·대상: PPT 8장의 여섯 요소
    # 완료 기준: 6개 키가 모두 있고 각 문장이 비어 있지 않습니다.
    # 핵심: 역할을 전문가로 꾸미는 것과 정확한 근거를 제공하는 것은 다릅니다.
    # BEGIN D21-01-I01
    requirements = {
        "role": "",         # TODO: 누구를 돕는 작성자인가?
        "task": "",         # TODO: 어떤 질문에, 어떤 언어·길이로 답할까?
        "input": "",        # TODO: 질문과 선택 지식
        "constraints": "",  # TODO: 근거 범위와 예제 ID 사용 금지
        "failure": "",      # TODO: 없는 사실을 추측하지 않는 처리
        "output": "",       # TODO: 출력할 네 필드 이름
    }
    # [해설-중학생용] 위의 여섯 칸이 전부 ""(빈칸)이라 "누가, 무엇을, 어떻게 할지" 아무 정보도 없었어요.
    #  좋은 부탁 글(프롬프트)은 여섯 가지가 필요해요: 역할·작업·입력·제약·실패 처리·출력 모양.
    #  (심부름을 시킬 때 "누가 / 뭘 / 뭘 가지고 / 하지 말 것 / 모르면 어떻게 / 결과는 어떤 모양" 을 말해 주는 것과 같아요)
    #  기존 줄은 지우지 않으려고, 아래에서 빈칸을 진짜 문장으로 다시 채웠어요.
    requirements.update({
        "role": "초보 수강생의 실습 도움말 작성자",
        "task": "제공된 지식으로 질문에 한국어 2문장 이내로 답합니다.",
        "input": "사용자 질문과 선택한 지식 목록",
        "constraints": "제공된 근거만 사용하고 예제 ID를 답에 복사하지 않습니다.",
        "failure": "답을 뒷받침하는 사실이 없으면 정보 부족을 명시합니다.",
        "output": "status, answer, source_ids, missing_information 네 필드 JSON",
    })
    # [해설] 아래 raise는 "아직 숙제 안 했어요!" 하고 멈추는 경고문이에요. 숙제를 끝냈으니 #으로 잠재웠어요.
    # raise NotImplementedError("D21-01-I01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-01-I01
    return requirements

def build_prompt(question, rows, requirements):
    # TODO D21-01-I02: 빈 질문과 필수 요구사항 누락을 먼저 거부하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 빈 질문/빈 조건을 유효 Prompt처럼 저장하지 않습니다.
    # BEGIN D21-01-I02
    required = {"role", "task", "input", "constraints", "failure", "output"}
    # TODO: question.strip(), 키 집합, 각 값의 빈 문자열 여부를 검사합니다.
    invalid = False  # TODO: 조건을 작성하고 ValueError로 중단하세요.
    # [해설-중학생용] 위의 invalid가 항상 False라서 "아무 검사도 안 하고 다 통과"시키고 있었어요.
    #  문 앞에서 입장권을 검사하는 것처럼, 프롬프트를 만들기 전에 먼저 이상한 입력을 막아요.
    #   ① 질문이 비었거나 공백뿐이면 거부 (question.strip()이 빈 글이면 거짓)
    #   ② 여섯 칸의 이름이 정확히 맞지 않으면 거부 (하나 빠졌거나 더 있어도 안 돼요)
    #   ③ 칸 중에 내용이 빈 곳이 있으면 거부
    #  하나라도 걸리면 ValueError로 바로 멈춰서, 엉터리 프롬프트가 저장되는 걸 막아요.
    invalid = (not question.strip()) or set(requirements) != required or any(not v.strip() for v in requirements.values())
    if invalid:
        raise ValueError("빈 질문이거나 요구사항 여섯 칸이 완성되지 않았습니다")
    # [해설] 아래 raise는 멈춤 경고문이라, 숙제를 끝낸 뒤 #으로 잠재웠어요.
    # raise NotImplementedError("D21-01-I02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-01-I02
    # TODO D21-01-I03: Template에 질문·직렬화한 지식·출력 계약을 대입하세요.
    # 입력·대상: question, rows, requirements; CONTRACT_TEXT는 제공 코드
    # 완료 기준: 질문·지식 원문·네 필드 약속이 prompt에 있으며 $question이 남지 않습니다.
    # 핵심: 지식 본문은 데이터입니다. Template 대입은 코드 실행 또는 보안 권한 부여가 아닙니다.
    # BEGIN D21-01-I03
    context_json = json.dumps([], ensure_ascii=False)  # TODO: rows
    # JSON 중괄호와 충돌하지 않도록 $변수 형식인 Template을 사용합니다.
    template = Template("[역할] $role\n[작업] $task\n[입력] $input\n[질문] $question\n[지식 데이터] $context_json\n[제약] $constraints\n[실패] $failure\n[출력] $contract")
    prompt = template.substitute(
        **requirements,
        question="",           # TODO: question
        context_json="",       # TODO: 위 context_json
        contract=CONTRACT_TEXT,
    )
    # [해설-중학생용] 위에서는 질문(question)과 지식(context_json)이 ""(빈칸)이어서 편지에 내용이 없었어요.
    #  편지 양식(Template)의 $빈칸에 진짜 질문과 지식 글(JSON)을 끼워 넣어 완성해요.
    #  - 지식은 json.dumps로 글자로 바꿔요(한글이 깨지지 않게 ensure_ascii=False).
    #  - 지식 본문은 그냥 '자료'일 뿐이라, 끼워 넣는다고 코드가 실행되거나 권한이 생기지는 않아요.
    context_json = json.dumps(rows, ensure_ascii=False)
    prompt = template.substitute(**requirements, question=question, context_json=context_json, contract=CONTRACT_TEXT)
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-01-I03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-01-I03
    return prompt

def main():
    requirements=build_requirements()
    rows=read_json(DATA / "knowledge_v1.json")[:1]
    prompt=build_prompt("파일을 어디에 보관하나요?",rows,requirements)
    # TODO D21-01-I04: 요구사항과 Prompt 원문을 저장하고 기준 질문을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: outputs/requirements.json 및 prompt.txt 생성. 아직 실제 모델 품질 결과는 없습니다.
    # BEGIN D21-01-I04
    assert len(requirements) == 6
    # TODO: prompt에 질문과 '개인 폴더'가 있는지 확인하세요.
    write_json(HERE / "outputs" / "requirements.json", {})  # TODO: requirements
    write_text(HERE / "outputs" / "prompt.txt", "")        # TODO: prompt
    # [해설-중학생용] 위에서는 빈 내용({}와 "")을 저장해 버렸어요. 진짜 내용으로 다시 저장해요(덮어쓰기).
    #  저장하기 전에 assert로 검사해요: 여섯 칸이 다 차 있는지, 프롬프트에 질문과 '개인 폴더'(지식 101의 내용)가 들어갔는지.
    #  틀리면 바로 알려 줘서, 잘못된 파일이 저장되는 걸 막아요.
    #  (아직 실제 AI가 답한 게 아니라 '부탁 글'만 만든 거라, 모델 품질 결과는 없어요.)
    assert all(requirements.values())
    assert "파일을 어디에 보관하나요?" in prompt and "개인 폴더" in prompt
    write_json(HERE / "outputs" / "requirements.json", requirements)
    write_text(HERE / "outputs" / "prompt.txt", prompt)
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-01-I04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-01-I04
    # TODO D21-01-I05: 정상·정보 부족 두 질문에 같은 요구사항을 적용하고 충돌 지시를 고치세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 두 Prompt의 질문만 달라집니다. 예상 행동과 실측을 구분합니다.
    # BEGIN D21-01-I05
    questions = ["파일을 어디에 보관하나요?", "파일은 몇 년 보관하나요?"]
    prompts = []  # TODO: 각 질문을 build_prompt에 전달
    conflict = {"before":"근거가 없어도 반드시 숫자로 답한다.","after":"","reason":""}
    # TODO: 충돌을 제거하는 문장과 이유를 적고 two_cases.json으로 저장
    # [해설-중학생용] 두 질문(정상 / 정보 부족)에 '같은 여섯 칸'을 써서 프롬프트를 두 개 만들어요.
    #  바뀌는 건 질문뿐이라, 나중에 결과가 달라져도 "질문 때문이구나" 하고 원인을 알 수 있어요(한 번에 하나만 바꾸기).
    #  그리고 위의 conflict는 "근거가 없어도 반드시 숫자로 답한다"인데, 이건 "주어진 근거만 써라"와 서로 싸워요.
    #  (숙제에 "모르는 문제도 꼭 답을 써라"와 "아는 것만 써라"가 같이 있는 것과 같아요.)
    #  그래서 "기간 정보가 없으면 insufficient_context(정보 부족)로 답한다"로 고치고, 이유도 적어요.
    prompts = [build_prompt(q, rows, requirements) for q in questions]
    conflict["after"] = "기간 정보가 없으면 insufficient_context로 응답한다."
    conflict["reason"] = "추측 강제는 제공 근거만 사용하라는 규칙과 충돌한다."
    write_json(HERE / "outputs" / "two_cases.json", {"prompts":prompts, "conflict_review":conflict})
    # [해설] 아래 raise는 멈춤 경고문이라 #으로 잠재웠어요.
    # raise NotImplementedError("D21-01-I05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-01-I05
    print("[01] Prompt 요구사항과 원문 저장 완료. 모델 결과가 아닙니다.")
