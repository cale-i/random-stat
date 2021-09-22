<template>
	<b-container id="chart">
		<br />
		<b-overlay spinner-variant="success" :show="!loaded.mixChart" rounded="sm">
			<b-card class="mb-4">
				<chart
					v-if="loaded.mixChart"
					:chart-data="displayDataMix"
					:options="displayOptionMix"
				></chart>
			</b-card>
		</b-overlay>

		<b-row>
			<b-col md="6">
				<b-card>
					<chart
						v-if="loaded.first"
						:chart-data="displayDataFirst"
						:options="displayOptionFirst"
					></chart>
					<hr />
					<b-tabs class="mt-4" content-class="mt-3" v-model="tabIndex.first">
						<b-tab
							title="統計表取得"
							:title-link-class="linkClass(0, 'first')"
							active
						>
							<div class="btn btn-secondary" @click="getStatData('first')">
								ランダムな統計表を取得
							</div>
							<StatsCodeContainer
								v-if="loaded.first"
								:stats-code-list="statData.first.stats_code_list"
								:statsCodeID="statData.first.table.id"
								@catchSelected="searchStatsCode('first', $event)"
							/>
						</b-tab>

						<b-tab
							title="カテゴリー検索"
							:title-link-class="linkClass(1, 'first')"
						>
							<CategoryContainer
								v-if="loaded.first"
								:statsCodeID="statData.first.table.id"
								:area-list="statData.first.area_list"
								:area-id="statData.first.area.id"
								:category-list="statData.first.category_list"
								:sub-category="statData.first.sub_category"
								@catchSelected="searchStatData('first', $event)"
							/>
						</b-tab>
						<b-tab title="統計表詳細" :title-link-class="linkClass(2, 'first')">
						</b-tab>
					</b-tabs>
				</b-card>
			</b-col>
			<b-col md="6">
				<b-card>
					<chart
						v-if="loaded.second"
						:chart-data="displayDataSecond"
						:options="displayOptionSecond"
					></chart>
					<hr />
					<b-tabs class="mt-4" content-class="mt-3" v-model="tabIndex.second">
						<b-tab
							title="統計表取得"
							:title-link-class="linkClass(0, 'second')"
							active
						>
							<div class="btn btn-secondary" @click="getStatData('second')">
								ランダムな統計表を取得
							</div>
							<StatsCodeContainer
								v-if="loaded.second"
								:stats-code-list="statData.second.stats_code_list"
								:statsCodeID="statData.second.table.id"
								@catchSelected="searchStatsCode('second', $event)"
							/>
						</b-tab>
						<b-tab
							title="カテゴリーを指定"
							:title-link-class="linkClass(1, 'second')"
						>
							<CategoryContainer
								v-if="loaded.second"
								:statsCodeID="statData.second.table.id"
								:area-list="statData.second.area_list"
								:area-id="statData.second.area.id"
								:category-list="statData.second.category_list"
								:sub-category="statData.second.sub_category"
								@catchSelected="searchStatData('second', $event)"
							/>
						</b-tab>
						<b-tab
							title="統計表詳細"
							:title-link-class="linkClass(2, 'second')"
						>
						</b-tab>
					</b-tabs>
				</b-card>
			</b-col>
		</b-row>
	</b-container>
</template>

<script>
// import dayjs from 'dayjs'
import chart from "@/services/chart.js";
import CategoryContainer from "./CategoryContainer.vue";
import StatsCodeContainer from "./StatsCodeContainer";

// import BarChart from "./chart/BarChart.vue"
export default {
	name: "ChartContainer",
	components: {
		chart,
		CategoryContainer,
		StatsCodeContainer,
		// BarChart
	},
	data: () => ({
		statData: {
			first: null,
			second: null,
		},
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
		},
	}),
	computed: {
		displayDataFirst() {
			const self = this;

			// sub_categoryからlabelを取得
			let subCategory = self.statData.first.sub_category.map((e) => e.name);
			// areaを取得
			const area = self.statData.first.area.name;

			const transparentWhite = "rgba(255,255,255,0)";
			const dataCollection = {
				labels: self.timeSeriesData.first.map((e) => e.time),
				// labels: self.statData.first.results.map((e) => e.time.date.slice(0, 4)),
				datasets: [
					{
						label: `【${area}】${subCategory.join(" : ")}`,
						type: "bar",
						data: self.timeSeriesData.first.map((e) => e.value),
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

			// sub_categoryからlabelを取得
			let subCategory = self.statData.second.sub_category.map((e) => e.name);
			// areaを取得
			const area = self.statData.second.area.name;

			const transparentWhite = "rgba(255,255,255,0)";
			const dataCollection = {
				labels: self.timeSeriesData.second.map((e) => e.time),
				datasets: [
					{
						label: `【${area}】${subCategory.join(" : ")}`,
						type: "bar",
						data: self.timeSeriesData.second.map((e) => e.value),
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

			const labels = self.displayDataFirst.labels;

			const transparentWhite = "rgba(255,255,255,0)";
			const dataCollection = {
				labels,
				datasets: [
					{
						label: self.displayDataFirst.datasets[0].label,
						type: "bar",
						data: self.timeSeriesData.first.map((e) => e.value),
						backgroundColor: "#00a040",

						categoryPercentage: 0.4,
						borderWidth: 2,
						borderColor: transparentWhite,
						yAxisID: "second-y-axis",
					},
					{
						label: self.displayDataSecond.datasets[0].label,
						type: "line",
						data: self.timeSeriesData.second.map((e) => e.value),
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
					text: self.statData.first.table.name,
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
							// type: "bar",

							// time: {
							// 	unit: "year",
							// 	displayFormats: {
							// 		// year: 'YYYY[年]MM[月]DD[日]'
							// 		year: "YYYY[年]",
							// 	},
							// 	parser: "YYYY",
							// },
							// グリッドラインを消す
							gridLines: {
								drawOnChartArea: false,
							},
							// ticks: {
							//     callback: (value) => {
							//         return dayjs(value).format('D')
							//     }
							// }
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
									return `${value}${self.statData.first.unit}`;
								},
							},
						},
					],
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
					text: self.statData.second.table.name,
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
							// type: "time",
							// time: {
							// 	unit: "year",
							// 	displayFormats: {
							// 		// year: 'YYYY[年]MM[月]DD[日]'
							// 		year: "YYYY[年]",
							// 	},
							// 	parser: "YYYY",
							// },
							// グリッドラインを消す
							gridLines: {
								drawOnChartArea: false,
							},
							// ticks: {
							//     callback: (value) => {
							//         return dayjs(value).format('D')
							//     }
							// }
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
									return `${value}${self.statData.second.unit}`;
								},
							},
						},
					],
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
					text: `${self.statData.first.table.name}   /   ${self.statData.second.table.name}`,
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
							// グリッドラインを消す
							// type: "time",
							// time: {
							// 	unit: "year",
							// 	displayFormats: {
							// 		// year: 'YYYY[年]MM[月]DD[日]'
							// 		year: "YYYY[年]",
							// 	},
							// 	parser: "YYYY",
							// },
							gridLines: {
								drawOnChartArea: false,
							},
							// ticks: {
							//     callback: (value) => {
							//         return dayjs(value).format('D')
							//     }
							// }
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
									return `${value}${self.statData.second.unit}`;
								},
							},
						},
					],
				},
				responsive: true,
				maintainAspectRatio: false,
			};
			return options;
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

			Promise.all([first, second]).then(() => {
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
			// console.log(this.statData);
			// console.log(await this.$store.dispatch("chart/searchChart", params));
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
			// console.log(this.statData);
			// console.log(await this.$store.dispatch("chart/searchChart", params));
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
			} else {
				return ["text-dark"];
			}
		},
	},
	created() {
		this.getRandomStats();
	},
};
</script>

<style scoped></style>
