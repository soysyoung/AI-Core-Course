# -*- coding: utf-8 -*-
# 2026-10-20 Day 2 | 실습 02 | 응용
# 수강생 Dict에 평균 추가 | PPT 30쪽
# 실행: python main.py (이 파일이 있는 폴더에서)
# 입력·완료 기준·예상 결과: 같은 폴더의 README.md, sample_input.txt, expected_output.txt
# 수강생용: TODO 부분을 완성한다. 제공된 입출력 형식과 함수 이름은 유지한다.
# NotImplementedError는 미완성 위치를 알리는 표식이다. 해당 줄을 실제 구현으로 교체한다.

# TODO 01: 지정한 키 name·desired_role·scores를 가진 수강생 Dict를 작성하세요.
student = {"name": "민지", "desired_role": "AI Agent 개발자", "scores": [82, 95, 76, 88], "average": 0.0}
# input_name = input("이름: ")
# input_desired_role = input("관심직무: ")
# student["name"] = input_name
# student["desired_role"] = input_desired_role
# input_scores = input("점수(쉼표로 구분): ")
# student["scores"] = [int(score) for score in input_scores.split(",")]
# TODO 02: 점수 List로 평균을 계산하여 average 키에 저장하세요. 
# student["average"] = 0.0
input_average = sum(student["scores"]) / len(student["scores"])
student["average"] = input_average

print(f"이름: {student['name']}")
print(f"관심직무: {student['desired_role']}")
print(f"점수: {student['scores']}")
print(f"평균: {student['average']:.1f}")
