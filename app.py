from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()

# 定数
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.5
MAX_RESPONSE_LENGTH = 200

def initialize_llm(model_name, temperature):
    """LLMの初期化"""
    return ChatOpenAI(model_name=model_name, temperature=temperature)

def create_system_message(role):
    """システムメッセージを生成"""
    return SystemMessage(content=f"あなたは{role}に関する専門家です。質問に対して{MAX_RESPONSE_LENGTH}文字以内で回答してください。")

def handle_user_input(llm, conversation_history, user_input):
    """ユーザー入力を処理し、LLMの応答を取得"""
    if not user_input.strip():
        st.warning("入力が空です。相談内容を入力してください。")
        return None
    conversation_history.append(HumanMessage(content=user_input))
    return llm(conversation_history)

# Streamlit UI
st.title("LLMに相談するアプリ")
st.write("動作モードに応じて、LLMが回答を返します")

# 動作モード選択
llm_role = st.radio("動作モードを選択してください。", ["掃除", "料理", "育児"])

st.divider()

# LLMの初期化
llm = initialize_llm(DEFAULT_MODEL, DEFAULT_TEMPERATURE)

# 会話履歴の初期化
conversation_history = [create_system_message(llm_role)]

# ユーザー入力
input_message = st.text_input(label="相談したいことを入力してください")

if st.button("実行"):
    st.divider()
    result = handle_user_input(llm, conversation_history, input_message)
    if result:
        st.write(f"**{result.content}**")
