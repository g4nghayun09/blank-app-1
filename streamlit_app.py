import streamlit as st
from collections import Counter

# -------------------- 페이지 설정 --------------------
st.set_page_config(
    page_title="테트리스 스타일 진단기",
    page_icon="🎮",
    layout="centered",
)

# -------------------- 세션 상태 초기화 --------------------
# 앱의 상태를 저장하고 관리하기 위해 세션 상태(Session State)를 사용합니다.
if 'answers' not in st.session_state:
    st.session_state['answers'] = {}
if 'show_result' not in st.session_state:
    st.session_state['show_result'] = False

# -------------------- 앱 제목 및 설명 --------------------
st.title("🎮 당신의 테트리스 스타일은?")
st.write("---")
st.write("당신의 플레이 성향을 자세히 분석하기 위한 10가지 질문입니다. 가장 가까운 답을 선택해 주세요.")

# -------------------- 1. 나의 테트리스 성향 테스트 (10가지 질문) --------------------
st.header("1. 나의 테트리스 성향 테스트")

# 질문 리스트: 각 질문과 선택지를 딕셔너리 형태로 저장
questions = {
    "question1": {
        "text": "게임을 시작하면 가장 먼저 무엇을 생각하나요?",
        "options": {
            "A": "완벽하게 평평한 벽을 만든다.",
            "B": "콤보를 위한 빈 공간을 남겨둔다.",
            "C": "T-스핀을 위한 모양을 먼저 만든다.",
            "D": "빠르게 줄을 지워 점수를 올린다."
        }
    },
    "question2": {
        "text": "가장 선호하는 블록은 무엇인가요?",
        "options": {
            "A": "길고 납작해서 쌓기 좋은 I 블록",
            "B": "콤보를 만들기 좋은 O, J, L 블록",
            "C": "회전으로 빈 공간을 파고드는 T 블록",
            "D": "어떤 상황에서든 빠르게 놓을 수 있는 블록"
        }
    },
    "question3": {
        "text": "상대방과의 대결에서 승리하는 가장 좋은 방법은?",
        "options": {
            "A": "빈틈없는 방어로 상대방의 공격을 막는다.",
            "B": "콤보로 끊임없이 공격 블록을 보낸다.",
            "C": "T-스핀 같은 강력한 한 방으로 상대를 제압한다.",
            "D": "상대방보다 빠르게 블록을 쌓아 심리적으로 압박한다."
        }
    },
    "question4": {
        "text": "블록이 거의 끝까지 쌓였을 때, 당신의 마음은?",
        "options": {
            "A": "침착하게 빈 공간을 찾아 메우며 버틴다.",
            "B": "콤보나 T-스핀으로 한 번에 여러 줄을 지워 위기를 넘긴다.",
            "C": "다음 블록을 홀드하며 '테트리스' 기회를 노린다.",
            "D": "포기하지 않고 가장 빠르게 놓을 수 있는 곳을 찾는다."
        }
    },
    "question5": {
        "text": "테트리스에서 가장 짜릿한 순간은?",
        "options": {
            "A": "완벽하게 평평한 바닥을 만들었을 때",
            "B": "긴 콤보를 성공시켜 상대방을 압도할 때",
            "C": "예상치 못한 공간에 T-스핀을 성공했을 때",
            "D": "상대보다 빠르게 블록을 놓아 승리했을 때"
        }
    },
    "question6": {
        "text": "당신이 가장 자주 사용하는 전략은?",
        "options": {
            "A": "모든 블록을 한쪽에 몰아서 쌓고, I 블록으로 테트리스를 노리는 '포 테트리스'",
            "B": "한 줄만 비워두는 공간을 만들고 연속 콤보를 이어가는 '콤보'",
            "C": "좁은 공간에 T 블록을 파고드는 'T-스핀'",
            "D": "특정 전략 없이 상황에 맞게 유연하게 플레이하는 것"
        }
    },
    "question7": {
        "text": "테트리스 플레이 중 가장 피하고 싶은 것은?",
        "options": {
            "A": "빈틈이 생겨 블록이 울퉁불퉁하게 쌓이는 것",
            "B": "어렵게 만든 콤보가 끊어지는 것",
            "C": "T-스핀을 실패해서 블록이 이상하게 놓이는 것",
            "D": "상대방의 공격에 내 플레이가 방해받는 것"
        }
    },
    "question8": {
        "text": "'홀드(Hold)' 기능을 어떻게 사용하나요?",
        "options": {
            "A": "I 블록이나 T 블록처럼 원하는 블록이 나올 때까지 아껴둔다.",
            "B": "현재 상황에 맞지 않는 블록을 잠시 치워두는 용도로 사용한다.",
            "C": "거의 사용하지 않는다.",
            "D": "여러 개의 블록을 한 번에 바꾸는 용도로 사용한다."
        }
    },
    "question9": {
        "text": "상대방에게 공격할 때 가장 효과적인 방법은?",
        "options": {
            "A": "4줄 테트리스로 한 번에 많은 공격을 보낸다.",
            "B": "콤보로 지속적인 압박을 가한다.",
            "C": "T-스핀으로 예상치 못한 순간에 공격한다.",
            "D": "상대방이 실수를 하도록 유도한다."
        }
    },
    "question10": {
        "text": "당신의 테트리스 플레이 성향은?",
        "options": {
            "A": "수비적이고 안정적이다.",
            "B": "공격적이고 과감하다.",
            "C": "전략적이고 계산적이다.",
            "D": "유연하고 즉흥적이다."
        }
    },
}

# 각 질문을 동적으로 생성
for key, q in questions.items():
    user_answer_text = st.radio(
        label=f"**{key.upper().replace('QUESTION', '질문 ')}:** {q['text']}",
        options=list(q["options"].values()),
        index=None,
        key=key
    )
    if user_answer_text:
        for option_key, option_value in q['options'].items():
            if option_value == user_answer_text:
                st.session_state['answers'][key] = option_key
                break
    else:
        if key in st.session_state['answers']:
            del st.session_state['answers'][key]

# -------------------- 2. 진단 결과 --------------------
st.write("---")
st.header("2. 진단 결과")

# '결과 보기' 버튼을 누르면 세션 상태의 'show_result' 값을 True로 변경
def show_result_callback():
    st.session_state['show_result'] = True

# '결과 초기화' 버튼을 누르면 모든 세션 상태를 초기화
def reset_callback():
    st.session_state['answers'] = {}
    st.session_state['show_result'] = False

col_result, col_reset = st.columns(2)

with col_result:
    # 모든 질문에 답변해야만 '결과 보기' 버튼이 활성화됩니다.
    is_all_answered = len(st.session_state['answers']) == len(questions)
    st.button("결과 보기", use_container_width=True, on_click=show_result_callback, disabled=not is_all_answered)

with col_reset:
    st.button("결과 초기화", use_container_width=True, on_click=reset_callback)


# '결과 보기' 상태일 때만 결과를 표시합니다.
if st.session_state['show_result']:
    user_answers = list(st.session_state['answers'].values())
    
    # Counter를 사용하여 답변의 개수를 계산합니다.
    count = Counter(user_answers)
    
    if count:
        most_common_answer = count.most_common(1)[0][0]
        result_type = most_common_answer
    else:
        result_type = None

    # 결과에 따라 다른 제목과 설명을 표시합니다.
    if result_type == 'A':
        st.subheader("🛡️ 빌드 마스터")
        st.info(
            """
            **특징:** 안정적인 블록 쌓기를 통해 실수를 최소화합니다. '평평한 바닥'을 만드는 데 탁월하며, 쉽게 무너지지 않는 것이 가장 큰 강점입니다.
            **관련 스킬:**
            - **테트리스:** 4줄을 한 번에 지워 점수와 공격력을 얻는 기술.
            - **빌드:** 블록을 효율적으로 쌓는 기술.
            **보완할 점:** 안정적인 플레이가 강점이지만, 공격 능력이 부족할 수 있습니다. 콤보나 T-스핀 같은 공격 기술을 배워, 수비에만 치중하지 않고 상대방을 압박할 수 있는 능력을 키워야 합니다.
            """
        )
    elif result_type == 'B':
        st.subheader("✨ 콤보 마스터")
        st.info(
            """
            **특징:** 연속해서 줄을 지우는 콤보 플레이에 재능이 있습니다. 상대를 끊임없이 압박하며 공격하는 데 능숙합니다.
            **관련 스킬:**
            - **콤보:** 연속으로 줄을 지우는 기술.
            - **연속 줄 지우기:** 콤보를 이어가기 위한 블록 배치 전략.
            **보완할 점:** 콤보가 끊길 경우 순식간에 불리해질 수 있습니다. 콤보가 불가능한 상황을 대비해 T-스핀 빌드나 '테트리스'를 위한 안정적인 빌드 연습이 필요합니다.
            """
        )
    elif result_type == 'C':
        st.subheader("⚔️ T-스핀 스페셜리스트")
        st.info(
            """
            **특징:** T-스핀 기술을 자유자재로 구사하는 전문가입니다. 예상치 못한 순간에 강력한 공격을 보내 상대를 당황시키는 데 능숙합니다.
            **관련 스킬:**
            - **T-스핀:** T 블록을 회전시켜 좁은 공간에 넣는 기술.
            - **스핀 기술:** T 블록 외 다른 블록을 회전시켜 빈틈을 메우는 기술.
            **보완할 점:** 공격적인 T-스핀을 만들기 위해 블록을 복잡하게 쌓다가 필드가 망가질 위험이 있습니다. 안정적으로 블록을 쌓는 '빌드' 능력을 함께 길러야 합니다.
            """
        )
    elif result_type == 'D':
        st.subheader("🚀 속도광")
        st.info(
            """
            **특징:** 빠른 판단력과 순발력으로 블록을 순식간에 배치해 상대를 압박합니다.
            **관련 스킬:**
            - **대시(DAS):** 블록을 빠르게 좌우로 이동시키는 기술.
            - **하드 드롭(Hard Drop):** 블록을 한 번에 바닥까지 떨어뜨리는 기술.
            **보완할 점:** 속도가 빠른 만큼 정확도가 떨어져 블록이 울퉁불퉁하게 쌓일 위험이 있습니다. 속도를 조금 늦추고 정교하게 블록을 쌓는 연습을 통해 실수를 줄여야 합니다.
            """
        )
    else:
        # A, B, C, D 중 3개 이상을 선택한 경우
        unique_answers = set(user_answers)
        if len(unique_answers) >= 3:
            st.subheader("🎯 올라운더")
            st.info(
                """
                **특징:** 특정 전략에 얽매이지 않고, 상황에 따라 가장 효율적인 방법을 선택합니다. 모든 기술을 적절하게 활용하며 유연함을 가지고 있습니다.
                **관련 스킬:**
                - **다양한 빌드:** 여러 빌드 방식을 모두 알고 사용.
                - **전술적 판단:** 상황에 맞춰 콤보, T-스핀 등 가장 적합한 전략을 선택.
                **보완할 점:** 모든 것을 다 잘하지만, 한 가지 분야에서 최고가 되기 어렵다는 단점이 있습니다. 특정 기술(예: T-스핀 더블, 긴 콤보)을 자신만의 주력기로 만들면 더욱 강력한 플레이어가 될 수 있습니다.
                """
            )
        else:
            st.warning("결과를 표시할 수 없습니다. 모든 질문에 답변해주세요.")
else:
    st.info("모든 질문에 답한 후 '결과 보기' 버튼을 눌러주세요.")
