<template>
	<div id="home-page">
		<GlobalHeader />

		<GlobalMessage />

		<router-view />

		<GlobalFooter />
	</div>
</template>

<script>
import GlobalHeader from "@/components/GlobalHeader.vue";
import GlobalMessage from "@/components/GlobalMessage.vue";
import GlobalFooter from "@/components/GlobalFooter.vue";

// import { mapGetters } from 'vuex'

export default {
	components: {
		GlobalHeader,
		GlobalMessage,
		GlobalFooter,
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
};
</script>
