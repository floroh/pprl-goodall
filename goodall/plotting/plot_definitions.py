from goodall.plotting.quality_history_plotter import PlotDefinition, DataToShow


def get_plot_definition(name: str) -> PlotDefinition:
    plot_definition = PlotDefinition()
    if name == "fig3_left":
        plot_definition.plot_mode = DataToShow.ERROR
        plot_definition.name_color = "err"
        plot_definition.name_symbol = "b"
        plot_definition.legend_title = "(err, b)"
        plot_definition.filter_budget = 100
        plot_definition.filter_dataset_ids = [2032]
        plot_definition.file_name = "2032-error.pdf"
    return plot_definition

def get_plot_definition_by_mode(plot_mode: DataToShow) -> PlotDefinition:
    pdef = PlotDefinition()
    pdef.plot_mode = plot_mode
    match plot_mode:
        case DataToShow.ERROR:
            pdef.name_color = "err"
            pdef.name_symbol = "b"
            pdef.reverse_colors = True
            pdef.legend_title = "(err, b)"
        case DataToShow.BUDGET:
            pdef.name_color = "b"
            pdef.name_symbol = "err"
            pdef.legend_title = "(err, b)"
        case DataToShow.BUDGET_THRESHOLD:
            pdef.name_color = "b"
            pdef.name_symbol = "rbfInitThreshold"
            pdef.legend_title = "(b, thr)"
        case DataToShow.THRESHOLD:
            pdef.name_symbol = None
            pdef.name_color = "rbfInitThreshold"
            pdef.legend_title = "(thr)"
        case DataToShow.BUDGET_DATASET:
            pdef.name_color = "plaintextDatasetId"
            pdef.name_symbol = "b"
            pdef.legend_title = "(Dataset, b)"
            pdef.legend_width = 300
    return pdef