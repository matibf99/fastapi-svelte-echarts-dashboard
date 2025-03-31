import type {
	PieChartAPIResponse,
	BarPlotAPIResponse,
	PieChartDataPoint,
	BarChartData,
	APIResponse
} from '../types/types';

export class DataTransformer {
	static transformPieData(apiData: PieChartAPIResponse): PieChartDataPoint[] {
		if (apiData.labels.length !== apiData.values.length) {
			throw new Error('Labels and values length mismatch in pie chart data');
		}

		return apiData.labels.map((label, index) => ({
			name: label,
			value: apiData.values[index]
		}));
	}

	static transformBarData(apiData: BarPlotAPIResponse): BarChartData {
		if (apiData.categories.length !== apiData.values.length) {
			throw new Error('Categories and values length mismatch in bar chart data');
		}

		return {
			categories: apiData.categories,
			values: apiData.values
		};
	}

	static transformAPIResponse(apiData: APIResponse) {
		return {
			pieChartData: this.transformPieData(apiData.piechart),
			barChartData: this.transformBarData(apiData.barplot)
		};
	}
}
