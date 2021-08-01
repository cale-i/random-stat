<template>
	<div id="home-page">
		<GlobalHeader />

		<GlobalMessage />

		<ChartContainer />
	</div>
</template>

<script>
import GlobalHeader from "@/components/GlobalHeader.vue";
import GlobalMessage from "@/components/GlobalMessage.vue";
import ChartContainer from "@/components/ChartContainer.vue";

// import { mapGetters } from 'vuex'

export default {
	components: {
		GlobalHeader,
		GlobalMessage,
		ChartContainer,
	},
	data: function() {
		return {
			today: "",
		};
	},
	methods: {
		async authReload() {
			// Tokenが存在する場合はユーザー情報を取得する
			const token = localStorage.getItem("access");
			if (token != null) {
				await this.$store.dispatch("auth/reload");
			}
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
