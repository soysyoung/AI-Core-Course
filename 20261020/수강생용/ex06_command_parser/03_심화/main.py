# -*- coding: utf-8 -*-
# 2026-10-20 Day 2 | 실습 06 | 심화
# 입력·분석·처리·출력 함수 분리 | PPT 61쪽
# 실행: python main.py (이 파일이 있는 폴더에서)
# 입력·완료 기준·예상 결과: 같은 폴더의 README.md, sample_input.txt, expected_output.txt
# 수강생용: TODO 부분을 완성한다. 제공된 입출력 형식과 함수 이름은 유지한다.
# NotImplementedError는 미완성 위치를 알리는 표식이다. 해당 줄을 실제 구현으로 교체한다.

def normalize_input(text):
    """사용자 입력의 앞뒤 공백만 제거한다."""
    # TODO 01: 앞뒤 공백만 정리해 반환하세요.
    # if not isinstance(text, str):
    #     raise NotImplementedError("TODO 1: normalize_input")
    return text.strip() # strip()를 사용하여 문자열의 앞뒤 공백을 제거한다.


def parse_command(text):
    """원본 입력을 받아 (명령, 인수) Tuple을 반환한다. 빈 입력은 ('', '')이다."""
    # TODO 02: 명령만 소문자로 바꾸고 (명령, 인수)를 반환하세요. 빈 입력도 처리하세요.
    # if not isinstance(text, str):
    #     raise NotImplementedError("TODO 2: parse_command")
    parts = text.strip().split(maxsplit=1) # strip()로 앞뒤 공백 제거 후, split()으로 공백 기준으로 나눈다. maxsplit=1로 명령과 나머지 전체를 분리한다.
    command = parts[0].lower() if parts else "" # parts[0].lower()로 명령을 소문자로 변환한다. parts가 비어있으면 command는 빈 문자열("")이 된다.
    value = parts[1] if len(parts) > 1 else "" # parts[1]이 존재하면 value에 할당하고, 없으면 빈 문자열("")을 할당한다.
    return command, value


def add_item(items, value):
    """공백 정리 후 유효한 항목을 추가하고 bool을 반환한다."""
    # TODO 03: 유효 항목 추가와 성공 여부 반환을 구현하세요.
    # if not isinstance(items, list):
    #     raise NotImplementedError("TODO 3: add_item")
    # if not isinstance(value, str):
    #     raise NotImplementedError("TODO 3: add_item")
    value = normalize_input(value) # normalize_input() 함수를 사용하여 value의 앞뒤 공백을 제거한다.
    if not value:
        return False
    items.append(value) # items 리스트에 value를 추가한다.
    return True


def search_items(items, keyword):
    """원본을 바꾸지 않고 부분 일치한 항목의 새 List를 반환한다."""
    # TODO 04: 빈 검색어는 []를, 그 외는 부분 일치 List를 반환하세요.
    # if not isinstance(items, list):
    #     raise NotImplementedError("TODO 4: search_items")
    # if not isinstance(keyword, str):
    #     raise NotImplementedError("TODO 4: search_items")
    keyword = normalize_input(keyword)
    if not keyword:
        return []
    return [item for item in items if keyword.lower() in item.lower()]


def format_items(items):
    """데이터를 콘솔용 문자열로 변환한다. 화면에 직접 출력하지 않는다."""
    # TODO 05: 목록을 번호가 포함된 여러 줄 문자열로 반환하세요.
    # if not isinstance(items, list):
    #     raise NotImplementedError("TODO 5: format_items")
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, start=1)) 
    # join()을 사용하여 각 항목을 번호와 함께 문자열로 변환하고, 여러 줄 문자열로 반환한다.


def main():
    items = []
    while True:
        command, value = parse_command(input("명령> "))
        if not command:
            print("명령을 입력하세요.")
        elif command == "quit":
            if value:
                print("quit에는 인수를 붙이지 않습니다.")
            else:
                print("종료합니다.")
                break
        elif command == "add":
            if add_item(items, value):
                print("추가했습니다.")
            else:
                print("추가할 항목을 입력하세요.")
        elif command == "list":
            if value:
                print("list에는 인수를 붙이지 않습니다.")
            else:
                print(format_items(items))
        elif command == "search":
            if not value:
                print("검색어를 입력하세요.")
            else:
                matches = search_items(items, value)
                if matches:
                    print(format_items(matches))
                else:
                    print("검색 결과가 없습니다.")
        else:
            print("알 수 없는 명령입니다.")


if __name__ == "__main__":
    main()


# 명령> 추가했습니다.
# 명령> 추가했습니다.
# 명령> 1. AI Agent
# 명령> 1. AI Agent
# 2. Python
# 명령> 종료합니다.
