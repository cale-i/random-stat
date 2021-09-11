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
		<b-overlay :show="changingPassword" rounded="sm">
			<template #default="{}">
				<div class="card-body p-0">
					<h4 class="text-center my-2 font-weight-bold title">
						パスワード変更
					</h4>
					<b-form @submit.prevent="changePassword">
						<b-form-group
							id="inputGroupCurrentPassword"
							label="Current Password:"
							label-cols-md="4"
							label-align-md="right"
							label-for="inputCurrentPassword"
							class="my-4"
						>
							<b-form-input
								id="inputCurrentPassword"
								v-model="form.currentPassword"
								type="password"
								placeholder="現在のパスワード"
								required
								autofocus
								autocomplete="true"
							></b-form-input>
						</b-form-group>

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
							class="mb-0"
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

						<div class="d-flex align-items-center justify-content-between mb-0">
							<div></div>
							<b-button size="md" class="change-button" type="submit">
								変更
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
		modalId: "changePasswordModal",
		form: {
			currentPassword: "",
			newPassword: "",
			reNewPassword: "",
		},
		changingPassword: false,
	}),
	computed: {
		validation() {
			// rePasswordが空白の場合はvalidation error messageを表示させない｡
			if (!this.form.reNewPassword) return true;
			return this.form.newPassword === this.form.reNewPassword;
		},
	},
	methods: {
		changePassword() {
			// confirm password
			if (this.form.newPassword !== this.form.reNewPassword) {
				console.log("パスワードが一致しません");
				return;
			}

			this.$store
				.dispatch("auth/setPassword", {
					current_password: this.form.currentPassword,
					new_password: this.form.newPassword,
					re_new_password: this.form.reNewPassword,
				})
				.then(() => {
					// message
					this.$store.dispatch("message/setInfoMessage", {
						message: "パスワードを変更しました",
					});

					// Clear input data
					this.form = {
						currentPassword: "",
						newPassword: "",
						reNewPassword: "",
					};
					this.changingPassword = false;

					// モーダルウィンドウを閉じる
					this.$bvModal.hide(this.modalId);
				})
				.catch(() => {
					this.changingPassword = false;
				});
			this.changingPassword = true;
		},
	},
	watch: {},
	mounted() {},
	// updated() {
	//   this.makeSelected();
	// },
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
.change-button {
	background: #00a040;
}
.change-button:hover {
	opacity: 0.8;
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
