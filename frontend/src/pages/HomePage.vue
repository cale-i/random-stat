<template>
    <div id="home-page">
        <GlobalHeader/>
        <!-- <InputField/> -->
        <!-- <OutputField/> -->
        <ChartContainer/>
        <b-container>
            <!-- <chart :chartdata="chartData" :options="chartOptions"/> -->
        </b-container>        
    </div>
</template>

<script>
    import GlobalHeader from '@/components/GlobalHeader.vue'
    // import InputField from '@/components/InputField.vue'
    // import OutputField from '@/components/OutputField.vue'
    import ChartContainer from '@/components/ChartContainer.vue'


    // import { mapGetters } from 'vuex'

    export default {
        components: {
            GlobalHeader,
            // InputField,
            // OutputField,
            ChartContainer
        },
        data: function() {
            return  {
                today: '',
            }
        },
        methods: {
        },

        mounted() {

        },
        created() {

        },
        computed: {

        }
        
    }
</script>

<style scoped>

</style>