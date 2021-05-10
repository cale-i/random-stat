<template>
	<div id="chart">
		<b-container>
			<b-card>
				<template v-if="loaded.mixChart">
					<chart
						v-if="loaded.mixChart"
						:chart-data="displayDataMix"
						:options="displayOptionMix"
					></chart>
				</template>
				<template v-if="!loaded.mixChart">
					<b-spinner variant="success" label="Text Centered"></b-spinner>
				</template>
			</b-card>

			<b-row>
				<b-col md="6">
					<b-card>
						<b-button @click="getStatData('first')">別データを取得</b-button>
						<chart
							v-if="loaded.first"
							:chart-data="displayDataFirst"
							:options="displayOptionFirst"
						></chart>
						<CategoryContainer
							v-if="loaded.first"
							:area-list="statData.first.area_list"
							:area-id="statData.first.area.id"
							:category-list="statData.first.category_list"
							:sub-category="statData.first.sub_category"
							@catchSelected="searchStatData('first', $event)"
						/>
					</b-card>
				</b-col>
				<b-col md="6">
					<b-card>
						<b-button @click="getStatData('second')">別データを取得</b-button>
						<chart
							v-if="loaded.second"
							:chart-data="displayDataSecond"
							:options="displayOptionSecond"
						></chart>
						<CategoryContainer
							v-if="loaded.second"
							:area-list="statData.second.area_list"
							:area-id="statData.second.area.id"
							:category-list="statData.second.category_list"
							:sub-category="statData.second.sub_category"
							@catchSelected="searchStatData('second', $event)"
						/>
					</b-card>
				</b-col>
			</b-row>
		</b-container>
	</div>
</template>

<script>
// import dayjs from 'dayjs'
import chart from "@/services/chart.js";
import CategoryContainer from "./CategoryContainer.vue";
// import BarChart from "./chart/BarChart.vue"
export default {
	name: "ChartContainer",
	components: {
		chart,
		CategoryContainer,
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
				labels: self.statData.first.results.map((e) => e.time.date.slice(0, 4)),
				datasets: [
					{
						label: `【${area}】${subCategory.join(" : ")}`,
						type: "bar",
						data: self.statData.first.results.map((e) => e.value),
						backgroundColor: "#00a040",

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
				labels: self.statData.second.results.map((e) =>
					e.time.date.slice(0, 4)
				),
				datasets: [
					{
						label: `【${area}】${subCategory.join(" : ")}`,
						type: "bar",
						data: self.statData.second.results.map((e) => e.value),
						backgroundColor: "#bd3f4c",

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
						data: self.statData.first.results.map((e) => e.value),
						backgroundColor: "#00a040",

						borderWidth: 2,
						borderColor: transparentWhite,
						yAxisID: "second-y-axis",
					},
					{
						label: self.displayDataSecond.datasets[0].label,
						type: "line",
						data: self.statData.second.results.map((e) => e.value),
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
					text: self.statData.first.table_name,
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
							categoryPercentage: 0.4,

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
					text: self.statData.second.table_name,
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
							categoryPercentage: 0.4,
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
					text: `${self.statData.first.table_name}   /   ${self.statData.second.table_name}`,
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
							categoryPercentage: 0.4,
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
		async getStatData(target) {
			// ランダムデータを取得
			this.statData[target] = await this.$store.dispatch("chart/getChart");
		},
		async searchStatData(target, selected) {
			// CategoryContainerコンポーネントにて指定した条件のデータを取得
			const params = {
				area: selected.area,
				sub_category: Object.values(selected.subCategory),
			};
			// console.log(params);
			// console.log(this.statData);
			// console.log(await this.$store.dispatch("chart/searchChart", params));
			this.statData[target] = await this.$store.dispatch(
				"chart/searchChart",
				params
			);
		},
	},
	async mounted() {
		// this.loaded = false
		try {
			await this.getStatData("first");
			await this.getStatData("second");
			// console.log(this.statData);
			this.loaded.first = true;
			this.loaded.second = true;
			this.loaded.mixChart = true;
		} catch (e) {
			console.error(e);
		}
	},
};
</script>

<style scoped>
#chart {
	background-color: #f8f8f8;
}
</style>
