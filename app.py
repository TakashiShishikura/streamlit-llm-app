
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

load_dotenv()

# Webアプリの概要・操作説明
st.title("LLM専門家相談アプリ")
st.markdown("""
このアプリは、選択した専門家の視点でLLM（大規模言語モデル）に質問できるデモです。\
1. 専門家の種類を選択してください。\
2. 質問や相談内容を入力し、送信ボタンを押してください。\
3. LLMが専門家として回答します。
""")

# 専門家の種類を定義
experts = {
	"キャリアコンサルタント": "あなたは優秀なキャリアコンサルタントです。相談者のキャリアや仕事の悩みに親身に答えてください。",
	"健康アドバイザー": "あなたは信頼できる健康アドバイザーです。健康や生活習慣に関する質問に丁寧に答えてください。",
	"ITエンジニア": "あなたは経験豊富なITエンジニアです。技術的な質問に分かりやすく答えてください。"
}

# ラジオボタンで専門家選択
selected_expert = st.radio("専門家を選択してください", list(experts.keys()))

# 入力フォーム
user_input = st.text_area("質問・相談内容を入力してください", height=100)

# LLM呼び出し関数
def ask_llm(user_text: str, expert_key: str) -> str:
	"""
	入力テキストと専門家種別を受け取り、LLMからの回答を返す
	"""
	system_prompt = experts[expert_key]
	openai_api_key = os.getenv("OPENAI_API_KEY")
	if not openai_api_key:
		return "OpenAI APIキーが設定されていません。環境変数 'OPENAI_API_KEY' を設定してください。"
	llm = ChatOpenAI(
		openai_api_key=openai_api_key,
		model_name="gpt-4o-mini",
		temperature=0.7
	)
	messages = [
		SystemMessage(content=system_prompt),
		HumanMessage(content=user_text)
	]
	response = llm(messages)
	return response.content

# 送信ボタン
if st.button("送信"):
	if not user_input.strip():
		st.warning("質問内容を入力してください。")
	else:
		with st.spinner("LLMが回答中..."):
			answer = ask_llm(user_input, selected_expert)
		st.markdown("#### 回答")
		st.write(answer)