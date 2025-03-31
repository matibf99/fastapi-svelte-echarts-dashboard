<script lang="ts">
	export let message: string = 'Cargando...';
</script>

<div class="flex h-64 w-full items-center justify-center">
	<div class="flex flex-col items-center">
		<div class="h-10 w-10 animate-spin rounded-full border-t-4 border-solid border-blue-500"></div>
		<p class="mt-2 text-gray-600">{message}</p>
	</div>
</div>
