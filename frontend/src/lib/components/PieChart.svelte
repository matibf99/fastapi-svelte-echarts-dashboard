<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as echarts from 'echarts';
	import type { PieChartProps } from '$lib/types/types';

	export let data: PieChartProps['data'];
	export let title: PieChartProps['title'] = 'Gráfico circular';

	let chartEl: HTMLDivElement;
	let chart: echarts.ECharts;

	onMount(() => {
		chart = echarts.init(chartEl);
		updateChart();
		window.addEventListener('resize', handleResize);
	});

	onDestroy(() => {
		chart?.dispose();
		window.removeEventListener('resize', handleResize);
	});

	function handleResize() {
		chart?.resize();
	}

	function updateChart() {
		chart?.setOption({
			title: { text: title, left: 'center' },
			tooltip: { trigger: 'item' },
			legend: { bottom: 0 },
			series: [
				{
					name: 'Distribución',
					type: 'pie',
					radius: '50%',
					data: data,
					emphasis: {
						itemStyle: {
							shadowBlur: 10,
							shadowOffsetX: 0,
							shadowColor: 'rgba(0, 0, 0, 0.5)'
						}
					}
				}
			]
		});
	}

	$: if (data) updateChart();
</script>

<div class="h-full w-full rounded-lg bg-white p-4 shadow">
	<div bind:this={chartEl} class="h-64 w-full"></div>
</div>
