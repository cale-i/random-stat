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
		complete() {
			this.$store
				.dispatch("socialAuth/authComplete", {
					code: this.$route.query.code,
					state: this.$route.query.state,
					provider: this.$route.params.provider,
				})
				.then((response) => {
					this.$router.replace(response.next);
					this.$store.dispatch("message/setInfoMessage", {
						message: response.message,
					});
				});
		},
	},
	watch: {},
	mounted() {
		this.complete();
	},
	updated() {},
};
</script>
<style scoped></style>
