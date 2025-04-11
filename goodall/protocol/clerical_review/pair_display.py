import re

from pprl_linkage_unit_service_api_client import RecordPairDto, RecordDto
from pydantic import BaseModel

from goodall.protocol.clerical_review.mask import Mask, create_mask, BaselineMask
from goodall.ui.PPRL_Services_UI import ATTRIBUTE_ORDER, ATTRIBUTES_FOR_DISPLAY

SYMBOL_UNEQUAL = "❌"
# SYMBOL_EQUAL = "✔️"
SYMBOL_EQUAL = "&#x2705;"

FREQUENCY_LABELS = [
    ("🔴", "Very Frequent"),  # 0
    ("🟠", "Frequent"),  # 1
    ("🟡", "Average"),  # 2
    ("🟢", "Rare"),  # 3
    ("🔵", "Very Rare")  # 4
]


class PairDescription(BaseModel):
    attributes0: dict[str, str]
    attributes1: dict[str, str]
    attribute_types: dict[str, str]
    attribute_similarities: dict[str, float]
    gt_label: str


def format_bitset_as_bitstring(bitset_base64: str) -> str:
    """
    Convert a BITSET_BASE64 string to a bitstring and format it as blocks of 32 characters.
    :param bitset_base64: The base64 encoded bitset string.
    :rtype: str
    """
    import base64
    import binascii

    if not bitset_base64:
        return ""

    try:
        decoded_bytes = base64.b64decode(bitset_base64)
        bitstring = "".join(f"{byte:08b}" for byte in decoded_bytes)
        # bitstring = bitstring[:512]
        return f"{bitstring}"
    except (binascii.Error, ValueError):
        return "Invalid BITSET_BASE64"


class PairDisplay:
    def __init__(self,
                 pairs: list[RecordPairDto],
                 records: list[RecordDto],
                 mask: Mask | str = None,
                 show_only_first_record: bool = False,
                 cell_length: int = 100,
                 show_similarities: bool = False,
                 show_values_as_popup: bool = False,
                 ):
        self.pairs = pairs
        self.records = records
        if isinstance(mask, str):
            mask = create_mask(mask)
        self.mask = mask
        self.attribute_order = ATTRIBUTES_FOR_DISPLAY
        self.show_only_first_record = show_only_first_record
        self.pair_descriptions = self.build_pair_descriptions()
        self.cell_length = cell_length
        self.show_similarities = show_similarities
        self.show_values_as_popup = show_values_as_popup

    def build_pair_descriptions(self) -> list[PairDescription]:
        records_by_id = {}
        for record in self.records:
            records_by_id[record.id.unique] = record

        pair_descriptions = []
        for pair in self.pairs:
            pair_description = PairDescription(
                attributes0={},
                attributes1={},
                attribute_types={},
                attribute_similarities={},
                gt_label="",
            )
            for tag in pair.tags:
                if tag.tag == "Groundtruth-Label":
                    pair_description.gt_label = tag.string_value
            attributes0 = records_by_id[pair.id0.unique].attributes
            attributes1 = records_by_id[pair.id1.unique].attributes
            for name, value in attributes0.items():
                pair_description.attribute_types[name] = value.type
                pair_description.attributes0[name] = value.value
                if name in attributes1.keys():
                    pair_description.attributes1[name] = attributes1[name].value
            pair_description.attribute_similarities = pair.attribute_similarities
            pair_descriptions.append(pair_description)
        return pair_descriptions

    def render_html(self, table_width: int = 900, hide_header: bool = False) -> list[str]:
        """
        Render the record pairs as individual html tables with attributes as columns sorted by the given order.
        If the attribute type is BITSET_BASE64, convert the attribute value to a bitstring and print it as a block of 32 char width.
        :rtype: list[str]
        """
        html_tables = []

        # Inline CSS for table styling
        style = self.get_css_style_element(table_width)

        for pair_descr in self.pair_descriptions:
            table_html = style + "<table class='pair-table'>"
            if not hide_header:
                table_html += "<thead><tr>"

                # Add header row with attributes
                for attribute in self.attribute_order:
                    table_html += f"<th>{attribute}</th>"
                table_html += "</tr></thead>"
            table_html += "<tbody>"

            first_row = "<tr>"
            second_row = "<tr>"
            for attribute in self.attribute_order:
                multiline_content = None
                background_color = "transparent"
                display_class = ""
                # if self.mask is not None and not type(self.mask) is BaselineMask:
                if self.mask is not None:
                    similarity = pair_descr.attribute_similarities.get(attribute,
                                                                       None)
                    if similarity is not None:
                        if self.show_similarities:
                            multiline_content = round(similarity, 2)
                        else:
                            if similarity == 1:
                                multiline_content = SYMBOL_EQUAL
                                frq_label = pair_descr.attributes0.get(
                                    attribute + "_FRQLABEL")
                                if frq_label is not None:
                                    multiline_content = f"{self.get_frequency_label(frq_label)}"
                            elif similarity < 0.4:
                                # multiline_content = SYMBOL_UNEQUAL + f" {round(similarity, 2)}"
                                multiline_content = SYMBOL_UNEQUAL
                        if similarity == 1:
                            # background_color = "green"
                            display_class = "equal"
                        elif similarity < 0.4:
                            # background_color = "red"
                            display_class = "unequal"
                if multiline_content is not None and not type(self.mask) is BaselineMask:
                    first_row += f"<td class='merged align-center {display_class}' rowspan='2'>{multiline_content}</td>"
                else:
                    value0 = pair_descr.attributes0.get(attribute, "")
                    value1 = pair_descr.attributes1.get(attribute, "")
                    if pair_descr.attribute_types.get(attribute, "") == "BITSET_BASE64":
                        value0 = format_bitset_as_bitstring(value0)
                        value1 = format_bitset_as_bitstring(value1)
                    if len(value0) == len(value1) == 0:
                        if multiline_content is None:
                            multiline_content = "❓"
                        first_row += f"<td class='merged align-center  {display_class}' rowspan='2'>{multiline_content}</td>"
                    else:
                        if self.mask is not None:
                            self.mask.html = True
                            value0, value1, _ = self.mask.apply(value0, value1)
                            value0 = self.add_br_every_n_bits(value0)
                            value1 = self.add_br_every_n_bits(value1)
                        first_row += f"<td class='{display_class}' >{value0}</td>"
                        second_row += f"<td class='{display_class}' >{value1}</td>"
            first_row += "</tr>"
            second_row += "</tr>"

            table_html += first_row
            if not self.show_only_first_record:
                table_html += second_row
            table_html += "</tbody></table>"

            html_tables.append(table_html)

        return html_tables

    def add_br_every_n_bits(self, html):
        # TODO Fix breaks being off by 1 positions sometimes
        # Pattern to match spans
        span_pattern = r'<span(.*?)>(.*?)</span>'

        # Find all spans
        spans = re.findall(span_pattern, html)

        result = []  # List to store the reconstructed HTML
        current_row_length = 0  # Tracks the current row length
        current_row = []  # Tracks spans in the current row

        for attrs, content in spans:
            while content:  # Continue until all content in the span is handled
                remaining_space = self.cell_length - current_row_length

                if len(content) > remaining_space:  # Content exceeds the row length
                    # Take only the part that fits
                    current_row.append((attrs, content[:remaining_space]))
                    result.append(current_row)
                    result.append('<br />')  # Add a line break
                    content = content[remaining_space:]  # Remaining content
                    current_row = []  # Start a new row
                    current_row_length = 0
                else:
                    # Entire content fits in the current row
                    current_row.append((attrs, content))
                    current_row_length += len(content)
                    content = ""  # No remaining content

            # Add an empty span if no content, to preserve structure
            if not content and not attrs.strip():
                current_row.append((attrs, ""))

        # Add the final row to the result
        if current_row:
            result.append(current_row)

        # Rebuild the HTML from rows
        rebuilt_html = ""
        for row in result:
            if row == '<br />':
                rebuilt_html += row
            else:
                for attrs, content in row:
                    rebuilt_html += f'<span{attrs}>{content}</span>'

        return rebuilt_html

    def get_frequency_label(self, category: str) -> str:
        """
        Returns a string with a colored dot and text describing the frequency category
        based on the input category index (0 to 4).
        """
        category = int(category)
        # Validate the input category
        if not (0 <= category < len(FREQUENCY_LABELS)):
            raise ValueError("Invalid category. Must be an integer between 0 and 4.")

        # Return the emoji and label as a string
        emoji, label = FREQUENCY_LABELS[category]
        return f"{emoji} {label}"

    def get_css_style_element(self, table_width: int):
        return f"""
        <style>
            table.pair-table {{
                width: {table_width}px;
                border-collapse: collapse;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }}
            .pair-table th, .pair-table td {{
                padding: 8px 12px;
                border: 1px solid #aaa;
                vertical-align: middle; /* Center vertically */
            }}
            .pair-table th {{
                background-color: #eee;
            }}
            .pair-table td {{
                word-wrap: break-word;
                width: 100px;
            }}
            .pair-table td.align-center {{
                text-align: center; /* Center horizontally */
            }}
            .pair-table p {{
                font-family: Arial, sans-serif;
                font-size: 14px;
                margin: 10px 0;
            }}
            .pair-table strong {{
                color: #333;
            }}
            .pair-table .text-diff {{
                background-color: #f66;
            }}
            .pair-table .text-transpose {{
                background-color: #f33;
            }}
            .pair-table .equal {{
                background-color: #ccff99;
            }}
            .pair-table .unequal {{
                background-color: #ff9999;
            }}
        </style>
        """
