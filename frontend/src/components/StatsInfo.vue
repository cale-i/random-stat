<template>
	<div>
		<b-row>
			<b-col><span class="text-justify">政府統計名</span></b-col>
			<b-col><span class="text-justify">国勢調査</span></b-col>
		</b-row>
		<b-row>
			<b-col><span class="text-justify">担当機関</span></b-col>
			<b-col><span class="text-justify">内閣府</span></b-col>
		</b-row>
		<b-row>
			<b-col><span class="text-justify">データセットの概要</span></b-col>
			<b-col>
				<b-icon id="explanation" icon="info-circle-fill"></b-icon>
				<b-popover target="explanation" triggers="hover">
					{{ getExplanation(statsCodeID) }}
				</b-popover>
			</b-col>
		</b-row>
		<b-row>
			<b-col><span class="text-justify">表題</span></b-col>
			<b-col>{{ statsCodeAlias[statsCodeID] }}</b-col>
		</b-row>

		<b-row>
			<b-col><span>地域</span> </b-col>
			<b-col>
				<span>{{ areaName }} </span>
			</b-col>
		</b-row>
		<template v-if="hasCategoryList">
			<b-row md="" v-for="item in categoryList" :key="item.id">
				<b-col>
					<span class="text-justify">
						{{ item.name }}
					</span>
				</b-col>
				<b-col>
					<span>
						{{ statsInfo.subCategory[item.id] }}
					</span>
				</b-col>
			</b-row>
		</template>
		<b-row>
			<b-col>
				<span class="text-justify">出典</span>
			</b-col>
			<b-col>
				<a href="https://www.stat.go.jp/index.html">総務省統計局</a>
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
		areaName: {
			type: String,
			default: null,
		},
		subCategory: {
			type: Array,
			default: null,
		},
	},
	data: () => ({
		statsInfo: {
			table_name: "",
			explanation: "",
			subCategory: {},
			statsCodeList: [],
		},
		categoryList: [],
		hasCategoryList: false,
		statsCodeAlias: {
			"0003410379": "総人口",
			"0003412175": "労働力状態",
			"0003412176": "労働力状態",
		},
	}),
	methods: {
		getStatsInfo(statsCodeID) {
			// 統計情報を取得
			this.$store
				.dispatch("chart/getStatsInfo", statsCodeID)
				.then((response) => {
					this.statsInfo = response.data;
				});
		},
		getCategoryList(statsCodeID) {
			this.hasCategoryList = false;
			this.$store
				.dispatch("chart/getCategoryList", statsCodeID)
				.then((response) => {
					this.categoryList = response.data;
					console.log(this.categoryList);

					this.subCategory.map((e) => {
						this.statsInfo.subCategory[e.category] = e.name;
					});
					this.hasCategoryList = true;
				});
		},
		getExplanation(statsCodeID) {
			const statsCodeList = this.statsCodeList;
			for (const el of statsCodeList) {
				if (el.id === statsCodeID) {
					let explanation = el.explanation.replaceAll("<br>", "\n");
					return explanation;
				}
			}
		},
	},
	watch: {
		statsCodeID: {
			handler: function(newValue) {
				this.getCategoryList(newValue);
			},
		},
		subCategory: function(newValue) {
			// 別統計表を再取得した場合、別統計表のsubCategoryが追加登録されてしまうため、
			// 必ず初期化
			this.statsInfo.subCategory = {};
			newValue.map((e) => {
				this.statsInfo.subCategory[e.category] = e.name;
			});
		},
	},
	created() {
		this.getCategoryList(this.statsCodeID);
		// this.getStatsInfo(this.statsCodeID);
	},
};
</script>
