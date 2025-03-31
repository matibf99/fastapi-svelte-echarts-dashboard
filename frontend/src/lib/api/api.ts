import { DataTransformer } from '../services/dataTransformer';
import type { APIResponse } from '../types/types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/data';

export async function fetchChartData() {
	try {
		const response = await fetch(API_URL);

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const apiData: APIResponse = await response.json();
		return DataTransformer.transformAPIResponse(apiData);
	} catch (error) {
		console.error('Error fetching chart data:', error);
		throw new Error('Failed to load chart data. Please try again later.');
	}
}
