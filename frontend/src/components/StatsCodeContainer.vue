<template>
	<div>
		<b-row class="mt-3">
			<b-col md="6">
				<span class="stats-code"></span>
				<b-form-select
					v-model="selected.statsCodeID"
					:options="statsCodeList"
					class="mb-3"
					value-field="id"
					text-field="table_name_alias"
				></b-form-select>
			</b-col>
			<b-col md="6">
				<div @click="searchStatData" class="btn btn btn-secondary">
					統計表を指定して取得
				</div>
			</b-col>
		</b-row>
	</div>
</template>

<script>
export default {
	props: {
		statsCodeID: {
			type: String,
			default: null,
		},
		statsCodeList: {
			type: Array,
			default: null,
		},
	},
	data: () => ({
		selected: {
			statsCodeID: null,
		},
	}),
	computed: {},
	methods: {
		makeSelected() {
			// 初期 IDを格納
			this.selected.statsCodeID = this.statsCodeID;
		},
		searchStatData() {
			this.$emit("catchSelected", this.selected);
		},
	},
	watch: {
		statsCodeID: {
			handler: function(newValue) {
				this.selected.statsCodeID = newValue;
			},
		},
	},
	created() {
		this.makeSelected();
	},
};
</script>
<style scoped>
.stats-code {
	font-weight: bold;
}
.btn {
	font-size: 0.7em;
}
</style>
