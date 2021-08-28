<template>
	<b-modal
		:id="modalId"
		title="Login"
		header-bg-variant="dark"
		header-text-variant="light"
		body-bg-variant="light"
		body-text-variant="dark"
		footer-bg-variant="light"
		footer-text-variant="dark"
		centered
		no-stacking
		size="md"
	>
		<template #modal-header="{}">
			<b-col md="4">
				<div v-b-modal.signUpModal class="btn btn-sm btn-warning">
					Sign Up
				</div>
			</b-col>
			<b-col md="4">
				<h4 class="text-center">Login</h4>
			</b-col>
			<b-col md="4"> </b-col>
		</template>
		<template #default="{}">
			<div @click="socialLoginGoogle" class="btn btn-sm btn-success">
				Google
			</div>
		</template>
		<template #modal-footer="{}">
			<b-col md="3" v-b-modal.guestLoginModal class="btn btn-sm btn-info">
				Guest Login
			</b-col>
			<b-col></b-col>
			<b-col md="4" class="text-muted small">&copy; Random Stat 2021</b-col>
		</template>
	</b-modal>
</template>

<script>
export default {
	components: {},
	props: {},
	data: () => ({
		form: {
			email: "",
			password: "",
		},
		modalId: "loginGoogleModal",
	}),
	computed: {},
	methods: {
		socialLoginGoogle() {
			this.$store.dispatch("socialAuth/googleLogin");
		},
	},
	watch: {},
	mounted() {},
};
</script>
<style scoped></style>
