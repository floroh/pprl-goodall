from typing import List, Dict

import jellyfish
import streamlit as st
import pprl_linkage_unit_service_api_client as lu
import pprl_data_owner_service_api_client as do
from pprl_data_owner_service_api_client import RecordDto

from goodall.api_helper import do_api

from goodall.protocol.clerical_review.pair_display import format_bitset_as_bitstring, \
    PairDisplay


def subsubheader(subsubheader_text: str, style: str = 'Default'):
    css_style = "font-size: 18px;"
    if style == 'Underline':
        css_style += "text-decoration: underline; text-underline-offset: 5px; text-decoration-thickness: 2px;"
        css_style += "margin-top: 10px; margin-bottom: 10px;"
    st.markdown(f"""<div style='{css_style}'>{subsubheader_text}</div>""", unsafe_allow_html=True)

def calculate_similarity(str1, str2, method="jaro-winkler"):
    if method == "jaro-winkler":
        return jellyfish.jaro_winkler_similarity(str1, str2)
    elif method == "edit-distance":
        return 1 - (jellyfish.levenshtein_distance(str1, str2) / max(len(str1),
                                                                     len(str2)))
    elif method == "binary-dice":
        bitstring1 = format_bitset_as_bitstring(str1)
        bitstring2 = format_bitset_as_bitstring(str2)
        intersection = sum(
            1 for b1, b2 in zip(bitstring1, bitstring2) if b1 == '1' and b2 == '1')
        denominator = bitstring1.count('1') + bitstring2.count('1')
        if denominator == 0:
            return 1.0
        dice_similarity = (2 * intersection) / denominator
        return dice_similarity

    else:
        raise ValueError(f"Unknown method: {method}")


def render_edit_form(input_pair: List[Dict[str, str]]) -> List[Dict[str, str]]:
    # Assuming input_pair is a list of dictionaries with attribute names as keys
    updated_input_pair = []

    for idx, record_data in enumerate(input_pair):
        record_data = {key: value for key, value in record_data.items() if
                           "FRQ" not in key}

        columns = st.columns(
            len(record_data))  # Create as many columns as there are attributes
        updated_record = {}

        for i, (attribute, value) in enumerate(record_data.items()):
            if "FRQ" in attribute:
                continue
            updated_value = columns[i].text_input(label=attribute,
                                                  value=value,
                                                  key=f"{attribute}_{idx}",
                                                  label_visibility="visible" if idx == 0 else "collapsed"
                                                  )
            updated_record[attribute] = updated_value

        updated_input_pair.append(updated_record)

    if st.button("Update"):
        return updated_input_pair  # Return the updated pair

    return input_pair  # Return the original pair if not submitte


def render_multi_layer_comparison_example(
        input_pair: List[Dict[str, str]] | None = None,
        gt_label: str | None = None,
        show_encodings: bool = False) -> List[Dict[str, str]]:
    if input_pair is None:
        if gt_label is None or gt_label == "TRUE_MATCH":
            input_pair = get_example_true_match_pair()
            gt_label = "TRUE_NON_MATCH"
        else:
            input_pair = get_example_true_non_match_pair()
            gt_label = "TRUE_MATCH"
    if gt_label is None:
        gt_label = "TRUE_MATCH"
    gt_labels = [gt_label]
    with st.expander("Edit records"):
        input_pair = render_edit_form(input_pair)

    records = []
    for idx, record_data in enumerate(input_pair):
        record_id = f"u{idx + 1}"  # Create unique IDs for records
        attributes = {
            key: lu.AttributeDto(type="STRING", value=value)
            for key, value in record_data.items()
        }
        record = lu.RecordDto(
            id=lu.RecordIdDto(unique=record_id),
            attributes=attributes
        )
        records.append(record)

    attribute_similarities = calculate_attribute_similarities(records)
    pair = lu.RecordPairDto(
        id0=records[0].id,
        id1=records[1].id,
        tags=[lu.Tag(tag="Groundtruth-Label", string_value=gt_labels[0])],
        attribute_similarities=attribute_similarities
    )
    pairs = [pair]

    options = ["Plaintext", "Record-level comparison", "Attribute-level comparison",
               "Masked Clerical review"]
    pair_display_modes = st.segmented_control("Select comparison mode", options,
                                              default=options[0],
                                              # selection_mode="multi"
                                              selection_mode="single"
                                              )
    if pair_display_modes is None:
        pair_display_modes = []
    # pair_display_modes = options[1:]
    # st.json(pair)

    def render_display(display: PairDisplay,
                       attribute_order: List[str]|None = None,
                       hide_header: bool = False):
        if attribute_order is None:
            attribute_order = ["FIRSTNAME", "LASTNAME", "DATEOFBIRTH", "CITY"]
        display.attribute_order = attribute_order
        st.html(display.render_html(hide_header=hide_header)[0])

    do_record_dtos = [do.RecordDto.from_dict(record.to_dict()) for record in records]

    if options[0] in pair_display_modes:
        subsubheader("Plaintext records")
        render_display(PairDisplay(pairs, records, mask="none"))
        subsubheader("Plaintext similarities")
        render_display(PairDisplay([pair], records,
                                   mask="full",
                                   show_similarities=True,
                                   ))

    if options[1] in pair_display_modes:
        rbf_record_dtos = [do_api.encode(record, "DBSLeipzig/RBF/FNLNDOBCITY") for record in
                       do_record_dtos]
        rbf_display_name = "Record-level Bloom filter"
        for record in rbf_record_dtos:
            rbf_attribute = record.attributes.pop("RBF")
            record.attributes[rbf_display_name] = rbf_attribute
        pair = lu.RecordPairDto(
            id0=records[0].id,
            id1=records[1].id,
            tags=[lu.Tag(tag="Groundtruth-Label", string_value=gt_labels[0])],
            attribute_similarities=calculate_attribute_similarities(rbf_record_dtos,
                                                                  method="binary-dice")
        )
        if show_encodings:
            subsubheader("Record-level Bloom Filter encoding")
            render_display(PairDisplay(pairs, rbf_record_dtos,
                                       mask="none",
                                       cell_length=92,
                                       show_only_first_record=True,
                                       show_similarities=True,
                                       ),
                           attribute_order=[rbf_display_name])
        subsubheader("Similarity based on record-level encodings")
        render_display(PairDisplay([pair], records,
                                   mask="full",
                                   show_similarities=True,
                                   ),
                       attribute_order=[rbf_display_name],
                       hide_header=False)

    if options[2] in pair_display_modes:
        abf_record_dtos = [do_api.encode(record, "DBSLeipzig/FBF/FNLNDOBCITY") for record in
                       do_record_dtos]
        # st.json(abf_record_dtos)
        pair = lu.RecordPairDto(
            id0=records[0].id,
            id1=records[1].id,
            tags=[lu.Tag(tag="Groundtruth-Label", string_value=gt_labels[0])],
            attribute_similarities=calculate_attribute_similarities(abf_record_dtos,
                                                                  method="binary-dice")
        )
        # st.json(pair)

        if show_encodings:
            subsubheader("Attribute-level Bloom Filter encodings")
            render_display(PairDisplay([pair], abf_record_dtos,
                                       mask="none",
                                       cell_length=24,
                                       show_only_first_record=True,
                                       show_similarities=True,
                                       ))
        subsubheader("Similarities based on attribute-level encodings")
        render_display(
            PairDisplay([pair], records, mask="difference", show_similarities=True))

    if options[3] in pair_display_modes:
        subsubheader("Mask equal and very dissimilar attributes")
        render_display(PairDisplay(pairs, records, mask="minimal"))

        subsubheader("Mask equal, very dissimilar attributes, as well as equal characters")
        render_display(PairDisplay(pairs, records, mask="difference"))


        subsubheader("Mask also differing characters with placeholders")
        render_display(PairDisplay(pairs, records, mask="full"))

    return input_pair


def calculate_attribute_similarities(records: List[RecordDto], method="edit-distance"):
    attribute_similarities = {}
    for key in records[0].attributes.keys():
        value1 = records[0].attributes[key].value
        value2 = records[1].attributes[key].value
        similarity = calculate_similarity(value1, value2, method=method)
        attribute_similarities[key] = similarity
    return attribute_similarities


def get_example_true_match_pair():
    input_pair = [
        {
            "FIRSTNAME": "Peter",
            "FIRSTNAME_FRQLABEL": "1",
            "LASTNAME": "Cohen",
            "LASTNAME_FRQLABEL": "2",
            "DATEOFBIRTH": "07.09.1976",
            "CITY": "LELAND",
        },
        {
            "FIRSTNAME": "Peter",
            "FIRSTNAME_FRQLABEL": "1",
            "LASTNAME": "Cohen",
            "LASTNAME_FRQLABEL": "2",
            "DATEOFBIRTH": "07.09.1976",
            "CITY": "RALEIGH",
        }
    ]
    return input_pair


def get_example_true_non_match_pair():
    input_pair = [
        {
            "FIRSTNAME": "Paula",
            "LASTNAME": "Smith",
            "LASTNAME_FRQLABEL": "0",
            "DATEOFBIRTH": "07.09.1976",
            "CITY": "RALEIGH",
        },
        {
            "FIRSTNAME": "Paul",
            "LASTNAME": "Smith",
            "LASTNAME_FRQLABEL": "0",
            "DATEOFBIRTH": "07.06.1967",
            "CITY": "RALEIGH",
        }
    ]
    return input_pair