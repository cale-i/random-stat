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
			<b-col md="3">
				<div v-b-modal.signUpModal class="btn btn-sm btn-warning">
					Sign Up
				</div>
			</b-col>
			<b-col md="6">
				<h4 class="text-center">Guest Login</h4>
			</b-col>
			<b-col md="3"></b-col>
		</template>
		<template #default="{}">
			<div class="card-body">
				<b-form @submit.prevent="submitGuestLogin">
					<b-form-group
						id="inputGroupEmail"
						label="Email:"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputEmail"
						class="my-4"
					>
						<b-form-input
							id="inputEmail"
							v-model="form.email"
							type="email"
							placeholder="example@example.com"
							required
							autofocus
							disabled
						></b-form-input>
					</b-form-group>

					<b-form-group
						id="inputGroupPassword"
						label="Password"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputPassword"
						class="my-4"
					>
						<b-form-input
							id="inputPassword"
							v-model="form.password"
							type="password"
							placeholder="password"
							required
							autocomplete="true"
							disabled
						></b-form-input>
					</b-form-group>

					<div
						class="d-flex align-items-center justify-content-between mt-4 mb-0"
					>
						<div></div>
						<b-button size="md" variant="success" type="submit">
							Login
						</b-button>
					</div>
				</b-form>
			</div>
		</template>
		<template #modal-footer="{}">
			<div class="text-muted small">&copy; Random Stat 2021</div>
		</template>
	</b-modal>
</template>

<script>
export default {
	components: {},
	props: {},
	data: () => ({
		modalId: "guestLoginModal",
		form: {
			email: "guest@randomstat.work",
			password: "********",
		},
	}),
	computed: {},
	methods: {
		submitGuestLogin() {
			console.log("test");
			// ログイン
			this.$store
				.dispatch("guestLogin/login")
				.then(() => {
					console.log("success");
					this.$store.dispatch("message/setInfoMessage", {
						message: "ログインしました。",
					});
					// クエリ文字列に「next」がなければダッシュボード画面へ
					const next = this.$route.query.next || "/dashboard";
					console.log("next:", next);
					this.$router.replace(next);
				})
				.catch(() => {
					// ログイン失敗
				});
		},
	},
	watch: {},
	mounted() {},
};
</script>
<style scoped></style>
