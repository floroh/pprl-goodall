import pandas as pd
from pprl_protocol_manager_service_api_client import (
    MultiLayerProtocol,
    Layer,
    ProcessingStep,
)

import streamlit as st
from streamlit import session_state as sts

from goodall.modifier.record_pair_filter import filter_pairs
from goodall.result_analysis.pair_evaluation import combine_MatchGrade, combine_FP
from goodall.ui.components.api import lu_api_streamlit
from goodall.ui.constants import matchGradeWithOriginColorMap
from goodall.api_helper.parser import get_tag_value
from goodall.ui.components.projects import render_plot_histogram
from goodall.ui.components.protocol_helper import (
    get_current_classifier_threshold,
    update_classifier_threshold,
)


class RecordLevelLayerAdaptionRenderer:
    def __init__(self, protocol: MultiLayerProtocol):
        self.protocol = protocol

    def get_layer_with_name(self, name: str):
        for layer in self.protocol.layers:
            if layer.name == name:
                return layer

    @staticmethod
    def get_pairs(layer: Layer):
        if "pairs" in sts:
            pairs = sts["pairs"]
        else:
            pairs = lu_api_streamlit.get_record_pairs_cached(layer.project_id, ["new"])
            sts["pairs"] = pairs
        return pairs

    def get_layer_of_project_id(self, project_id: str):
        for layer in self.protocol.layers:
            if layer.project_id == project_id:
                return layer

    def render_threshold_adaption(self) -> bool:
        new_threshold = self.render_threshold_selection()
        btn_update_threshold = st.button("Update threshold and reclassify")
        if btn_update_threshold:
            layer = self.get_layer_with_name("RBF")
            update_classifier_threshold(layer, new_threshold)
            if (
                self.protocol.step_queue is not None
                and len(self.protocol.step_queue) > 0
            ):
                next_step = self.protocol.step_queue.pop()
                if next_step.type != "UPDATE_MATCHER":
                    reclassification_step = ProcessingStep(
                        type="RECLASSIFY_PAIRS",
                        properties={
                            "projectId": layer.project_id,
                        },
                    )
                    self.protocol.step_queue.clear()
                    self.protocol.step_queue.append(reclassification_step)
                    self.protocol.step_history.append(
                        ProcessingStep(
                            type="UPDATE_MATCHER",
                            properties={
                                "projectId": layer.project_id,
                                "method": "external",
                                "matcher.rbf.threshold": f"{new_threshold:.2f}",
                            },
                        )
                    )
                else:
                    next_step.properties["method"] = "external"
                    next_step.properties["matcher.rbf.threshold"] = (
                        f"{new_threshold:.2f}"
                    )
                    self.protocol.step_queue.append(next_step)
            return True
        return False

    def render_threshold_selection(self):
        layer = self.get_layer_with_name("RBF")
        # lu_api.get_record_pairs.clear()  # Clear cached pairs from previous iteration
        df_record_pairs = lu_api_streamlit.get_record_pairs_as_dataframe_cached(
            layer.project_id, []
        )
        df_record_pairs = combine_FP(df_record_pairs)
        df_record_pairs = combine_MatchGrade(df_record_pairs)
        sts["barmode"] = "stack"
        options = ["RBF", "ABF", "CR"]
        included_layers = st.pills(
            label="Show pair similarities from layer",
            options=options,
            default=options,
            selection_mode="multi",
        )
        df_record_pairs["review_method"] = df_record_pairs["tags"].apply(
            lambda tags: get_tag_value(tags, "MATCHING_METHOD", False)
        )

        def update_properties(row):
            props = row.get("properties", [])
            if not isinstance(props, list):
                props = []
            if row["review_method"] is None:
                props.append("RBF")
            elif "ABF" in row["review_method"]:
                props.append("ABF")
            elif "CR" in row["review_method"]:
                props.append("CR")
            return list(set(props))  # remove duplicates

        def append_origin_to_match_grade(df: pd.DataFrame) -> pd.DataFrame:
            def append_origin(row):
                origins = [
                    o
                    for o in ["ABF", "CR", "RBF"]
                    if o
                    in (
                        row["properties"] if isinstance(row["properties"], list) else []
                    )
                ]
                if origins:
                    return f"{row['matchGrade']}_{'_'.join(origins)}"
                return row["matchGrade"]

            df["matchGrade"] = df.apply(append_origin, axis=1)
            return df

        df_record_pairs["properties"] = df_record_pairs.apply(update_properties, axis=1)
        df_record_pairs = filter_pairs(
            df_record_pairs, included_layers, [], match_all=False
        )
        append_origin_to_match_grade(df_record_pairs)
        # st.dataframe(df_record_pairs)
        # st.text(f"Length after filtering is {len(df_record_pairs)}")
        hist = render_plot_histogram(
            df_record_pairs,
            x_col="similarity",
            color="matchGrade",
            color_map=matchGradeWithOriginColorMap,
            render=False,
            x_min=0.6,
        )
        with st.container(border=True):
            current_threshold = get_current_classifier_threshold(layer)
            hist.add_vline(
                x=current_threshold, line=dict(color="Gray", width=2, dash="dot")
            )
            new_threshold = st.slider(
                label="Select threshold",
                min_value=0.6,
                max_value=1.0,
                value=current_threshold,
                step=0.01,
            )
            hist.add_vline(
                x=new_threshold, line=dict(color="blue", width=3, dash="dash")
            )
            hist.update_layout(showlegend=False)
            hist.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=200,
            )
            hist.update_yaxes(
                title=None,
                showticklabels=False,
            )
            st.plotly_chart(hist)
        return new_threshold
