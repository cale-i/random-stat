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
			<b-col md="1"> </b-col>
			<b-col>
				<h4 class="text-center">新しいパスワードの入力</h4>
			</b-col>
			<b-col md="1"></b-col>
		</template>
		<b-overlay :show="confirmPassword" rounded="sm">
			<template #default="{}">
				<div class="card-body">
					<b-form @submit.prevent="submitConfirmation">
						<b-form-group
							id="inputGroupNewPassword"
							label="New Password:"
							label-cols-md="4"
							label-align-md="right"
							label-for="inputNewPassword"
						>
							<b-form-input
								id="inputNewPassword"
								v-model="form.newPassword"
								type="password"
								placeholder="新しいパスワード"
								required
								autocomplete="true"
							></b-form-input>
						</b-form-group>

						<b-form-group
							id="inputGroupConfirmPassword"
							label="Confirm Password:"
							label-cols-md="4"
							label-align-md="right"
							label-for="inputConfirmPassword"
						>
							<b-form-input
								id="inputConfirmPassword"
								v-model="form.reNewPassword"
								type="password"
								placeholder="確認"
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
							<b-button size="md" variant="primary" type="submit">
								変更
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
	props: {},
	data: () => ({
		modalId: "resetPasswordConfirmationModal",
		form: {
			newPassword: "",
			reNewPassword: "",
		},
		confirmPassword: false,
	}),
	computed: {
		validation() {
			// rePasswordが空白の場合はvalidation error messageを表示させない｡
			if (!this.form.reNewPassword) return true;
			return this.form.newPassword === this.form.reNewPassword;
		},
	},
	methods: {
		submitConfirmation() {
			// confirm password
			if (this.form.newPassword !== this.form.reNewPassword) {
				console.log("パスワードが一致しません");
				return;
			}
			this.$store
				.dispatch("resetPassword/confirmation", {
					uid: this.$route.params.uid,
					token: this.$route.params.token,
					new_password: this.form.newPassword,
					re_new_password: this.form.reNewPassword,
				})
				.then((response) => {
					console.log(response);
					this.resultMessage = "パスワードを変更しました｡";
					this.$store.dispatch("message/setInfoMessage", {
						message: "パスワードを変更しました｡",
					});
					this.confirmPassword = false;

					// 現在のページが"/"でない場合"/"に移動
					if (window.location.pathname !== "/") {
						this.$router.replace("/");
					}
				})
				.catch((response) => {
					console.log(response);
					this.resultMessage = "パスワード変更に失敗しました｡";
					this.confirmPassword = false;
				});

			this.confirmPassword = true;
		},
	},
	watch: {},
	mounted() {},
};
</script>
<style scoped></style>
