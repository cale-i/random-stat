<template>
	<div>
		<b-row>
			<b-col md="4">
				<span class="area-name">
					地域
				</span>
				<b-form-select
					v-model="selected.area"
					:options="areaList"
					class="mb-3"
					value-field="id"
					text-field="name"
					:disabled="!hasChoice(areaList)"
				></b-form-select>
			</b-col>

			<b-col md="4" v-for="item in categoryList" :key="item.id">
				<span class="category-name">
					{{ item.name }}
				</span>
				<b-form-select
					@change="changeSubCategory(item.id, $event)"
					:value="selected.subCategory[item.id]"
					:options="item.sub_category_list"
					class="mb-3"
					value-field="id"
					text-field="name"
					:disabled="!hasChoice(item.sub_category_list)"
				></b-form-select>
			</b-col>
		</b-row>
		<b-row>
			<b-col>
				<div class="btn btn-secondary" @click="searchStatData">
					カテゴリーを指定して検索
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
		areaId: {
			type: String,
			default: null,
		},
		areaList: {
			type: Array,
			default: null,
		},
		categoryList: {
			type: Array,
			default: null,
		},
		subCategory: {
			type: Array,
			default: null,
		},
	},
	data: () => ({
		selected: {
			statsCodeID: null,
			area: null,
			subCategory: {},
		},
	}),
	computed: {},
	methods: {
		makeSelected() {
			// stats code
			this.selected.statsCodeID = this.statsCodeID;
			// area
			// 初期 area IDを格納
			this.selected.area = this.areaId;

			// subcategory
			// this.selected.subCategory = {
			//    category: "sub_category",
			//    category2: "sub_category2",
			// }
			this.subCategory.map((e) => {
				this.selected.subCategory[e.category.id] = e.id;
			});
		},
		changeSubCategory(target, event) {
			this.selected.subCategory[target] = event;
		},
		searchStatData() {
			this.$emit("catchSelected", this.selected);
		},
		hasChoice(list) {
			return list.length > 1;
		},
	},
	watch: {
		statsCodeID: {
			handler: function(newValue) {
				this.selected.statsCodeID = newValue;
			},
		},
		areaId: {
			handler: function(newValue) {
				this.selected.area = newValue;
			},
		},
		subCategory: function(newValue) {
			// console.log(newValue);
			// console.log(this.selected.subCategory);
			// 別統計表を再取得した場合、別統計表のsubCategoryが追加登録されてしまうため、
			// 必ず初期化
			this.selected.subCategory = {};
			newValue.map((e) => {
				this.selected.subCategory[e.category.id] = e.id;
			});
		},
	},
	created() {
		this.makeSelected();
	},
};
</script>
<style scoped>
.area-name {
	font-weight: bold;
}
.category-name {
	font-weight: bold;
	font-size: 0.8rem;
}
</style>
