import pandas as pd
from pprl_protocol_manager_service_api_client import (
    ProtocolAnalysisRequestDto,
    MultiLayerProtocol,
)

from goodall.api_helper.parser import parse_serialized_table_to_dataframe
from goodall.api_helper.pm_api import protocol_analyzer_controller

from goodall.ui.components.api import lu_api_streamlit
from goodall.ui.components.protocol_tag_analyzer import ProtocolTagAnalyzer


class ProtocolTagFromServicesAnalyzer(ProtocolTagAnalyzer):
    def __init__(self, protocol: MultiLayerProtocol,
                 df_tags: pd.DataFrame | None = None):
        super().__init__(df_tags=df_tags)
        self.protocol = protocol

    @staticmethod
    def get_df_tags(protocol_id: str) -> pd.DataFrame:
        tagtable = protocol_analyzer_controller.get_tags_from_protocol_as_table(
            ProtocolAnalysisRequestDto(protocolId=protocol_id)
        )
        df_tags = parse_serialized_table_to_dataframe(tagtable)
        df_tags = df_tags[
            df_tags["tag"] != "..."
        ]  # Workaround, TODO Find cause of this row
        return df_tags

    def get_tag_dataframe(self) -> pd.DataFrame:
        if self.df_tags is None:
            self.df_tags = self.get_df_tags(self.protocol.protocol_id)
        return self.df_tags

    def get_record_pairs(self) -> pd.DataFrame:
        df_pairs = lu_api_streamlit.get_record_pairs_as_dataframe_cached(
            self.protocol.layers[0].project_id, []
        )
        return df_pairs