<template>
    <div id="chart">
        <b-container>
            <b-card>
            <b-row>
                <b-col>
                    <div>{{ this.firstLegend.title }}</div>
                    <div>地域 : {{ this.firstLegend.area}}</div>
                    <div>単位 : {{ this.firstLegend.unit}}</div>
                    <div>{{ this.firstLegend.sub_category}}</div>
                </b-col>
                <b-col>
                    <div>{{ this.secondLegend.title }}</div>
                    <div>地域 : {{ this.secondLegend.area}}</div>
                    <div>単位 : {{ this.secondLegend.unit}}</div>
                    <div>{{ this.secondLegend.sub_category}}</div>
                </b-col>
            </b-row>
            <chart
                v-if="loaded.mixChart"
                :chart-data="chartDataMix"
                :options="mixOption"
            ></chart>
            </b-card>

            <b-row>
                <b-col md="6">
                    <b-card>
                        <h3>{{ this.firstLegend.title }}</h3>
                        <div>地域 : {{ this.firstLegend.area}}</div>
                        <div>単位 : {{ this.firstLegend.unit}}</div>
                        <div>{{ this.firstLegend.sub_category}}</div>

                        <chart
                            v-if="loaded.firstChart"
                            :chart-data="chartDataFirst"
                            :options="firstOption"
                        ></chart>

                        <b-button @click="reloadChart('first')">更新</b-button>
                    </b-card>
                </b-col>
                <b-col md="6">
                    <b-card>
                        <h3>{{ this.secondLegend.title }}</h3>
                        <div>地域 : {{ this.secondLegend.area}}</div>
                        <div>単位 : {{ this.secondLegend.unit}}</div>
                        <div>{{ this.secondLegend.sub_category}}</div>
                        <chart
                            v-if="loaded.secondChart"
                            :chart-data="chartDataSecond"
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
            setFirstChart() {
                const firstData = this.getRandomStat()
                const firstDataSet = this.setFirstStatData(firstData)
                this.setFirstOption(firstData)
                this.loaded.firstChart = true

                return firstDataSet
            },
            setSecondChart() {
                const secondData = this.getRandomStat()
                const secondDataSet = this.setSecondStatData(secondData)
                this.setSecondOption(secondData)
                this.loaded.secondChart = true

                return secondDataSet
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
                this.loaded.mixChart = true
                
                    // datasets: [
                    //     {
                    //         label: '三重県 人口 総数',
                    //         type: 'bar',
                    //         // borderColor: '#f87979',
                    //         data: firstDataSet.dataList,
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
                    //         data: secondDataSet.dataList,
                    //         yAxisID: 'second-y-axis'
                    //     },
                    // ]
            },
            setFirstStatData(data) {
                let labelList = []
                let dataList = []
                const dataset = data.then(response => {
                    response.forEach(el => {
                        let formattedTime = (el.time.date).slice(0,4)
                        labelList.push(formattedTime)
                        dataList.push(el.value)
                    })
                    const dataset =  {
                        labels: labelList,
                        datasets: [
                            {
                                label: 'Bar Chart',
                                type: 'bar',
                                data: dataList,
                                backgroundColor: '#f87979',
                                
                                borderWidth: 0,
                                borderColor: 'rgba(255,255,255,0)',
                                yAxisID: 'first-y-axis'
                            }, 
                        ]
                    }
                    this.chartDataFirst = dataset
                    return dataset
                })
                return dataset
            },
            setSecondStatData(data) {
                let labelList = []
                let dataList = []
                const dataset = data.then(response => {
                    response.forEach(el => {
                        let formattedTime = (el.time.date).slice(0,4)
                        labelList.push(formattedTime)
                        dataList.push(el.value)
                    })
                    const dataset = {
                        labels: labelList,
                        datasets: [
                            {
                                label: 'Line Chart',
                                type: 'bar',
                                data: dataList,
                                backgroundColor: '#2f8888',
                                
                                borderWidth: 0,
                                borderColor: 'rgba(255,255,255,0)',
                                yAxisID: 'second-y-axis'
                            }, 
                        ]
                    }
                    this.chartDataSecond = dataset
                    return dataset
                })
                return dataset
            },
            setFirstOption(data) {
                data.then(response => {
                    const dataset = response[0]
                    let sub_category = []
                    dataset.sub_category.map(el => {
                        sub_category.push(el.name)
                    })
                    this.firstLegend = {
                        area : dataset.area.name,
                        title: dataset.stats_code.table_name,
                        unit: dataset.unit,
                        sub_category: sub_category,

                    }
                })
            },
            setSecondOption(data) {
                data.then(response => {
                    const dataset = response[0]
                    let sub_category = []
                    dataset.sub_category.map(el => {
                        sub_category.push(el.name)
                    })
                    this.secondLegend = {
                        area : dataset.area.name,
                        title: dataset.stats_code.table_name,
                        unit: dataset.unit,
                        sub_category: sub_category,

                    }
                })
            },
            async reloadChart(target) {
                this.loaded.mixChart = false

                try {

                    // 引数でターゲットとなるchartを指定
                    if (target == 'first') {
                        // first chart
                        const firstDataSet = await this.setFirstChart()
                        this.chartDataMix.datasets[0] = firstDataSet.datasets[0]
                    } else if (target == 'second') {
                        // second chart
                        const secondDataSet = await this.setSecondChart()
                        this.chartDataMix.datasets[1] = secondDataSet.datasets[0]

                    }

                    this.loaded.mixChart = true
                    // this.setMixChart(firstDataSet, secondDataSet)
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
        },
        mounted () {
            // this.loaded = false
            try {
                const firstDataSet = this.setFirstChart()
                const secondDataSet = this.setSecondChart()
                this.setMixChart(firstDataSet, secondDataSet)
            } catch (e) {
                console.error(e)
            }
        }
    }
</script>

<style scoped>

</style>