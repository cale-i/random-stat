<template>
    <div id="chart">
        <b-container>
            
            <!-- <b-button @click="getDataMix()">更新</b-button>
            <chart
                v-if="loaded"
                :chart-data="chartdataMix"
                :options="optionsMix"
            ></chart> -->
            <b-card>
                <b-button @click="setFirstChart()">更新</b-button>
                <h3>{{ this.firstLegend.title }}</h3>
                <div>地域 : {{ this.firstLegend.area}}</div>
                <div>単位 : {{ this.firstLegend.unit}}</div>
                <div>{{ this.firstLegend.sub_category}}</div>

                <chart
                    v-if="loaded"
                    :chart-data="chartDataFirst"
                    :options="firstOption"
                ></chart>
            </b-card>
            <b-card>
            <b-button @click="setSecondChart()">更新</b-button>
            <h3>{{ this.secondLegend.title }}</h3>
            <div>地域 : {{ this.secondLegend.area}}</div>
            <div>単位 : {{ this.secondLegend.unit}}</div>
            <div>{{ this.secondLegend.sub_category}}</div>
            <chart
                v-if="loaded"
                :chart-data="chartDataSecond"
                :options="SecondOption"
            ></chart>
            </b-card>

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
            setFirstChart() {
                const firstData = this.getRandomStat()
                this.setFirstStatData(firstData)
                this.setFirstOption(firstData)
            },
            setSecondChart() {
                const secondData = this.getRandomStat()
                this.setSecondStatData(secondData)
                this.setSecondOption(secondData)
            },
            setFirstStatData(data) {
                let labelList = []
                let dataList = []
                data.then(response => {
                    response.forEach(el => {
                        let formattedTime = (el.time.date).slice(0,4)
                        labelList.push(formattedTime)
                        dataList.push(el.value)
                        })
                    
                this.chartDataFirst = {
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
                    
                this.chartDataSecond = {
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
            setFirstOption(data) {
                data.then(response => {
                    const dataset = response[0]
                    let sub_category = []
                    dataset.sub_category.map(el => {
                        sub_category.push(el.name)
                    })
                    console.log(dataset)
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
                    console.log(dataset)
                    this.secondLegend = {
                        area : dataset.area.name,
                        title: dataset.stats_code.table_name,
                        unit: dataset.unit,
                        sub_category: sub_category,

                    }
                })
            },
            getRandomStat() {
                // APIリクエストし、ランダム
                // promiseのままreturnしている点に注意
                return this.$store.dispatch(
                    'chart/getChart',
                )
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
                this.setFirstChart()
                this.setSecondChart()

                // this.getDataFirst()
                // this.getDataMix()
                // this.getDataSecond()
                    
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