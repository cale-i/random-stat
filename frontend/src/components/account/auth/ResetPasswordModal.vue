<template>
	<b-modal
		:id="modalId"
		title="パスワード再設定"
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
			<b-col md="2"> </b-col>
			<b-col md="">
				<h4 class="text-center">パスワード再設定</h4>
			</b-col>
			<b-col md="2"></b-col>
		</template>
		<b-overlay :show="sendingEmail" rounded="sm">
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
								placeholder="Registered email address"
								required
								autofocus
							></b-form-input>
						</b-form-group>

						<div
							class="d-flex align-items-center justify-content-between mt-4 mb-0"
						>
							<div></div>
							<b-button size="md" variant="success" type="submit">
								Send
							</b-button>
						</div>
					</b-form>
				</div>
			</template>
		</b-overlay>

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
<style scoped></style>
