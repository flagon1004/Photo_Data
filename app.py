import streamlit as st
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from io import BytesIO
from datetime import datetime
import folium
from streamlit_folium import st_folium

# ─── 페이지 설정 ───
st.set_page_config(
    page_title="📸 사진 데이터 관리",
    page_icon="📸",
    layout="wide",
)

# ─── 라이트 테마 커스텀 CSS ───
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    /* 전체 배경 & 폰트 */
    .stApp {
        background-color: #f8f9fc;
    }
    html, body, [class*="st-"] {
        font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
    }

    /* ─── 헤더 (상단 고정) ─── */
    .main-header {
        background: #e0ecff !important;
        padding: 0.7rem 2rem !important;
        border-radius: 0 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    .header-left {
        display: flex !important;
        align-items: center !important;
        gap: 0.8rem !important;
    }
    .header-left h1 {
        color: #1e3a5f !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: -0.3px !important;
    }
    .header-left p {
        color: #4a6fa5 !important;
        font-size: 0.78rem !important;
        font-weight: 400 !important;
        margin: 0 !important;
    }
    .header-right {
        color: #7a9cc6 !important;
        font-size: 0.72rem !important;
        font-weight: 500 !important;
        white-space: nowrap !important;
    }

    /* 헤더 고정에 따른 본문 여백 */
    section.main > div.block-container {
        padding-top: 4rem !important;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 4rem !important;
    }
    /* Streamlit 기본 헤더 숨기기 */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* ─── 업로드 파일 목록 축소 (10개 보이도록) ─── */
    [data-testid="stFileUploader"] li {
        padding: 0.15rem 0.5rem !important;
        margin: 0 !important;
        font-size: 0.75rem !important;
        line-height: 1.3 !important;
        min-height: unset !important;
    }
    [data-testid="stFileUploader"] li span {
        font-size: 0.75rem !important;
    }
    [data-testid="stFileUploader"] li button {
        padding: 0.1rem !important;
        width: 1.2rem !important;
        height: 1.2rem !important;
        min-height: unset !important;
    }
    [data-testid="stFileUploader"] li button svg {
        width: 0.7rem !important;
        height: 0.7rem !important;
    }
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFileList"] {
        max-height: 280px !important;
        overflow-y: auto !important;
    }
    /* 업로드된 파일 아이콘 축소 */
    [data-testid="stFileUploader"] li img,
    [data-testid="stFileUploader"] li svg:first-child {
        width: 1rem !important;
        height: 1rem !important;
    }

    /* ─── 섹션 타이틀 ─── */
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #1e293b;
        margin: 2rem 0 0.8rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
        letter-spacing: -0.3px;
    }

    /* ─── 통계 카드 ─── */
    .stat-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.3rem 1rem;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .stat-card .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }
    .stat-card .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2563eb;
        line-height: 1.2;
    }
    .stat-card .stat-label {
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 0.2rem;
        font-weight: 500;
    }

    /* ─── 업로드 영역 ─── */
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 14px;
        padding: 1rem;
        transition: border-color 0.2s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #2563eb;
    }

    /* ─── 데이터프레임 ─── */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* ─── 다운로드 버튼 (중앙) ─── */
    .stDownloadButton,
    div[data-testid="stDownloadButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }
    .stDownloadButton > button,
    div[data-testid="stDownloadButton"] > button {
        background: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
        transition: all 0.2s !important;
    }
    .stDownloadButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* ─── 정보/경고 박스 ─── */
    .info-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem 1.2rem;
        border-radius: 0 10px 10px 0;
        margin: 0.8rem 0;
        color: #1e40af;
        font-size: 0.88rem;
        line-height: 1.6;
    }
    .warning-box {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem 1.2rem;
        border-radius: 0 10px 10px 0;
        margin: 0.8rem 0;
        color: #92400e;
        font-size: 0.88rem;
        line-height: 1.6;
    }
    .error-box {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem 1.2rem;
        border-radius: 0 10px 10px 0;
        margin: 0.8rem 0;
        color: #991b1b;
        font-size: 0.88rem;
        line-height: 1.6;
    }

    /* ─── 푸터 ─── */
    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.78rem;
        padding: 1.5rem 0 0.5rem 0;
        letter-spacing: -0.2px;
    }

    /* ─── Streamlit 기본 요소 미세 조정 ─── */
    .stMarkdown { color: #334155; }
    hr { border-color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)


# ─── EXIF 추출 함수들 ───

def dms_to_dd(dms, ref):
    """DMS(도/분/초) → DD(십진수) 변환"""
    try:
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
        dd = degrees + minutes / 60 + seconds / 3600
        if ref in ['S', 'W']:
            dd *= -1
        return round(dd, 6)
    except (TypeError, IndexError, ZeroDivisionError):
        return None


def extract_gps(exif_data):
    """EXIF에서 GPS 정보 추출"""
    gps_info = {}
    if not exif_data:
        return gps_info

    # 방법 1: get_ifd()로 GPS IFD 가져오기 (Pillow 10+)
    try:
        gps_ifd = exif_data.get_ifd(0x8825)
        if gps_ifd:
            for gps_tag_id, gps_value in gps_ifd.items():
                gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                gps_info[gps_tag] = gps_value
    except Exception:
        pass

    # 방법 2: 방법 1이 안 되면 기존 방식 시도
    if not gps_info:
        try:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo" and isinstance(value, dict):
                    for gps_tag_id, gps_value in value.items():
                        gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        gps_info[gps_tag] = gps_value
                    break
        except Exception:
            pass

    result = {}

    # 위도
    if 'GPSLatitude' in gps_info and 'GPSLatitudeRef' in gps_info:
        result['위도'] = dms_to_dd(gps_info['GPSLatitude'], gps_info['GPSLatitudeRef'])

    # 경도
    if 'GPSLongitude' in gps_info and 'GPSLongitudeRef' in gps_info:
        result['경도'] = dms_to_dd(gps_info['GPSLongitude'], gps_info['GPSLongitudeRef'])

    # 고도
    if 'GPSAltitude' in gps_info:
        try:
            alt = float(gps_info['GPSAltitude'])
            alt_ref = gps_info.get('GPSAltitudeRef', 0)
            if alt_ref == 1:
                alt *= -1
            result['고도(m)'] = round(alt, 1)
        except (TypeError, ValueError):
            pass

    # 촬영 방향
    if 'GPSImgDirection' in gps_info:
        try:
            result['방향(°)'] = round(float(gps_info['GPSImgDirection']), 1)
        except (TypeError, ValueError):
            pass

    return result


def extract_exif(image):
    """이미지에서 EXIF 데이터 추출"""
    exif_data = image.getexif()
    if not exif_data:
        return None

    info = {}

    tag_map = {
        'Make': '제조사',
        'Model': '카메라 모델',
        'DateTime': '촬영일시',
        'DateTimeOriginal': '촬영일시',
        'ExposureTime': '셔터스피드',
        'FNumber': '조리개',
        'ISOSpeedRatings': 'ISO',
        'ImageWidth': '가로(px)',
        'ImageLength': '세로(px)',
        'ExifImageWidth': '가로(px)',
        'ExifImageHeight': '세로(px)',
    }

    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag in tag_map:
            key = tag_map[tag]
            if key == '촬영일시' and isinstance(value, str):
                try:
                    dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    value = dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            elif key == '조리개':
                try:
                    value = f"f/{float(value):.1f}"
                except (TypeError, ValueError):
                    pass
            elif key == '셔터스피드':
                try:
                    val = float(value)
                    if val < 1:
                        value = f"1/{int(1/val)}"
                    else:
                        value = f"{val:.1f}s"
                except (TypeError, ValueError, ZeroDivisionError):
                    pass
            info[key] = value

    # IFD EXIF (서브 EXIF) 데이터도 확인
    ifd_exif = exif_data.get_ifd(0x8769)
    if ifd_exif:
        for tag_id, value in ifd_exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag in tag_map:
                key = tag_map[tag]
                if key not in info:
                    if key == '촬영일시' and isinstance(value, str):
                        try:
                            dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                            value = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            pass
                    elif key == '조리개':
                        try:
                            value = f"f/{float(value):.1f}"
                        except (TypeError, ValueError):
                            pass
                    elif key == '셔터스피드':
                        try:
                            val = float(value)
                            if val < 1:
                                value = f"1/{int(1/val)}"
                            else:
                                value = f"{val:.1f}s"
                        except (TypeError, ValueError, ZeroDivisionError):
                            pass
                    elif key == 'ISO':
                        try:
                            value = int(value)
                        except (TypeError, ValueError):
                            pass
                    info[key] = value

    # GPS 정보 추가
    gps = extract_gps(exif_data)
    info.update(gps)

    # Google Maps 링크 생성
    if '위도' in info and '경도' in info and info['위도'] and info['경도']:
        info['구글지도'] = f"https://www.google.com/maps?q={info['위도']},{info['경도']}"

    return info if info else None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  메인 UI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 헤더
st.markdown("""
<div class="main-header">
    <div class="header-left">
        <h1>📸 사진 데이터 관리</h1>
        <p>촬영 위치 · 시간 · 카메라 정보 자동 추출</p>
    </div>
    <div class="header-right">Created by Han Sang Hoon</div>
</div>
""", unsafe_allow_html=True)

# ─── 사진 업로드 ───
st.markdown('<div class="section-title">📁 사진 업로드</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "사진 파일을 선택하세요 (여러 장 가능)",
    type=["jpg", "jpeg", "png", "tiff", "heic"],
    accept_multiple_files=True,
    help="EXIF 데이터가 포함된 원본 사진을 업로드하세요"
)

st.markdown("""
<div class="info-box">
    💡 <strong>팁:</strong> iPhone 사진은 HEIC 형식일 수 있습니다. 
    HEIC 업로드 시 오류가 나면 iPhone 설정 → 카메라 → 포맷 → <strong>호환성 우선</strong>으로 변경 후 촬영하거나,
    기존 사진은 JPG로 변환 후 업로드하세요.
</div>
""", unsafe_allow_html=True)


# ─── 데이터 처리 ───

if uploaded_files:
    all_data = []
    no_exif_files = []
    no_gps_files = []
    error_files = []

    for file in uploaded_files:
        try:
            if file.name.lower().endswith('.heic'):
                try:
                    from pillow_heif import register_heif_opener
                    register_heif_opener()
                except ImportError:
                    error_files.append(f"{file.name} (HEIC: pillow-heif 필요)")
                    continue

            image = Image.open(file)
            exif = extract_exif(image)

            if exif:
                exif['파일명'] = file.name
                all_data.append(exif)
                if '위도' not in exif or '경도' not in exif:
                    no_gps_files.append(file.name)
            else:
                no_exif_files.append(file.name)

        except Exception as e:
            error_files.append(f"{file.name} ({str(e)})")

    # 경고/오류 메시지
    if error_files:
        st.markdown(f"""
        <div class="error-box">
            ❌ <strong>처리 실패:</strong> {', '.join(error_files)}
        </div>
        """, unsafe_allow_html=True)

    if no_exif_files:
        st.markdown(f"""
        <div class="warning-box">
            ⚠️ <strong>EXIF 데이터 없음:</strong> {', '.join(no_exif_files)}<br>
            메신저(카카오톡 등)로 전달받은 사진이나 스크린샷은 EXIF가 제거되어 있을 수 있습니다.
        </div>
        """, unsafe_allow_html=True)

    if no_gps_files:
        st.markdown(f"""
        <div class="warning-box">
            📍 <strong>GPS 정보 없음:</strong> {', '.join(no_gps_files)}<br>
            촬영 시 위치 서비스가 꺼져 있었을 수 있습니다.
        </div>
        """, unsafe_allow_html=True)

    if all_data:

        # ─── 통계 카드 ───
        st.markdown('<div class="section-title">📊 요약</div>', unsafe_allow_html=True)

        total = len(uploaded_files)
        with_exif = len(all_data)
        with_gps = sum(1 for d in all_data if '위도' in d and '경도' in d)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">🖼️</div>
                <div class="stat-number">{total}</div>
                <div class="stat-label">업로드된 사진</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-number">{with_exif}</div>
                <div class="stat-label">EXIF 추출 성공</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">📍</div>
                <div class="stat-number">{with_gps}</div>
                <div class="stat-label">GPS 정보 있음</div>
            </div>
            """, unsafe_allow_html=True)

        # ─── 결과 테이블 + Excel 다운로드 ───
        st.markdown('<div class="section-title">📋 추출 결과</div>', unsafe_allow_html=True)

        display_columns = ['파일명', '촬영일시', '위도', '경도', '고도(m)', '방향(°)',
                           '제조사', '카메라 모델', '조리개', '셔터스피드', 'ISO', '구글지도']

        df = pd.DataFrame(all_data)
        existing_cols = [c for c in display_columns if c in df.columns]
        df_display = df[existing_cols].copy()

        # 구글지도 링크 처리
        if '구글지도' in df_display.columns:
            df_display['구글지도'] = df_display['구글지도'].apply(
                lambda x: x if pd.notna(x) else ''
            )

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            height=min(len(df_display) * 40 + 60, 500),
            column_config={
                "파일명": st.column_config.TextColumn("파일명", width="medium"),
                "촬영일시": st.column_config.TextColumn("촬영일시", width="medium"),
                "구글지도": st.column_config.LinkColumn(
                    "구글지도",
                    display_text="🔗 열기",
                    width="small",
                ),
                "위도": st.column_config.NumberColumn("위도", format="%.6f", width="small"),
                "경도": st.column_config.NumberColumn("경도", format="%.6f", width="small"),
                "고도(m)": st.column_config.NumberColumn("고도(m)", format="%.1f", width="small"),
                "방향(°)": st.column_config.NumberColumn("방향(°)", format="%.1f", width="small"),
                "ISO": st.column_config.NumberColumn("ISO", width="small"),
            }
        )

        # Excel 다운로드
        df_excel = df[existing_cols].copy()
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df_excel.to_excel(writer, index=False, sheet_name='사진데이터')
            worksheet = writer.sheets['사진데이터']
            for i, col in enumerate(df_excel.columns):
                max_len = max(
                    df_excel[col].astype(str).map(len).max() if len(df_excel) > 0 else 0,
                    len(col)
                ) + 3
                col_letter = chr(65 + i) if i < 26 else f"A{chr(65 + i - 26)}"
                worksheet.column_dimensions[col_letter].width = min(max_len, 45)

        today = datetime.now().strftime("%Y-%m-%d")

        st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Excel 다운로드",
            data=excel_buffer.getvalue(),
            file_name=f"사진데이터_{today}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.document",
        )

        # ─── 지도 표시 ───
        gps_data = [d for d in all_data if '위도' in d and '경도' in d and d['위도'] and d['경도']]

        if gps_data:
            st.markdown('<div class="section-title">🗺️ 촬영 위치 지도</div>', unsafe_allow_html=True)

            avg_lat = sum(d['위도'] for d in gps_data) / len(gps_data)
            avg_lon = sum(d['경도'] for d in gps_data) / len(gps_data)

            m = folium.Map(
                location=[avg_lat, avg_lon],
                zoom_start=14,
                tiles='OpenStreetMap'
            )

            for d in gps_data:
                popup_html = f"""
                <div style="font-family: 'Noto Sans KR', sans-serif; min-width: 200px;">
                    <strong>📷 {d['파일명']}</strong><br>
                    {'📅 ' + d['촬영일시'] + '<br>' if '촬영일시' in d else ''}
                    📍 {d['위도']}, {d['경도']}<br>
                    {'📐 고도: ' + str(d['고도(m)']) + 'm<br>' if '고도(m)' in d else ''}
                    {'🧭 방향: ' + str(d['방향(°)']) + '°<br>' if '방향(°)' in d else ''}
                    <a href="{d.get('구글지도', '#')}" target="_blank">🔗 구글지도에서 열기</a>
                </div>
                """

                folium.Marker(
                    location=[d['위도'], d['경도']],
                    popup=folium.Popup(popup_html, max_width=300),
                    tooltip=d['파일명'],
                    icon=folium.Icon(color='blue', icon='camera', prefix='fa')
                ).add_to(m)

            if len(gps_data) > 1:
                bounds = [[d['위도'], d['경도']] for d in gps_data]
                m.fit_bounds(bounds, padding=(30, 30))

            st_folium(m, use_container_width=True, height=500)

        else:
            st.markdown("""
            <div class="info-box">
                🗺️ GPS 정보가 있는 사진이 없어 지도를 표시할 수 없습니다.
            </div>
            """, unsafe_allow_html=True)

    elif uploaded_files and not all_data:
        st.markdown("""
        <div class="warning-box">
            ⚠️ 업로드한 사진에서 EXIF 데이터를 찾을 수 없습니다.<br>
            원본 사진인지 확인해주세요. (메신저로 전달받은 사진은 EXIF가 제거됩니다)
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="info-box">
        📌 <strong>사용 방법</strong><br>
        1. 위 업로드 영역에 사진을 드래그하거나 파일을 선택하세요<br>
        2. 여러 장을 한 번에 업로드할 수 있습니다<br>
        3. EXIF/GPS 데이터가 자동으로 추출됩니다<br>
        4. 결과를 Excel로 다운로드하거나 지도에서 확인하세요
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box">
        ⚠️ <strong>주의:</strong> 카카오톡, iCloud 웹 다운로드 등으로 받은 사진은 EXIF가 제거되어 있을 수 있습니다.<br>
        원본 사진을 직접 업로드해주세요.
    </div>
    """, unsafe_allow_html=True)


# ─── 푸터 ───
st.markdown("---")
st.markdown("""
<div class="footer-text">
    📸 사진 데이터 관리 웹앱 &nbsp;·&nbsp; 업로드한 사진은 서버에 저장되지 않습니다
</div>
""", unsafe_allow_html=True)