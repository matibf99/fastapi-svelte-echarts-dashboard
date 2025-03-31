import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchChartData } from './api';
import { DataTransformer } from '../services/dataTransformer';
import type { APIResponse } from '../types/types';

// Mockear DataTransformer para aislar el test de fetch
vi.mock('../services/dataTransformer', () => ({
	DataTransformer: {
		transformAPIResponse: vi.fn((data) => ({
			// Devolvemos algo simple para verificar que se llamó
			pieChartData: [{ name: 'MockPie', value: 1 }],
			barChartData: { categories: ['MockBar'], values: [1] }
		}))
	}
}));

// Datos de ejemplo para la respuesta mock de fetch
const mockApiResponse: APIResponse = {
	piechart: { labels: ['A'], values: [10] },
	barplot: { categories: ['Jan'], values: [100] }
};

describe('API fetchChartData', () => {
	const mockFetch = vi.fn();

	beforeEach(() => {
		vi.stubGlobal('fetch', mockFetch);
	});

	afterEach(() => {
		vi.unstubAllGlobals();
		vi.clearAllMocks();
	});

	it('should fetch and transform data successfully', async () => {
		mockFetch.mockResolvedValue({
			ok: true,
			json: async () => mockApiResponse,
			status: 200
		});

		const result = await fetchChartData();

		expect(mockFetch).toHaveBeenCalledOnce();
		// Verifica la URL por defecto si VITE_API_URL no está definida en el entorno de test
		const expectedUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/data';
		expect(mockFetch).toHaveBeenCalledWith(expectedUrl);

		// Verifica que el transformador fue llamado con los datos correctos
		expect(DataTransformer.transformAPIResponse).toHaveBeenCalledWith(mockApiResponse);

		// Verifica que la función devuelve el resultado del transformador mockeado
		expect(result).toEqual({
			pieChartData: [{ name: 'MockPie', value: 1 }],
			barChartData: { categories: ['MockBar'], values: [1] }
		});
	});

	it('should throw error on HTTP error status', async () => {
		mockFetch.mockResolvedValue({
			ok: false,
			status: 404,
			statusText: 'Not Found'
		});

		await expect(fetchChartData()).rejects.toThrow(
			'Failed to load chart data. Please try again later.'
		);
		expect(mockFetch).toHaveBeenCalledOnce();
	});

	it('should throw specific error on HTTP error', async () => {
		const status = 500;
		mockFetch.mockResolvedValue({
			ok: false,
			status: status,
			statusText: 'Internal Server Error'
		});

		try {
			await fetchChartData();
		} catch (e) {
			expect(e).toBeInstanceOf(Error);
			expect((e as Error).message).toContain('Failed to load chart data');
		}
		expect(mockFetch).toHaveBeenCalledOnce();
	});

	it('should throw error on network failure', async () => {
		const networkError = new Error('Network failed');
		mockFetch.mockRejectedValue(networkError);

		await expect(fetchChartData()).rejects.toThrow(
			'Failed to load chart data. Please try again later.'
		);
		expect(mockFetch).toHaveBeenCalledOnce();
	});
});
