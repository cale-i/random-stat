<template>
	<div id="pagination" class="overflow-auto">
		<div id="pageInfo" class="text-center">
			<span>{{ page.count }}件中 </span>
			<span>{{ firstPage }}~{{ lastPage }}件目</span>
		</div>
		<b-pagination
			v-model="currentPage"
			:total-rows="page.count"
			:per-page="page.perPage"
			first-text="最初"
			prev-text="前"
			next-text="次"
			last-text="最後"
			size="md"
			align="center"
		></b-pagination>
	</div>
</template>

<script>
export default {
	props: {
		page: {
			type: Object,
			default: null,
		},
	},
	data: () => ({
		currentPage: null,
	}),
	computed: {
		firstPage: function() {
			let ret = 0;
			if (this.page.count) {
				ret += (this.currentPage - 1) * this.page.perPage + 1;
			}
			return ret;
		},
		lastPage: function() {
			return Math.min(
				Math.ceil(this.currentPage * this.page.perPage),
				this.page.count
			);
		},
	},
	watch: {
		currentPage: {
			handler: function(newValue) {
				this.currentPage = newValue;
				this.$emit("movePage", { page: newValue });
			},
		},
	},
	methods: {
		setCurrentPage() {
			this.currentPage = this.page.current;
		},
	},
	mounted() {
		this.setCurrentPage();
	},
};
</script>

<style scoped>
#pagination {
	user-select: none;
}
</style>
