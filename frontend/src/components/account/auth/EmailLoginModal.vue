<template>
	<b-modal
		id="emailLoginModal"
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
				<div v-b-modal.emailSignUpModal class="btn btn-sm btn-warning">
					Sign Up
				</div>
			</b-col>
			<b-col md="4">
				<h4 class="text-center">Login</h4>
			</b-col>
			<b-col md="4"> </b-col>
		</template>
		<template #default="{}">
			<div class="card-body">
				<b-form @submit.prevent="submitLogin">
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
						></b-form-input>
					</b-form-group>

					<div
						class="d-flex align-items-center justify-content-between mt-4 mb-0"
					>
						<div
							v-b-modal.resetPasswordModal
							class="btn btn-sm btn-link text-black-50"
						>
							パスワードをお忘れの場合
						</div>
						<b-button size="md" variant="success" type="submit">
							Login
						</b-button>
					</div>
				</b-form>
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
	}),
	computed: {},
	methods: {
		submitLogin() {
			// ログイン
			this.$store
				.dispatch("auth/login", {
					email: this.form.email,
					password: this.form.password,
				})
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
