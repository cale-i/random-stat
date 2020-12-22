<template>
    <div id="chart">
        <b-container>
            <chart
                v-if="loaded"
                :chart-data="chartData"
                :options="options"
            ></chart>
        </b-container>
    </div>
</template>

<script>
    import chart from "@/services/chart.js"

    export default {
        name: 'BarChart',
        components: {
            chart
        },
        props: {
            chartData: {
                type: Object,
                default: null
            },
            options: {
                type: Object,
                default: null
            },
            unit: {
                type: String,
                default: '',
            },
        },
        data: () => ({
        }),
        computed: {

        },
        methods: {

        },
        async mounted () {
        }
    }
</script>

<style scoped>

</style>