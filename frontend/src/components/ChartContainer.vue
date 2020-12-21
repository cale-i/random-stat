<template>
  <div id="chart">
    <b-container>
      <b-card>
        <b-row>
          <b-col md="6">
            <div>{{ this.legends.first.title }}</div>
            <div>{{ this.legends.first.sub_category }}</div>
          </b-col>

          <b-col md="6">
            <div>{{ this.legends.second.title }}</div>
            <div>{{ this.legends.second.sub_category }}</div>
          </b-col>
        </b-row>

        <template v-if="loaded.mixChart">
          <chart
            v-if="loaded.mixChart"
            :chart-data="chartDataMix"
            :options="displayMixOption"
          ></chart>
        </template>
        <template v-if="!loaded.mixChart">
          <b-spinner variant="success" label="Text Centered"></b-spinner>
        </template>
      </b-card>

      <b-row>
        <b-col md="6">
          <b-card>
            <div>{{ this.legends.first.sub_category }}</div>

            <chart
              v-if="loaded.first"
              :chart-data="chartData.first"
              :options="displayOption.first"
            ></chart>

            <b-button @click="reloadChart('first')">更新</b-button>
          </b-card>
        </b-col>
        <b-col md="6">
          <b-card>
            <div>{{ this.legends.second.sub_category }}</div>
            <chart
              v-if="loaded.second"
              :chart-data="chartData.second"
              :options="displayOption.second"
            ></chart>

            <b-button @click="reloadChart('second')">更新</b-button>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
// import dayjs from 'dayjs'
import chart from "@/services/chart.js";
// import BarChart from "./chart/BarChart.vue"
export default {
  name: "ChartContainer",
  components: {
    chart,
    // BarChart
  },
  data: () => ({
    statData: {
      first: null,
      second: null,
    },
    chartData: {
      first: {
        labels: [],
        datasets: [],
      },
      second: {
        labels: [],
        datasets: [],
      },
    },
    options: {
      first: {
        title: {
          text: "",
        },
        unit: "",
      },
      second: {
        title: {
          text: "",
        },
        unit: "",
      },
    },
    legends: {
      first: {
        title: "",
        area: "",
        unit: "",
        stats_name: "",
        sub_category: [],
      },
      second: {
        title: "",
        area: "",
        unit: "",
        stats_name: "",
        sub_category: [],
      },
    },
    mixLegend: {
      first: {},
      second: {},
    },
    loaded: {
      mixChart: false,
      firstChart: false,
      secondChart: false,
    },
    chartDataMix: {
      labels: [],
      datasets: [{}, {}],
    },
  }),
  computed: {
    displayOption() {
      const self = this;
      // const unit = this.ounit
      // const options = this.options
      const options = {
        first: {
          title: {
            display: true,
            text: self.options.first.title.text,
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
                type: "time",

                time: {
                  unit: "year",
                  displayFormats: {
                    // year: 'YYYY[年]MM[月]DD[日]'
                    year: "YYYY[年]",
                  },
                  parser: "YYYY",
                },
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
                    return `${value}${self.options.first.unit}`;
                  },
                },
              },
            ],
          },
          responsive: true,
          maintainAspectRatio: false,
        },
        second: {
          title: {
            display: true,
            text: self.options.second.title.text,
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
                type: "time",

                time: {
                  unit: "year",
                  displayFormats: {
                    // year: 'YYYY[年]MM[月]DD[日]'
                    year: "YYYY[年]",
                  },
                  parser: "YYYY",
                },
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
                    return `${value}${self.options.second.unit}`;
                  },
                },
              },
            ],
          },
          responsive: true,
          maintainAspectRatio: false,
        },
      };
      return options;
    },
    displayMixOption() {
      const self = this;
      const suggestedMax = Math.max(
        ...self.statData.first.map((e) => e.value),
        ...self.statData.second.map((e) => e.value)
      );
      console.log(self.statData);
      console.log(suggestedMax);
      // const unit = this.unit
      // const options = this.options
      const options = {
        title: {
          display: true,
          text: "",
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
              type: "time",

              time: {
                unit: "year",
                displayFormats: {
                  // year: 'YYYY[年]MM[月]DD[日]'
                  year: "YYYY[年]",
                },
                parser: "YYYY",
              },
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
                  return `${value}${self.statData.first[0].unit}`;
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
                  return `${value}${self.statData.second[0].unit}`;
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
    setChart(target) {
      const statData = this.statData[target];
      const dataSet = this.setStatData(statData, target);
      this.setOption(statData, target);
      this.loaded[target] = true;
      return dataSet;
    },
    async setMixChart(firstData, secondData) {
      this.chartDataMix = {
        labels: firstData.labels,
        datasets: [firstData.datasets[0], secondData.datasets[0]],
      };
      this.convertLineChart();

      this.loaded.mixChart = true;
    },
    setStatData(statData, target) {
      let labels = statData.map((e) => e.time.date.slice(0, 4));
      let data = statData.map((e) => e.value);

      // sub_categoryからlabelを取得
      let subCategory = statData[0].sub_category.map((e) => e.name);
      // areaを取得
      const area = statData[0].area.name;
      const label = `【${area}】${subCategory.join(" : ")}`;
      const transparentWhite = "rgba(255,255,255,0)";
      let dataset;
      if (target === "first") {
        dataset = {
          labels,
          datasets: [
            {
              label,
              type: "bar",
              data,
              backgroundColor: "#f87979",

              borderWidth: 2,
              borderColor: transparentWhite,
              yAxisID: "first-y-axis",
            },
          ],
        };
      } else if (target === "second") {
        dataset = {
          labels,
          datasets: [
            {
              label,
              type: "bar",
              data,
              backgroundColor: "#2f8888",

              borderWidth: 2,
              borderColor: transparentWhite,
              yAxisID: "second-y-axis",
            },
          ],
        };
      }
      this.chartData[target] = dataset;
      return dataset;
    },
    setOption(data, target) {
      const dataset = data[0];
      const legend = {
        title: dataset.stats_code.table_name,
      };
      this.legends[target] = legend;

      // set title
      this.options[target].title.text = data[0].stats_code.table_name;
      this.options[target].unit = data[0].unit;
    },
    async reloadChart(target) {
      this.loaded.mixChart = false;
      try {
        // 引数でターゲットとなるchartを指定
        await this.getStatData(target);
        const dataSet = await this.setChart(target);

        if (target == "first") {
          this.chartDataMix.datasets[0] = dataSet.datasets[0];
        } else if (target == "second") {
          this.chartDataMix.datasets[1] = dataSet.datasets[0];

          // bar chartを line chartに変更
          this.convertLineChart();
        }

        this.loaded.mixChart = true;
      } catch (e) {
        console.error(e);
      }
    },
    getRandomStat() {
      // ランダムデータを取得
      // promiseのままreturnしている点に注意
      return this.$store.dispatch("chart/getChart");
    },
    convertLineChart() {
      this.chartDataMix.datasets[1].type = "line";
      this.chartDataMix.datasets[1].backgroundColor = "#0000";
      this.chartDataMix.datasets[1].borderColor = "#2f8888";
    },
    async getStatData(target) {
      // ランダムデータを取得
      this.statData[target] = await this.$store.dispatch("chart/getChart");
      // console.log(this.statData[target]);
      console.log(target);
    },
  },
  async mounted() {
    // this.loaded = false
    try {
      await this.getStatData("first");
      await this.getStatData("second");
      const firstDataSet = this.setChart("first");
      const secondDataSet = this.setChart("second");
      this.setMixChart(firstDataSet, secondDataSet);
    } catch (e) {
      console.error(e);
    }
  },
};
</script>

<style scoped></style>
