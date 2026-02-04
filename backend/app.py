from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# CORS 설정 (프론트엔드 URL에 맞게 조정 필요)
# 개발 단계에서는 모든 접근 허용 (보안에 주의)
CORS(app) 

# Groq API 키 로드
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/convert", methods=["POST"])
def convert_tone():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    text = data.get("text")
    target = data.get("target")

    if not text or not target:
        return jsonify({"error": "Missing 'text' or 'target' in request"}), 400

    # TODO: Groq AI API 연동 로직 구현 (현재는 더미 응답)
    # 실제 Groq API 호출은 이 부분에 구현됩니다.
    # 예시:
    # from groq import Groq
    # client = Groq(api_key=GROQ_API_KEY)
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": f"다음 문장을 {target}에게 적합한 말투로 변환해줘: {text}",
    #         }
    #     ],
    #     model="llama3-8b-8192", # 사용할 모델 지정
    # )
    # converted_text = chat_completion.choices[0].message.content

    # 더미 응답
    if target == "상사":
        converted_text = f"상사에게 보고하는 말투로 변환되었습니다: {text} (원본)"
    elif target == "타팀 동료":
        converted_text = f"타팀 동료에게 요청하는 말투로 변환되었습니다: {text} (원본)"
    elif target == "고객":
        converted_text = f"고객에게 응대하는 말투로 변환되었습니다: {text} (원본)"
    else:
        converted_text = f"알 수 없는 대상입니다. 변환 실패: {text}"

    return jsonify({"original_text": text, "converted_text": converted_text, "target": target})

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "BizTone Converter backend is running!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
