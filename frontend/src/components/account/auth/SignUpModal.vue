<template>
	<b-modal
		id="signUpModal"
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
				<div v-b-modal.loginModal class="btn btn-sm btn-success">
					Login
				</div>
			</b-col>
			<b-col>
				<h4 class="text-center">Sign Up</h4>
			</b-col>
			<b-col md="4"></b-col>
		</template>
		<template #default="{}">
			<div class="card-body form-signin mt-4">
				<b-form @submit.prevent="submitSignUp">
					<b-form-group
						id="inputGroupUsername"
						label="Username:"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputUsername"
					>
						<b-form-input
							id="inputUsername"
							v-model="form.username"
							type="text"
							placeholder="username"
							required
							autofocus
						></b-form-input>
					</b-form-group>

					<b-form-group
						id="inputGroupEmail"
						label="Email:"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputEmail"
					>
						<b-form-input
							id="inputEmail"
							v-model="form.email"
							type="email"
							placeholder="example@example.com"
							required
						></b-form-input>
					</b-form-group>

					<b-form-group
						id="inputGroupPassword"
						label="Password"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputPassword"
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

					<b-form-group
						id="inputGroupRePassword"
						label="Confirm"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputRePassword"
					>
						<b-form-input
							id="inputRePassword"
							v-model="form.rePassword"
							type="password"
							placeholder="Confirm Password"
							required
							autocomplete="true"
						></b-form-input>
						<b-form-valid-feedback :state="validation">
							<br />
						</b-form-valid-feedback>

						<b-form-invalid-feedback :state="validation">
							パスワードが一致しません｡
						</b-form-invalid-feedback>
					</b-form-group>
					<div
						class="d-flex align-items-center justify-content-between mt-4 mb-0"
					>
						<div></div>

						<b-button size="md" variant="warning" type="submit">
							Resister
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
	props: {},
	data: () => ({
		form: {
			username: "",
			email: "",
			password: "",
			rePassword: "",
		},
	}),
	computed: {
		validation() {
			// rePasswordが空白の場合はvalidation error messageを表示させない｡
			if (!this.form.rePassword) return true;
			return this.form.password === this.form.rePassword;
		},
	},
	methods: {
		submitSignUp() {
			// confirm password
			if (this.form.password !== this.form.rePassword) {
				console.log("パスワードが一致しません");
				return;
			}

			// Sign Up
			this.$store
				.dispatch("auth/createAccount", {
					username: this.form.username,
					email: this.form.email,
					password: this.form.password,
					rePassword: this.form.rePassword,
				})
				.then((response) => {
					if (response) {
						console.log("success");
						this.$store.dispatch("message/setInfoMessage", {
							message: "アカウントを作成しました｡",
						});

						// ログインモーダルを表示
						this.$bvModal.show("loginModal");
					}
				});
		},
	},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped></style>
