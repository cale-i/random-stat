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
				<h4 class="text-center">アカウント削除</h4>
			</b-col>
			<b-col md="1"></b-col>
		</template>

		<template #default="{}">
			<div class="card-body">
				<b-form @submit.prevent="deleteAccount">
					<b-form-group
						id="inputGroupPassword"
						label="Password:"
						label-cols-md="4"
						label-align-md="right"
						label-for="inputPassword"
						class="mt-5"
					>
						<b-form-input
							id="inputPassword"
							v-model="form.currentPassword"
							type="password"
							placeholder="パスワード"
							required
						></b-form-input>
					</b-form-group>

					<b-form-group
						id="inputGroupConfirmPassword"
						label="Confirm:"
						label-cols-md="4"
						label-align-md="right"
						label-for="inputConfirmPassword"
					>
						<b-form-input
							id="inputConfirmPassword"
							v-model="form.reCurrentPassword"
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

					<div class="d-flex align-items-center justify-content-between mb-0">
						<div></div>
						<b-button size="md" variant="danger" type="submit">
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
		modalId: "deleteAccountModal",

		form: {
			username: "",
			email: "",
			currentPassword: "",
			reCurrentPassword: "",
		},
	}),
	computed: {
		validation() {
			// rePasswordが空白の場合はvalidation error messageを表示させない｡
			if (!this.form.reCurrentPassword) return true;
			return this.form.currentPassword === this.form.reCurrentPassword;
		},
	},
	methods: {
		deleteAccount() {
			// password validation
			if (this.form.currentPassword !== this.form.reCurrentPassword) {
				console.log("パスワード不一致");
				return;
			}

			// 確認
			// const res = confirm("削除します。よろしいですか");
			// console.log(res);
			// if (!res) return;

			// 削除実行
			this.$store
				.dispatch("auth/deleteAccount", {
					current_password: this.form.currentPassword,
				})
				.then(() => {
					console.log("アカウントを削除しました｡");
					this.$store.dispatch("message/setInfoMessage", {
						message: "アカウントを削除しました｡",
					});
					// ホーム画面へ
					this.$router.replace("/");
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
