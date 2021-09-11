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
		<b-overlay :show="sendingEmail" rounded="sm">
			<template>
				<div class="card-body p-0">
					<h4 class="text-center my-2 font-weight-bold title">
						パスワード再設定
					</h4>
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
								placeholder="登録済みメールアドレス"
								required
								autofocus
							></b-form-input>
						</b-form-group>

						<div class="d-flex align-items-center justify-content-between mb-0">
							<div></div>
							<b-button size="md" class="send-button" type="submit">
								送信
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
		modalId: "resetPasswordModal",
		form: {
			email: "",
		},
		sendingEmail: false,
	}),
	computed: {},
	methods: {
		submitLogin() {
			// 確認メール送信
			this.$store
				.dispatch("resetPassword/sendEmail", {
					email: this.form.email,
				})
				.then(() => {
					console.log("success");
					this.$store.dispatch("message/setInfoMessage", {
						message: "確認メールを送信しました｡",
					});
					this.sendingEmail = false;
					this.$bvModal.hide("resetPasswordModal");
				});
			// 確認メール送信完了までSpinner動かす
			this.sendingEmail = true;
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
.send-button {
	background: #bd3f4c;
}
.send-button:hover {
	opacity: 80%;
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
