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
			class="stats-data-table"
		></b-table>
	</div>
</template>
<script>
export default {
	props: {
		dataset: {
			type: Object,
			default: null,
		},
		labels: {
			type: Array,
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
					key: "value",
					label: this.dataset.label,
					sortable: true,
					formatter: (value) => {
						return parseInt(value).toLocaleString();
					},
				},
			];
		},
		items() {
			const labels = this.labels;
			const dataset = this.dataset;
			return labels.map((year, index) => {
				return { date: year, value: dataset.data[index] };
			});
		},
	},
};
</script>
<style scoped>
.stats-data-table {
	user-select: none;
}
</style>
