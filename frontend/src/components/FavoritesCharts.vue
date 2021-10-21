<template>
	<b-card>
		<chart
			v-if="loaded"
			:chart-data="displayData"
			:options="displayOption"
			:styles="favoritesChartStyles"
		></chart>
		<StatsDataTable v-if="loaded" :dataset="datasets" :labels="labels" />

		<Pagination v-if="loaded" :page="page" @movePage="getFavorites($event)" />
		<div if="loaded">
			<div
				id="deleteFavoritesBtn"
				class="btn favorites-icon"
				@click="deleteFavorites"
			>
				<b-icon icon="heart-fill"></b-icon>
			</div>
			<b-popover
				target="deleteFavoritesBtn"
				placement="topright"
				triggers="hover focus"
				content="お気に入りから削除"
			></b-popover>
			<div id="reloadBtn" class="btn reload-icon">
				<b-icon icon="arrow-clockwise" @click="getFavorites()"></b-icon>
			</div>
			<b-popover
				target="reloadBtn"
				placement="topright"
				triggers="hover focus"
				content="再読み込み"
			></b-popover>
		</div>
	</b-card>
</template>

<script>
import chart from "@/services/chart.js";
import Pagination from "@/components/Pagination.vue";
import StatsDataTable from "./StatsDataTable";
export default {
	components: {
		chart,
		Pagination,
		StatsDataTable,
	},
	props: {},
	data: () => ({
		loaded: null,
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
		favoritesChartStyles() {
			return {
				"min-height": "35vh",
				"max-height": "35vh",
				position: "relative",
			};
		},
	},
	methods: {
		getFavorites(page = { page: 1 }) {
			this.$store.dispatch("chart/getFavorites", page).then((response) => {
				// お気に入りが0個の場合
				if (response.data.count === 0) {
					this.loaded = false;

					return;
				}
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
		deleteFavorites() {
			console.log(this.params);
			this.$store.dispatch("chart/deleteFavorites", this.params).then(() => {
				this.$store.dispatch("message/setInfoMessage", {
					message: "お気に入から削除しました｡",
				});
				this.getFavorites();
			});
		},
	},
	mounted() {
		this.getFavorites();
	},
};
</script>
<style scoped>
.favorites-icon {
	color: red;
}
.favorites-icon:hover {
	color: gray;
}
.reload-icon {
	color: #00a040;
}
.reload-icon:hover {
	color: black;
}
</style>
