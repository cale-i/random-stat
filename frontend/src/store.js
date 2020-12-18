import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/services/api'

Vue.use(Vuex)

const itemModule = {
    namespaced: true,
    state: {
        getURL:'list/books/',
        postURL:'post/books/',
        updateURL:'update/books/',
        deleteURL:'delete/books/',
    },
    getters: {
        getURL: state => state.getURL,
        postURL: state => state.postURL,
        updateURL: state => state.updateURL,
        deleteURL: state => state.deleteURL,
    },
    mutations: {

    },
    actions: {
        retlieve(context) {
            return api({
                method: 'get',
                url: context.getters.getURL
            })
            .then(response => {
                return response.data
            })
        },
        create(context, payload) {
            return api({
                method: 'post',
                url: context.getters.postURL,
                data: {
                    title: payload.title,
                    price: payload.price
                }
            })
            .then(response => {
                return response.data
                
            })
        },
        put(context, payload) {
            return api({
                method: 'put',
                url: context.getters.updateURL + payload.id + '/',
                data: {
                    id: payload.id,
                    title: payload.title,
                    price: payload.price,
                    created_at: payload.created_at,

                }
            })
        },
        delete(context, payload) {
            return api({
                method: 'delete',
                url:context.getters.deleteURL + payload.item.id + '/',
            })
            .then(response => {
                return response
            })
        }
    }
}
const chartModule = {
    namespaced: true,
    state: {
        chartURL:'chronological/',
    },
    getters: {
        chartURL: state => state.chartURL,
    },
    mutations: {

    },
    actions: {
        getChart(context) {
            return api({
                method: 'get',
                url: context.getters.chartURL
            })
            .then(response => {
                return response.data
            })
        },
    }
}


const store = new Vuex.Store({
    modules: {
        item: itemModule,
        chart:chartModule
    }
})

export default store