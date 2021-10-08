<template>
	<b-modal
		:id="modalId"
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
		<b-overlay spinner-variant="success" :show="loginAttempting" rounded="sm">
			<template #default="{}">
				<div class="card-body p-0">
					<h4 class="text-center my-2 font-weight-bold title">ログイン</h4>

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
							label="Password:"
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

						<div class="d-flex align-items-center justify-content-between mb-0">
							<div
								v-b-modal.resetPasswordModal
								class="btn btn-sm btn-link text-black-50"
								tabindex="-1"
							>
								パスワードをお忘れの場合
							</div>
							<b-button size="md" class="signup-button" type="submit">
								ログイン
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
	components: {},
	props: {},
	data: () => ({
		form: {
			email: "",
			password: "",
		},
		loginAttempting: false,
		modalId: "emailLoginModal",
	}),
	computed: {},
	methods: {
		async submitLogin() {
			// ログイン

			// ログイン試行中Spinner動かす
			this.loginAttempting = true;

			this.$store
				.dispatch("auth/login", {
					email: this.form.email,
					password: this.form.password,
				})
				.then(() => {
					this.$store.dispatch("message/setInfoMessage", {
						message: "ログインしました。",
					});
					// クエリ文字列に「next」がなければホーム画面へ
					const next = this.$route.query.next || "/";
					if (next === "/") {
						// モーダルウィンドウを閉じる
						this.$bvModal.hide(this.modalId);
					} else {
						// window.location.href = next;
						this.$router.replace(next);
					}
				})
				.finally(() => {
					// Spinner停止
					this.loginAttempting = false;
				});
		},
	},
	watch: {},
	mounted() {},
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
.signup-button {
	background: #00a040;
}
.signup-button:hover {
	opacity: 0.8;
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
