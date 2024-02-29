"""This module contains code for creating a dynamic Sankey diagram using Streamlit."""

import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sankeyflow import Sankey

st.set_page_config(layout="wide", page_title="Dynamic Sankey Diagram")
st.title("Dynamic Sankey Diagram")

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

# Initialize or retrieve the DataFrame from the session state
if "df" not in st.session_state:
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

    s = Sankey(
        flows=flows_clean,
        cmap=plt.get_cmap(st.session_state.color),
        node_opts={"label_opts": {"fontsize": st.session_state.font_size}},
        flow_opts={"curvature": st.session_state.curvature / 10.0},
    )

    s.draw()
    st.pyplot(plt)
    img = io.BytesIO()
    plt.savefig(img, format="png")
    st.session_state.image = img


# create an empty dataframe
def empty_df():
    df = pd.DataFrame({"source": [""], "target": [""], "value": [None]})
    st.session_state.df = df.astype({"value": float})


def load_demo_df():
    st.session_state.df = pd.DataFrame(
        {
            "source": ["Product", "Service and other", "Total revenue", "Total revenue"],
            "target": ["Total revenue", "Total revenue", "Gross margin", "Cost of revenue"],
            "value": [20779, 30949, 34768, 10000],
        }
    )


def timestamp():
    return pd.Timestamp.now().strftime("%Y%m%d%H%M%S")


def generate_image():
    img = io.BytesIO()
    plt.savefig(img, format="png")
    return img


col1, col2, col3, col4 = st.columns(4)
col1.button("Empty Table", on_click=empty_df)
col2.button("Load Demo", on_click=load_demo_df)
col3.download_button(
    "Download Table",
    data=st.session_state.df.to_csv(index=False),
    file_name=f"sankey-{timestamp()}.csv",
    mime="text/csv",
)


if "image" in st.session_state and st.session_state.image:
    col4.download_button(
        "Download Diagram",
        data=st.session_state.image,
        file_name=f"sankey-{timestamp()}.png",
        mime="image/png",
    )


edited_df = st.data_editor(
    st.session_state.df,
    key="demo_df",
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
)


sankey_placeholder = st.empty()

sankey_placeholder.empty()
draw_sankey(edited_df)
