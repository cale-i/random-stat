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
		<b-overlay spinner-variant="danger" :show="deletingAccount" rounded="sm">
			<template #default="{}">
				<div class="card-body p-0">
					<h4 class="text-center my-2 font-weight-bold title">
						アカウント削除
					</h4>
					<b-form @submit.prevent="deleteAccount">
						<b-form-group
							id="inputGroupPassword"
							label="Password:"
							label-cols-md="4"
							label-align-md="right"
							label-for="inputPassword"
							class="my-4"
						>
							<b-form-input
								id="inputPassword"
								v-model="form.currentPassword"
								type="password"
								placeholder="パスワード"
								required
								autocomplete="true"
							></b-form-input>
						</b-form-group>

						<b-form-group
							id="inputGroupConfirmPassword"
							label="Confirm:"
							label-cols-md="4"
							label-align-md="right"
							label-for="inputConfirmPassword"
							class="mb-0"
						>
							<b-form-input
								id="inputConfirmPassword"
								v-model="form.reCurrentPassword"
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
							<b-button size="md" class="delete-button" type="submit">
								削除
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
		modalId: "deleteAccountModal",

		form: {
			username: "",
			email: "",
			currentPassword: "",
			reCurrentPassword: "",
		},
		deletingAccount: false,
	}),
	computed: {
		validation() {
			// rePasswordが空白の場合はvalidation error messageを表示させない｡
			if (!this.form.reCurrentPassword) return true;
			return this.form.currentPassword === this.form.reCurrentPassword;
		},
		isGuestUser() {
			return this.$store.getters["auth/isGuestUser"];
		},
	},
	methods: {
		async deleteAccount() {
			// ゲストユーザーの場合処理なし
			if (this.isGuestUser) {
				alert("ゲストユーザーのアカウントは削除できません｡");
				return;
			}
			// password validation
			if (this.form.currentPassword !== this.form.reCurrentPassword) {
				console.log("パスワード不一致");
				return;
			}

			// 確認
			if (!confirm("アカウントを削除します。よろしいですか")) return;

			// 削除中Spinner動かす
			this.deletingAccount = true;

			// 削除実行
			await this.$store
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
				})
				.finally(() => {
					// Spinner停止
					this.deletingAccount = false;
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
.delete-button {
	background: #bd3f4c;
}
.delete-button:hover {
	opacity: 0.8;
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
