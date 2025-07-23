import streamlit as st
import re

st.set_page_config(page_title="프레이어 모델 - 변화", layout="wide")
st.title("개념과 연관짓기")

# ===============================
# 개념 렌즈 표
st.markdown("""
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
  <table style="width: 300px; border-collapse: collapse; text-align: center; border: 2px solid black;">
    <tr style="background-color: #f0f0f0; border-bottom: 2px solid black;">
      <th style="padding: 10px; font-size: 28px;">🔍 개념 렌즈</th>
    </tr>
    <tr>
      <td style="padding: 20px; font-size: 32px; font-weight: bold;">변화</td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

# ===============================
# 개념 정의와 특성 표
st.markdown("""
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
  <table style="width:80%; border-collapse: collapse; border: 2px solid black; text-align: center;">
    <colgroup>
      <col style="width: 50%;">
      <col style="width: 50%;">
    </colgroup>
    <tr style="background-color: #f0f0f0; border-bottom: 2px solid black;">
      <th style="border: 2px solid black; padding: 13px; font-size: 28px;">📘 개념 정의</th>
      <th style="border: 2px solid black; padding: 13px; font-size: 28px;">📘 개념 특성</th>
    </tr>
    <tr>
      <td style="border: 2px solid black; padding: 10px; font-size: 20px;">
        하나의 형태, 상태가 다른 형태, 상태로 전환, 변형 또는 이동하는 것.
      </td>
      <td style="border: 2px solid black; padding: 10px; font-size: 20px;">
        원인, 과정, 결과를 포함한다.<br>시간의 흐름에 따른 과정이다.
      </td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

# ===============================
# 예시 문장 & 변화를 포함하는 문장 정의
sentences = [
    "세포에는 여러 가지 세포 소기관이 있다.",
    "모든 생물은 생명의 중심원리를 따른다.",
    "과산화수소수에 감자를 넣으면 기포가 발생한다.",
    "세포를 고장액에 넣으면 물이 빠져나온다.",
    "분자의 구조는 기능과 관계가 있다.",
    "세포막은 인지질과 단백질로 되어있다.",
    "염기 서열이 바뀌어도 단백질의 입체구조는 바뀌지 않을 수 있다.",
    "구성 요소간 상호작용으로 생명 시스템이 안정적으로 유지된다.",
]

# 정답 예시 문장 (사용자 지정)
true_examples = {
    "과산화수소수에 감자를 넣으면 기포가 발생한다.",
    "세포를 고장액에 넣으면 물이 빠져나온다.",
    "염기 서열이 바뀌어도 단백질의 입체구조는 바뀌지 않을 수 있다.",
    "구성 요소간 상호작용으로 생명 시스템이 안정적으로 유지된다.",
}

def is_example(sentence):
    return sentence.strip() in true_examples

# ===============================
# 상태 초기화
if "example_flags" not in st.session_state:
    st.session_state.example_flags = {}
if "non_example_flags" not in st.session_state:
    st.session_state.non_example_flags = {}

# ===============================
# 문장 분류
st.markdown("### 🧩 예시 / 비예시 문장 선택")
st.write("각 문장별로 ‘예시’ 또는 ‘비예시’ 중 하나를 선택해 보세요.")

for s in sentences:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"- {s}")
    with col2:
        choice = st.radio(
            "", ["", "예시", "비예시"], key=f"choice_{s}", horizontal=True, label_visibility="collapsed"
        )
        st.session_state.example_flags[s] = (choice == "예시")
        st.session_state.non_example_flags[s] = (choice == "비예시")

    # 피드백
    if choice == "예시" and not is_example(s):
        st.info("❌ 다시 한 번 확인해 보세요.")
    elif choice == "비예시" and is_example(s):
        st.info("❌ 다시 한 번 확인해 보세요.!")

# ===============================
# 생각 꺼내기
st.divider()
st.subheader("💡 생각 꺼내기")

col5, col6 = st.columns(2)
with col5:
    student_example = st.text_area("💬 '변화'에 해당하는 예시를 작성해 보세요.", key="student_ex")
with col6:
    student_non_example = st.text_area("💬 '변화'에 해당하지 않는 비예시를 작성해 보세요.", key="student_non_ex")

# ===============================
# 예시 / 비예시 피드백 나란히
st.markdown("### 🧠 생각 피드백")
col_ex_fb, col_nonex_fb = st.columns(2)

def is_change(sentence):
    keywords = ["발생", "빠져", "나오", "바뀌", "전환", "변형", "이동", "움직", "분해", "형성",
                "성장", "진화", "변화", "증가", "감소", "녹는", "녹았", "사라지", "생기", "깨지", "썩는"]
    return any(k in sentence for k in keywords)

with col_ex_fb:
    st.markdown("#### ✨ 예시 피드백")
    if student_example:
        example_sentences = [line.strip() for line in student_example.split("\n") if line.strip()]
        for i, ex in enumerate(example_sentences, 1):
            st.markdown(f"**예시 {i}:** {ex}")
            if is_change(ex):
                st.success("✅ 잘했어요! 변화의 특성을 잘 담은 예시입니다.")
            else:
                st.warning("✏️ 변화와 관련이 적은 문장 같아요. 원인→과정→결과 흐름을 떠올려보세요.")
    else:
        st.info("📝 예시 문장을 입력해주세요.")

with col_nonex_fb:
    st.markdown("#### ✨ 비예시 피드백")
    if student_non_example:
        nonexample_sentences = [line.strip() for line in student_non_example.split("\n") if line.strip()]
        for i, ne in enumerate(nonexample_sentences, 1):
            st.markdown(f"**비예시 {i}:** {ne}")
            if is_change(ne):
                st.warning("🤔 변화와 관련된 표현이 포함되어 있어요. 비예시는 변화가 없는 설명이 더 적절해요.")
            else:
                st.success("✅ 좋아요! 변화와 무관한 내용을 잘 작성했어요.")
    else:
        st.info("📝 비예시 문장을 입력해주세요.")

# ===============================
# 질문
st.divider()
st.subheader("❓ 질문 만들기")
st.markdown("아래 두 개념을 활용한 탐구 질문을 작성해 보세요.")
st.markdown("- 변화\n- 생태계")

student_question = st.text_area("✏️ 질문을 작성해 보세요. (여러개 작성하는 경우 shift키로 줄바꿈)", key="student_question")

if student_question:
    st.markdown("🧠 **탐구 가능성 피드백**")
    questions = [q.strip() for q in student_question.split("\n") if q.strip()]
    for i, q in enumerate(questions, 1):
        st.markdown(f"**질문 {i}:** {q}")
        if any(q.startswith(k) for k in ["왜", "어떻게", "무엇", "어떤", "무슨"]):
            st.success("👍 조사를 통해 탐구해봅시다")
        else:
            st.info("👉 ‘왜’, ‘어떻게’ 등으로 시작하면 더 탐구적인 질문이 됩니다.")

# ===============================
# 결과 저장
st.divider()
st.subheader("📄 결과 저장")

if st.button("📥 텍스트 파일로 결과 저장"):
    output = []
    output.append("✅ 프레이어 모델 결과 - 개념: 변화")
    output.append("\n[개념 정의]\n- 하나의 형태, 상태가 다른 형태, 상태로 전환, 변형 또는 이동하는 것.")
    output.append("\n[개념 특성]\n- 원인, 과정, 결과를 포함한다.\n- 시간의 흐름에 따른 과정이다.")

    output.append("\n[예시로 선택한 문장]")
    for s in sentences:
        if st.session_state.example_flags[s]:
            mark = "✅ 정답" if is_example(s) else "❌ 오답"
            output.append(f"- {s} ({mark})")
    if student_example:
        lines = [line.strip() for line in student_example.split("\n") if line.strip()]
        for line in lines:
            mark = "✅ 관련 있음" if is_change(line) else "❌ 관련 없음"
            output.append(f"- 작성 예시: {line} ({mark})")

    output.append("\n[비예시로 선택한 문장]")
    for s in sentences:
        if st.session_state.non_example_flags[s]:
            mark = "✅ 정답" if not is_example(s) else "❌ 오답"
            output.append(f"- {s} ({mark})")
    if student_non_example:
        lines = [line.strip() for line in student_non_example.split("\n") if line.strip()]
        for line in lines:
            mark = "✅ 관련 없음" if not is_change(line) else "❌ 관련 있음"
            output.append(f"- 작성 비예시: {line} ({mark})")

    output.append("\n[작성한 질문]")
    if student_question:
        for q in questions:
            output.append(f"- {q}")

    file_data = "\n".join(output).encode("utf-8")
    st.download_button(
        label="📄 텍스트 파일 다운로드",
        data=file_data,
        file_name="프레이어모델_변화_결과.txt",
        mime="text/plain"
    )
