import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time
from scipy.special import airy

st.set_page_config(layout="centered")

st.title("Airy Beam Advanced Visualization")

st.markdown("""
## 🎯 Objective

This app demonstrates key properties of Airy beams:

- Parabolic trajectory (self-acceleration)
- Shape preservation (non-diffraction)
- Circular Airy beam dynamics

The results validate theoretical predictions using numerical simulation.
""")

# =========================
# 🔧 PARAMETERS
# =========================
z_max = st.slider("Max propagation distance", 1.0, 10.0, 5.0)
steps = st.slider("Trajectory steps", 10, 100, 40)

# =========================
# 🧱 GRID (FIXED DOMAIN)
# =========================
N = 200
x = np.linspace(-10, 30, N)
y = np.linspace(-10, 10, N)
X, Y = np.meshgrid(x, y)

a = 0.05

# =========================
# 🌊 STANDARD AIRY BEAM
# =========================
def airy_beam(X, Y, z):
    shift = (z**2) / 4.0
    Xs = X - shift
    Ys = Y - shift

    Ai_x = airy(Xs)[0]
    Ai_y = airy(Ys)[0]

    envelope = np.exp(a * (Xs + Ys))
    field = Ai_x * Ai_y * envelope

    return np.abs(field)**2

# =========================
# 🌊 CIRCULAR AIRY BEAM (CAB)
# =========================
def circular_airy_beam(X, Y, z):
    r = np.sqrt(X**2 + Y**2)
    shift = (z**2)/4
    
    Ai = airy(r - shift)[0]
    envelope = np.exp(a * (r - shift))
    
    return np.abs(Ai * envelope)**2




# =========================
# 🔴 TRAJECTORY
# =========================
st.subheader("Trajectory (Simulation vs Theory)")
st.markdown(r"""
### 🧮 Simulation Model (How the Beam is Computed)

The simulated Airy beam intensity is obtained from the field:

$$
\psi(x, y, z) = \mathrm{Ai}\left(x - \frac{z^2}{4}\right)\,\mathrm{Ai}(y)\,e^{a(x+y)}
$$

where:

- $\mathrm{Ai}(\cdot)$ is the **Airy function**
- $\frac{z^2}{4}$ represents the **parabolic shift** of the beam
- $a$ is a small positive parameter ensuring **finite energy**

The intensity is then computed as:

$$
I(x,y,z) = |\psi(x,y,z)|^2
$$

---

### 🔍 How Simulation Tracks the Beam

At each propagation distance $z$:

1. Compute intensity $I(x,y,z)$ on a grid  
2. Locate the maximum intensity point using:
   $$
   (x_{\text{peak}}, y_{\text{peak}}) = \arg\max I(x,y,z)
   $$
3. Record $x_{\text{peak}}$ as the beam position  

This produces the red points in the trajectory plot.
""")

z_vals = np.linspace(0, z_max, steps)

sim_x = []
sim_z = []

for z in z_vals:
    I = airy_beam(X, Y, z)
    idx = np.unravel_index(np.argmax(I), I.shape)
    peak_x = x[idx[1]]

    sim_x.append(peak_x)
    sim_z.append(z)

# theory
z_theory = np.linspace(0, z_max, 200)
x_theory = (z_theory**2)/4

fig1, ax1 = plt.subplots(figsize=(4,3))
ax1.plot(sim_z, sim_x, 'ro', label="Sim")
ax1.plot(z_theory, x_theory, 'b-', label="Theory")
ax1.set_xlabel("z")
ax1.set_ylabel("x")
ax1.legend()
ax1.grid()

st.pyplot(fig1)



# =========================
# 🔵 PROPAGATION + TRAJECTORY OVERLAY
# =========================
st.markdown("---")
st.subheader("Propagation with Parabolic Trajectory Overlay")
st.markdown(r"""
### 🌊 Beam Propagation

The transverse field of the Airy beam is:

$$
\psi(x, y, z) = \mathrm{Ai}(x - \frac{z^2}{4}) \cdot \mathrm{Ai}(y - \frac{z^2}{4}) \cdot e^{a(x+y)}
$$

- The Airy function **Ai(x)** governs the beam structure.
- The exponential term ensures **finite energy**.
- The beam maintains its shape → **non-diffracting behavior**.

🔴 The dashed line shows the **theoretical trajectory**  
🔴 The red dot shows the **current beam peak**
""")

z = st.slider("z position", 0.0, z_max, 0.0, 0.1)

I = airy_beam(X, Y, z)

fig2, ax2 = plt.subplots(figsize=(4,3))
ax2.imshow(I, extent=[x.min(), x.max(), y.min(), y.max()], cmap='gray')

# Overlay trajectory
z_line = np.linspace(0, z, 100)
x_line = (z_line**2)/4
ax2.plot(x_line, np.zeros_like(x_line), 'r--', linewidth=2)

# Mark current position
current_x = (z**2)/4
ax2.plot(current_x, 0, 'ro')

ax2.set_title(f"z = {z:.2f}")
ax2.set_xlabel("x")
ax2.set_ylabel("y")

st.pyplot(fig2)

st.markdown(r"""
### ▶ Dynamic Propagation

This animation shows:

- Continuous propagation of the Airy beam
- Movement of the main lobe along a **parabolic path**
- Preservation of beam structure over distance

🧠 Key Properties:
- **Self-acceleration**
- **Non-diffraction**
- Energy transfer from side lobes to main lobe
""")

# =========================
# ▶ ANIMATION
# =========================
st.subheader("Propagation Animation")

if st.button("▶ Play"):
    placeholder = st.empty()

    z_all = np.linspace(0, z_max, 100)
    x_all = (z_all**2)/4

    for zz in np.linspace(0, z_max, 40):

        I_temp = airy_beam(X, Y, zz)
        center_x = (zz**2) / 4

        # 🔥 SIDE-BY-SIDE FIGURE
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,4))

        # =========================
        # 🔵 LEFT: INTENSITY
        # =========================
        ax1.imshow(
            I_temp,
            extent=[x.min(), x.max(), y.min(), y.max()],
            cmap='gray'
        )

        ax1.set_xlim(-10, 30)
        ax1.set_ylim(-10, 10)

        ax1.set_title(f"Beam (z = {zz:.2f})")
        ax1.set_xlabel("x")
        ax1.set_ylabel("y")

        # beam peak
        ax1.plot(center_x, 0, 'ro')

        # =========================
        # 🔴 RIGHT: TRAJECTORY
        # =========================
        ax2.plot(z_all, x_all, 'b-', label="Theory")
        ax2.plot(zz, center_x, 'ro', label="Current position")

        ax2.set_xlabel("z")
        ax2.set_ylabel("x")
        ax2.set_title("Parabolic Trajectory")
        ax2.grid()
        ax2.legend()

        placeholder.pyplot(fig)
        time.sleep(0.05)




# =========================
# 🟢 SHAPE PRESERVATION (LARGE Z)
# =========================
st.markdown("---")
st.subheader("Shape Preservation at Large Distance")

st.markdown(r"""
### 🧠 Concept

Even at very large propagation distances, the Airy beam maintains its shape.

Instead of simulating the entire domain, we move a **local observation window** with the beam.

This allows us to observe **shape preservation** clearly.

The beam peak follows:

$$
x(z) = \frac{z^2}{4}
$$
""")

z_large = st.slider("Large z", 0.0, 400.0, 50.0, 10.0)

center = (z_large**2) / 4

# 🔥 MOVING WINDOW IN BOTH x AND y
x_local = np.linspace(center - 10, center + 10, 200)
y_local = np.linspace(center - 10, center + 10, 200)

Xl, Yl = np.meshgrid(x_local, y_local)

I_large = airy_beam(Xl, Yl, z_large)

fig_large, ax_large = plt.subplots(figsize=(5,5))

ax_large.imshow(
    I_large,
    extent=[x_local.min(), x_local.max(), y_local.min(), y_local.max()],
    cmap='gray',
    aspect='equal'
)

ax_large.set_xlim(center - 10, center + 10)
ax_large.set_ylim(center - 10, center + 10)

ax_large.set_title(f"Beam at z = {z_large:.1f} (Fully Moving Frame)")
ax_large.set_xlabel("x")
ax_large.set_ylabel("y")

# mark center
ax_large.plot(center, center, 'ro')

st.pyplot(fig_large)


# =========================
# 🟣 CIRCULAR AIRY BEAM
# =========================
st.markdown("---")
st.markdown(r"""
### 🟣 Circular Airy Beam (CAB)

The circular Airy beam is defined using radial coordinates:

$$
r = \sqrt{x^2 + y^2}
$$

$$
\psi(r, z) = \mathrm{Ai}(r - \frac{z^2}{4}) \cdot e^{a(r - \frac{z^2}{4})}
$$

- Exhibits **radial symmetry**
- Maintains structure while expanding
- Useful in optical manipulation and beam shaping
""")

st.subheader("Circular Airy Beam (CAB)")

z_cab = st.slider("CAB z position", 0.0, z_max, 0.0, 0.1)

I_cab = circular_airy_beam(X, Y, z_cab)

fig3, ax3 = plt.subplots(figsize=(4,3))
ax3.imshow(I_cab, extent=[-10,10,-10,10], cmap='gray')
ax3.set_title(f"CAB at z = {z_cab:.2f}")
ax3.set_xlabel("x")
ax3.set_ylabel("y")

st.pyplot(fig3)