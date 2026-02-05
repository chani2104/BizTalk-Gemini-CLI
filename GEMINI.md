# Gemini 컨텍스트: BizTone Converter

## 1. 프로젝트 개요

"BizTone Converter" 프로젝트는 사용자가 일상적인 언어를 다양한 대상에 적합한 전문적인 비즈니스 커뮤니케이션으로 변환할 수 있도록 돕는 웹 기반 솔루션입니다.

-   **목적**: 상사(Upward), 동료(Lateral), 고객(External) 등 대상에 따라 텍스트의 톤을 자동으로 적절하게 다듬는 것을 목표로 합니다.
-   **아키텍처**: 프론트엔드와 백엔드가 명확하게 분리된 모놀리식 웹 애플리케이션입니다.
    -   **백엔드**: Python **Flask** 서버로, 단일 RESTful API 엔드포인트(`convert`)를 제공합니다. 이 엔드포인트는 비즈니스 로직을 처리하며, **Groq AI API**를 호출하여 대상별 프롬프트에 따라 텍스트 변환을 수행합니다. 또한 정적 프론트엔드 파일을 제공하는 역할도 합니다.
    -   **프론트엔드**: 바닐라 **HTML**, **CSS**, **JavaScript**로 구축된 단일 페이지 애플리케이션입니다. 스타일링을 위해 **Tailwind CSS** (CDN을 통해)를 사용하며, `fetch` API를 사용하여 백엔드와 통신합니다.

프로젝트는 `PRD.md` 및 `프로그램개요서.md`에 상세히 문서화되어 있으며, 제품 목표, 사용자 요구사항, 기술 스택 및 릴리스 계획을 설명하고 있습니다.

## 2. 빌드 및 실행

애플리케이션은 Python 백엔드와 정적 JavaScript 프론트엔드로 구성됩니다. 백엔드가 프론트엔드를 제공하므로, 백엔드만 활성 상태로 실행하면 됩니다.

### 백엔드 설정 및 실행

1.  **가상 환경 설정**:
    기존 `.venv` 가상 환경을 사용하는 것이 좋습니다.
    ```bash
    # 가상 환경 활성화 (Windows)
    .\.venv\Scripts\activate
    ```

2.  **의존성 설치**:
    모든 백엔드 의존성은 `backend/requirements.txt`에 나열되어 있습니다.
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **환경 변수 설정**:
    애플리케이션은 Groq AI API 키를 필요로 합니다. 프로젝트 루트 디렉토리에 `.env` 파일을 생성하세요.
    ```
    # .env
    GROQ_API_KEY="YOUR_API_KEY_HERE"
    ```
    `backend/app.py` 파일은 `python-dotenv`를 사용하여 이 변수를 로드합니다.

4.  **서버 실행**:
    메인 Flask 애플리케이션 파일을 실행하세요. 서버는 `http://localhost:5000`에서 디버그 모드로 시작됩니다.
    ```bash
    python backend/app.py
    ```

### 프론트엔드

프론트엔드는 `frontend/` 디렉토리에 있는 정적 파일로 구성됩니다. Flask 백엔드 서버를 실행하기만 하면 루트 URL(`http://localhost:5000`)에서 `index.html` 파일이 자동으로 제공됩니다. 프론트엔드에 대한 별도의 빌드 단계는 필요하지 않습니다.

## 3. 개발 규칙

-   **디렉토리 구조**: 프로젝트는 `backend/` 및 `frontend/` 디렉토리로 엄격하게 분리됩니다.
-   **API**: 단일 API 엔드포인트 `/convert` (POST)는 `text` 및 `target` 필드를 포함하는 JSON 본문을 예상하며, `convertedText`를 반환합니다.
-   **스타일링**: Tailwind CSS 유틸리티 클래스를 `index.html`에 직접 사용하여 스타일링을 처리합니다. 기존 `frontend/css/style.css`는 현재 비어 있습니다.
-   **의존성**: 백엔드 Python 의존성은 `pip` 및 `requirements.txt`로 관리됩니다.
-   **보안**: PRD의 `NFR-03`에 따라 API 키와 같은 민감한 정보는 환경 변수를 통해 관리되어야 하며 하드코딩되어서는 안 됩니다.
-   **Git 워크플로우**: 문서는 `feature -> develop -> main` 브랜치 전략을 언급하며, 이는 구조화된 Git 워크플로우가 의도되었음을 나타냅니다.
