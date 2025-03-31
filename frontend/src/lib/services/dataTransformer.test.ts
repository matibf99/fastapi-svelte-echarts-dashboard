import { describe, it, expect } from 'vitest';
import { DataTransformer } from './dataTransformer';
import type { APIResponse, PieChartDataPoint, BarChartData } from '../types/types';

describe('DataTransformer', () => {
	const mockApiResponse: APIResponse = {
		piechart: {
			labels: ['Producto A', 'Producto B', 'Producto C'],
			values: [30, 50, 20]
		},
		barplot: {
			categories: ['Enero', 'Febrero', 'Marzo'],
			values: [150, 200, 180]
		}
	};

	it('should transform pie chart data correctly', () => {
		const expectedPieData: PieChartDataPoint[] = [
			{ name: 'Producto A', value: 30 },
			{ name: 'Producto B', value: 50 },
			{ name: 'Producto C', value: 20 }
		];
		const transformed = DataTransformer.transformPieData(mockApiResponse.piechart);
		expect(transformed).toEqual(expectedPieData);
	});

	it('should throw error if pie chart labels and values mismatch', () => {
		const invalidPieApi = { labels: ['A'], values: [10, 20] };
		expect(() => DataTransformer.transformPieData(invalidPieApi)).toThrow(
			'Labels and values length mismatch in pie chart data'
		);
	});

	it('should transform bar chart data correctly', () => {
		const expectedBarData: BarChartData = {
			categories: ['Enero', 'Febrero', 'Marzo'],
			values: [150, 200, 180]
		};
		const transformed = DataTransformer.transformBarData(mockApiResponse.barplot);
		expect(transformed).toEqual(expectedBarData);
	});

	it('should throw error if bar chart categories and values mismatch', () => {
		const invalidBarApi = { categories: ['Jan'], values: [100, 120] };
		expect(() => DataTransformer.transformBarData(invalidBarApi)).toThrow(
			'Categories and values length mismatch in bar chart data'
		);
	});

	it('should transform the full API response correctly', () => {
		const transformed = DataTransformer.transformAPIResponse(mockApiResponse);
		expect(transformed).toHaveProperty('pieChartData');
		expect(transformed).toHaveProperty('barChartData');
		expect(transformed.pieChartData).toHaveLength(3);
		expect(transformed.barChartData.categories).toHaveLength(3);
		expect(transformed.pieChartData[0]).toEqual({ name: 'Producto A', value: 30 });
		expect(transformed.barChartData.values[1]).toBe(200);
	});
});
