<template>
    <div id="chart">
        <b-container>
            
            <!-- <b-button @click="getDataMix()">更新</b-button>
            <chart
                v-if="loaded"
                :chart-data="chartdataMix"
                :options="optionsMix"
            ></chart> -->

            <b-button @click="getDataFirst()">更新</b-button>
            <chart
                v-if="loaded"
                :chart-data="chartdataFirst"
                :options="optionsFirst"
            ></chart>

            <b-button @click="getDataSecond()">更新</b-button>
            <chart
                v-if="loaded"
                :chart-data="chartdataSecond"
                :options="optionsSecond"
            ></chart>

        </b-container>
    </div>
</template>

<script>
    // import dayjs from 'dayjs'
    import chart from "@/services/chart.js"
    // import BarChart from "./chart/BarChart.vue"
    // import LineChart from "@/services/chart/lineChart.js"
    export default {
        name: 'ChartContainer',
        components: {
            chart,
            // BarChart
        },
        data: () => ({
            chartdataFirst: {
                    labels: [],
                    datasets: [],
            },
            chartdataSecond: {
                    labels: [],
                    datasets: [],
            },
            optionsFirst: {
                title: {
                    display: true,
                    text: '気温1(1月1日~1月10日)'
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
                        }
                    ]
                },
                responsive: true,
                maintainAspectRatio: false,
            },
            optionsSecond: {
                title: {
                    display: true,
                    text: '気温2(2月1日~2月10日)'
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
                        }
                    ]
                },
                responsive: true,
                maintainAspectRatio: false,
            },
            


            loaded: false,

            chartdataMix: null,
            optionsMix: {
                title: {
                    display: true,
                    text: '気温(8月1日~8月10日)'
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
                                unit: 'day',
                                displayFormats: {
                                    day: 'M[月]D[日]'
                                },
                                parser: 'MMM D'
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
                                suggestedMax: 60,
                                stepSize: 10,
                                callback: (value) => {
                                    return value + '万円'
                                }
                            },

                        },{
                            // line chart
                            id: 'second-y-axis',
                            position: 'right',
                            ticks: {
                                suggestedMin: 0,
                                suggestedMax: 60,
                                stepSize: 10,
                                callback: (value) => {
                                    return value + '万人'
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
            setStatData(data) {
                let labelList = []
                let dataList = []
                data.then(response => {
                    response.forEach(el => {
                        let formattedTime = (el.time.date).slice(0,4)
                        labelList.push(formattedTime)
                        dataList.push(el.value)
                        })
                    
                this.chartdataFirst = {
                    labels: labelList,
                    datasets: [
                        {
                            // data: [1,2,3,4,5,6,7,8,9,10],
                            data: dataList,
                            backgroundColor: '#f87979',
                            
                            borderWidth: 0,
                            borderColor: 'rgba(255,255,255,0)',
                            yAxisID: 'first-y-axis'
                        }, 
                    ]
                }
                })
            },
            setSecondStatData(data) {
                let labelList = []
                let dataList = []
                data.then(response => {
                    response.forEach(el => {
                        let formattedTime = (el.time.date).slice(0,4)
                        labelList.push(formattedTime)
                        dataList.push(el.value)
                        })
                    
                this.chartdataSecond = {
                    labels: labelList,
                    datasets: [
                        {
                            // data: [1,2,3,4,5,6,7,8,9,10],
                            data: dataList,
                            backgroundColor: '#f87979',
                            
                            borderWidth: 0,
                            borderColor: 'rgba(255,255,255,0)',
                            yAxisID: 'first-y-axis'
                        }, 
                    ]
                }
                })
            },
            getRandomStat() {
                // promiseのままreturnしている点に注意
                return this.$store.dispatch(
                    'chart/getChart',
                )
            },
            getDataFirst () {
                const NUM = 10
                this.chartdataFirst = {
                    labels: ['jan 1', 'jan 2', 'jan 3', 'jan 4', 'jan 5', 'jan 6', 'jan 7', 'jan 8', 'jan 9', 'jan 10'],
                    datasets: [
                        {
                            // data: [1,2,3,4,5,6,7,8,9,10],
                            data: this.getRandomList(NUM),
                            backgroundColor: '#f87979',
                            
                            borderWidth: 0,
                            borderColor: 'rgba(255,255,255,0)',
                            yAxisID: 'first-y-axis'
                        }, 
                    ]
                }
            },
            getDataSecond () {
                const NUM = 10
                this.chartdataSecond = {
                    labels: ['feb 1', 'feb 2', 'feb 3', 'feb 4', 'feb 5', 'feb 6', 'feb 7', 'feb 8', 'feb 9', 'feb 10'],
                    datasets: [
                        {
                            // data: [1,2,3,4,5,6,7,8,9,10],
                            data: this.getRandomList(NUM),
                            backgroundColor: '#227979',
                            
                            borderWidth: 0,
                            borderColor: 'rgba(255,255,255,0)',
                            yAxisID: 'first-y-axis'
                        }, 
                    ]
                }
            },
            getDataMix () {
                const NUM = 10
                this.chartdataMix = {
                    labels: ['Sep 1', 'Sep 2', 'Sep 3', 'Sep 4', 'Sep 5', 'Sep 6', 'Sep 7', 'Sep 8', 'Sep 9', 'Sep 10'],
                    datasets: [
                        {
                            label: 'Bar Chart',
                            type: 'bar',
                            // borderColor: '#f87979',
                            data: [1,2,3,4,5,6,7,8,9,10],
                            backgroundColor: '#f87979',
                            // backgroundColor: '#f87979',
                            
                            borderWidth: 0,
                            borderColor: 'rgba(255,255,255,0)',
                            // data: this.getRandomList(NUM)
                            yAxisID: 'first-y-axis'
                        }, 
                        {
                            label: 'Line Chart',
                            type: 'line',
                            // lineTension: 0,
                            borderColor: '#2f8888',
                            // backgroundColor: '#2f8888',
                            backgroundColor: '#0000',
                            data: this.getRandomList(NUM),
                            yAxisID: 'second-y-axis'
                        }
                    ]
                }
                // this.options = {
                //     responsive: true,
                //     maintainAspectRatio: false
                // }

            },
            getRandomList (num) {
                let res = []
                for (let i=0; i<num; i++) {
                    res.push(this.getRandomInt())
                }
                return res
            },
            getRandomInt () {
                return Math.floor(Math.random() * (50 - 5 + 1)) + 5
            }
        },
        async mounted () {
            this.loaded = false
            try {
                const firstData = this.getRandomStat()
                this.setStatData(firstData)

                const secondData = this.getRandomStat()
                this.setSecondStatData(secondData)
                // this.getDataFirst()
                // this.getDataMix()
                this.getDataSecond()
                    
                // this.chartData = datalist
                this.loaded = true
            } catch (e) {
                console.error(e)
            }
        }
    }
</script>

<style scoped>

</style>