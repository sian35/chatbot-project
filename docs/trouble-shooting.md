# Trouble Shooting 기록
## 260705
### 문제 1 : 로컬 모델의 대답이 내 의도와 다르다.
#### 1) 상황
문서만을 근거로 답변하고 근거가 된 문서의 출처를 밝히도록 프롬프트를 설정하였지만 Gemini는 이 프롬프트를 이해하여 출처를 잘 남겼으나, Ollama 모델은 출처를 밝히지 않는 문제 발생.  
예외 상황 : Ollama 모델도 어떨 때는 출처를 남기기도 한다.

#### 2) 원인 : 모델 별 성능 차이

#### 3) 시도한 방법
모델 별로 프롬프트를 다르게 설정, 로컬 모델의 경우 하드 코딩으로 출처를 따로 설정해줌

#### 4) 결론
해결이 되었나? 확실하지 않음

### 문제2 : API 모델과 로컬 모델의 응답 형태 차이
#### 1) 상황
최신 Gemini 모델은 content를 문자열 대신 content block 리스트로 반환한다.

#### 2) 해결 방법 : 어떤 형태로 답변이 오든 문자열로 형태 변환을 해줘서 반환하기


## 260707
### 문제 : 문서 로딩 후 임베딩 시 메모리 부족 문제
#### 1) 에러 발생 위치 : data_loader.py
```
RuntimeError: Invalid buffer size: 21.98 GiB
```
#### 2) 원인 : 청킹 없이 문서 로딩해서 임베딩
- 임베딩 모델이 임베딩할 때 입력 텍스트 길이에 비례해서 메모리를 사용한다.
- 임베딩 모델의 최대 입력 길이 제한 (e.g., BGE-M3 : 8192 tokens)

#### 또다른 해결법: 임베딩 모델 생성시 청크 사이즈 설정 -> 직접 해보기 필요 

#### 3) 새롭게 알게 된 방법 : MarkdownHeaderTextSplitter

#### 4) 결론 : 청킹은 선택이 아니라 필수이다. 
청킹을 하지 않았던 이유는 문서들이 이미 주제별로 나뉘어져 있어서 청킹을 해서 문맥이 겹치게 되면 오히려 검색에 방해가 될 것이라고 생각했다.  
하지만 임베딩 모델의 최대 입력 길이에 제한이 있고, 또한 오히려 문서 전체를 하나의 벡터로 만들면 전체에서 관련 내용을 찾아야 하기 때문에 검색도의 정확도가 떨어진다는 것을 알게 되었다.


## 260712
### Mac 파일 시스템(HFS+) 한글 유니코드 정규화 문제 
pdf_name: str = "2026_경제금융용어_800선.pdf"
#### 원인: NFC(완성형) vs NFD(분해형)
파일명은 분해형, 검색어는 완성형 

```
print("경제금융" in settings.pdf_name)
print(repr("경제금융"))
print(repr(settings.pdf_name))

print(unicodedata.normalize("NFC", "경제금융") in unicodedata.normalize("NFC", settings.pdf_name))
# → True

# NFD 분해형 문제
print([hex(ord(c)) for c in "경제금융"])           # 검색어 유니코드
print([hex(ord(c)) for c in settings.pdf_name[:6]])  # 파일명 앞부분 유니코드
#  파일명이 분해형으로 되어있음
```
#### settings.py
```
    @field_validator("pdf_name")
    @classmethod
    def normalize_pdf_name(cls, v):
        return unicodedata.normalize("NFC", v)
```

### Preprocessing
pdf 내의 수식 처리 필요 
```
경제성장률(%) = 
금년 실질GDP - 전년 실질GDP
전년 실질GDP'
```

## 260714
### Docling 으로 로드시 DoclingDocument 객체로 로드됨.
LangGraph에 사용하기 위해서는 Document 객체로의 변환이 필요하다.

예시
```python
def docling_to_documents_by_page(doc, source_path):
    documents = []
    for page_no in sorted(doc.pages.keys()):
        page_doc = extract_single_page_doc(doc, page_no)   # 해당 페이지 아이템만 남긴 서브 트리
        documents.append(
            Document(
                page_content=page_doc.export_to_markdown(),
                metadata={"source": source_path, "page": page_no - 1},
            )
        )
    return documents
```

Document 객체로 변환 후 chunking 적용?

### Docling converter에 수식 옵션을 줘야 수식 영역이 제대로 변환됨
do_formula_enrichment=True

#### Issue
메모리 사용량 급증 -> 수식을 위해 감수할 가치가 있나?
