<template>
	<b-container>
		<GlobalHeader />
		<GlobalMessage />
	</b-container>
</template>

<script>
import GlobalMessage from "@/components/GlobalMessage.vue";
import GlobalHeader from "@/components/GlobalHeader.vue";

export default {
	components: {
		GlobalMessage,
		GlobalHeader,
	},
	props: {},
	data: () => ({}),
	computed: {},
	methods: {
		register() {
			this.$store
				.dispatch("socialAuth/authComplete", {
					code: this.$route.query.code,
					state: this.$route.query.state,
					provider: this.$route.params.provider,
				})
				.then(() => {
					this.$store.dispatch("message/setInfoMessage", {
						message: "ログインしました｡",
					});
					// 現在のページが"/"でない場合"/dashboard"に移動
					if (window.location.pathname !== "/") {
						this.$router.replace("/dashboard");
					}
				});
		},
	},
	watch: {},
	mounted() {
		this.register();
	},
	updated() {},
};
</script>
<style scoped></style>
