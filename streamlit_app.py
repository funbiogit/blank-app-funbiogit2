import streamlit as st

st.set_page_config(page_title="프레이어 모델 - 변화", layout="wide")
st.title("🔍 개념과 연관짓기")
st.markdown("""
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
  <table style="width: 300px; border-collapse: collapse; text-align: center; border: 2px solid #000;">
    <tr style="border-bottom: 2px solid #000; background-color: #f0f0f0;">
      <th style="padding: 10px; font-size: 24px;">개념 렌즈</th>
    </tr>
    <tr>
      <td style="padding: 20px; font-size: 32px; font-weight: bold;">변화</td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)


# 표 형태로 개념 정의와 특성
st.markdown("""
<div style="display: flex; justify-content: center; margin-bottom: 20px;">
  <table style="width:80%; border-collapse: collapse; border:1px solid #ccc; text-align: center;">
    <tr style="background-color: #f0f0f0;">
      <th style="border:1px solid #ccc; padding: 8px;">📘 개념 정의</th>
      <th style="border:1px solid #ccc; padding: 8px;">📘 개념 특성</th>
    </tr>
    <tr>
      <td style="border:1px solid #ccc; padding: 8px;">
        하나의 형태, 상태가 다른 형태, 상태로 전환, 변형 또는 이동하는 것.
      </td>
      <td style="border:1px solid #ccc; padding: 8px;">
        원인, 과정, 결과를 포함한다.  
        시간의 흐름에 따른 과정이다.
      </td>
    </tr>
  </table>
</div>
""", unsafe_allow_html=True)

# 예시 문장
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

# 세션 상태 초기화
if "example_flags" not in st.session_state:
    st.session_state.example_flags = {s: False for s in sentences}
if "non_example_flags" not in st.session_state:
    st.session_state.non_example_flags = {s: False for s in sentences}

st.markdown("### 🧩 예시 / 비예시 문장 선택")
st.write("각 문장별로 ‘예시’ 또는 ‘비예시’를 체크하세요. 두 항목을 동시에 선택할 수 없습니다.")

overlap_msgs = []

for s in sentences:
    col1, col2, col3 = st.columns([4, 1, 1])  # 폭 조절
    with col1:
        st.write(s)
    with col2:
        st.write("예시")
        example_chk = st.checkbox("", key=f"ex_{s}")
    with col3:
        st.write("비예시")
        non_example_chk = st.checkbox("", key=f"non_ex_{s}")

    # 중복 체크 즉시 경고 메시지 출력
    if example_chk and non_example_chk:
        st.warning(f"❗ '{s}' 문장은 예시와 비예시에 동시에 선택할 수 없습니다. 하나만 선택해주세요.")
    st.session_state.example_flags[s] = example_chk
    st.session_state.non_example_flags[s] = non_example_chk

if overlap_msgs:
    for msg in overlap_msgs:
        st.warning(msg)

# 키워드 기반 판단
def is_change(sentence):
    keywords = ["발생", "빠져나온다", "바뀌", "전환", "변형", "이동"]
    return any(k in sentence for k in keywords)

# 생각 꺼내기
st.divider()
st.subheader("💡 생각 꺼내기")

col5, col6 = st.columns(2)
with col5:
    student_example = st.text_area(
        "💬 학습한 내용 중에서 '변화'에 해당하는 예시를 작성해 보세요.",
        key="student_ex"
    )
with col6:
    student_non_example = st.text_area(
        "💬 학습한 내용 중에서 '변화'에 해당하지 않는 비예시를 작성해 보세요.",
        key="student_non_ex"
    )

# 질문 만들기
st.divider()
st.subheader("❓ 질문 만들기")
st.markdown(
    """
    아래 두 가지 개념을 활용하여 관련된 탐구 질문을 자유롭게 작성해 보세요.  
    - 변화  
    - 생태계  
    """
)
student_question = st.text_area("✏️ 질문을 작성해 보세요.", key="student_question")

# 질문 탐구 가능성 피드백
if student_question:
    st.markdown("🧠 **질문에 대한 탐구 가능성 피드백**")
    if any(kw in student_question for kw in ["왜", "어떻게", "무엇"]):
        st.success("👍 탐구 중심의 질문입니다. 실험이나 관찰로 접근할 수 있겠어요!")
    else:
        st.info("질문이 탐구 중심으로 적절한지 다시 생각해 보세요. '왜', '어떻게'로 시작해보는 건 어떨까요?")

# 결과 저장
st.divider()
st.subheader("📄 결과를 파일로 저장")

if st.button("📥 저장 파일 생성하기"):
    output = []
    output.append("프레이어 모델 결과 - 개념: 변화")
    output.append("\n[개념 정의]")
    output.append("하나의 형태, 상태가 다른 형태, 상태로 전환, 변형 또는 이동하는 것.")
    output.append("\n[개념 특성]")
    output.append("원인, 과정, 결과를 포함한다.")
    output.append("시간의 흐름에 따른 과정이다.")

    output.append("\n[예시로 선택한 문장]")
    for s, flag in st.session_state.example_flags.items():
        if flag:
            mark = "✅ 관련 있음" if is_change(s) else "❌ 관련 없음"
            output.append(f"- {s} ({mark})")
    if student_example:
        mark = "✅ 관련 있음" if is_change(student_example) else "❌ 관련 없음"
        output.append(f"- ✍️ 작성 예시: {student_example} ({mark})")

    output.append("\n[비예시로 선택한 문장]")
    for s, flag in st.session_state.non_example_flags.items():
        if flag:
            mark = "✅ 관련 있음" if is_change(s) else "❌ 관련 없음"
            output.append(f"- {s} ({mark})")
    if student_non_example:
        mark = "✅ 관련 있음" if is_change(student_non_example) else "❌ 관련 없음"
        output.append(f"- ✍️ 작성 비예시: {student_non_example} ({mark})")

    if student_question:
        output.append(f"\n❓ 작성한 질문: {student_question}")

    file_content = "\n".join(output).encode("utf-8")
    st.download_button(
        label="📄 텍스트 파일 다운로드",
        data=file_content,
        file_name="프레이어_모델_변화_결과.txt",
        mime="text/plain"
    )
