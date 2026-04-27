import streamlit as st
import numpy as np
import random
import time
import plotly.express as px

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(page_title="RQS Visual Lab", layout="wide")

# ============================================
# 🎨 HIGH-CONTRAST UI (FIXED)
# ============================================

st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #020617;
    color: #ffffff;
}

/* Title */
h1 {
    text-align: center;
    font-size: 3rem;
    background: linear-gradient(90deg, #00eaff, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Headings */
h2, h3 {
    color: #e2e8f0 !important;
}

/* Text */
p, label, span {
    color: #cbd5f5 !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #94a3b8 !important;
    font-size: 18px;
    font-weight: bold;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #22d3ee !important;
    border-bottom: 3px solid #22d3ee !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
}

/* Charts */
.js-plotly-plot {
    background-color: transparent !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.title("⚡ Randomized Quick Sort Visual Lab")

st.markdown(
    "<p style='text-align:center;'>Real-world simulation of sorting in modern systems</p>",
    unsafe_allow_html=True
)

# ============================================
# RANDOMIZED QUICK SORT
# ============================================

def partition(arr, low, high, counter):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        counter[0] += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

def randomized_quicksort(arr, low, high, counter):
    if low < high:
        rand = random.randint(low, high)
        arr[high], arr[rand] = arr[rand], arr[high]
        pi = partition(arr, low, high, counter)
        randomized_quicksort(arr, low, pi-1, counter)
        randomized_quicksort(arr, pi+1, high, counter)

# ============================================
# HELPER FUNCTION
# ============================================

def run_sort(data, reverse=False):
    arr = data.tolist()
    counter = [0]

    start = time.time()
    randomized_quicksort(arr, 0, len(arr)-1, counter)
    end = time.time()

    if reverse:
        arr = arr[::-1]

    return arr, counter[0], end-start

# ============================================
# TABS
# ============================================

tab1, tab2, tab3 = st.tabs(["🛒 E-Commerce", "🗄 Database", "🔍 Search Engine"])

# ============================================
# 🛒 E-COMMERCE
# ============================================

with tab1:
    st.subheader("🛒 Product Price Sorting")

    size = st.slider("Number of Products", 50, 300, 120)

    data = np.random.randint(100, 5000, size)
    sorted_data, comp, t = run_sort(data)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Before")
        fig = px.bar(data, color=data, color_continuous_scale="blues")
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### After")
        fig2 = px.bar(sorted_data, color=sorted_data, color_continuous_scale="greens")
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("⏱ Time", f"{t:.5f}s")
    m2.metric("🔁 Comparisons", comp)
    m3.metric("📊 Complexity", "O(n log n)")

# ============================================
# 🗄 DATABASE
# ============================================

with tab2:
    st.subheader("🗄 Query Result Sorting")

    size = st.slider("Number of Records", 50, 300, 150, key="db")

    data = np.arange(size)
    np.random.shuffle(data)

    sorted_data, comp, t = run_sort(data)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Before")
        st.line_chart(data)

    with col2:
        st.markdown("### After")
        st.line_chart(sorted_data)

    m1, m2, m3 = st.columns(3)
    m1.metric("Latency", f"{t:.5f}s")
    m2.metric("Comparisons", comp)
    m3.metric("Efficiency", "High")

# ============================================
# 🔍 SEARCH ENGINE
# ============================================

with tab3:
    st.subheader("🔍 Ranking Optimization")

    size = st.slider("Number of Pages", 50, 300, 120, key="search")

    data = np.random.rand(size)

    sorted_data, comp, t = run_sort(data, reverse=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Initial Ranking")
        st.area_chart(data)

    with col2:
        st.markdown("### Optimized Ranking")
        st.area_chart(sorted_data)

    m1, m2, m3 = st.columns(3)
    m1.metric("Time", f"{t:.5f}s")
    m2.metric("Comparisons", comp)
    m3.metric("Ranking Quality", "Improved")

# ============================================
# FOOTER
# ============================================

st.markdown("---")

st.markdown("""
### 🚀 Why Randomized Quick Sort?

- Avoids worst-case scenarios using random pivot  
- Works efficiently with real-world unpredictable data  
- Expected time complexity: O(n log n)  

Used in:
- E-commerce platforms  
- Database systems  
- Search engine ranking  
""")