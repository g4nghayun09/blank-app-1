import streamlit as st
from collections import Counter

# -------------------- 페이지 설정 --------------------
st.set_page_config(
    page_title="테트리스 스타일 진단기",
    page_icon="🎮",
    layout="centered",
)

# -------------------- 앱 제목 및 설명 --------------------
st.title("🎮 당신의 테트리스 스타일은?")
st.write("---")
st.write("간단한 세 가지 질문을 통해 당신의 플레이 성향을 알아보고, 필요한 기술을 확인해보세요!")


# -------------------- 1. 실력 진단 (질문) --------------------
st.header("1. 실력 진단: 3가지 질문")
st.write("각 질문에 가장 가깝다고 생각하는 답변을 하나씩 선택해주세요.")

# 질문 리스트: 각 질문과 선택지를 딕셔너리 형태로 저장
questions = {
    "question1": {
        "text": "질문 1: 당신이 가장 중요하게 생각하는 것은?",
        "options": {
            "A": "블록을 빨리 쌓는 속도",
            "B": "콤보를 만들 수 있는 빈 공간",
            "C": "완벽한 T-스핀 각도"
        }
    },
    "question2": {
        "text": "질문 2: 블록이 애매하게 남을 때, 당신의 선택은?",
        "options": {
            "A": "당장 다음 블록을 놓기 위해 빈 공간을 만든다.",
            "B": "다음에 올 블록을 보며 콤보를 위한 빈 공간을 남겨둔다.",
            "C": "무리해서라도 콤보를 이어나간다."
        }
    },
    "question3": {
        "text": "질문 3: 게임 후반부, 블록이 거의 끝까지 쌓였을 때 당신의 마음은?",
        "options": {
            "A": "어떻게든 빈 공간을 메우며 버텨야 한다.",
            "B": "콤보나 T-스핀으로 한 방에 뒤집을 기회를 노린다.",
            "C": "'테트리스'를 위한 I 블록을 기다린다."
        }
    }
}

# 답변을 저장할 리스트 초기화
answers = []

# 각 질문을 동적으로 생성
for key, q in questions.items():
    # st.radio는 선택된 '옵션의 텍스트'를 반환합니다.
    user_answer_text = st.radio(
        label=q["text"],
        options=list(q["options"].values()),
        key=key # 각 위젯을 구분하기 위한 고유 키
    )
    
    # *** ✨ 수정된 부분 시작 ✨ ***
    # 선택된 텍스트(value)를 기반으로 원래의 키('A', 'B', 'C')를 찾습니다.
    # 이것이 이전 코드의 오류를 수정한 핵심 로직입니다.
    for option_key, option_value in q["options"].items():
        if option_value == user_answer_text:
            answers.append(option_key)
            break
    # *** ✨ 수정된 부분 끝 ✨ ***


# -------------------- 2. 진단 결과 --------------------
st.write("---")
st.header("2. 진단 결과")

# '결과 보기' 버튼을 누르면 진단 로직이 실행됩니다.
if st.button("결과 보기", use_container_width=True):
    # Counter를 사용하여 답변('A', 'B', 'C')의 개수를 계산합니다.
    count = Counter(answers)
    
    # 가장 많이 선택된 답변을 찾습니다.
    if count:
        # most_common(1)은 [('A', 2)] 와 같은 형태로 가장 빈번한 항목과 횟수를 반환합니다.
        most_common_answer = count.most_common(1)[0][0]
        result_type = most_common_answer
    else:
        result_type = None

    # 결과에 따라 다른 제목과 설명을 표시합니다.
    if result_type == 'A':
        st.subheader("당신의 타입은: 🛡️ 안정형 플레이어")
        st.info(
            """
            **진단:** 당신은 실수를 줄이며 안정적으로 게임을 운영하는 타입입니다. 
            기본기가 탄탄하니, 이제 T-스핀이나 콤보 같은 고급 기술을 익혀 공격 능력을 키워보세요.
            """
        )
    elif result_type == 'B':
        st.subheader("당신의 타입은: ✨ 콤보 마스터")
        st.info(
            """
            **진단:** 당신은 콤보를 만들어 상대를 압박하는 데 능숙합니다. 
            더 강력한 공격을 위해 T-스핀 기술을 익히는 것을 추천합니다.
            """
        )
    elif result_type == 'C':
        st.subheader("당신의 타입은: ⚔️ 공격형 플레이어")
        st.info(
            """
            **진단:** 당신은 T-스핀이나 테트리스 같은 한 방 기술로 승부를 보는 타입입니다. 
            하지만 공격 기회가 오지 않을 때를 대비해, 안정적으로 블록을 쌓는 연습도 함께 하는 것이 좋습니다.
            """
        )
    else:
        st.warning("결과를 표시할 수 없습니다. 모든 질문에 답변해주세요.")
else:
    st.info("모든 질문에 답한 후 '결과 보기' 버튼을 눌러주세요.")


# -------------------- 3. 기술 가이드 --------------------
st.write("---")
st.header("3. 핵심 기술 가이드")

# 두 개의 컬럼을 만들어 T-스핀과 콤보 설명을 나란히 배치합니다..
col1, col2 = st.columns(2)

with col1:
    st.subheader("🧩 T-스핀 (T-Spin)")
    st.markdown("**무엇인가?**")
    st.write("T 블록을 좁은 공간에 회전시켜 넣는 기술입니다.")
    st.markdown("**왜 중요한가?**")
    st.write("일반적인 줄 지우기보다 점수가 훨씬 높고, 상대에게 더 많은 방해 블록을 보낼 수 있습니다.")

with col2:
    st.subheader("🔗 콤보 (Combo)")
    st.markdown("**무엇인가?**")
    st.write("연속으로 줄을 지우는 기술입니다.")
    st.markdown("**왜 중요한가?**")
    st.write("콤보가 길어질수록 점수가 폭발적으로 늘어나고, 상대방에게 계속해서 방해 블록을 보낼 수 있습니다.")