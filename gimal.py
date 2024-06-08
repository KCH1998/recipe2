import os
from dotenv import load_dotenv
import streamlit as st
import fitz  # PyMuPDF
import openai

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 OpenAI API 키를 가져옵니다.
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_dishes_from_text(text):
    lines = text.split('\n')
    dishes = [line.strip() for line in lines if line.strip()]
    return dishes

def get_recipe_from_openai(dish_name):
    prompt = f"{dish_name}의 레시피를 알려주세요."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def main():
    st.title("🍲 요리 레시피 검색기")
    
    file_path = "cook1.pdf"  # 현재 디렉토리에 있는 PDF 파일의 경로
    text = extract_text_from_pdf(file_path)
    dishes = extract_dishes_from_text(text)
    
    st.header("요리를 선택하세요:")
    dish_name = st.selectbox("요리명", dishes)
    
    if st.button("레시피 보기"):
        recipe = get_recipe_from_openai(dish_name)
        st.write(f"**{dish_name}의 레시피**")
        st.write(recipe)

if __name__ == "__main__":
    main()
