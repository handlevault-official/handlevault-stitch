import os
import numpy as np
import streamlit as st
from PIL import Image
from stitch import make_pattern, build_pdf

st.set_page_config(page_title="Cross-Stitch Pattern Maker | Handle Vault Stitch", page_icon="🧵")
home = os.environ.get("HOME_URL", "")
if home:
    st.markdown(f"[← Handle Vault]({home})")
st.title("🧵 Cross-Stitch Pattern Maker")
st.caption("Handle Vault Stitch: turn any image into a printable cross-stitch pattern PDF. Files are processed in memory and not saved.")

up = st.file_uploader("Image", type=["png", "jpg", "jpeg", "webp", "gif", "bmp"])
title = st.text_input("Title", "My Cross-Stitch Pattern", max_chars=60)
c1, c2, c3 = st.columns(3)
width = c1.number_input("Width in stitches", 20, 200, 80)
colors = c2.number_input("Max thread colors", 2, 40, 16)
fabric = c3.selectbox("Aida fabric count", [11, 14, 16, 18], index=1)

if st.button("Generate PDF", type="primary", disabled=up is None):
    with st.spinner("Building your pattern..."):
        try:
            grid, legend = make_pattern(up.getvalue(), int(width), int(colors))
            pdf = build_pdf(grid, legend, int(fabric), title or "Cross-Stitch Pattern")
            st.session_state["stitch"] = dict(pdf=pdf, grid=grid, legend=legend)
        except Exception as e:
            st.session_state.pop("stitch", None)
            st.error(f"Could not process image: {e}")

r = st.session_state.get("stitch")
if r:
    pal = np.array([l["rgb"] for l in r["legend"]], np.uint8)
    H, W = r["grid"].shape
    st.image(Image.fromarray(pal[r["grid"]]).resize((W * 6, H * 6), Image.NEAREST),
             caption=f"{W} x {H} stitches, {len(r['legend'])} colors")
    st.dataframe([{"Symbol": l["sym"], "DMC": l["code"], "Stitches": l["count"]} for l in r["legend"]], hide_index=True)
    st.download_button("Download PDF", r["pdf"], "cross-stitch-pattern.pdf", "application/pdf", type="primary")
st.divider()
st.link_button("☕ Support this tool", "https://ko-fi.com/handlevaultofficial")
st.divider()
st.link_button("☕ Support this tool", "https://ko-fi.com/handlevaultofficial", type="primary")
