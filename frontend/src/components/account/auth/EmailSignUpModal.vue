<template>
	<b-modal
		id="emailSignUpModal"
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
			<div class="header d-flex flex-grow-1">
				<b-icon icon="bar-chart-line" aria-hidden="true" class="mr-2"></b-icon>
				<div>
					<span class="rs-green">R</span>andom <span class="rs-red">S</span>tat
				</div>
			</div>
		</template>
		<b-overlay :show="sendingActivationEmail" rounded="sm">
			<template>
				<div class="card-body p-0">
					<h4 class="text-center my-2 font-weight-bold title">
						アカウント登録
					</h4>

					<b-form @submit.prevent="submitSignUp">
						<b-form-group
							id="inputGroupUsername"
							label="Username:"
							label-cols-md="3"
							label-align-md="right"
							label-for="inputUsername"
							class="my-4"
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
							class="mb-0"
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
						<div class="d-flex align-items-center justify-content-between mb-0">
							<div
								v-b-modal.resetPasswordModal
								class="btn btn-sm btn-link text-black-50"
								tabindex="-1"
							>
								アクティベーションメールを再送信
							</div>

							<b-button size="md" class="login-button" type="submit">
								登録
							</b-button>
						</div>
					</b-form>
				</div>
			</template>
		</b-overlay>

		<template #modal-footer="{}">
			<div class="d-flex justify-content-center flex-grow-1 text-muted small">
				Random Stat 2021
			</div>
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
		sendingActivationEmail: false,
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
			// メール送信完了まで処理が止まるため､非常に時間がかかる
			// 失敗時は高速
			this.$store
				.dispatch("auth/createAccount", {
					username: this.form.username,
					email: this.form.email,
					password: this.form.password,
					rePassword: this.form.rePassword,
				})
				.then(() => {
					this.$store.dispatch("message/setInfoMessage", {
						message: "認証メールを送信しました｡",
					});

					// 	// ログインモーダルを表示
					// 	this.$bvModal.show("emailLoginModal");

					// SignUpModalを閉じる
					this.sendingActivationEmail = false;
					this.$bvModal.hide("emailSignUpModal");
				})
				.catch(() => {
					this.sendingActivationEmail = false;
					return;
				});

			// 認証メール送信完了までSpinner動かす
			this.sendingActivationEmail = true;
		},
	},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped>
.header {
	align-items: center;
	height: 1.6rem;
	font-size: 1.6rem;
	color: white;
	justify-content: center;
	align-items: center;
	user-select: none;
}
.title {
	user-select: none;
}
.login-button {
	background: #bd3f4c;
}
.login-button:hover {
	opacity: 80%;
}

.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
