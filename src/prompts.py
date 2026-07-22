# source/prompts.py
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

SYSTEM_PROMPT = (
    "다음 문서만을 근거로 사용자 질문에 답하세요.\n"
    "답변 후 반드시 '[출처] '라는 표시와 함께 참고한 문서의 파일명과 pdf문서의 경우에는 출처 페이지를 나열하세요.\n"
    "여러 문서나 페이지를 참고했다면 모두 나열하세요.\n"
    "근거가 부족하면 '주어진 자료에서는 확인할 수 없습니다.'라고 답하세요.\n\n"
    "{context}"
)

# from_template은 문자열에서 {변수}를 자동으로 감지한다.
SYSTEM_PROMPT2 = PromptTemplate.from_template(
    "다음 문서만을 근거로 사용자 질문에 답하세요.\n"
    "답변 후 반드시 '[출처] '라는 표시와 함께 참고한 문서의 파일명과 pdf문서의 경우에는 출처 페이지를 나열하세요.\n"
    "여러 문서나 페이지를 참고했다면 모두 나열하세요.\n"
    "근거가 부족하면 '주어진 자료에서는 확인할 수 없습니다.'라고 답하세요.\n\n"
    "{context}"
)
# 템플릿 사용 안 한것과 사용법은 동일 : prompt.format(context=)

# 로컬 모델은 직접 출처 넣어야 함.
SYSTEM_PROMPT_LOCAL = (
    "다음 문서만을 근거로 사용자 질문에 답하세요.\n"
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