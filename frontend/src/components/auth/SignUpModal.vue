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
	computed: {},
	methods: {
		submitSignUp() {
			// confirm password
			console.log();
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
						// クエリ文字列に「next」がなければホーム画面へ
						const next = this.$route.query.next || "/";
						this.$router.replace(next);

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
<style scoped>
html,
body {
	height: 100%;
}

body {
	display: flex;
	-ms-flex-align: center;
	align-items: center;
	padding-top: 40px;
	padding-bottom: 40px;
	background-color: #f5f5f5;
}

.form-signin {
	width: 100%;
	max-width: 330px;
	padding: 15px;
	margin: auto;
}

.form-signin .checkbox {
	font-weight: 400;
}

.form-signin .form-floating:focus-within {
	z-index: 2;
}

.form-signin input[type="text"] {
	margin-bottom: 10px;
	border-bottom-right-radius: 0;
	border-bottom-left-radius: 0;
}
.form-signin input[type="email"] {
	margin-bottom: 10px;
	border-bottom-right-radius: 0;
	border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
	margin-bottom: 10px;
	border-top-left-radius: 0;
	border-top-right-radius: 0;
}
</style>
