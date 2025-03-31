<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as echarts from 'echarts';
	import type { BarChartProps } from '$lib/types/types';

	export let data: BarChartProps['data'];
	export let title: BarChartProps['title'] = 'Gráfico de barras';

	let chartEl: HTMLDivElement;
	let chart: echarts.ECharts | null = null;

	onMount(() => {
		chart = echarts.init(chartEl);
		updateChart();
		window.addEventListener('resize', handleResize);
	});

	onDestroy(() => {
		if (chart) {
			chart.dispose();
			window.removeEventListener('resize', handleResize);
		}
	});

	function handleResize() {
		chart?.resize();
	}

	function updateChart() {
		chart?.setOption({
			title: { text: title, left: 'center' },
			tooltip: { trigger: 'axis' },
			xAxis: { type: 'category', data: data.categories },
			yAxis: { type: 'value' },
			series: [
				{
					type: 'bar',
					data: data.values
				}
			]
		});
	}

	$: if (data) updateChart();
</script>

<div class="h-full w-full rounded-lg bg-white p-4 shadow">
	<div bind:this={chartEl} class="h-64 w-full"></div>
</div>
