<template>
	<b-container>
		<GlobalHeader />
		<GlobalMessage />
		{{ resultMessage }}
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
	data: () => ({
		resultMessage: "アクティベーション中",
	}),
	computed: {},
	methods: {
		show: function() {
			console.log(this.$route.params.uid);
			console.log(this.$route.params.token);
			this.$store
				.dispatch("activation/activate", {
					uid: this.$route.params.uid,
					token: this.$route.params.token,
				})
				.then((response) => {
					console.log(response);
				})
				.catch((response) => {
					console.log(response);
				});
		},
	},
	watch: {},
	mounted() {
		this.$store
			.dispatch("activation/activate", {
				uid: this.$route.params.uid,
				token: this.$route.params.token,
			})
			.then((response) => {
				console.log(response);
				this.resultMessage = "アクティベーションを完了しました｡";
				this.$store.dispatch("message/setInfoMessage", {
					message: "アクティベーション完了",
				});
				// 現在のページが"/"でない場合"/"に移動
				if (window.location.pathname !== "/") {
					this.$router.replace("/");
				}
			})
			.catch((response) => {
				console.log(response);
				this.resultMessage = "アクティベーションに失敗しました｡";
			});
	},
	updated() {},
};
</script>
<style scoped></style>
