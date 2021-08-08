<template>
	<div class="container">
		<b-card>
			<div>あばたー画像</div>
			<b-form-file v-model="avaterImage" plain></b-form-file>
		</b-card>
	</div>
</template>

<script>
export default {
	props: {},
	data: () => ({
		avaterImage: null,
	}),
	computed: {
		user: function() {
			return this.$store.state.auth;
		},
	},
	methods: {},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped></style>
