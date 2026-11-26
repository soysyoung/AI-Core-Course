"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record
from langchain_core.documents import Document
import argparse

# 오늘의 최소 Metadata 계약. 여섯 값 모두 입력 Hit에서 가져옵니다.
METADATA_KEYS = ("citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category")

def to_document(hit: dict) -> Document:
    """한 Hit의 본문과 여섯 Metadata 값을 Document로 옮깁니다."""
    # BEGIN D26-04-B01
    # TODO D26-04-B01: 본문을 page_content로, 제공된 여섯 Key를 metadata로 옮깁니다.
    # 힌트: Document(page_content=..., metadata=...)를 사용합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-04-B01 TODO 미완성")
    # [추가 설명] Hit은 "검색으로 찾은 글 조각 카드"이고, Document는 LangChain이 쓰는 "공식 서류 봉투"예요.
    # 봉투에는 두 칸이 있어요.
    #   - page_content: 봉투 안에 넣는 본문(글 내용)
    #   - metadata: 봉투 겉면에 붙이는 라벨(번호, 문서 이름, 버전, 위치, 분류)
    # 카드의 본문(body)은 봉투 안에, 정해진 여섯 라벨(METADATA_KEYS)은 겉면에 "그대로" 옮겨 적습니다.
    # hit[key]처럼 직접 꺼내므로, 라벨 하나라도 빠져 있으면 KeyError가 나서 바로 알 수 있어요.
    # (빠진 라벨을 몰래 빈칸으로 채우면 나중에 출처를 잃어버리니까, 일부러 오류가 나게 둡니다.)
    metadata = {key: hit[key] for key in METADATA_KEYS}  # 여섯 라벨을 하나씩 같은 이름으로 복사
    return Document(page_content=hit["body"], metadata=metadata)  # 본문은 바꾸지 않고 그대로 넣기
    # END D26-04-B01

def hits_to_documents(hits: list[dict]) -> list[Document]:
    """순서대로 변환한 Document 목록을 반환합니다. 빈 입력은 빈 목록입니다."""
    # BEGIN D26-04-B02
    # TODO D26-04-B02: 입력 순서대로 to_document를 호출해 목록을 반환합니다.
    # 힌트: 빈 목록도 특별한 가짜 문서 없이 그대로 빈 결과가 됩니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    # (아래 raise는 함수가 값을 돌려주려면 실행되면 안 되어서 주석 처리했습니다)
    # raise NotImplementedError("D26-04-B02 TODO 미완성")
    # [추가 설명] 카드 여러 장을 앞에서부터 한 장씩 봉투(Document)에 옮겨 담는 일이에요.
    # 순서를 바꾸지 않아야 "몇 번째 카드가 몇 번째 봉투"인지 나중에 맞춰 볼 수 있어요.
    # 카드가 한 장도 없으면(빈 목록) 봉투도 0개, 즉 빈 목록 []을 돌려주면 됩니다.
    # 아래 한 줄짜리 for문(리스트 컴프리헨션)은 빈 목록이 들어오면 자연스럽게 []가 돼요.
    return [to_document(hit) for hit in hits]
    # END D26-04-B02

def metadata_is_preserved(hit: dict, metadata: dict) -> bool:
    """제공된 관찰 함수: 여섯 필드가 모두 있고 각 값이 같은지 확인합니다."""
    required = {"citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category"}
    # 일부 필드만 복사한 결과를 '보존 완료'로 표시하지 않도록 Key 집합부터 확인합니다.
    return set(metadata) == required and all(metadata[key] == hit[key] for key in required)


def main():
    parser = argparse.ArgumentParser(description="Hit → 실제 LangChain Document 변환")
    parser.add_argument("--live-db", action="store_true", help="실제 E5·PostgreSQL 검색 결과를 입력으로 사용")
    parser.add_argument("--question", default="15분 늦으면 어떻게 기록되나요?")
    parser.add_argument("--category", default="학사", choices=["학사", "시설", "지원"])
    parser.add_argument("--candidate-k", type=int, default=3)
    args = parser.parse_args()
    if args.live_db:
        # --live-db를 선택한 경우에만 실제 모델·DB 준비 함수를 불러옵니다.
        from coursekit.live import make_search_hits
        search_hits = make_search_hits()
        hits = search_hits(args.question, args.category, k=args.candidate_k)
        mode, input_source = "live_db", "E5_PostgreSQL"
    else:
        hits = [example_hit()]
        mode, input_source = "local_adapter", "lecture_fixture"
    documents = hits_to_documents(hits)
    comparisons = []
    for hit, doc in zip(hits, documents):
        comparisons.append({
            "citation_id": doc.metadata["citation_id"],
            "body_preserved": doc.page_content == hit["body"],
            "metadata_preserved": metadata_is_preserved(hit, doc.metadata),
            "citation_id_type": type(doc.metadata["citation_id"]).__name__,
            "page_content": doc.page_content,
            "metadata": doc.metadata,
        })
    report = {
        "execution": execution_record(mode, db=args.live_db, embedding=args.live_db),
        "input_source": input_source,
        "input_count": len(hits), "document_count": len(documents),
        "documents": comparisons,
    }
    path = save_json(HERE, "document_adapter.json", report)
    show_success("04 기본필수", path)

if __name__ == "__main__":
    main()
