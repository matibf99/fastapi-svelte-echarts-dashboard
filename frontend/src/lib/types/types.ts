// Types for the API
export type PieChartAPIResponse = {
	labels: string[];
	values: number[];
};

export type BarPlotAPIResponse = {
	categories: string[];
	values: number[];
};

export type APIResponse = {
	piechart: PieChartAPIResponse;
	barplot: BarPlotAPIResponse;
};

// Types for components
export type PieChartDataPoint = {
	name: string;
	value: number;
};

export type BarChartData = {
	categories: string[];
	values: number[];
};

// Types for component's props
export type PieChartProps = {
	data: PieChartDataPoint[];
	title?: string;
};

export type BarChartProps = {
	data: BarChartData;
	title?: string;
};
