<template>
	<b-card>
		<chart
			v-if="loaded"
			:chart-data="displayData"
			:options="displayOption"
			:styles="historyChartStyles"
		></chart>
		<StatsDataTable v-if="loaded" :dataset="datasets" :labels="labels" />
		<Pagination v-if="loaded" :page="page" @movePage="getStatHistory($event)" />
		<Favorites
			v-if="loaded"
			:statsCodeID="statData.stats_code.id"
			:areaId="statData.area.id"
			:subCategory="statData.sub_category"
		></Favorites>
	</b-card>
</template>

<script>
import chart from "@/services/chart.js";
import Pagination from "@/components/Pagination.vue";
import Favorites from "./Favorites";
import StatsDataTable from "./StatsDataTable";

export default {
	components: {
		chart,
		Pagination,
		Favorites,
		StatsDataTable,
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
		title() {
			return this.statData.stats_code.table_name_alias_alias;
		},
		labels() {
			return this.timeSeriesData.map((e) => e.time);
		},
		datasets() {
			const area = this.statData.area.name;

			const subCategory = this.statData.sub_category
				.map((e) => e.name)
				.join(" : ");

			return {
				data: this.timeSeriesData.map((e) => e.value),
				label: `【${area}】${subCategory}`,
			};
		},
		displayData() {
			const self = this;

			const transparentWhite = "rgba(255,255,255,0)";
			const dataCollection = {
				labels: self.labels,
				datasets: [
					{
						label: self.datasets.label,
						type: "bar",
						data: self.datasets.data,
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
					text: self.statData.stats_code.table_name_alias,
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
		params() {
			return {
				stats_code: this.statData.stats_code.id,
				area: this.statData.area.id,
				sub_category: this.statData.sub_category.map((el) => el.id),
			};
		},
		historyChartStyles() {
			return {
				"min-height": "35vh",
				"max-height": "35vh",
				position: "relative",
			};
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
