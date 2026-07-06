import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# National Delivery Fund - Prototype v3 Clean
# =========================================================
st.set_page_config(
    page_title="National Delivery Fund | Prototype v3",
    page_icon="NDF",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BG = "#06111F"
BG2 = "#07192D"
PANEL = "rgba(8, 28, 52, 0.94)"
PANEL2 = "rgba(10, 40, 73, 0.90)"
BORDER = "rgba(0, 207, 255, 0.34)"
BORDER2 = "rgba(242, 201, 76, 0.40)"
CYAN = "#00D4FF"
BLUE = "#1677FF"
GOLD = "#F2C94C"
GREEN = "#28E07B"
RED = "#FF4D6D"
ORANGE = "#FF9F1C"
TEXT = "#EAF7FF"
MUTED = "#8DAFD3"
GRID = "rgba(141, 175, 211, 0.14)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {{
    direction: rtl;
    text-align: right;
    font-family: 'Cairo', 'Segoe UI', Tahoma, Arial, sans-serif;
}}
.stApp {{
    background:
        radial-gradient(circle at 15% 10%, rgba(0, 212, 255, 0.18), transparent 28%),
        radial-gradient(circle at 90% 12%, rgba(242, 201, 76, 0.12), transparent 28%),
        linear-gradient(135deg, {BG} 0%, {BG2} 55%, #030912 100%);
    color: {TEXT};
}}
.block-container {{
    padding-top: 0.8rem;
    padding-left: 1.15rem;
    padding-right: 1.15rem;
    padding-bottom: 1.2rem;
    max-width: 1650px;
}}
h1, h2, h3, h4, h5, h6, p, div, span, label {{ color: {TEXT}; }}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #06111F 0%, #0A203A 100%);
    border-left: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
div[data-testid="stRadio"] label {{
    background: rgba(0, 212, 255, 0.055);
    border: 1px solid rgba(0, 212, 255, 0.11);
    border-radius: 12px;
    padding: 8px 10px;
    margin-bottom: 4px;
}}
[data-testid="stMetric"] {{
    background: linear-gradient(135deg, rgba(9,32,60,0.96), rgba(12,52,95,0.88));
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 12px 14px;
    box-shadow: inset 0 0 20px rgba(0,212,255,0.04), 0 8px 25px rgba(0,0,0,0.25);
}}
[data-testid="stMetricLabel"] div {{ color: {MUTED} !important; font-size: 13px; }}
[data-testid="stMetricValue"] div {{ color: {TEXT} !important; font-size: 28px; font-weight: 800; direction: ltr; }}
.neo-header {{
    position: relative;
    background:
        linear-gradient(135deg, rgba(7,25,45,0.98), rgba(10,48,87,0.94)),
        repeating-linear-gradient(90deg, rgba(0,212,255,0.05) 0px, rgba(0,212,255,0.05) 1px, transparent 1px, transparent 38px);
    border: 1px solid {BORDER};
    border-radius: 22px;
    padding: 20px 24px;
    margin-bottom: 12px;
    box-shadow: 0 0 0 1px rgba(0,212,255,0.08), 0 16px 38px rgba(0,0,0,0.30);
    overflow: hidden;
}}
.neo-header:after {{
    content:"";
    position:absolute;
    bottom:0;
    left:0;
    width:100%;
    height:2px;
    background: linear-gradient(90deg, transparent, {CYAN}, {GOLD}, transparent);
    opacity:0.7;
}}
.neo-title {{ font-size: 31px; font-weight: 800; margin: 0; letter-spacing: -0.5px; }}
.neo-subtitle {{ color: {MUTED}; margin-top: 7px; font-size: 15px; }}
.chip {{
    display: inline-block;
    border: 1px solid {BORDER2};
    background: rgba(242,201,76,0.10);
    color: {GOLD};
    border-radius: 999px;
    padding: 5px 12px;
    font-size: 13px;
    margin-left: 8px;
    margin-top: 8px;
}}
.panel {{
    background: linear-gradient(135deg, {PANEL}, {PANEL2});
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 16px;
    min-height: 100px;
    box-shadow: inset 0 0 18px rgba(0,212,255,0.035), 0 12px 28px rgba(0,0,0,0.24);
    position: relative;
    overflow: hidden;
    margin-bottom: 12px;
}}
.panel:after {{
    content:"";
    position:absolute;
    top:0;
    right:0;
    width:100%;
    height:2px;
    background: linear-gradient(90deg, transparent, {CYAN}, {GOLD}, transparent);
    opacity: 0.65;
}}
.panel-title {{ color: {MUTED}; font-size: 13px; font-weight: 600; margin-bottom: 7px; }}
.panel-value {{ color: {TEXT}; font-size: 27px; font-weight: 800; line-height: 1.15; }}
.panel-note {{ color: {GOLD}; font-size: 12px; margin-top: 8px; }}
.mini-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 10px; }}
.mini-cell {{ background: rgba(0, 212, 255, 0.06); border: 1px solid rgba(0, 212, 255, 0.18); border-radius: 14px; padding: 12px; }}
.mini-label {{ color:{MUTED}; font-size:12px; }}
.mini-value {{ color:{CYAN}; font-size:22px; font-weight:800; }}
.timeline {{ display: flex; gap: 10px; margin-top: 10px; }}
.timeline-item {{ flex: 1; min-height: 142px; background: linear-gradient(135deg, rgba(8,28,52,0.98), rgba(12,52,95,0.82)); border: 1px solid rgba(0,212,255,0.24); border-radius: 16px; padding: 14px; }}
.timeline-year {{ color: {GOLD}; font-weight: 800; font-size: 22px; }}
.timeline-stage {{ color: {TEXT}; font-weight: 700; font-size: 16px; margin-top: 4px; }}
.timeline-desc {{ color: {MUTED}; font-size: 12px; margin-top: 10px; line-height: 1.7; }}
[data-testid="stDataFrame"] {{ border: 1px solid rgba(0,212,255,0.18); border-radius: 16px; overflow: hidden; }}
hr {{ border-color: rgba(0, 212, 255, 0.14); }}
.stButton > button {{ background: linear-gradient(90deg, {BLUE}, {CYAN}); color: #00111F; border: 0; border-radius: 12px; font-weight: 800; padding: 0.55rem 1rem; }}
.stButton > button:hover {{ border: 0; color: #00111F; filter: brightness(1.08); }}

/* تحسين وضوح حقول الإدخال والقوائم */
div[data-baseweb="input"], div[data-baseweb="select"] > div {{
    background: rgba(234, 247, 255, 0.08) !important;
    border: 1px solid rgba(0, 212, 255, 0.32) !important;
    border-radius: 12px !important;
    color: #EAF7FF !important;
}}
div[data-baseweb="input"] input, div[data-baseweb="select"] input {{
    color: #EAF7FF !important;
    -webkit-text-fill-color: #EAF7FF !important;
    font-weight: 700 !important;
}}
div[data-baseweb="select"] span, div[data-baseweb="select"] div {{
    color: #EAF7FF !important;
}}
input[type="number"] {{
    color: #EAF7FF !important;
    -webkit-text-fill-color: #EAF7FF !important;
    direction: ltr !important;
    text-align: right !important;
}}
label, .stTextInput label, .stNumberInput label, .stSelectbox label {{
    color: #B9D9FF !important;
    font-weight: 700 !important;
}}

.muted {{ color: #8DAFD3; font-size: 13px; }}
code {{ direction: ltr; text-align: left; }}


/* =========================
   Mobile Responsive Fix
   ========================= */
.desktop-only {{ display: inline; }}
.mobile-only {{ display: none; }}
section[data-testid="stSidebar"] * {{
    word-break: normal !important;
    overflow-wrap: normal !important;
}}

@media only screen and (max-width: 768px) {{
    .block-container {{
        padding-left: 0.65rem !important;
        padding-right: 0.65rem !important;
        padding-top: 0.6rem !important;
        max-width: 100% !important;
    }}

    section[data-testid="stSidebar"] {{
        width: 17rem !important;
        min-width: 17rem !important;
        max-width: 17rem !important;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div {{
        white-space: normal !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
        line-height: 1.5 !important;
    }}

    .desktop-only {{ display: none !important; }}
    .mobile-only {{ display: inline !important; }}

    .neo-header {{
        padding: 16px 14px !important;
        border-radius: 18px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }}

    .neo-title {{
        font-size: 26px !important;
        line-height: 1.45 !important;
        letter-spacing: 0 !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
        white-space: normal !important;
    }}

    .neo-subtitle {{
        font-size: 13px !important;
        line-height: 1.7 !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
    }}

    .chip {{
        display: inline-block !important;
        font-size: 11px !important;
        padding: 4px 9px !important;
        margin-left: 4px !important;
        margin-top: 7px !important;
        max-width: 100% !important;
        white-space: normal !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
    }}

    .panel {{
        min-height: auto !important;
        padding: 14px !important;
        margin-bottom: 12px !important;
        border-radius: 16px !important;
        overflow: hidden !important;
    }}

    .panel-title {{
        font-size: 13px !important;
        line-height: 1.6 !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
    }}

    .panel-value {{
        font-size: 28px !important;
        line-height: 1.25 !important;
        word-break: normal !important;
        overflow-wrap: normal !important;
        white-space: normal !important;
    }}

    .panel-note {{
        font-size: 12px !important;
        line-height: 1.5 !important;
    }}

    .mini-grid {{
        grid-template-columns: 1fr !important;
    }}

    .mini-value {{
        font-size: 21px !important;
    }}

    .timeline {{
        display: block !important;
    }}

    .timeline-item {{
        width: 100% !important;
        min-height: auto !important;
        margin-bottom: 10px !important;
    }}

    div[data-testid="column"] {{
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }}

    [data-testid="stHorizontalBlock"] {{
        gap: 0.6rem !important;
        flex-wrap: wrap !important;
    }}

    [data-testid="stMetric"] {{
        min-width: 100% !important;
        padding: 12px !important;
    }}

    [data-testid="stMetricValue"] div {{
        font-size: 24px !important;
        line-height: 1.25 !important;
    }}

    [data-testid="stMetricLabel"] div {{
        font-size: 12px !important;
    }}

    div[data-baseweb="input"], div[data-baseweb="select"] > div {{
        min-height: 44px !important;
        font-size: 14px !important;
    }}

    div[data-baseweb="input"] input,
    div[data-baseweb="select"] input,
    input[type="number"] {{
        font-size: 14px !important;
        min-height: 38px !important;
    }}

    .stDataFrame, [data-testid="stDataFrame"] {{
        overflow-x: auto !important;
        max-width: 100% !important;
    }}

    iframe {{
        max-width: 100% !important;
    }}

    h1 {{ font-size: 28px !important; line-height: 1.4 !important; }}
    h2 {{ font-size: 23px !important; line-height: 1.4 !important; }}
    h3 {{ font-size: 19px !important; line-height: 1.4 !important; }}
}}

/* ===== Force hide sidebar on mobile ===== */
@media only screen and (max-width: 768px) {

    section[data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
    }

    div[data-testid="stSidebarContent"] {
        display: none !important;
    }

    button[kind="header"] {
        display: none !important;
    }

    .main .block-container {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 100% !important;
    }

    [data-testid="collapsedControl"] {
        display: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# Helpers
# =========================================================
def kpi_card(title, value, note="", color=CYAN):
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">{title}</div>
        <div class="panel-value">{value}</div>
        <div class="panel-note" style="color:{color};">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def fig_dark(fig, title=None, height=None):
    fig.update_layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,18,34,0.45)",
        font=dict(color=TEXT, family="Cairo"),
        margin=dict(l=12, r=12, t=48, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
        height=height
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, color=TEXT)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, color=TEXT)
    return fig

def ring(value, title, color=GOLD, suffix="%"):
    value = max(min(float(value), 100), 0)
    fig = go.Figure(go.Pie(
        values=[value, 100-value], hole=0.76, sort=False, direction="clockwise",
        marker=dict(colors=[color, "rgba(22,119,255,0.24)"], line=dict(width=0)),
        textinfo="none"
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
        margin=dict(l=4, r=4, t=32, b=4),
        title=dict(text=title, x=0.5, font=dict(size=14, color=TEXT)),
        annotations=[dict(text=f"<b>{value:.0f}</b><br><span style='font-size:11px;color:{MUTED}'>{suffix}</span>", x=0.5, y=0.5, showarrow=False, font=dict(color=TEXT, size=24))]
    )
    return fig

def normalize_percent(x):
    return max(0, min(100, float(x)))

def status_ar(s):
    s = str(s).strip().lower()
    if s == "paid": return "ملتزم"
    if s == "pending": return "قيد المتابعة"
    return "متأخر"

# =========================================================
# Data
# =========================================================
DATA_FILE = Path("delivery_orders_sample.csv")

@st.cache_data
def load_data():
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame({
            "month": ["2026-01","2026-01","2026-01","2026-02","2026-02","2026-03","2026-03","2026-04"],
            "platform_name": ["Talabat","Deliveroo","Careem Food","Noon Food","InstaShop","Smiles","Talabat","Careem Food"],
            "emirate": ["Dubai","Dubai","Abu Dhabi","Sharjah","Dubai","Ajman","Dubai","Abu Dhabi"],
            "area": ["Deira","Marina","Al Reem","Al Majaz","Jumeirah","Al Nuaimia","Business Bay","Khalifa City"],
            "completed_orders": [450000,210000,180000,160000,90000,60000,380000,150000],
            "cancelled_orders": [12000,8000,6000,5000,2500,1500,9000,4000],
            "active_drivers": [1800,950,700,650,300,220,1500,620],
            "traffic_violations": [320,140,120,150,60,40,260,90],
            "accidents": [14,6,5,7,2,1,11,3],
            "payment_status": ["Paid","Paid","Pending","Late","Paid","Pending","Paid","Late"]
        })
    df["month_date"] = pd.to_datetime(df["month"], errors="coerce")
    df["month_label"] = df["month_date"].dt.strftime("%Y-%m").fillna(df["month"].astype(str))
    df["fee_due"] = df["completed_orders"]
    df["collected_fee"] = df.apply(lambda r: r["fee_due"] if str(r["payment_status"]).lower().strip() == "paid" else 0, axis=1)
    df["uncollected_fee"] = df["fee_due"] - df["collected_fee"]
    df["risk_score"] = ((df["accidents"] * 5) + df["traffic_violations"] + (df["completed_orders"] / 100000)).round(2)
    df["completion_rate"] = (df["completed_orders"] / (df["completed_orders"] + df["cancelled_orders"])).fillna(0)
    df["accidents_per_100k_orders"] = (df["accidents"] / df["completed_orders"] * 100000).replace([float("inf")], 0).fillna(0).round(2)
    df["violations_per_100k_orders"] = (df["traffic_violations"] / df["completed_orders"] * 100000).replace([float("inf")], 0).fillna(0).round(2)
    return df

df = load_data()
platforms = sorted(df["platform_name"].unique())

driver_df = pd.DataFrame({
    "platform_name": platforms,
    "avg_driver_income_before": [5400, 5220, 5100, 5000, 4920, 4850, 4800, 4750, 4700, 4650][:len(platforms)],
    "avg_driver_income_after":  [5400, 5240, 5100, 5000, 4920, 4850, 4800, 4750, 4700, 4650][:len(platforms)],
    "insurance_coverage": ["نعم","نعم","قيد التفعيل","قيد التفعيل","نعم","قيد التفعيل","نعم","قيد التفعيل","نعم","قيد التفعيل"][:len(platforms)],
    "complaints_channel": ["مفعل"] * len(platforms)
})
driver_df["income_change"] = driver_df["avg_driver_income_after"] - driver_df["avg_driver_income_before"]
driver_df["protection_status"] = driver_df["income_change"].apply(lambda x: "مستقر / محمي" if x >= 0 else "يحتاج تدقيق")

scenario_df = pd.DataFrame({
    "السيناريو": ["متحفظ", "متوسط (مرجح)", "متفائل"],
    "الطلبات السنوية": [120_000_000, 200_000_000, 300_000_000],
    "الإيرادات التراكمية 5 سنوات": [676_000_000, 1_200_000_000, 1_910_000_000],
    "توقعات 10 سنوات": [1_690_000_000, 3_040_000_000, 4_850_000_000]
})

roadmap = [
    ("2026", "التأسيس", "إصدار التشريعات • تأسيس الحوكمة • تجربة محدودة"),
    ("2027", "التجريب", "إطلاق منصة التحصيل • أول مسارات دراجات • ربط البيانات"),
    ("2028", "التوسع", "تعميم على المدن الرئيسية • مركز البيانات الوطني"),
    ("2029", "الترسيخ", "كاميرات AI ضمن إطار خصوصية متين • معايير سلامة"),
    ("2030", "التصدير", "White-Label للخليج ثم الإقليم")
]

risk_mitigation = pd.DataFrame({
    "المخاطرة": ["الخصوصية وحماية البيانات", "تمرير الرسم إلى دخل السائق", "دقة التقديرات وحجم الطلبات"],
    "الأثر": ["عالٍ", "عالٍ", "متوسط"],
    "استراتيجية التخفيف": ["تأجيل الكاميرات + إطار قانوني + رقابة مستقلة", "نص تشريعي + تدقيق عقود + خط شكاوى محايد", "دراسة اكتوارية + سيناريوهات + مراجعة سنوية"]
})

governance_df = pd.DataFrame({
    "العنصر": ["الجهة المشغلة", "مجلس الإدارة", "نموذج التشغيل", "التدقيق", "حماية السائق", "البيانات الشخصية"],
    "الوضع": ["كيان شبه حكومي مستقل", "حكومة + قطاع خاص + ممثلو السائقين", "تحصيل رقمي لكل طلب مكتمل", "مراجعة دورية لبيانات المنصات", "منع تمرير الرسم إلى دخل السائق", "غير مستخدمة في النسخة الأولى"]
})

coords = {
    "Dubai": (25.2048, 55.2708), "Abu Dhabi": (24.4539, 54.3773), "Sharjah": (25.3463, 55.4209),
    "Ajman": (25.4052, 55.5136), "Umm Al Quwain": (25.5647, 55.5552),
    "Ras Al Khaimah": (25.8007, 55.9762), "Fujairah": (25.1288, 56.3265)
}

total_orders = int(df["completed_orders"].sum())
total_due = int(df["fee_due"].sum())
total_collected = int(df["collected_fee"].sum())
total_uncollected = int(df["uncollected_fee"].sum())
total_accidents = int(df["accidents"].sum())
total_violations = int(df["traffic_violations"].sum())
compliance_rate = round(total_collected / total_due * 100, 1) if total_due else 0
platform_count = df["platform_name"].nunique()

# =========================================================
# Sidebar
# =========================================================
st.sidebar.markdown("## صندوق التوصيل")
st.sidebar.markdown("<span class='muted'>Prototype v3</span>", unsafe_allow_html=True)
st.sidebar.markdown("---")

pages_list = [
    "الصفحة الرئيسية | Dashboard",
    "تسجيل بيانات منصة توصيل",
    "التحصيل والامتثال",
    "توزيع الإيرادات",
    "مؤشر المخاطر",
    "أثر السلامة",
    "السيناريوهات المالية",
    "الحوكمة وحماية السائقين",
    "خارطة التنفيذ",
    "الكاميرات قريبًا"
]

# Sidebar for desktop
page = st.sidebar.radio("التنقل", pages_list)

# Mobile navigation inside page
mobile_page = st.selectbox("القائمة", pages_list, index=pages_list.index(page))

# Use mobile selection
page = mobile_page)

# =========================================================
# Dashboard
# =========================================================
if page == "Dashboard الرئيسي":
    st.markdown(f"""
    <div class="neo-header">
        <div class="neo-title">صندوق التوصيل الوطني — لوحة التحكم المركزية</div>
        <div class="neo-subtitle">تحصيل • امتثال • مخاطر • أثر السلامة • حوكمة</div>
        <span class="chip">1 درهم / طلب مكتمل</span>
        <span class="chip">بدون كاميرات في المرحلة الأولى</span>
        <span class="chip">Prototype v3</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi_card("الطلبات المكتملة", f"{total_orders:,.0f}", "إجمالي النشاط", CYAN)
    with c2: kpi_card("الرسوم المستحقة", f"{total_due:,.0f}", "درهم", GOLD)
    with c3: kpi_card("الرسوم المحصلة", f"{total_collected:,.0f}", "درهم", GREEN)
    with c4: kpi_card("غير المحصل", f"{total_uncollected:,.0f}", "درهم", RED)
    with c5: kpi_card("المنصات", f"{platform_count}", "مشغلين", CYAN)

    left, center, right = st.columns([1.1, 1.3, 1.7])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        a, b = st.columns(2)
        with a: st.plotly_chart(ring(compliance_rate, "الامتثال", GOLD), use_container_width=True)
        with b: st.plotly_chart(ring(normalize_percent((100-total_uncollected/max(total_due,1)*100)), "التحصيل", GREEN), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel"><div class="mini-grid">', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="mini-cell"><div class="mini-label">الحوادث</div><div class="mini-value" style="color:{RED};">{total_accidents}</div></div>
            <div class="mini-cell"><div class="mini-label">المخالفات</div><div class="mini-value" style="color:{GOLD};">{total_violations}</div></div>
            <div class="mini-cell"><div class="mini-label">أعلى مؤشر خطر</div><div class="mini-value">{df['risk_score'].max():.1f}</div></div>
            <div class="mini-cell"><div class="mini-label">هدف التحصيل</div><div class="mini-value" style="color:{GREEN};">90%</div></div>
        """, unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with center:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        status_df = df.groupby("payment_status", as_index=False)["fee_due"].sum()
        fig_status = px.pie(status_df, names="payment_status", values="fee_due", hole=0.64,
                            color="payment_status", color_discrete_map={"Paid": GREEN, "Pending": GOLD, "Late": RED})
        fig_status.update_traces(textinfo="label+percent")
        fig_status.update_layout(title="حالة السداد", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT), margin=dict(l=6,r=6,t=45,b=6), showlegend=False)
        st.plotly_chart(fig_status, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        monthly = df.groupby("month_label", as_index=False)[["completed_orders", "collected_fee"]].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly["month_label"], y=monthly["completed_orders"], mode="lines+markers", name="الطلبات", line=dict(color=CYAN, width=3)))
        fig.add_trace(go.Scatter(x=monthly["month_label"], y=monthly["collected_fee"], mode="lines+markers", name="التحصيل", line=dict(color=GOLD, width=3)))
        st.plotly_chart(fig_dark(fig, "الاتجاه الشهري", 250), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        map_df = df.groupby("emirate", as_index=False).agg({"completed_orders":"sum", "fee_due":"sum", "risk_score":"sum"})
        map_df["lat"] = map_df["emirate"].map(lambda x: coords.get(x, (None,None))[0])
        map_df["lon"] = map_df["emirate"].map(lambda x: coords.get(x, (None,None))[1])
        map_df = map_df.dropna(subset=["lat","lon"])
        fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="completed_orders", color="risk_score",
                                    hover_name="emirate", color_continuous_scale=[[0, CYAN], [0.5, GOLD], [1, RED]], zoom=5.2, height=430)
        fig_map.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=35,b=0), title="خريطة النشاط والمخاطر", font=dict(color=TEXT))
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    r1, r2, r3 = st.columns([1.3, 1.2, 1.1])
    with r1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        platform_sum = df.groupby("platform_name", as_index=False)[["fee_due", "collected_fee"]].sum()
        fig = px.bar(platform_sum, x="platform_name", y=["fee_due", "collected_fee"], barmode="group", color_discrete_sequence=[CYAN, GOLD])
        st.plotly_chart(fig_dark(fig, "الرسوم حسب المنصة", 320), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        risk_area = df.groupby(["emirate","area"], as_index=False)["risk_score"].sum().sort_values("risk_score", ascending=False).head(8)
        fig = px.bar(risk_area, x="risk_score", y="area", orientation="h", color="risk_score", color_continuous_scale=[[0, CYAN], [0.6, GOLD], [1, RED]])
        st.plotly_chart(fig_dark(fig, "أعلى مناطق الخطورة", 320), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with r3:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="panel-title">الأهداف الاستراتيجية</div>
        <div class="mini-grid">
            <div class="mini-cell"><div class="mini-label">السلامة</div><div class="mini-value">-30%</div></div>
            <div class="mini-cell"><div class="mini-label">زمن الرحلة</div><div class="mini-value">-15%</div></div>
            <div class="mini-cell"><div class="mini-label">التحصيل</div><div class="mini-value">≥90%</div></div>
            <div class="mini-cell"><div class="mini-label">التصدير</div><div class="mini-value">2030</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# Register Platform
# =========================================================
elif page == "تسجيل منصة":
    st.markdown('<div class="neo-header"><div class="neo-title">تسجيل تقرير منصة توصيل</div><div class="neo-subtitle">نموذج مبسط لإدخال بيانات شهرية واحتساب الرسم تلقائيًا</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### بيانات التقرير")

    a, b = st.columns(2)
    with a:
        platform_name = st.text_input("اسم المنصة", value="منصة تجريبية", help="مثال: Talabat أو Deliveroo أو Careem")
        emirate_input = st.selectbox("الإمارة", sorted(df["emirate"].unique()))
        completed = st.number_input("الطلبات المكتملة", min_value=0, value=100000, step=1000, help="عدد الطلبات التي وصلت للعميل وتم إغلاقها كمكتملة")
        violations = st.number_input("المخالفات", min_value=0, value=80, step=1, help="عدد المخالفات المسجلة على المنصة/السائقين خلال الشهر")
    with b:
        month_input = st.selectbox("الشهر", sorted(df["month_label"].unique()))
        area_input = st.text_input("المنطقة", value="منطقة تجريبية")
        cancelled = st.number_input("الطلبات الملغاة", min_value=0, value=4000, step=500)
        accidents = st.number_input("الحوادث", min_value=0, value=3, step=1)

    drivers = st.number_input("السائقون النشطون", min_value=0, value=450, step=10)
    payment_status = st.selectbox("حالة السداد", ["Paid", "Pending", "Late"], help="Paid = تم السداد، Pending = قيد المتابعة، Late = متأخر")
    st.markdown('</div>', unsafe_allow_html=True)

    fee_due = completed
    collected = fee_due if payment_status == "Paid" else 0
    uncollected = fee_due - collected
    risk = (accidents * 5) + violations + round(completed / 100000, 2)
    completion = completed / max(completed + cancelled, 1) * 100

    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("الرسم المستحق", f"{fee_due:,.0f}", "درهم", GOLD)
    with k2: kpi_card("المبلغ المحصل", f"{collected:,.0f}", "درهم", GREEN)
    with k3: kpi_card("المبلغ غير المحصل", f"{uncollected:,.0f}", "درهم", RED if uncollected > 0 else GREEN)
    with k4: kpi_card("مؤشر الخطر", f"{risk:.2f}", "تجريبي", RED if risk > 100 else GOLD)

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### طريقة الحساب")
    calc_df = pd.DataFrame({
        "البند": ["الرسم", "نسبة الإكمال", "مؤشر الخطر"],
        "طريقة الحساب": [
            "الطلبات المكتملة × 1 درهم",
            "الطلبات المكتملة ÷ (الطلبات المكتملة + الطلبات الملغاة)",
            "الحوادث × 5 + المخالفات + (الطلبات المكتملة ÷ 100000)"
        ],
        "النتيجة": [f"{fee_due:,.0f} درهم", f"{completion:.1f}%", f"{risk:.2f}"]
    })
    st.dataframe(calc_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("عرض التقرير"):
        report = pd.DataFrame({
            "الحقل": [
                "المنصة", "الشهر", "الإمارة", "المنطقة", "الطلبات المكتملة", "الطلبات الملغاة",
                "السائقون", "المخالفات", "الحوادث", "حالة السداد", "الرسم المستحق", "المبلغ المحصل", "مؤشر الخطر"
            ],
            "القيمة": [
                platform_name, month_input, emirate_input, area_input, f"{completed:,.0f}", f"{cancelled:,.0f}",
                f"{drivers:,.0f}", f"{violations:,.0f}", f"{accidents:,.0f}", payment_status, f"{fee_due:,.0f} درهم", f"{collected:,.0f} درهم", f"{risk:.2f}"
            ]
        })
        st.dataframe(report, use_container_width=True, hide_index=True)

# =========================================================
# Collection & Compliance
# =========================================================
elif page == "التحصيل والامتثال":
    st.markdown('<div class="neo-header"><div class="neo-title">التحصيل والامتثال</div><div class="neo-subtitle">حالة السداد والمستحقات حسب المنصات</div></div>', unsafe_allow_html=True)
    compliance = df.groupby(["platform_name", "payment_status"], as_index=False).agg({"completed_orders":"sum", "fee_due":"sum", "collected_fee":"sum", "uncollected_fee":"sum"})
    compliance["حالة الامتثال"] = compliance["payment_status"].apply(status_ar)
    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi_card("المستحق", f"{total_due:,.0f}", "درهم", GOLD)
    with c2: kpi_card("المحصل", f"{total_collected:,.0f}", "درهم", GREEN)
    with c3: kpi_card("المتأخر", f"{total_uncollected:,.0f}", "درهم", RED)
    with c4: kpi_card("نسبة التحصيل", f"{compliance_rate}%", "KPI ≥ 90%", CYAN)
    st.dataframe(compliance, use_container_width=True, hide_index=True)
    a,b = st.columns(2)
    with a:
        fig = px.bar(compliance, x="platform_name", y="uncollected_fee", color="payment_status", color_discrete_map={"Paid": GREEN, "Pending": GOLD, "Late": RED})
        st.plotly_chart(fig_dark(fig, "المبالغ غير المحصلة"), use_container_width=True)
    with b:
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=compliance_rate, title={'text': "نسبة التحصيل"}, gauge={'axis': {'range': [0,100]}, 'bar': {'color': GOLD}, 'threshold': {'line': {'color': GREEN, 'width': 4}, 'value': 90}}))
        gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT), margin=dict(l=20,r=20,t=60,b=20))
        st.plotly_chart(gauge, use_container_width=True)

# =========================================================
# Revenue Allocation
# =========================================================
elif page == "توزيع الإيرادات":
    st.markdown('<div class="neo-header"><div class="neo-title">توزيع الإيرادات</div><div class="neo-subtitle">توجيه التمويل نحو برامج السلامة والبنية التحتية والحماية</div></div>', unsafe_allow_html=True)
    allocation = pd.DataFrame({"البند": ["التدريب والسلامة", "البنية التحتية الذكية", "التأمين والحماية الاجتماعية", "البيانات والتحليل"], "النسبة %": [40,25,20,15]})
    allocation["المبلغ التقديري"] = (allocation["النسبة %"]/100*total_collected).round(0)
    a,b = st.columns([1,1.4])
    with a: st.dataframe(allocation, use_container_width=True, hide_index=True)
    with b:
        fig = px.pie(allocation, names="البند", values="المبلغ التقديري", hole=0.62, color_discrete_sequence=[GOLD, CYAN, GREEN, BLUE])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT), title="توزيع التمويل")
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# Risk Index
# =========================================================
elif page == "مؤشر المخاطر":
    st.markdown('<div class="neo-header"><div class="neo-title">مؤشر المخاطر</div><div class="neo-subtitle">ترتيب المناطق حسب أولوية التدخل</div><span class="chip">الحوادث × 5 + المخالفات + الطلبات ÷ 100000</span></div>', unsafe_allow_html=True)
    risk_area = df.groupby(["emirate","area"], as_index=False).agg({"completed_orders":"sum", "traffic_violations":"sum", "accidents":"sum", "risk_score":"sum", "accidents_per_100k_orders":"mean", "violations_per_100k_orders":"mean"}).sort_values("risk_score", ascending=False)
    st.dataframe(risk_area, use_container_width=True, hide_index=True)
    a,b = st.columns([1.3,1])
    with a:
        fig = px.bar(risk_area.head(10), x="area", y="risk_score", color="emirate", color_discrete_sequence=[CYAN, GOLD, GREEN, RED, BLUE])
        st.plotly_chart(fig_dark(fig, "أعلى 10 مناطق حسب مؤشر الخطر"), use_container_width=True)
    with b:
        top = risk_area.iloc[0]
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">المنطقة الأعلى خطورة</div>
            <div class="panel-value">{top['area']}</div>
            <div class="panel-note">{top['emirate']}</div>
            <hr>
            <div class="mini-grid">
                <div class="mini-cell"><div class="mini-label">مؤشر الخطر</div><div class="mini-value">{top['risk_score']:.1f}</div></div>
                <div class="mini-cell"><div class="mini-label">الحوادث</div><div class="mini-value" style="color:{RED};">{top['accidents']}</div></div>
                <div class="mini-cell"><div class="mini-label">المخالفات</div><div class="mini-value" style="color:{GOLD};">{top['traffic_violations']}</div></div>
                <div class="mini-cell"><div class="mini-label">الطلبات</div><div class="mini-value">{top['completed_orders']:,.0f}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# Safety Impact
# =========================================================
elif page == "أثر السلامة":
    st.markdown('<div class="neo-header"><div class="neo-title">أثر السلامة</div><div class="neo-subtitle">تتبع مؤشرات السلامة المستهدفة حتى 2030</div></div>', unsafe_allow_html=True)
    baseline_accidents = 616
    target_accidents = round(baseline_accidents * 0.70)
    reduction_count = baseline_accidents - target_accidents
    c1,c2,c3 = st.columns(3)
    with c1: kpi_card("خفض الحوادث/الوفيات", "-30%", f"{baseline_accidents} → {target_accidents}", GREEN)
    with c2: kpi_card("تحسن زمن الرحلة", "-15%", "في المناطق الحضرية", CYAN)
    with c3: kpi_card("الحوادث المطلوب تقليلها", f"{reduction_count}", "تقديري", GOLD)
    impact_df = pd.DataFrame({"المؤشر": ["تحصيل الرسوم", "خفض الحوادث", "تحسن زمن الرحلة", "مركز البيانات", "جاهزية التصدير"], "المستهدف": ["≥90%", "-30%", "-15%", "2028", "2030"], "الوضع الحالي": [f"{compliance_rate}%", "قيد القياس", "قيد القياس", "تصميم", "مستقبلي"]})
    st.dataframe(impact_df, use_container_width=True, hide_index=True)

# =========================================================
# Financial Scenarios
# =========================================================
elif page == "السيناريوهات المالية":
    st.markdown('<div class="neo-header"><div class="neo-title">السيناريوهات المالية</div><div class="neo-subtitle">محاكاة الإيرادات حسب حجم الطلبات</div></div>', unsafe_allow_html=True)
    st.dataframe(scenario_df, use_container_width=True, hide_index=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=scenario_df["السيناريو"], y=scenario_df["الإيرادات التراكمية 5 سنوات"], name="5 سنوات", marker_color=CYAN))
    fig.add_trace(go.Bar(x=scenario_df["السيناريو"], y=scenario_df["توقعات 10 سنوات"], name="10 سنوات", marker_color=GOLD))
    fig.update_layout(barmode="group")
    st.plotly_chart(fig_dark(fig, "مقارنة السيناريوهات"), use_container_width=True)

# =========================================================
# Governance & Drivers
# =========================================================
elif page == "الحوكمة وحماية السائقين":
    st.markdown('<div class="neo-header"><div class="neo-title">الحوكمة وحماية السائقين</div><div class="neo-subtitle">الهيكل التشغيلي وضمانات عدم تحميل السائق الرسم</div></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["الحوكمة", "حماية السائقين"])
    with tab1:
        st.dataframe(governance_df, use_container_width=True, hide_index=True)
    with tab2:
        st.dataframe(driver_df, use_container_width=True, hide_index=True)
        fig = px.bar(driver_df, x="platform_name", y=["avg_driver_income_before", "avg_driver_income_after"], barmode="group", color_discrete_sequence=[CYAN, GOLD])
        st.plotly_chart(fig_dark(fig, "دخل السائق قبل/بعد"), use_container_width=True)

# =========================================================
# Roadmap
# =========================================================
elif page == "خارطة التنفيذ":
    st.markdown('<div class="neo-header"><div class="neo-title">خارطة التنفيذ 2026 — 2030</div><div class="neo-subtitle">التأسيس، التجريب، التوسع، الترسيخ، التصدير</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for year, stage, desc in roadmap:
        st.markdown(f'<div class="timeline-item"><div class="timeline-year">{year}</div><div class="timeline-stage">{stage}</div><div class="timeline-desc">{desc}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("### المخاطر والتخفيف")
    st.dataframe(risk_mitigation, use_container_width=True, hide_index=True)

# =========================================================
# Cameras
# =========================================================
elif page == "الكاميرات قريبًا":
    st.markdown('<div class="neo-header"><div class="neo-title">وحدة الكاميرات والذكاء الاصطناعي — قريبًا</div><div class="neo-subtitle">قدرة مستقبلية بعد اكتمال المتطلبات القانونية والخصوصية</div></div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">الاستخدامات المستقبلية</div>
            <div class="mini-grid">
                <div class="mini-cell"><div class="mini-label">انعطاف مفاجئ</div><div class="mini-value">AI</div></div>
                <div class="mini-cell"><div class="mini-label">مسافة أمان</div><div class="mini-value">AI</div></div>
                <div class="mini-cell"><div class="mini-label">وقوف عشوائي</div><div class="mini-value">AI</div></div>
                <div class="mini-cell"><div class="mini-label">مناطق خطر</div><div class="mini-value">GIS</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="panel">
            <div class="panel-title">ضوابط التفعيل</div>
            <div class="mini-grid">
                <div class="mini-cell"><div class="mini-label">قانوني</div><div class="mini-value" style="color:{GOLD};">✓</div></div>
                <div class="mini-cell"><div class="mini-label">خصوصية</div><div class="mini-value" style="color:{GOLD};">✓</div></div>
                <div class="mini-cell"><div class="mini-label">رقابة</div><div class="mini-value" style="color:{GOLD};">✓</div></div>
                <div class="mini-cell"><div class="mini-label">حوكمة</div><div class="mini-value" style="color:{GOLD};">✓</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
