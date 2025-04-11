import pandas as pd
from pandas import DataFrame


def grouped_figure(func, df: DataFrame, x_columns: list, y_col: str = None):
    rows = []
    for x_column in x_columns:
        for val in df[x_column].values:
            rows.append([val, x_column])
    grouped_df = pd.DataFrame(rows, columns=["x", "g"])
    return func(grouped_df, x="x", color="g")


def grouped_figure_x_y(func, df: DataFrame, x_col: str, y_columns: list):
    rows = []
    for y_column in y_columns:
        for index, row in df.iterrows():
            x_val = row[x_col]
            y_val = row[y_column]
            rows.append([x_val, y_val, y_column])
    grouped_df = pd.DataFrame(rows, columns=["x", "y", "g"])
    return func(grouped_df, x="x", y="y", color="g")
