from random import random

import streamlit as st
from pprl_protocol_manager_service_api_client import MultiLayerProtocol, Layer
from streamlit import session_state as sts

from goodall.api_helper import lu_api
from goodall.protocol.clerical_review.mask import MASKS
from goodall.protocol.clerical_review.pair_display import PairDisplay
from goodall.ui.components.protocols import rename_attributes, clean_labeling_states
from goodall.ui.streamlit_utils import get_state_or_default


class ClericalReviewRenderer:

    def __init__(self, protocol: MultiLayerProtocol):
        self.protocol = protocol

    def get_layer_with_name(self, name: str):
        for layer in self.protocol.layers:
            if layer.name == name:
                return layer

    def render_clerical_review(self) -> bool:
        layer = self.get_layer_with_name("PPCR")
        lu_api.get_record_pairs.clear()  # Clear cached pairs from previous iteration
        pairs = self.get_new_pairs(layer)
        records = self.get_records(pairs)
        labelings = self.get_labels(pairs)

        rename_attributes({"PLZ": "ZIP"}, records, pairs)
        mask_name = st.selectbox("Masking", MASKS.keys(), index=2)
        pair_displays = []
        for pair in pairs:
            pair_displays.append(PairDisplay([pair], records, mask=mask_name))

        if get_state_or_default("view_mode", "Simple") == "Expert":
            with st.expander("Full"):
                st.json(pairs)
                st.dataframe(
                    lu_api.get_record_pairs_as_dataframe(layer.project_id, ["new"]))

        labelings = self.show_autofill_labels_options(pair_displays, labelings)
        # st.text(get_state_or_default("knowledge_mode", "Simple"))
        show_labeling_feedback = False
        if get_state_or_default("knowledge_mode", "Simple") == "Evaluation":
            show_labeling_feedback = st.sidebar.toggle("Show correctness", value=True)
        self.render_pair_displays(pair_displays, labelings, show_labeling_feedback)

        if show_labeling_feedback:
            self.render_labeling_quality_summary(pair_displays, labelings)
        return self.submit_clerical_review_labels(labelings, pairs)

    def render_labeling_quality_summary(self,
                                        pair_displays: list[PairDisplay],
                                        labelings: list[int]
                                        ):
        correct_counter = 0
        completed = len(labelings) - labelings.count(None)
        if completed > 0:
            for idx, label in enumerate(labelings):
                if label is None:
                    continue
                gt = pair_displays[idx].pair_descriptions[0].gt_label
                sel_string = "TRUE_MATCH" if label == 1 else "TRUE_NON_MATCH"
                if gt is not None and gt == sel_string:
                    correct_counter += 1
            st.info(
                f"{correct_counter}/{completed} ({int(100 * correct_counter / completed)}%) are correct")

    def get_labels(self, pairs):
        if "manual_pair_labelings" in sts:
            labelings = sts["manual_pair_labelings"]
        else:
            labelings = [None] * len(pairs)
            sts["manual_pair_labelings"] = labelings
        return labelings

    def get_records(self, pairs):
        if "records" in sts:
            records = sts["records"]
        else:
            rids = []
            for pair in pairs:
                rids = rids + [pair.id0.unique, pair.id1.unique]
            records = lu_api.get_records_by_unique_id(rids)
            sts["records"] = records
        return records

    @staticmethod
    def get_new_pairs(layer: Layer):
        if "pairs" in sts:
            pairs = sts["pairs"]
        else:
            pairs = lu_api.get_record_pairs(layer.project_id, ["new"])
            sts["pairs"] = pairs
        return pairs

    def render_pair_displays(self,
                             pair_displays: list[PairDisplay],
                             labelings: list[int],
                             show_correctness: bool = False):
        for pair_idx, pair_display in enumerate(pair_displays):
            col_disp, col_sel, col_feedback = st.columns([5, 1, 1])
            with col_disp:
                # pair_display.show_similarities = True
                st.html(pair_display.render_html()[0])
            with col_sel:
                options = ["Non-Match", "Match"]
                if labelings[pair_idx] is None:
                    previous_selection = None
                else:
                    previous_selection = options[labelings[pair_idx]]
                st.markdown("""<div style='height=100px'></div>""", unsafe_allow_html=True)
                new_selection = st.segmented_control("Is a match?", options,
                                                     default=previous_selection,
                                                     selection_mode='single',
                                                     key="label" + str(pair_idx),
                                                     # on_change=store_manual_labeling
                                                     )
                labelings[pair_idx] = options.index(
                    new_selection) if new_selection is not None else None
                sts["manual_pair_labelings"] = labelings
            with col_feedback:
                if show_correctness and new_selection is not None:
                    gt = pair_display.pair_descriptions[0].gt_label
                    sel_string = "TRUE_MATCH" if new_selection == options[
                        1] else "TRUE_NON_MATCH"

                    st.markdown("""<div height='100px'></div>""", unsafe_allow_html=True)
                    if gt == sel_string:
                        st.success("Correct")
                    else:
                        st.error("Incorrect")

    def submit_clerical_review_labels(self, labelings, pairs) -> bool:
        btn_submit_clerical_review = st.button("Submit labeled pairs")
        if btn_submit_clerical_review:
            if None in labelings:
                st.error("Missing labels, please complete review first.")
            else:
                # st.text(labelings)
                for i, pair in enumerate(pairs):
                    label = labelings[i]
                    pair.match_grade = "CERTAIN_MATCH" if label == 1 else "NON_MATCH"
                    pair.properties = [p for p in pair.properties if p != "new"]
                    pair.tags = None
                    pair.attribute_similarities = None
                    pair.id0.unique = None
                    pair.id1.unique = None
                # st.json(pairs)
                lu_api.update_record_pairs(pairs)
                review_step = self.protocol.step_queue.pop()
                review_step.properties["method"] = "external"
                self.protocol.step_history.append(review_step)
                clean_labeling_states()
                return True
        return False

    def show_autofill_labels_options(self, pair_displays: list[PairDisplay],
                                     labelings: list[int]):
        with st.expander("Autolabel configuration"):
            autofill_mode = st.segmented_control("Autolabel mode",
                                                 ["Match rate", "Error rate"],
                                                 selection_mode="single",
                                                 default="Error rate")
            if autofill_mode == "Match rate":
                match_rate = st.slider(label="Match rate", min_value=0.0,
                                       max_value=1.0, value=0.5, step=0.05)
            elif autofill_mode == "Error rate":
                sel_error_rate = st.slider(label="Error rate", min_value=0.0,
                                           max_value=1.0, value=0.1, step=0.05)
        btn_auto_fill = st.button("Autolabel remaining pairs")
        if btn_auto_fill:
            def replace_randomly(value):
                if value is None:
                    return 1 if random() < match_rate else 0
                return value  # Keep the original value

            def label_based_on_error_rate(value, row_number):
                if value is None:
                    gt_label = pair_displays[row_number].pair_descriptions[0].gt_label
                    gt_label_display = 1 if gt_label == "TRUE_MATCH" else 0
                    inverse_gt_label_display = 0 if gt_label == "TRUE_MATCH" else 1
                    return inverse_gt_label_display if random() < sel_error_rate else gt_label_display
                return value  # Keep the original value

            if autofill_mode == "Match rate":
                labelings = [replace_randomly(label) for label in labelings]
            elif autofill_mode == "Error rate":
                labelings = [label_based_on_error_rate(label, idx) for idx, label in
                             enumerate(labelings)]
            else:
                st.error("Unknown autofill mode")
        return labelings
