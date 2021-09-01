<template>
	<div>
		<h1 class="my-5">アカウント連携</h1>

		<div>
			<div v-if="this.providers['google-oauth2']" class="btn btn-warning">
				Google連携解除
			</div>
			<div v-else class="btn btn-success">
				Google連携
			</div>
		</div>
	</div>
</template>

<script>
export default {
	components: {},
	props: {},
	data: () => ({}),
	computed: {
		providers() {
			return this.$store.getters["socialAuth/providers"];
		},
	},
	methods: {},
	watch: {},
	mounted() {
		this.$store.dispatch("socialAuth/getAssociatedServices");
	},
	updated() {},
};
</script>
<style scoped></style>
