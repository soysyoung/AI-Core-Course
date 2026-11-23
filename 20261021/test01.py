class Idea:
    def __init__(self, name, problem, roles, difficulty):
        self.name = name.strip()
        self.problem = problem.strip()
        self.roles = list(roles)
        self.difficulty = difficulty

    def summary(self):
        return f"{self.name}:  역할 {self.roles}개"


# a = Idea("문서 도우미", "자료 찾기", ["Researcher", "Writer"], "응용")
# print(a.summary())


# first = Idea("문서", "검색", ["Researcher"], "응용")
# second = Idea("학습", "복습", ["Tutor"], "기본필수")
# first.roles.append("Writer")

# print(first.summary())
# print(second.summary())
# print(Idea.summary(first) == first.summary())


# class WorngIdea:
#     roles = []

# x = WrongIdea()
# y = WrongIdea()
# x.roles.append("Writer")
# print(


from pathlib import Path

base = Path(__file__).resolve().parent
path = base / "data" / "note.txt"
path.parent.mkdir(parents=True, exist_ok=True)

with path.open("w", encoding="utf-8") as f:
    f.write("오늘은 클래스와 파일을 배웁니다\n")

with path.open("r", encoding="utf-8") as f:
    text = f.read()

print(path.name)
print(text.strip())