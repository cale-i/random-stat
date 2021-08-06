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
				<h4 class="text-center">パスワード変更</h4>
			</b-col>
			<b-col md="1"></b-col>
		</template>

		<template #default="{}">
			<div class="card-body">
				<b-form @submit.prevent="changePassword">
					<b-form-group
						id="inputGroupCurrentPassword"
						label="Current Password:"
						label-cols-md="4"
						label-align-md="right"
						label-for="inputCurrentPassword"
						class="mb-5"
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
		<template #modal-footer="{}">
			<div class="text-muted small">&copy; Random Stat 2021</div>
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
					console.log("password changed!");

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

					// モーダルウィンドウを閉じる
					this.$bvModal.hide(this.modalId);
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
