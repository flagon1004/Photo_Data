# 📸 사진 데이터 관리 웹앱

사진을 업로드하면 **촬영 위치(GPS)·시간·카메라 정보**를 자동으로 추출하는 웹앱입니다.

## 주요 기능
- 📁 여러 장 사진 동시 업로드 (JPG, HEIC, PNG, TIFF)
- 📊 EXIF 데이터 자동 추출 (촬영일시, GPS, 카메라 정보)
- 🔗 Google Maps 링크 자동 생성
- 📥 Excel 파일 다운로드
- 🗺️ 촬영 위치 지도 표시

## 로컬 실행 방법

### 1. Python 설치
- [python.org](https://www.python.org/downloads/)에서 Python 3.10 이상 설치
- 설치 시 **"Add Python to PATH" 체크 필수**

### 2. 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 3. 실행
```bash
streamlit run app.py
```
브라우저가 자동으로 열리며 `http://localhost:8501` 에서 앱을 사용할 수 있습니다.

## 주의사항
- 카카오톡, iCloud 웹 다운로드로 받은 사진은 EXIF가 제거되어 있을 수 있습니다
- 원본 사진을 직접 업로드해주세요
- 업로드한 사진은 서버에 저장되지 않습니다 (세션 종료 시 삭제)
