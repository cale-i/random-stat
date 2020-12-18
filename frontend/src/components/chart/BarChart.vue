<template>
    <div id="chart">
        <b-container>
            <chart
                v-if="loaded"
                :chartData="chartdata"
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
        data: () => ({

        }),
        methods: {

        },
        async mounted () {
        }
    }
</script>

<style scoped>

</style>