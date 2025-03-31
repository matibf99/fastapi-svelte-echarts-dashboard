from pydantic import BaseModel, ValidationInfo, field_validator


class PieChartData(BaseModel):
    labels: list[str]
    values: list[int]

    @field_validator("values")
    @classmethod
    def check_pie_lengths_match(cls, v: list[int], info: ValidationInfo) -> list[int]:
        if "labels" in info.data and len(v) != len(info.data["labels"]):
            raise ValueError("Number of labels must match number of values in piechart")
        return v


class BarPlotData(BaseModel):
    categories: list[str]
    values: list[int]

    @field_validator("values")
    @classmethod
    def check_bar_lengths_match(cls, v: list[int], info: ValidationInfo) -> list[int]:
        if "categories" in info.data and len(v) != len(info.data["categories"]):
            raise ValueError(
                "Number of categories must match number of values in barplot"
            )
        return v


class VisualizationData(BaseModel):
    piechart: PieChartData
    barplot: BarPlotData

    @classmethod
    def from_json(cls, json_data: dict):
        pie_data = PieChartData(
            labels=json_data["piechart"]["labels"],
            values=json_data["piechart"]["values"],
        )

        bar_data = BarPlotData(
            categories=json_data["barplot"]["categories"],
            values=json_data["barplot"]["values"],
        )

        return cls(piechart=pie_data, barplot=bar_data)
