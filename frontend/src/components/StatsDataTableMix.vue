<template>
	<div>
		<b-table
			small
			striped
			bordered
			sticky-header
			no-border-collapse
			:fields="fields"
			:items="items"
			:sort-by.sync="sortBy"
			:sort-desc.sync="sortDesc"
			responsive="sm"
			class="stats-data-table-mix"
		></b-table>
	</div>
</template>
<script>
export default {
	props: {
		datasets: {
			type: Object,
			default: null,
		},
		labels: {
			type: Object,
			default: null,
		},
	},
	data() {
		return {
			sortBy: "date",
			sortDesc: false,
		};
	},
	computed: {
		fields() {
			return [
				{ key: "date", label: "年", sortable: true },
				{
					key: "firstValue",
					label: this.datasets.first.label,
					sortable: true,
					formatter: (firstValue) => {
						return parseInt(firstValue).toLocaleString();
					},
				},
				{
					key: "secondValue",
					label: this.datasets.second.label,
					sortable: true,
					formatter: (secondValue) => {
						return parseInt(secondValue).toLocaleString();
					},
				},
			];
		},
		items() {
			const labels = this.labels.first;
			const datasets = this.datasets;
			return labels.map((year, index) => {
				return {
					date: year,
					firstValue: datasets.first.data[index],
					secondValue: datasets.second.data[index],
				};
			});
		},
	},
};
</script>
<style scoped>
.stats-data-table-mix {
	user-select: none;
}
</style>
