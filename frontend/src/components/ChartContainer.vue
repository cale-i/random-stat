<template>
    <div id="chart">
        <b-container>
            <b-card>
                <b-row>
                    <b-col md="6">
                        <div>{{ this.firstLegend.title }}</div>
                        <div>{{ this.firstLegend.sub_category }}</div>
                    </b-col>

                    <b-col md="6">
                            <div>{{ this.secondLegend.title }}</div>
                            <div>{{ this.secondLegend.sub_category }}</div>
                    </b-col>
                </b-row>

                <template v-if="loaded.mixChart">
                    <chart
                        v-if="loaded.mixChart"
                        :chart-data="chartDataMix"
                        :options="mixOption"
                    ></chart>
                </template>
                <template v-if="!loaded.mixChart">
                    <b-spinner
                        variant='success'
                        label="Text Centered"
                    ></b-spinner>
                </template>
            </b-card>

            <b-row>
                <b-col md="6">
                    <b-card>
                        <h3>{{ this.firstLegend.title }}</h3>
                        <div>{{ this.firstLegend.sub_category }}</div>

                        <chart
                            v-if="loaded.first"
                            :chart-data="chartData.first"
                            :options="firstOption"
                        ></chart>

                        <b-button @click="reloadChart('first')">更新</b-button>
                    </b-card>
                </b-col>
                <b-col md="6">
                    <b-card>
                        <h3>{{ this.secondLegend.title }}</h3>
                        <div>{{ this.secondLegend.sub_category}}</div>
                        <chart
                            v-if="loaded.second"
                            :chart-data="chartData.second"
                            :options="SecondOption"
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
    import chart from "@/services/chart.js"
    // import BarChart from "./chart/BarChart.vue"
    export default {
        name: 'ChartContainer',
        components: {
            chart,
            // BarChart
        },
        data: () => ({
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
            chartDataFirst: {
                    labels: [],
                    datasets: [],
            },
            chartDataSecond: {
                    labels: [],
                    datasets: [],
            },
            firstOption: {
                title: {
                    display: true,
                    text: ''
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
                            type: 'time',
                            
                            time: {
                                unit: 'year',
                                displayFormats: {
                                    // year: 'YYYY[年]MM[月]DD[日]'
                                    year: 'YYYY[年]'
                                },
                                parser: 'YYYY'
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
                            id: 'first-y-axis',
                            position: 'left',
                            ticks: {
                                suggestedMin: 0,
                                // suggestedMax: 60,
                                // stepSize: 10,
                                callback: (value) => {
                                    return value
                                }
                            },
                        }
                    ]
                },
                responsive: true,
                maintainAspectRatio: false,
            },
            SecondOption: {
                title: {
                    display: true,
                    text: ''
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
                            type: 'time',
                            
                            time: {
                                unit: 'year',
                                displayFormats: {
                                    // year: 'YYYY[年]MM[月]DD[日]'
                                    year: 'YYYY[年]'
                                },
                                parser: 'YYYY'
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
                            id: 'second-y-axis',
                            position: 'left',
                            ticks: {
                                suggestedMin: 0,
                                // suggestedMax: 60,
                                // stepSize: 10,
                                callback: (value) => {
                                    return value + '人'
                                }
                            },
                        }
                    ]
                },
                responsive: true,
                maintainAspectRatio: false,
            },
            firstLegend: {
                title: '',
                area: '',
                unit: '',
                stats_name: '',
                sub_category: [],

            },
            secondLegend: {
                title: '',
                area: '',
                unit: '',
                stats_name: '',
                sub_category: [],

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
                    datasets: [{},{}],
            },
            mixOption: {
                title: {
                    display: true,
                    text: ''
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
                            type: 'time',
                            
                            time: {
                                unit: 'year',
                                displayFormats: {
                                    // year: 'YYYY[年]MM[月]DD[日]'
                                    year: 'YYYY[年]'
                                },
                                parser: 'YYYY'
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
                            id: 'first-y-axis',
                            position: 'left',
                            ticks: {
                                suggestedMin: 0,
                                // suggestedMax: 60,
                                // stepSize: 10,
                                callback: (value) => {
                                    return value + '人'
                                }
                            },

                        },{
                            // line chart
                            id: 'second-y-axis',
                            position: 'right',
                            ticks: {
                                suggestedMin: 0,
                                // suggestedMax: 60,
                                // stepSize: 10,
                                callback: (value) => {
                                    return value + '人'
                                }
                            },

                        }
                    ],
                },
                responsive: true,
                maintainAspectRatio: false,
                }
        }),
        methods: {
            setChart(target) {
                const statData = this.getRandomStat()
                const dataSet = this.setStatData(statData, target)
                this.setOption(statData, target)
                this.loaded[target] = true
                return dataSet
            },
            async setMixChart(firstData, secondData) {
                const firstDataSet = await firstData.then(res => res)
                const secondDataSet = await secondData.then(res => res)

                this.chartDataMix = {
                    labels: firstDataSet.labels,
                    datasets: [
                        firstDataSet.datasets[0],
                        secondDataSet.datasets[0],
                    ]
                }
                this.convertLineChart()
                this.loaded.mixChart = true
                
                    // datasets: [
                    //     {
                    //         label: '三重県 人口 総数',
                    //         type: 'bar',
                    //         // borderColor: '#f87979',
                    //         data: firstDataSet.data,
                    //         backgroundColor: '#f87979',
                    //         // backgroundColor: '#f87979',
                            
                    //         borderWidth: 0,
                    //         borderColor: 'rgba(255,255,255,0)',
                    //         // data: this.getRandomList(NUM)
                    //         yAxisID: 'first-y-axis'
                    //     }, 
                    //     {
                    //         label: 'Line Chart',
                    //         type: 'line',
                    //         // lineTension: 0,
                    //         borderColor: '#2f8888',
                    //         // backgroundColor: '#2f8888',
                    //         backgroundColor: '#0000',
                    //         data: secondDataSet.data,
                    //         yAxisID: 'second-y-axis'
                    //     },
                    // ]
            },
            setStatData(statData, target) {
                const dataset = statData.then(response => {
                    let labels = response.map((e) => (e.time.date).slice(0, 4))
                    let data = response.map((e) => e.value)

                    // sub_categoryからlabelを取得
                    let subCategory = response[0].sub_category.map((e) => e.name)
                    // areaを取得
                    const area = response[0].area.name
                    const label = `【${area}】${subCategory.join(' : ')}`

                    let dataset
                    if (target === 'first') {
                        dataset =  {
                            labels,
                            datasets: [
                                {
                                    label,
                                    type: 'bar',
                                    data,
                                    backgroundColor: '#f87979',
                                    
                                    borderWidth: 2,
                                    borderColor: 'rgba(255,255,255,0)',
                                    yAxisID: 'first-y-axis'
                                }, 
                            ]
                        }

                    } else if (target === 'second') {
                        dataset = {
                            labels,
                            datasets: [
                                {
                                    label,
                                    type: 'bar',
                                    data,
                                    backgroundColor: '#2f8888',
                                    
                                    borderWidth: 2,
                                    borderColor: 'rgba(255,255,255,0)',
                                    yAxisID: 'second-y-axis'
                                }, 
                            ]
                        }
                    }
                    this.chartData[target] = dataset
                    return dataset
                })
                return dataset
            },
            setOption(data, target) {
                data.then(response => {
                    const dataset = response[0]
                    const legend = {
                            title: dataset.stats_code.table_name,
                        }
                    if (target ==='first') {
                        this.firstLegend = legend
                    } else if (target ==='second') {
                        this.secondLegend = legend
                    }
                })
            },
            async reloadChart(target) {
                this.loaded.mixChart = false
                try {

                    // 引数でターゲットとなるchartを指定
                    const dataSet = await this.setChart(target)

                    if (target == 'first') {
                        this.chartDataMix.datasets[0] = dataSet.datasets[0]
                    } else if (target == 'second') {
                        this.chartDataMix.datasets[1] = dataSet.datasets[0]

                        // bar chartを line chartに変更
                        this.convertLineChart()
                    }

                    this.loaded.mixChart = true
                } catch (e) {
                    console.error(e)
                }
            },
            getRandomStat() {
                // ランダムデータを取得
                // promiseのままreturnしている点に注意
                return this.$store.dispatch(
                    'chart/getChart',
                )
            },
            convertLineChart() {
                this.chartDataMix.datasets[1].type = 'line'
                this.chartDataMix.datasets[1].backgroundColor = '#0000'
                this.chartDataMix.datasets[1].borderColor = '#2f8888'
            },

        },
        mounted () {
            // this.loaded = false
            try {

                const firstDataSet = this.setChart('first')
                const secondDataSet = this.setChart('second')
                this.setMixChart(firstDataSet, secondDataSet)
            } catch (e) {
                console.error(e)
            }
        }
    }
</script>

<style scoped>

</style>