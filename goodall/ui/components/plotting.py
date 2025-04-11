import io

import pandas as pd
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.colors as pc
import streamlit as st
from pprl_linkage_unit_service_api_client import BatchMatchProjectDto

from goodall.api_helper.parser import parse_serialized_table_to_dataframe, \
    remove_weighted_columns
from goodall.ui.streamlit_utils import get_state_or_default, state_exists_and_equals

PLOT_HEIGHT = "plot_height"
PLOT_WIDTH = "plot_width"
PLOT_RESIZE = "plot_resize"


def add_plot_size_sidebar():
    # st.session_state[PLOT_RESIZE] = st.sidebar.checkbox(label="Plot resize", key="plotresize")
    st.session_state[PLOT_WIDTH] = st.sidebar.number_input(
        label="Plot width", key="plotwidth", min_value=30, max_value=1000, value=600
    )
    st.session_state[PLOT_HEIGHT] = st.sidebar.number_input(
        label="Plot height", key="plotheight", min_value=30, max_value=1000, value=500
    )


def add_plotly_chart_with_download_button(fig_orig: Figure):
    # uid = str(uuid.uuid4())
    uid = str(hash(fig_orig.to_json()))
    # ui =
    # if adapt_plot:
    # fig = copy.deepcopy(fig_orig)
    fig = fig_orig
    if get_state_or_default("mode.dev", False):
        if st.checkbox(label="Plot resize", key="plotresize" + uid):
            fig.update_layout(
                width=st.session_state[PLOT_WIDTH], height=st.session_state[PLOT_HEIGHT]
            )
            st.plotly_chart(fig)
            # Create an in-memory buffer
            buffer = io.BytesIO()
            # Save the figure as a pdf to the buffer
            fig.write_image(file=buffer, format="pdf")
            # Download the pdf from the buffer
            st.download_button(
                label="Download PDF",
                data=buffer,
                file_name="figure.pdf",
                mime="application/pdf",
                key="download" + uid,
            )
            return
    st.plotly_chart(fig, use_container_width=True)


def plot_gini(df: pd.DataFrame, y_limit: float = None, width: int = 600,
              title="Gini Index by Attribute-level Bloom Filter") -> Figure:
    if "type" in df.columns:
        df.loc[df['type'] == 'origin', 'type'] = 'Multi-layer comparison'
        df.loc[df['type'] == 'ref', 'type'] = 'Only attribute-level comparison'
    fig = px.bar(
        df,
        x="attribute",
        y="Gini",
        color="type" if "type" in df.columns else None,
        title=title,
        labels={"Gini": "Gini", "attribute": "Attribute"},
        barmode="group",
        height=300,
        width=width
    )
    if y_limit is not None:
        fig.update_yaxes(range=[0, y_limit])
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),  # Compact margins
        xaxis=dict(tickangle=-45, title=""),
        yaxis=dict(title=""),
        # showlegend=False  # Remove legend (not needed for a bar chart)
    )
    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal layout
            yanchor="bottom",  # Align to bottom
            y=-0.9,  # Position below the plot
            xanchor="center",  # Center align
            x=0.5,  # Center horizontally
            title_text=None,
        )
    )
    return fig

def plot_availability(df: pd.DataFrame) -> Figure:
    if "type" in df.columns:
        df.loc[df['type'] == 'origin', 'type'] = 'Multi-layer comparison'
        df.loc[df['type'] == 'ref', 'type'] = 'Without attribute-level comparison'
    fig = px.bar(
        df,
        x="attribute",
        y="valid",
        color="type" if "type" in df.columns else None,
        title="Attribute availability",
        labels={"valid": "Availability", "attribute": "Attribute"},
        barmode="group",
        height=300,  # Compact height
        width=600  # Compact width
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),  # Compact margins
        xaxis=dict(tickangle=-45, title=""),
        yaxis=dict(title=""),
        # showlegend=False  # Remove legend (not needed for a bar chart)
    )
    fig.update_layout(
        legend=dict(
            orientation="h",  # Horizontal layout
            yanchor="bottom",  # Align to bottom
            y=-0.9,  # Position below the plot
            xanchor="center",  # Center align
            x=0.5,  # Center horizontally
            title_text=None,
        )
    )
    return fig


def render_quality_development(prj: BatchMatchProjectDto):
    if "CLASSIFICATION" in prj.phases:
        phase = prj.phases["CLASSIFICATION"]
        if state_exists_and_equals("knowledge_mode", "Evaluation"):
            report = \
                phase.report_groups["Linkage quality evaluation"].reports[
                    "Improved links history"]
            if report.type == "TEXT":
                st.text(report.report)
            elif report.type == "TABLE":
                df_report = parse_serialized_table_to_dataframe(
                    report.table
                )
                x_column_name = "Number of reviews"
                df_report.rename(columns={"#Improved": x_column_name}, inplace=True)
                df = df_report[df_report[x_column_name] >= 0]
                df = remove_weighted_columns(df)

                color_map = pc.qualitative.Set1  # Use a predefined colormap
                line_colors = {"recall": color_map[0], "precision": color_map[1],
                               "F1-score": color_map[2]}
                quality_history = px.line(
                    df, x=x_column_name, y=["recall", "precision", "F1-score"],
                    markers=True,
                    color_discrete_map=line_colors
                )

                quality_history.update_layout(height=300)
                # quality_history.update_layout(showlegend=False)
                quality_history.update_layout(
                    legend=dict(
                        orientation="h",  # Horizontal layout
                        yanchor="bottom",  # Align to bottom
                        y=-0.3,  # Position below the plot
                        xanchor="center",  # Center align
                        x=0.5,  # Center horizontally
                        title_text=None,
                    )
                )
                quality_history.update_xaxes(title_standoff=20,
                                             ticklabelposition="inside",
                                             ticklabelstandoff=10)
                quality_history.update_yaxes(title=None)
                st.plotly_chart(quality_history)
                # btn = st.checkbox("Show data",
                #                   key=f"is_not_rendered_as_table{report.name}")
                # if btn:
                #     st.dataframe(df,
                #                  use_container_width=True)
