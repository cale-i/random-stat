import { Bar, mixins } from "vue-chartjs"

const { reactiveProp } = mixins

const chart = {
    extends: Bar,
    mixins: [reactiveProp],
    props: {
        chartdata: {
            type: Object,
            default: null
        },
        options: {
            type: Object,
            default: null
        }
    },
    mounted () {
        this.renderChart(this.chartData, this.options)
    }
}


export default chart
