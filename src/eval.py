#평가
from langsmith.evaluation import evaluate
from langsmith import Client

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from source.prompts import JUDGE_PROMPT
from source.eval.dataset import get_or_create_dataset, preview_dataset
from source.settings import settings

import os

# ==================================================
# 1. 평가자

# === 평가자 1 휴리스틱 Evaluator : 키워드 포함 여부 (규칙 기반) ===
def contains_expected_keyword(run, example):
  pred = run.outputs.get("answer", "")
  expected = example.outputs.get("answer","")

  # === 기대 답변에서 명사로 보이는 단어(2글자 이상 단어) 2개를 키워드로 사용 ===
  # 단점: 단어 선택이 split()이라 조사가 안 붙은 정확한 단어가 아니면 매칭 실패 가능
  keywords = [w for w in expected.split() if len(w) >= 2][:2]
  hit = all(k in pred for k in keywords)

  return {
      "key": "contains_expected_keyword",
      "score": 1 if hit else 0,
      "comment": f"필수 키워드 {keywords} 포함 여부"
  }

# === 평가자 2 LLM-as-Judge Evaluator : 의미 일치 판단 (의미 기반) ===
def make_llm_judge(llm):
  # llm을 주입받아 llm_judge 평가자 함수를 생성하는 팩토리 함수
  judge_chain = JUDGE_PROMPT | llm | StrOutputParser()

  def llm_judge(run, example):
    # LLM을 채점자로 활용해 0/0.5/1 점수 산출
    # 첫 줄 숫자만 파싱, 실패시 0점 처리
    reply = judge_chain.invoke({
        "question": example.inputs["question"],
        "reference": example.outputs["answer"],
        "prediction": run.outputs["answer"],
    })
    # === 첫 줄의 숫자만 점수로 사용 ===
    first_line = reply.strip().splitlines()[0].strip()
    try:
      score = float(first_line)
    except ValueError:
      score = 0
    return {
        "key": "llm_judge_semantic_match",
        "score": score,
        "comment": reply,
    }
  
  return llm_judge

# ==================================================
# 2. 평가대상 (target)
def make_target(rag):
  def target(inputs):
    return {"answer": rag.invoke(inputs["question"])}
  return target

# ==================================================
# 3. EVALUATION
def eval_rag(rag):
    client = Client()

        # ==== 필요없는 부분??
    #데이터셋 준비
    dataset = get_or_create_dataset(client)
    #확인용
    loaded = client.read_dataset(dataset_name=settings.eval_dataset_name)
    preview_dataset(client, loaded, 2)
        # ===================
    # 평가하는 모델은 평가 받는 모델과 다른 모델을 선택한다.
    judge_llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
    
    # 평가자
    llm_judge = make_llm_judge(judge_llm)

    # 평가 대상
    target = make_target(rag)

    # === 평가 실행 === 
    # target 함수를 데이터셋의 모든 질문에 대해 실행
    result = evaluate(
        target,
        data=settings.eval_dataset_name,
        evaluators = [contains_expected_keyword, llm_judge], # 규칙 기반 & 의미 기반
        experiment_prefix="v1-baseline",
    )

    return result