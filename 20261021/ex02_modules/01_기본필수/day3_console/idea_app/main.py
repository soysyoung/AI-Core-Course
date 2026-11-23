"""실행 진입점: 반드시 day3_console에서 python -m idea_app.main으로 실행합니다."""
from idea_app.models import Idea
from idea_app.service import IdeaCatalog

def main():
    catalog = IdeaCatalog()
    catalog.add(Idea("문서", "문서 검색", ["검색"], "기본"))
    catalog.add(Idea("학습", "학습 도움", ["설명", "복습"], "기본"))
    print(catalog.names())

if __name__ == "__main__":
    main()
