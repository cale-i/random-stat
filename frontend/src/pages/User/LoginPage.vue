<template>
	<div id="login-page" class="bg-success">
		<GlobalHeader />
		<GlobalMessage />

		<div id="layoutAuthentication">
			<div id="layoutAuthentication_content">
				<main>
					<div class="container">
						<div class="row justify-content-center">
							<div class="col-sm-8 col-md-6 col-lg-5 col-xl-4">
								<div class="card shadow-lg border-0 rounded-lg mt-5">
									<div class="card-header">
										<h3 class="text-center font-weight-light my-4">Login</h3>
									</div>
									<div class="card-body">
										<b-form @submit.prevent="submitLogin">
											<b-form-group
												id="inputGroupEmail"
												label="Email address"
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
												label-for="inputPassword"
											>
												<b-form-input
													id="inputPassword"
													v-model="form.password"
													type="password"
													placeholder="password"
													required
													autofocus
													autocomplete="true"
												></b-form-input>
											</b-form-group>

											<div
												class="d-flex align-items-center justify-content-between mt-4 mb-0"
											>
												<a class="small" href="password.html"
													>Forgot Password?</a
												>
												<b-button class="" variant="primary" type="submit"
													>Login</b-button
												>
											</div>
										</b-form>
									</div>

									<div class="card-footer text-center py-3">
										<router-link
											to="/create-account/"
											class="btn btn-sm btn-warning"
											>アカウントを作成</router-link
										>
									</div>
								</div>
							</div>
						</div>
					</div>
				</main>
			</div>
		</div>
		<div id="layoutAuthentication_footer">
			<footer class="py-4 bg-light mt-auto">
				<div class="container-fluid px-4">
					<div class="d-flex align-items-center justify-content-between small">
						<div class="text-muted">Copyright &copy; Your Website 2021</div>
						<div>
							<a href="#">Privacy Policy</a>
							&middot;
							<a href="#">Terms &amp; Conditions</a>
						</div>
					</div>
				</div>
			</footer>
		</div>
	</div>
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
