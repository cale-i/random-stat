<template>
	<b-modal id="loginModal" centered>
		<template #modal-header="{}">
			<router-link to="/create-account/" class="btn btn-sm btn-warning">
				アカウントを作成
			</router-link>
			<h5>
				<b-icon icon="bar-chart-line" aria-hidden="true"></b-icon> Random Stat
			</h5>
		</template>
		<template #default="{}">
			<div class="card-header">
				<h3 class="text-center font-weight-light">Login</h3>
			</div>
			<div class="card-body">
				<b-form @submit.prevent="submitLogin">
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
							autofocus
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

					<div
						class="d-flex align-items-center justify-content-between mt-4 mb-0"
					>
						<a class="small" href="password.html">Forgot Password?</a>
						<b-button class="" variant="success" type="submit">
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
					this.$router.replace(next);
				})
				.catch(() => {
					// ログイン失敗
				});
		},
	},
	watch: {},
	mounted() {},
	// updated() {
	//   this.makeSelected();
	// },
};
</script>
<style scoped></style>
