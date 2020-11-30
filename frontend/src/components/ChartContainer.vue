<template>
    <div id="chart">
        <b-container>
            <b-button @click="getData()">更新</b-button>
            <chart
                v-if="loaded"
                :chartData="chartdata"
                :options="options"
            ></chart>
        </b-container>
    </div>
</template>

<script>
    // import dayjs from 'dayjs'
    import chart from "@/services/chart.js"
    // import LineChart from "@/services/chart/lineChart.js"
    export default {
        name: 'ChartContainer',
        components: {
            chart
        },
        data: () => ({
            loaded: false,
            chartdata: null,
            options: {
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
            getData () {
                const NUM = 10
                this.chartdata = {
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
                // const { datalist } = await this.$store.dispatch(
                //     'chart/getChart',
                //     {
                //         id: '',
                //     }
                // )
                this.getData()
                    
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