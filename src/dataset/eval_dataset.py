from source.settings import settings

EVAL_QUESTIONS = [
    {
        "question": "RAG란 무엇인가요?",
        "answer":   "RAG란 외부 문서를 가져와서 그것을 기반으로 LLM이 답변하도록 하는 기법입니다.",
    },
    {
        "question": "유사도 검색은 무엇인가요?",
        "answer":   "사용자 질문 벡터와 벡터 DB에 있는 벡터 사이의 각도를 계산하여 유사도를 측정하는 방법입니다.",
    },
    {
        "question": "멀티 프로세스는 무엇인가요?",
        "answer":   "멀티 프로세스는 하나의 프로그램을 여러 프로세스로 나누어 동시에 실행하는 방식으로 멀티 코어일 경우 병렬 처리가 가능합니다.",
    },
    {
        "question": "시간 역전파에 대해 설명해주세요.",
        "answer":   "시간 역전파는 층(Layer)을 역으로 가는 것이 아니라 시간을 역으로 가면서 역전파를 계산하는 것입니다.",
    },
]

# ============================================
# 1. 데이터셋 
def get_or_create_dataset(client):
  # 1. 평가용 입력/출력 분리
  inputs = [{"question": ex["question"]} for ex in EVAL_QUESTIONS]
  outputs = [{"answer": ex["answer"]} for ex in EVAL_QUESTIONS]

  # 2. 데이터셋 존재 여부 확인 (중복 생성 방지)
  # 이미 데이터셋 존재하면 재사용, 없으면 새로 생성

  # 이름이 일치하는 데이터셋들을 리스트로 반환
  existing = [d for d in client.list_datasets(dataset_name=settings.eval_dataset_name)]

  if existing:
    dataset = existing[0]
    print(f"[INFO] 기존 Dataset 사용: {dataset.id}")
  else:
    dataset = client.create_dataset(  # 데이터셋 새로 생성
        dataset_name = settings.eval_dataset_name,
        description="TIL RAG 답변 품질 평가용"
    )
    print(f"[INFO] 새 Dataset 생성: {dataset.id}")
    client.create_examples(           # 데이터셋 새로 만든 경우에만 example 추가
        dataset_id = dataset.id,
        inputs=inputs,
        outputs=outputs,
    )
    print(f"[INFO] Example {len(EVAL_QUESTIONS)}건 추가 완료")

  return dataset

def preview_dataset(client, dataset, n):
  # 데이터셋 내용을 미리 확인 (디버깅용)
  examples = list(client.list_examples(dataset_id=dataset.id))
  print(f"[PREVIEW] 총 Example 수: {len(examples)}")

  # Example 미리 보기 출력 : 데이터가 제대로 들어갔는지 확인하는 디버깅용 코드
  for ex in examples[:n]:
    print("Q:", ex.inputs["question"])
    print("A:", ex.outputs["answer"] if ex.outputs else "(없음)")
    print()

  return examples