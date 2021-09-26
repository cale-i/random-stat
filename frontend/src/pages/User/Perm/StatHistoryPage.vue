<template>
	<b-card>
		<chart
			v-if="loaded"
			:chart-data="displayData"
			:options="displayOption"
		></chart>
		<Pagination v-if="loaded" :page="page" @movePage="getStatHistory($event)" />
	</b-card>
</template>

<script>
import chart from "@/services/chart.js";
import Pagination from "@/components/Pagination.vue";
export default {
	components: {
		chart,
		Pagination,
	},
	props: {},
	data: () => ({
		loaded: false,
		statData: null,
		timeSeriesData: null,
		page: null,
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
		displayData() {
			const self = this;

			// sub_categoryからlabelを取得
			let subCategory = self.statData.sub_category.map((e) => e.name);
			// areaを取得
			const area = self.statData.area.name;

			const transparentWhite = "rgba(255,255,255,0)";
			const dataCollection = {
				labels: self.timeSeriesData.map((e) => e.time),
				// labels: self.statData.results.map((e) => e.time.date.slice(0, 4)),
				datasets: [
					{
						label: `【${area}】${subCategory.join(" : ")}`,
						type: "bar",
						data: self.timeSeriesData.map((e) => e.value),
						backgroundColor: "#00a040",

						categoryPercentage: 0.4,
						borderWidth: 2,
						borderColor: transparentWhite,
						yAxisID: "y-axis",
					},
				],
			};
			return dataCollection;
		},
		displayOption() {
			const self = this;

			const options = {
				title: {
					display: true,
					text: self.statData.stats_code.table_name,
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
							gridLines: {
								drawOnChartArea: false,
							},
						},
					],
					yAxes: [
						{
							id: "y-axis",
							position: "left",
							ticks: {
								suggestedMin: 0,
								callback: (value) => {
									value = parseInt(value).toLocaleString();
									return `${value}${self.statData.unit}`;
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
	},
	methods: {
		getStatHistory(page = { page: 1 }) {
			this.$store.dispatch("chart/getStatHistory", page).then((response) => {
				this.statData = response.data;
				this.setTimeSeriesData();
				this.setPage();
			});
		},
		setTimeSeriesData() {
			// statData.resultsのvalue, time.idからtimeSeriesDataを作成する。

			// first.time, second.timeに存在する一意の値を格納
			let timeSet = new Set();

			let firstObj = {};
			for (const el of this.statData.results) {
				const year = el.time.date.slice(0, 4);
				timeSet.add(year);
				firstObj[year] = el.value;
			}

			for (const el of timeSet) {
				firstObj[el] = firstObj[el] ? firstObj[el] : "0";
			}

			// [{time: 1920, value: 0},{time: 1925, value: 100000}]の形に変形
			let firstArrObj = [];
			for (const [key, value] of Object.entries(firstObj)) {
				firstArrObj.push({ time: key, value: value });
			}

			this.timeSeriesData = firstArrObj;
			this.loaded = true;
		},
		setPage() {
			this.page = {
				count: this.statData.count,
				perPage: 1,
				current: this.statData.current,
			};
		},
	},
	mounted() {
		this.getStatHistory();
	},
};
</script>
<style scoped></style>
