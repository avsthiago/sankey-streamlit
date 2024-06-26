"""This module contains code for creating a dynamic Sankey diagram using Streamlit."""

import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sankeyflow import Sankey

st.set_page_config(layout="wide", page_title="Sankey Diagram Generator")
st.title("Sankey Diagram Generator")

st.sidebar.title("Sankey Diagram")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)

st.sidebar.number_input("Font Size", 5, 20, 10, 1, key="font_size")
st.sidebar.number_input("Curviness", 0, 10, 3, 1, key="curvature")
st.sidebar.selectbox(
    "Color Palette",
    index=0,
    options=["tab10", "tab20", "Pastel1", "Pastel2", "Set1", "Set2", "Set3"],
    key="color",
)
st.sidebar.selectbox("Flow Color Mode", index=0, options=["source", "dest"], key="flow_color_mode")
st.sidebar.markdown("---")  # Horizontal line
st.sidebar.markdown("**[Blog Post](https://thiagoalves.ai/sankey-streamlit/)**")  # Bold text

def load_demo_df():
    st.session_state.df = pd.DataFrame(
        {
            "source": ["Product", "Service and other", "Total revenue", "Total revenue"],
            "target": ["Total revenue", "Total revenue", "Gross margin", "Cost of revenue"],
            "value": [20779, 30949, 34768, 10000],
        }
    )


def draw_sankey(df):
    flows = list(df[["source", "target", "value"]].itertuples(index=False, name=None))
    # remove empty and nan values
    flows_clean = [x for x in flows if x[0] and x[1] and x[2] > 0]

    diagram = Sankey(
        flows=flows_clean,
        cmap=plt.get_cmap(st.session_state.color),
        flow_color_mode=st.session_state.flow_color_mode,
        node_opts={"label_opts": {"fontsize": st.session_state.font_size}},
        flow_opts={"curvature": st.session_state.curvature / 10.0},
    )
    _, col2, _ = st.columns([1, 7, 1])
    with col2:
        diagram.draw()
        st.pyplot(plt)
        img = io.BytesIO()
        plt.savefig(img, format="png")
        st.session_state.image = img


def empty_df():
    df = pd.DataFrame({"source": [""], "target": [""], "value": [None]})
    st.session_state.df = df.astype({"value": float})


def timestamp():
    return pd.Timestamp.now().strftime("%Y%m%d%H%M%S")


if "df" not in st.session_state:
    load_demo_df()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("Empty Table", on_click=empty_df)
with col2:
    st.button("Load Demo", on_click=load_demo_df)
with col3:
    st.download_button(
        "Download Table",
        data=st.session_state.df.to_csv(index=False),
        file_name=f"sankey-{timestamp()}.csv",
        mime="text/csv",
    )
with col4:
    download_button_placeholder = st.empty()

edited_df = st.data_editor(
    st.session_state.df,
    key="demo_df",
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
)


sankey_placeholder = st.empty()

draw_sankey(edited_df)

if "image" in st.session_state and st.session_state.image:
    download_button_placeholder.download_button(
        "Download Diagram",
        data=st.session_state.image,
        file_name=f"sankey-{timestamp()}.png",
        mime="image/png",
    )
