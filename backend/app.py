import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
# 프론트엔드からの 모든 출처에서의 요청을 허용
CORS(app) 

# Groq 클라이언트 초기화
# API 키는 환경 변수 'GROQ_API_KEY'에서 자동으로 로드됩니다.
try:
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    print("Groq client initialized successfully.")
except Exception as e:
    groq_client = None
    print(f"Error initializing Groq client: {e}")

@app.route('/convert', methods=['POST'])
def convert_text():
    """
    실제 Groq AI를 사용하여 텍스트 변환을 수행하는 API 엔드포인트.
    """
    if not groq_client:
        return jsonify({"error": "Groq 클라이언트가 초기화되지 않았습니다. API 키를 확인해주세요."}), 500

    data = request.json
    original_text = data.get('text')
    target = data.get('target')

    if not original_text or not target:
        return jsonify({"error": "텍스트와 변환 대상은 필수입니다."}), 400

    # 대상(페르소나)별 시스템 프롬프트 정의
    system_prompts = {
        "upward": "You are a helpful assistant who is an expert in business communication in Korean. Your role is to refine the user's text to be suitable for reporting to a superior. The tone should be formal, respectful, and clear. Start with the conclusion, and then provide the context or reason. Ensure the message is professional and builds trust.",
        "lateral": "You are a helpful assistant who is an expert in business communication in Korean. Your role is to refine the user's text for communicating with a colleague from another team. The tone should be friendly yet professional, fostering a collaborative atmosphere. Clearly state the request, background, and any deadlines. Use polite and respectful language.",
        "external": "You are a helpful assistant who is an expert in business communication in Korean. Your role is to refine the user's text for communicating with an external customer. The tone must be extremely polite, formal, and professional, using honorifics (극존칭). The message should build trust and convey a high level of service-mindedness. Respond only with the converted text, without any additional explanations."
    }

    system_prompt = system_prompts.get(target)
    if not system_prompt:
        return jsonify({"error": "유효하지 않은 변환 대상입니다."}), 400

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": original_text,
                }
            ],
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )

        converted_text = chat_completion.choices[0].message.content

        response_data = {
            "original_text": original_text,
            "convertedText": converted_text,
            "target": target
        }
        
        return jsonify(response_data)

    except Exception as e:
        print(f"Groq API call failed: {e}")
        # FR-05 요구사항: 사용자에게 명확한 오류 메시지 표시
        return jsonify({"error": "AI 모델을 호출하는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}), 500

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)