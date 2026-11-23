# course="AI 개발"
# day=2
# message=f"{course} Day {day} 시작!"
# print(message)


# a = 10
# input("나이: ")


# name = input("이름: ")
# hours = float(input("오늘 학습시간: "))
# target = 8
# rate = hours / target * 100
# print(f"{name}님의 달성률: {rate:.1f}%")


# student = {
#     "name": "민지",
#     "scores": [82,95,76,88],
#     "skills": ["Python", "Git", "Python"]
# }
# student["average"] = sum(student["scores"]) / len(student["scores"])
# print(f"{student['name']}님의 평균 점수: {student['average']:.1f}")
# print("기술:", student["skills"])


# age = int(input("나이: "))
# member = input("회원(y/n): ")

# if age < 19:
#     fee = 8000
# elif age >= 65:
#     fee = 7000
# else:
#     fee = 12000

# if member == "y":
#     fee = int(fee * 0.9)
# print(f"최종 요금: {fee:,}원")


# def average(values):
#     if not values:
#         return 0
#     return sum(values ) / len (values)    

# def summarize(name, scores):
#     avg = average(scores)
#     return f"{name}: 평균 {avg:.1f}"

# print(summarize("민지", [82, 95, 76, 88]))
# print(summarize("준호", []))


items = []

whie True:
    command = input("명령> ").strip()
    if command == "quit":
        break
    if command.startswith("add "):
        item = command[4:]
        item = item.strip()
        if item:
            items.append(item)
            print("추가했습니다.")
        else:
            print("빈 항목은 추가할 수 없습니다.")