import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide", page_title="חקר פונקציות", page_icon="📈")

st.title("📊 חקר פונקציות: חזקה, מעריכית ולוגריתמית")

st.sidebar.header("Parameters")
n = st.sidebar.number_input("Power (n)", min_value=-5, max_value=5, value=2, step=1)
a = st.sidebar.number_input("Base (a)", min_value=0.1, max_value=5.0, value=2.0, step=0.05)

col1, col2 = st.columns(2, gap="large")

with col1:
    if n == 0:
        power_str = "y = 1"
    elif n == 1:
        power_str = "y = x"
    elif n > 0:
        power_str = f"y = x^{{{n}}}"
    else:
        abs_n = abs(n)
        power_str = f"y = \\frac{{1}}{{x^{{{abs_n}}}}}" if abs_n > 1 else "y = \\frac{1}{x}"
        
    st.subheader(f"פונקציית חזקה: ${power_str}$")
    
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    
    x1 = np.linspace(-5, 5, 1200)
    with np.errstate(divide='ignore', invalid='ignore'):
        y1 = x1**n
        if n < 0:
            y1[np.abs(x1) < 0.05] = np.nan
        y1[y1 > 45] = np.nan
        y1[y1 < -45] = np.nan

    ax1.plot(x1, y1, lw=3.5, color='#1f77b4')
    ax1.axhline(0, color='black', lw=1.2)
    ax1.axvline(0, color='black', lw=1.2)
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax1.set_xlim(-5.5, 5.5)
    ax1.set_ylim(-9, 9)
    ax1.tick_params(labelsize=12)
    st.pyplot(fig1)

with col2:
    st.subheader(f"מעריכית ולוגריתמית ($a = {a:.2f}$)")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    x_exp = np.linspace(-5, 5, 1000)
    # Ограничиваем область логарифма, чтобы вертикальная асимптота не сливалась с осью Y, а график не уходил в бесконечный минус внизу
    x_log = np.linspace(0.03, 7.5, 1000)
    y2_exp = a**x_exp
    y2_log = np.log(x_log) / np.log(a)

    # Обрезаем значения логарифма снизу, чтобы линия не прилипала к нижней границе графика
    y2_log[y2_log < -8] = np.nan

    ax2.plot(x_exp, y2_exp, lw=3.5, color='#d62728', label=f'$y = {a:.2f}^{{x}}$')
    ax2.plot(x_log, y2_log, lw=3.5, color='#2ca02c', label=f'$y = \\log_{{{a:.2f}}}(x)$')
    ax2.plot(x_log, x_log, color='gray', linestyle='--', lw=1.5, label='$y = x$')
    
    ax2.axhline(0, color='black', lw=1.2)
    ax2.axvline(0, color='black', lw=1.2)
    ax2.grid(True, linestyle=':', alpha=0.7)
    ax2.set_xlim(-5.5, 7.5)
    ax2.set_ylim(-9, 10)
    ax2.legend(fontsize=12, loc='upper left')
    ax2.tick_params(labelsize=12)
    st.pyplot(fig2)
