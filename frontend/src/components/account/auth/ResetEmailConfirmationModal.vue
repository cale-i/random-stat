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
		<template #default="{}">
			<div class="card-body p-0">
				<h4 class="text-center my-2 font-weight-bold title">
					新しいメールアドレスの入力
				</h4>
				<b-form @submit.prevent="submitConfirmation">
					<b-form-group
						id="inputGroupNewEmail"
						label="New Email:"
						label-cols-md="4"
						label-align-md="right"
						label-for="inputNewEmail"
						class="my-4"
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
						label-cols-md="4"
						label-align-md="right"
						label-for="inputReNewEmail"
						class="mb-0"
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

					<div class="d-flex align-items-center justify-content-between mb-0">
						<div></div>
						<b-button size="md" class="change-button" type="submit">
							変更
						</b-button>
					</div>
				</b-form>
			</div>
		</template>
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
	background: #bd3f4c;
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
