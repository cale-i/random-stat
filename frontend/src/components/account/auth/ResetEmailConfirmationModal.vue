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
				<h4 class="text-center">新しいメールアドレスの入力</h4>
			</b-col>
			<b-col md="1"></b-col>
		</template>
		<template #default="{}">
			<div class="card-body">
				<b-form @submit.prevent="submitConfirmation">
					<b-form-group
						id="inputGroupNewEmail"
						label="New Email:"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputNewEmail"
						class="mt-5"
					>
						<b-form-input
							id="inputNewEmail"
							v-model="form.newEmail"
							type="email"
							required
							placeholder="新しいメールアドレス"
							autofocus
							autocomplete="true"
						></b-form-input>
					</b-form-group>

					<b-form-group
						id="inputGroupReNewEmail"
						label="Confirm:"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputReNewEmail"
						class="mb-2"
					>
						<b-form-input
							id="inputReNewEmail"
							v-model="form.reNewEmail"
							type="email"
							required
							placeholder="確認"
							autocomplete="true"
						></b-form-input>
						<b-form-valid-feedback :state="validation">
							<br />
						</b-form-valid-feedback>
						<b-form-invalid-feedback :state="validation">
							メールアドレスが一致しません｡
						</b-form-invalid-feedback>
					</b-form-group>

					<div
						class="d-flex align-items-center justify-content-between mt-2 mb-0"
					>
						<div></div>
						<b-button size="md" variant="success" type="submit">
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
		modalId: "resetEmailConfirmationModal",
		form: {
			newEmail: "",
			reNewEmail: "",
		},
	}),
	computed: {
		validation() {
			// rePasswordが空白の場合はvalidation error messageを表示させない｡
			if (!this.form.reNewEmail) return true;
			return this.form.newEmail === this.form.reNewEmail;
		},
	},
	methods: {
		submitConfirmation() {
			// confirm email
			if (this.form.newEmail !== this.form.reNewEmail) {
				console.log("メールアドレスが一致しません");
				return;
			}
			this.$store
				.dispatch("resetEmail/confirmation", {
					uid: this.$route.params.uid,
					token: this.$route.params.token,
					new_email: this.form.newEmail,
					re_new_email: this.form.reNewEmail,
				})
				.then((response) => {
					console.log(response);
					this.resultMessage = "メールアドレスを変更しました";
					this.$store.dispatch("message/setInfoMessage", {
						message: "メールアドレスを変更しました",
					});

					// 現在のページが"/"でない場合"/"に移動
					if (window.location.pathname !== "/") {
						this.$router.replace("/");
					}
				});
		},
	},
	watch: {},
	mounted() {},
};
</script>
<style scoped></style>
