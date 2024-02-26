import matplotlib.pyplot as plt
import streamlit as st
from sankeyflow import Sankey
import pandas as pd

st.title('Dynamic Sankey Diagram')

# Initialize or retrieve the DataFrame from the session state
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "source": ["Product", "Service and other", "Total revenue", "Total revenue"],
        "target": ["Total revenue", "Total revenue", "Gross margin", "Cost of revenue"],
        "value": [20779, 30949, 34768, 10000]
    })

# Function to draw the Sankey diagram
def draw_sankey(df):
    flows = list(df[['source', 'target', 'value']].itertuples(index=False, name=None))
    # remove none values
    flows_clean = [x for x in flows if x[0] and x[1] and x[2]]
    s = Sankey(flows=flows_clean) # node_opts=node_opts, flow_opts=flow_opts
    s.draw()
    st.pyplot(plt)

# Display the DataFrame to the user
edited_df = st.data_editor(st.session_state.df, key="demo_df", num_rows="dynamic", use_container_width=True, hide_index=True)

# Placeholder for the Sankey diagram
sankey_placeholder = st.empty()

# Update and redraw Sankey diagram
def update_sankey():
    sankey_placeholder.empty()
    draw_sankey(edited_df)

# Assuming you have a mechanism to edit the DataFrame here

# Initially draw the Sankey diagram
update_sankey()

# empty df , load demo, , side bar with upload, how to use, 