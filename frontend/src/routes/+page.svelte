<script lang="ts">
	import { onMount } from 'svelte';
	import { fetchChartData } from '$lib/api/api';
	import PieChart from '$lib/components/PieChart.svelte';
	import BarChart from '$lib/components/BarChart.svelte';
	import Loading from '$lib/components/Loading.svelte';
	import type { PieChartProps, BarChartProps } from '$lib/types/types';

	let loading = true;
	let error: string | null = null;

	let pieChartProps: PieChartProps | null = null;
	let barChartProps: BarChartProps | null = null;

	onMount(async () => {
		try {
			const { pieChartData, barChartData } = await fetchChartData();

			pieChartProps = {
				data: pieChartData
			};

			barChartProps = {
				data: barChartData
			};
		} catch (err) {
			error = err instanceof Error ? err.message : 'Unknown error occurred';
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>{'Dashboard'}</title>
</svelte:head>

<main class="bg-gray-50">
	<div class="mx-auto min-h-screen p-6 md:max-w-7xl">
		<h1 class="mb-8 text-3xl font-bold text-gray-800">Dashboard</h1>

		{#if loading}
			<Loading />
		{:else if error}
			<p>{error}</p>
		{:else}
			<div class="grid grid-cols-1 content-center gap-6 md:grid-cols-2">
				{#if pieChartProps}
					<PieChart {...pieChartProps} />
				{/if}
				{#if barChartProps}
					<BarChart {...barChartProps} />
				{/if}
			</div>
		{/if}
	</div>
</main>
