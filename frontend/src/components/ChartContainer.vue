<template>
	<div id="chart-body" class="chart-body">
		<b-overlay spinner-variant="success" :show="showOverlay" rounded="sm">
			<b-row>
				<b-col md="6" class="mix-chart">
					<b-tabs content-class="" v-model="tabIndex.mix">
						<b-tab
							title="統計表"
							:title-link-class="linkClass(0, 'mix')"
							active
						>
							<b-card class="mb-2">
								<chart
									v-if="loaded.mixChart"
									:chart-data="displayDataMix"
									:options="displayOptionMix"
									:styles="mixChartStyles"
								></chart>
								<div class="btn btn-secondary mt-3" @click="getRandomStats">
									ランダムな統計表セットを再取得
								</div>
							</b-card>
						</b-tab>
						<b-tab
							v-if="isLoggedIn && loaded.mixChart"
							title="履歴"
							:title-link-class="linkClass(1, 'mix')"
						>
							<StatHistory v-if="enableStatHistory" />
						</b-tab>
						<b-tab
							v-if="isLoggedIn && loaded.mixChart"
							title="お気に入り"
							:title-link-class="linkClass(2, 'mix')"
						>
							<FavoritesCharts v-if="enableFavoritesCharts" />
						</b-tab>
					</b-tabs>
				</b-col>

				<b-col md="6" class="chart">
					<b-card class="mb-3">
						<b-row>
							<b-col>
								<chart
									v-if="loaded.first"
									:chart-data="displayDataFirst"
									:options="displayOptionFirst"
									:styles="chartStyles"
								></chart>
								<Favorites
									v-if="loaded.first && this.isLoggedIn"
									:statsCodeID="statData.first.stats_code.id"
									:areaId="statData.first.area.id"
									:subCategory="statData.first.sub_category"
								></Favorites>
							</b-col>
							<b-col>
								<b-tabs
									class="mt-0"
									content-class="mt-2"
									v-model="tabIndex.first"
								>
									<b-tab
										title="統計表取得"
										:title-link-class="linkClass(0, 'first')"
										active
									>
										<div
											class="btn btn-secondary"
											@click="getStatData('first')"
										>
											ランダムな統計表を取得
										</div>
										<StatsCodeContainer
											v-if="loaded.first"
											:statsCodeList="statsCodeList"
											:statsCodeID="statData.first.stats_code.id"
											@catchSelected="searchStatsCode('first', $event)"
										/>
									</b-tab>

									<b-tab
										title="カテゴリー検索"
										:title-link-class="linkClass(1, 'first')"
									>
										<div
											class="btn btn-secondary mt-3"
											@click="copySubCategory('second', 'first')"
										>
											このカテゴリーをもう一方にコピー
										</div>
										<hr />
										<CategoryContainer
											v-if="loaded.first"
											:statsCodeID="statData.first.stats_code.id"
											:area-id="statData.first.area.id"
											:sub-category="statData.first.sub_category"
											target="first"
											@catchSelected="searchStatData('first', $event)"
										/>
									</b-tab>
									<b-tab
										title="統計数値"
										:title-link-class="linkClass(2, 'first')"
									>
										<StatsDataTable
											v-if="loaded.first"
											:dataset="datasets.first"
											:labels="labels.first"
										/>
									</b-tab>
									<b-tab
										title="統計表詳細"
										:title-link-class="linkClass(3, 'first')"
									>
										<StatsInfo
											v-if="loaded.first"
											:statsCodeID="statData.first.stats_code.id"
											:statsCodeList="statsCodeList"
											:areaName="statData.first.area.name"
											:subCategory="statData.first.sub_category"
											target="first"
											:dataset="datasets.first"
										/>
									</b-tab>
								</b-tabs>
							</b-col>
						</b-row>
					</b-card>
					<b-card>
						<b-row>
							<b-col>
								<chart
									v-if="loaded.second"
									:chart-data="displayDataSecond"
									:options="displayOptionSecond"
									:styles="chartStyles"
								></chart>
								<Favorites
									v-if="loaded.second && this.isLoggedIn"
									:statsCodeID="statData.second.stats_code.id"
									:areaId="statData.second.area.id"
									:subCategory="statData.second.sub_category"
								></Favorites>
							</b-col>
							<b-col>
								<b-tabs
									class="mt-0"
									content-class="mt-2"
									v-model="tabIndex.second"
								>
									<b-tab
										title="統計表取得"
										:title-link-class="linkClass(0, 'second')"
										active
									>
										<div
											class="btn btn-secondary"
											@click="getStatData('second')"
										>
											ランダムな統計表を取得
										</div>
										<StatsCodeContainer
											v-if="loaded.second"
											:statsCodeList="statsCodeList"
											:statsCodeID="statData.second.stats_code.id"
											@catchSelected="searchStatsCode('second', $event)"
										/>
									</b-tab>
									<b-tab
										title="カテゴリー検索"
										:title-link-class="linkClass(1, 'second')"
									>
										<div
											class="btn btn-secondary mt-3"
											@click="copySubCategory('second', 'first')"
										>
											このカテゴリーをもう一方にコピー
										</div>
										<hr />
										<CategoryContainer
											v-if="loaded.second"
											:statsCodeID="statData.second.stats_code.id"
											:area-id="statData.second.area.id"
											:sub-category="statData.second.sub_category"
											target="second"
											@catchSelected="searchStatData('second', $event)"
										/>
									</b-tab>
									<b-tab
										title="統計数値"
										:title-link-class="linkClass(2, 'second')"
									>
										<StatsDataTable
											v-if="loaded.second"
											:dataset="datasets.second"
											:labels="labels.second"
										/>
									</b-tab>
									<b-tab
										title="統計表詳細"
										:title-link-class="linkClass(3, 'second')"
									>
										<StatsInfo
											v-if="loaded.second"
											:statsCodeID="statData.second.stats_code.id"
											:statsCodeList="statsCodeList"
											:areaName="statData.second.area.name"
											:subCategory="statData.second.sub_category"
											target="second"
										/>
									</b-tab>
								</b-tabs>
							</b-col>
						</b-row>
					</b-card>
				</b-col>
			</b-row>
		</b-overlay>
	</div>
</template>

<script>
import chart from "@/services/chart.js";
import CategoryContainer from "./CategoryContainer.vue";
import StatsCodeContainer from "./StatsCodeContainer";
import StatsInfo from "./StatsInfo";
import StatsDataTable from "./StatsDataTable";
import Favorites from "./Favorites";
import FavoritesCharts from "./FavoritesCharts";
import StatHistory from "./StatHistory";

export default {
	name: "ChartContainer",
	components: {
		chart,
		CategoryContainer,
		StatsCodeContainer,
		StatsInfo,
		StatHistory,
		StatsDataTable,
		Favorites,
		FavoritesCharts,
	},
	data: () => ({
		statData: {
			first: null,
			second: null,
		},
		statsCodeList: [],
		loaded: {
			mixChart: false,
			firstChart: false,
			secondChart: false,
		},
		timeSeriesData: {
			first: null,
			second: null,
		},
		tabIndex: {
			first: 0,
			second: 0,
			mix: 0,
		},
		tooltipModel: {
			title: () => {
				return "";
			},
			label: (tooltipItem, data) => {
				const index = tooltipItem.datasetIndex;
				const label = data.datasets[index].label;
				return label;
			},
			afterLabel: (tooltipItem) => {
				const csv = parseInt(tooltipItem.value).toLocaleString();
				const title = `  ${tooltipItem.label}年`;
				const body = `${csv} 人`;
				return `${title} : ${body}`;
			},
		},
	}),
	computed: {
		title() {
			return {
				first: this.statData.first.stats_code.table_name_alias,
				second: this.statData.second.stats_code.table_name_alias,
			};
		},
		labels() {
			return {
				first: this.timeSeriesData.first.map((e) => e.time),
				second: this.timeSeriesData.second.map((e) => e.time),
			};
		},
		datasets() {
			const area = {
				first: this.statData.first.area.name,
				second: this.statData.second.area.name,
			};
			const subCategory = {
				first: this.statData.first.sub_category.map((e) => e.name).join(" : "),
				second: this.statData.second.sub_category
					.map((e) => e.name)
					.join(" : "),
			};
			return {
				first: {
					data: this.timeSeriesData.first.map((e) => e.value),
					label: `【${area.first}】${subCategory.first}`,
				},
				second: {
					data: this.timeSeriesData.second.map((e) => e.value),
					label: `【${area.second}】${subCategory.second}`,
				},
			};
		},
		displayDataFirst() {
			const self = this;

			const transparentWhite = "rgba(255,255,255,0)";
			const dataCollection = {
				labels: self.labels.first,
				// labels: self.statData.first.results.map((e) => e.time.date.slice(0, 4)),
				datasets: [
					{
						label: self.datasets.first.label,
						type: "bar",
						data: self.datasets.first.data,
						backgroundColor: "#00a040",

						categoryPercentage: 0.4,
						borderWidth: 2,
						borderColor: transparentWhite,
						yAxisID: "first-y-axis",
					},
				],
			};
			return dataCollection;
		},
		displayDataSecond() {
			const self = this;

			const transparentWhite = "rgba(255,255,255,0)";
			const dataCollection = {
				labels: self.labels.second,
				datasets: [
					{
						label: self.datasets.second.label,
						type: "bar",
						data: self.datasets.second.data,
						backgroundColor: "#bd3f4c",

						categoryPercentage: 0.4,
						borderWidth: 2,
						borderColor: transparentWhite,
						yAxisID: "second-y-axis",
					},
				],
			};
			return dataCollection;
		},
		displayDataMix() {
			const self = this;

			const transparentWhite = "rgba(255,255,255,0)";
			const dataCollection = {
				labels: self.labels.first,
				datasets: [
					{
						label: self.datasets.first.label,
						type: "bar",
						data: self.datasets.first.data,

						backgroundColor: "#00a040",

						categoryPercentage: 0.4,
						borderWidth: 2,
						borderColor: transparentWhite,
						yAxisID: "second-y-axis",
					},
					{
						label: self.datasets.second.label,
						type: "line",
						data: self.datasets.second.data,

						backgroundColor: transparentWhite,

						borderWidth: 2,
						borderColor: "#bd3f4c",
						yAxisID: "second-y-axis",
					},
				],
			};
			return dataCollection;
		},
		displayOptionFirst() {
			const self = this;

			const options = {
				title: {
					display: true,
					text: self.title.first,
				},
				hover: {
					intersect: false,
				},
				elements: {
					line: {
						tension: 0, // ベジェ曲線を無効にする
					},
				},
				scales: {
					xAxes: [
						{
							gridLines: {
								drawOnChartArea: false,
							},
						},
					],
					yAxes: [
						{
							// bar chart
							id: "first-y-axis",
							position: "left",
							ticks: {
								suggestedMin: 0,
								// suggestedMax: 60,
								// stepSize: 10,
								callback: (value) => {
									value = parseInt(value).toLocaleString();
									return `${value}${self.statData.first.unit}`;
								},
							},
						},
					],
				},
				tooltips: {
					callbacks: this.tooltipModel,
				},
				responsive: true,
				maintainAspectRatio: false,
			};
			return options;
		},
		displayOptionSecond() {
			const self = this;

			const options = {
				title: {
					display: true,
					text: self.statData.second.stats_code.table_name_alias,
				},
				hover: {
					intersect: false,
				},
				elements: {
					line: {
						tension: 0, // ベジェ曲線を無効にする
					},
				},
				scales: {
					xAxes: [
						{
							gridLines: {
								drawOnChartArea: false,
							},
						},
					],
					yAxes: [
						{
							// bar chart
							id: "second-y-axis",
							position: "left",
							ticks: {
								suggestedMin: 0,
								// suggestedMax: 60,
								// stepSize: 10,
								callback: (value) => {
									value = parseInt(value).toLocaleString();
									return `${value}${self.statData.second.unit}`;
								},
							},
						},
					],
				},
				tooltips: {
					callbacks: this.tooltipModel,
				},
				responsive: true,
				maintainAspectRatio: false,
			};
			return options;
		},
		displayOptionMix() {
			const self = this;
			const suggestedMax = Math.max(
				...self.statData.first.results.map((e) => e.value),
				...self.statData.second.results.map((e) => e.value)
			);

			const options = {
				title: {
					display: true,
					// text: "",
					text: `${self.statData.first.stats_code.table_name_alias}   /   ${self.statData.second.stats_code.table_name_alias}`,
				},
				hover: {
					intersect: false,
				},
				elements: {
					line: {
						tension: 0, // ベジェ曲線を無効にする
					},
				},
				scales: {
					xAxes: [
						{
							gridLines: {
								drawOnChartArea: false,
							},
						},
					],
					yAxes: [
						{
							// bar chart
							id: "first-y-axis",
							position: "left",
							ticks: {
								suggestedMin: 0,
								suggestedMax,
								// stepSize: 10,
								callback: (value) => {
									value = parseInt(value).toLocaleString();
									return `${value}${self.statData.first.unit}`;
								},
							},
						},
						{
							// line chart
							id: "second-y-axis",
							position: "right",
							ticks: {
								suggestedMin: 0,
								suggestedMax,
								// stepSize: 10,
								callback: (value) => {
									value = parseInt(value).toLocaleString();
									return `${value}${self.statData.second.unit}`;
								},
							},
						},
					],
				},
				tooltips: {
					mode: "index",
					callbacks: this.tooltipModel,
				},
				responsive: true,
				maintainAspectRatio: false,
			};
			return options;
		},
		isLoggedIn: function() {
			return this.$store.getters["auth/isLoggedIn"];
		},
		enableStatHistory() {
			return this.isLoggedIn && this.loaded.mixChart && this.tabIndex.mix === 1;
		},
		showOverlay() {
			return !this.loaded.mixChart;
		},
		mixChartStyles() {
			return {
				"min-height": "70vh",
				"max-height": "100vh",
				position: "relative",
			};
		},
		chartStyles() {
			return {
				// "max-height": "40vh",
				// "min-height": "40vh",
				height: "40vh",
				position: "relative",
			};
		},
		enableFavoritesCharts() {
			return this.isLoggedIn && this.loaded.mixChart && this.tabIndex.mix === 2;
		},
	},
	methods: {
		getRandomStats() {
			// 2つのランダムな統計表を取得
			const first = this.$store.dispatch("chart/getChart").then((response) => {
				this.statData["first"] = response.data;
			});
			const second = this.$store.dispatch("chart/getChart").then((response) => {
				this.statData["second"] = response.data;
			});

			const statsCodeList = this.$store
				.dispatch("chart/getStatsCodeList")
				.then((response) => {
					this.statsCodeList = response.data;
				});

			Promise.all([first, second, statsCodeList]).then(() => {
				this.setTimeSeriesData();
				this.loaded.first = true;
				this.loaded.second = true;
				this.loaded.mixChart = true;
			});
		},
		getStatData(target) {
			// ランダムデータを取得
			this.$store.dispatch("chart/getChart").then((response) => {
				this.statData[target] = response.data;
				this.setTimeSeriesData();
			});
		},
		async searchStatData(target, selected) {
			// CategoryContainerコンポーネントにて指定した条件のデータを取得

			const params = {
				stats_code: selected.statsCodeID,
				area: selected.area,
				sub_category: Object.values(selected.subCategory),
			};
			this.statData[target] = await this.$store.dispatch(
				"chart/searchChart",
				params
			);
			this.setTimeSeriesData();
		},
		async searchStatsCode(target, selected) {
			// CategoryContainerコンポーネントにて指定した条件のデータを取得

			const params = {
				stats_code: selected.statsCodeID,
			};
			this.statData[target] = await this.$store.dispatch(
				"chart/searchStatsCodeChart",
				params
			);
			this.setTimeSeriesData();
		},
		setTimeSeriesData() {
			// statData.<first/second>.resultsのvalue, time.idからtimeSeriesDataを作成する。

			// first, second 両方のデータがNullでない場合にのみ実行
			if (this.statData.first === null || this.statData.second === null) {
				return;
			}

			// first.time, second.timeに存在する一意の値を格納
			let timeSet = new Set();

			let firstObj = {};
			for (const el of this.statData.first.results) {
				const year = el.time.date.slice(0, 4);
				timeSet.add(year);
				firstObj[year] = el.value;
			}

			let secondObj = {};
			for (const el of this.statData.second.results) {
				const year = el.time.date.slice(0, 4);
				timeSet.add(year);
				secondObj[year] = el.value;
			}

			for (const el of timeSet) {
				firstObj[el] = firstObj[el] ? firstObj[el] : "0";
				secondObj[el] = secondObj[el] ? secondObj[el] : "0";
			}

			// [{time: 1920, value: 0},{time: 1925, value: 100000}]の形に変形
			let firstArrObj = [];
			for (const [key, value] of Object.entries(firstObj)) {
				firstArrObj.push({ time: key, value: value });
			}
			let secondArrObj = [];
			for (const [key, value] of Object.entries(secondObj)) {
				secondArrObj.push({ time: key, value: value });
			}

			this.timeSeriesData["first"] = firstArrObj;
			this.timeSeriesData["second"] = secondArrObj;
		},
		linkClass(idx, target) {
			if (this.tabIndex[target] === idx) {
				if (target === "first") return ["text-success", "font-weight-bold"];
				if (target === "second") return ["text-danger", "font-weight-bold"];
				if (target === "mix")
					return ["bg-success", "text-white", "font-weight-bold"];
			} else {
				if (target === "mix")
					return ["text-dark", "bg-white", "font-weight-bold", "border"];
				return ["text-dark"];
			}
		},
		copySubCategory(from, to) {
			// 一方の統計データをもう一方にコピーする
			this.statData[to] = this.statData[from];
			this.setTimeSeriesData();
		},
	},
	created() {
		this.getRandomStats();
	},
};
</script>

<style scoped>
.chart-body {
	margin: auto 60px;
}
.mix-chart {
}
.chart {
}
</style>
