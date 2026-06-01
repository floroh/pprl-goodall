import pandas as pd

from goodall.api_helper.common_api import get_tags_as_dataframe

import streamlit as st

from goodall.api_helper.pprl_clients import Service
from goodall.ui.components.tag_analyzer import TagAnalyzer


class DatasetTagAnalyzer(TagAnalyzer):
    def __init__(self,
                 dataset_id: int,
                 df_tags: pd.DataFrame | None = None,
                 service: Service = Service.Data_owner_1):
        super().__init__(df_tags)
        self.dataset_id = dataset_id
        self.service = service

    @staticmethod
    def get_df_tags(service: Service, dataset_id: int) -> pd.DataFrame:
        df_tags = get_tags_as_dataframe(
            service=service,
            dataset_id=dataset_id
        )
        df_tags = df_tags[
            df_tags["tag"] != "..."
        ]  # Workaround, TODO Find cause of this row

        return df_tags

    def get_tag_dataframe(self) -> pd.DataFrame:
        if self.df_tags is None:
            self.df_tags = self.get_df_tags(self.service, self.dataset_id)
        return self.df_tags

    def analyze(self):
        super().analyze()

        st.text("the end...")
