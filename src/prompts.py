# source/prompts.py
from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = (
    "다음 문서만을 근거로 사용자 질문에 답하세요."
    "근거가 부족하면 '주어진 자료에서는 확인할 수 없습니다.'라고 답하세요.\n\n"
    "{context}"
)


JUDGE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
      "당신은 답변 품질을 평가하는 채점자입니다.\n"
      "의미가 일치하면 1, 부분적으로만 일치하면 0.5, 무관하면 0을 점수로 매기세요.\n"
      "응답은 반드시 첫 줄에 0/0.5/1 중 하나의 숫자만, 둘째 줄부터 짧은 이유를 적으세요."),
    (
        "human",
        "질문: {question}\n\n"
        "기대 답변: {reference}\n\n"
        "모델 답변: {prediction}"
    ),
  ])