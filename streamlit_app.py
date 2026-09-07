import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide", page_title="חקר פונקציות", page_icon="📈")

st.title("📊 חקר פונקציות: חזקה, מעריכית ולוגריתמית")

st.sidebar.header("Parameters")
func_type = st.sidebar.selectbox(
    "Power Function Type", 
    ["Integer Power (x^n)", "Root Function (n-th root)", "Rational Power"]
)

if func_type == "Integer Power (x^n)":
    n = st.sidebar.number_input("Power (n)", min_value=-5, max_value=5, value=2, step=1)
elif func_type == "Root Function (n-th root)":
    root_n = st.sidebar.number_input("Root index (n)", min_value=2, max_value=6, value=2, step=1)
else:
    rational_options = {
        "√x": (1, 2),
        "√x³": (3, 2),
        "∛x": (1, 3),
        "∛x²": (2, 3),
        "∜x³": (3, 4),
        "1 / √x": (-1, 2),
        "1 / ∛x": (-1, 3)
    }
    selected_rat = st.sidebar.selectbox("Select rational power", list(rational_options.keys()))
    p, q = rational_options[selected_rat]

show_inverse = st.sidebar.checkbox("Show Inverse Function & Symmetry", value=False)

a_gt1 = st.sidebar.number_input("Base a > 1 (Growth)", min_value=1.05, max_value=5.0, value=2.0, step=0.05)
a_lt1 = st.sidebar.number_input("Base 0 < a < 1 (Decay)", min_value=0.1, max_value=0.95, value=0.5, step=0.05)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    fig1, ax1 = plt.subplots(figsize=(5, 5))
    
    ax1.axhline(0, color='black', lw=1.2, zorder=1)
    ax1.axvline(0, color='black', lw=1.2, zorder=1)
    
    if func_type == "Integer Power (x^n)":
        if n == 0:
            power_str = "y = 1"
        elif n == 1:
            power_str = "y = x"
        elif n > 0:
            power_str = f"y = x^{{{n}}}"
        else:
            abs_n = abs(n)
            power_str = f"y = \\frac{{1}}{{x^{{{abs_n}}}}}" if abs_n > 1 else "y = \\frac{1}{x}"
            
        if n < 0 and not show_inverse:
            x_left = np.linspace(-5.5, -0.001, 2000)
            x_right = np.linspace(0.001, 5.5, 2000)
            y_left = x_left**n
            y_right = x_right**n
            y_left[y_left > 100] = np.nan
            y_left[y_left < -100] = np.nan
            y_right[y_right > 100] = np.nan
            y_right[y_right < -100] = np.nan
            
            ax1.plot(x_left, y_left, lw=2.2, color='#1f77b4', zorder=3)
            ax1.plot(x_right, y_right, lw=2.2, color='#1f77b4', zorder=3)
        else:
            x_min = 0.001 if (n < 0 and show_inverse) else -5.5
            x1 = np.linspace(x_min, 5.5, 3000)
            y1 = x1**n
            y1[y1 > 100] = np.nan
            y1[y1 < -100] = np.nan
            ax1.plot(x1, y1, lw=2.2, color='#1f77b4', label=f'${power_str}$', zorder=3)
            
            if show_inverse and n != 0:
                x_pos = np.linspace(0.001 if n < 0 else 0, 5.5, 3000)
                y_inv = x_pos**(1/n)
                y_inv[y_inv > 100] = np.nan
                inv_label = f"$y = \\sqrt[{n}]{{x}}$" if n > 2 else ("$y = \\sqrt{x}$" if n == 2 else "$y = x$")
                ax1.plot(x_pos, y_inv, lw=2.2, color='#ff7f0e', label=inv_label, zorder=3)
                ax1.plot(np.linspace(-5.5, 5.5, 200), np.linspace(-5.5, 5.5, 200), color='gray', linestyle='--', lw=1.3, label='$y = x$', zorder=2)
                ax1.legend(fontsize=9, loc='upper left')
                
        ax1.set_xlim(-5.5, 5.5)
        ax1.set_ylim(-9, 9)
        
    elif func_type == "Root Function (n-th root)":
        if root_n == 2:
            power_str = "y = \\sqrt{x}"
            inv_str = "y = x^2"
        else:
            power_str = f"y = \\sqrt[{root_n}]{{x}}"
            inv_str = f"y = x^{{{root_n}}}"
            
        x1 = np.linspace(-5.5, 5.5, 3000)
        with np.errstate(divide='ignore', invalid='ignore'):
            if root_n % 2 == 1 and not show_inverse:
                y1 = np.sign(x1) * (np.abs(x1) ** (1 / root_n))
            else:
                y1 = np.where(x1 >= 0, x1 ** (1 / root_n), np.nan)
                
        ax1.plot(x1, y1, lw=2.2, color='#1f77b4', label=f'${power_str}$', zorder=3)
        
        if show_inverse:
            x_pos = np.linspace(0, 5.5, 3000)
            y_inv = x_pos**root_n
            y_inv[y_inv > 100] = np.nan
            ax1.plot(x_pos, y_inv, lw=2.2, color='#ff7f0e', label=f'${inv_str}$', zorder=3)
            ax1.plot(x_pos, x_pos, color='gray', linestyle='--', lw=1.3, label='$y = x$', zorder=2)
            ax1.legend(fontsize=9, loc='upper left')
            
        ax1.set_xlim(-5.5, 5.5)
        ax1.set_ylim(-9, 9)
        
    else:
        if p == 1 and q == 2:
            power_str = "y = \\sqrt{x}"
            inv_str = "y = x^2"
        elif p == 3 and q == 2:
            power_str = "y = \\sqrt{x^3}"
            inv_str = "y = \\sqrt[3]{x^2}"
        elif p == 1 and q == 3:
            power_str = "y = \\sqrt[3]{x}"
            inv_str = "y = x^3"
        elif p == 2 and q == 3:
            power_str = "y = \\sqrt[3]{x^2}"
            inv_str = "y = \\sqrt{x^3}"
        elif p == 3 and q == 4:
            power_str = "y = \\sqrt[4]{x^3}"
            inv_str = "y = \\sqrt[3]{x^4}"
        elif p == -1 and q == 2:
            power_str = "y = \\frac{1}{\\sqrt{x}}"
            inv_str = "y = \\frac{1}{x^2}"
        elif p == -1 and q == 3:
            power_str = "y = \\frac{1}{\\sqrt[3]{x}}"
            inv_str = "y = \\frac{1}{x^3}"
        else:
            power_str = f"y = x^{{\\frac{{{p}}}{{{q}}}}}"
            inv_str = f"y = x^{{\\frac{{{q}}}{{{p}}}}}"
        
        with np.errstate(divide='ignore', invalid='ignore'):
            if p < 0 and q % 2 == 1 and not show_inverse:
                x_left = np.linspace(-5.5, -0.001, 2000)
                x_right = np.linspace(0.001, 5.5, 2000)
                y_left = np.sign(x_left) * (np.abs(x_left) ** (p / q))
                y_right = np.sign(x_right) * (np.abs(x_right) ** (p / q))
                
                y_left[y_left > 100] = np.nan
                y_left[y_left < -100] = np.nan
                y_right[y_right > 100] = np.nan
                y_right[y_right < -100] = np.nan
                
                ax1.plot(x_left, y_left, lw=2.2, color='#1f77b4', zorder=3)
                ax1.plot(x_right, y_right, lw=2.2, color='#1f77b4', zorder=3)
            else:
                x_min = 0.001 if (show_inverse and (q % 2 == 1 or p < 0)) else -5.5
                x1 = np.linspace(x_min, 5.5, 3000)
                if q % 2 == 0:
                    y1 = np.where(x1 >= 0, x1 ** (p / q), np.nan)
                else:
                    if p % 2 == 0:
                        y1 = (np.abs(x1) ** (p / q))
                    else:
                        y1 = np.sign(x1) * ((np.abs(x1) ** (p / q)))
                
                y1[y1 > 100] = np.nan
                y1[y1 < -100] = np.nan
                ax1.plot(x1, y1, lw=2.2, color='#1f77b4', label=f'${power_str}$', zorder=3)
                
                if show_inverse:
                    x_pos = np.linspace(0.001 if p < 0 else 0, 5.5, 3000)
                    y_inv = x_pos**(q/p)
                    y_inv[y_inv > 100] = np.nan
                    ax1.plot(x_pos, y_inv, lw=2.2, color='#ff7f0e', label=f'${inv_str}$', zorder=3)
                    ax1.plot(x_pos, x_pos, color='gray', linestyle='--', lw=1.3, label='$y = x$', zorder=2)
                    ax1.legend(fontsize=9, loc='upper left')
                
        ax1.set_xlim(-5.5, 5.5)
        ax1.set_ylim(-9, 9)

    st.subheader(f"${power_str}$")
    ax1.grid(True, linestyle=':', alpha=0.7, zorder=0)
    ax1.tick_params(labelsize=10)
    st.pyplot(fig1)

with col2:
    st.subheader(f"גידול ($a = {a_gt1:.2f} > 1$)")
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    
    x_exp = np.linspace(-5.5, 5.5, 3000)
    x_log = np.linspace(0.00001, 7.5, 3000)
    
    y2_exp = a_gt1**x_exp
    y2_log = np.log(x_log) / np.log(a_gt1)

    ax2.axhline(0, color='black', lw=1.2, zorder=1)
    ax2.axvline(0, color='black', lw=1.2, zorder=1)
    ax2.plot(x_exp, y2_exp, lw=2.2, color='#d62728', label=f'$y = {a_gt1:.2f}^{{x}}$', zorder=3)
    # Исправленный формат логарифма: основание внизу, аргумент без скобок
    ax2.plot(x_log, y2_log, lw=2.2, color='#2ca02c', label=f'$y = \\log_{{{a_gt1:.2g}}} x$', zorder=3)
    ax2.plot(x_log, x_log, color='gray', linestyle='--', lw=1.3, label='$y = x$', zorder=2)
    
    ax2.grid(True, linestyle=':', alpha=0.7, zorder=0)
    ax2.set_xlim(-5.5, 7.5)
    ax2.set_ylim(-9, 10)
    ax2.legend(fontsize=10, loc='upper left')
    ax2.tick_params(labelsize=10)
    st.pyplot(fig2)

with col3:
    st.subheader(f"דעיכה ($0 < a = {a_lt1:.2f} < 1$)")
    fig3, ax3 = plt.subplots(figsize=(5, 5))
    
    x_exp = np.linspace(-5.5, 5.5, 3000)
    x_log = np.linspace(0.00001, 7.5, 3000)
    
    y3_exp = a_lt1**x_exp
    y3_log = np.log(x_log) / np.log(a_lt1)

    ax3.axhline(0, color='black', lw=1.2, zorder=1)
    ax3.axvline(0, color='black', lw=1.2, zorder=1)
    ax3.plot(x_exp, y3_exp, lw=2.2, color='#d62728', label=f'$y = {a_lt1:.2f}^{{x}}$', zorder=3)
    # Исправленный формат логарифма: основание внизу, аргумент без скобок
    ax3.plot(x_log, y3_log, lw=2.2, color='#2ca02c', label=f'$y = \\log_{{{a_lt1:.2g}}} x$', zorder=3)
    ax3.plot(x_log, x_log, color='gray', linestyle='--', lw=1.3, label='$y = x$', zorder=2)
    
    ax3.grid(True, linestyle=':', alpha=0.7, zorder=0)
    ax3.set_xlim(-5.5, 7.5)
    ax3.set_ylim(-9, 10)
    ax3.legend(fontsize=10, loc='upper left')
    ax3.tick_params(labelsize=10)
    st.pyplot(fig3)
