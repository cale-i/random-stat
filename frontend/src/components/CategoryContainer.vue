<template>
	<div>
		<b-form>
			<template>
				<b-form-group
					id="selectGroupArea"
					label="地域"
					label-cols-md="6"
					label-align-md="right"
					:label-for="`selectArea-${target}`"
					class="my-2"
				>
					<b-form-select
						:id="`selectArea-${target}`"
						v-model="selected.area"
						:options="areaList"
						class="mb-0"
						value-field="id"
						text-field="name"
						:disabled="!hasChoice(areaList)"
					></b-form-select>
				</b-form-group>
			</template>

			<template v-if="hasCategoryList">
				<div v-for="item in categoryList" :key="item.id">
					<b-form-group
						id="selectGroupSubCategory"
						:label="item.name"
						label-cols-md="6"
						label-align-md="right"
						label-for="inputSubCategory"
						class="my-2"
					>
						<b-form-select
							@change="changeSubCategory(item.id, $event)"
							:value="selected.subCategory[item.id]"
							:options="item.sub_category_list"
							class="mb-0"
							value-field="id"
							text-field="name"
							:disabled="!hasChoice(item.sub_category_list)"
						></b-form-select>
					</b-form-group>
				</div>
			</template>

			<div class="btn btn-secondary" @click="searchStatData">
				カテゴリーを指定して検索
			</div>
		</b-form>
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
		subCategory: {
			type: Array,
			default: null,
		},
		target: {
			type: String,
			default: null,
		},
	},
	data: () => ({
		selected: {
			statsCodeID: null,
			area: null,
			subCategory: {},
		},
		areaList: [],
		categoryList: [],
		hasCategoryList: false,
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
				this.selected.subCategory[e.category] = e.id;
			});
			this.hasCategoryList = true;
		},
		getAreaList(statsCodeID) {
			this.$store
				.dispatch("chart/getAreaList", statsCodeID)
				.then((response) => {
					this.areaList = response.data;
				});
		},
		getCategoryList(statsCodeID) {
			this.hasCategoryList = false;
			this.$store
				.dispatch("chart/getCategoryList", statsCodeID)
				.then((response) => {
					this.categoryList = response.data;
					this.makeSelected();
				});
		},
		changeSubCategory(target, event) {
			this.selected.subCategory[target] = event;
		},
		searchStatData() {
			if (this.isValueChaged()) {
				this.$emit("catchSelected", this.selected);
			} else {
				// メッセージ表示
				this.$store.dispatch("message/setWarningMessage", {
					message: ["カテゴリが変更されていません"],
				});
			}
		},
		hasChoice(list) {
			return list.length > 1;
		},
		isValueChaged() {
			if (this.areaId !== this.selected.area) return true;

			// 配列内の要素を比較
			const isChangedSubCategory = this.subCategory.some((e) => {
				// 一つでも異なる値があればtrueを返す
				return this.selected.subCategory[e.category] !== e.id;
			});
			return isChangedSubCategory;
		},
	},
	watch: {
		statsCodeID: {
			handler: function(newValue) {
				this.selected.statsCodeID = newValue;
				this.getAreaList(newValue);
				this.getCategoryList(newValue);
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
				this.selected.subCategory[e.category] = e.id;
			});
		},
	},
	created() {
		this.getAreaList(this.statsCodeID);
		this.getCategoryList(this.statsCodeID);
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
