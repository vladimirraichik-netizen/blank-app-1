import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("חקר פונקציות: חזקה, מעריכית ולוגריתמית")

st.sidebar.header("פרמטרים")
n = st.sidebar.slider("בחר חזקה (n)", -5, 5, 2, 1)
a = st.sidebar.slider("בחר בסיס (a)", 0.1, 5.0, 2.0, 0.05)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

x1 = np.linspace(-5, 5, 600)
x2 = np.linspace(0.01, 8, 600)

with np.errstate(divide='ignore', invalid='ignore'):
    y1 = x1**n
    y1[y1 > 100] = np.nan
    y1[y1 < -100] = np.nan

ax1.plot(x1, y1, lw=2.5, color='blue')
ax1.set_title(f'Power Function: y = x^{n}', fontsize=12)
ax1.axhline(0, color='black', lw=1)
ax1.axvline(0, color='black', lw=1)
ax1.grid(True, linestyle=':')
ax1.set_xlim(-6, 6)
ax1.set_ylim(-15, 15)

y2_exp = a**x1
y2_log = np.log(x2) / np.log(a)

ax2.plot(x1, y2_exp, lw=2.5, color='red', label=f'y = {a:.2f}^x')
ax2.plot(x2, y2_log, lw=2.5, color='darkgreen', label=f'y = log_{a:.2f}(x)')
ax2.plot(x2, x2, color='gray', linestyle='--', label='y = x')
ax2.set_title(f'Exponential & Logarithmic (a = {a:.2f})', fontsize=12)
ax2.axhline(0, color='black', lw=1)
ax2.axvline(0, color='black', lw=1)
ax2.grid(True, linestyle=':')
ax2.set_xlim(-6, 8)
ax2.set_ylim(-10, 15)
ax2.legend()

plt.tight_layout()
st.pyplot(fig)
