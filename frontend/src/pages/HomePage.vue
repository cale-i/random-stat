<template>
	<div id="home-page">
		<GlobalHeader />
		<ChartContainer />
	</div>
</template>

<script>
import GlobalHeader from "@/components/GlobalHeader.vue";
import ChartContainer from "@/components/ChartContainer.vue";

// import { mapGetters } from 'vuex'

export default {
	components: {
		GlobalHeader,
		ChartContainer,
	},
	data: function() {
		return {
			today: "",
		};
	},
	methods: {
		async authReload() {
			await this.$store.dispatch("auth/reload");
		},
	},

	mounted() {
		this.authReload();
	},
	created() {},
	computed: {},
};
</script>

<style scoped></style>
