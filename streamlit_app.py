import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Function to create a Sankey diagram
def create_sankey(source, target, value, label):
    data = go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label,
        ),
        link=dict(
            source=source,  # indices correspond to labels
            target=target,
            value=value
        )
    )
    
    fig = go.Figure(data)
    return fig

# Streamlit app
st.title('Sankey Diagram Generator')

# User input for the Sankey diagram
with st.form("sankey_data"):
    input_csv = st.file_uploader("Upload a CSV file with source, target, value columns", type=['csv'])
    submit_button = st.form_submit_button("Generate Diagram")

if submit_button and input_csv:
    df = pd.read_csv(input_csv)
    if {'source', 'target', 'value'}.issubset(df.columns):
        unique_nodes = pd.concat([df['source'], df['target']]).unique()
        label_dict = {name: idx for idx, name in enumerate(unique_nodes)}
        source_indices = df['source'].map(label_dict)
        target_indices = df['target'].map(label_dict)
        
        fig = create_sankey(
            source=source_indices,
            target=target_indices,
            value=df['value'],
            label=list(label_dict.keys())
        )
        st.plotly_chart(fig)
    else:
        st.error("CSV must contain source, target, and value columns.")
else:
    st.write("Upload a CSV file to see the Sankey diagram.")