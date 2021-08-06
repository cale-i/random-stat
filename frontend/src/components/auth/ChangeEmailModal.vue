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
				<h4 class="text-center">メールアドレス変更</h4>
			</b-col>
			<b-col md="1"></b-col>
		</template>
		<template #default="{}">
			<div class="card-body">
				<b-form @submit.prevent="changeEmail">
					<b-form-group
						id="inputGroupEmail"
						label="New Email:"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputEmail"
					>
						<b-form-input
							id="inputEmail"
							v-model="form.newEmail"
							type="email"
							required
							autofocus
							autocomplete="true"
						></b-form-input>
					</b-form-group>

					<b-form-group
						id="inputGroupConfirmEmail"
						label="Confirm:"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputConfirmEmail"
					>
						<b-form-input
							id="inputConfirmEmail"
							v-model="form.confirmEmail"
							type="email"
							required
							autofocus
							autocomplete="true"
						></b-form-input>
					</b-form-group>

					<b-form-group
						id="inputGroupPassword"
						label="Password"
						label-cols-md="3"
						label-align-md="right"
						label-for="inputPassword"
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

					<div
						class="d-flex align-items-center justify-content-between mt-4 mb-0"
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
		modalId: "changeEmailModal",
		form: {
			newEmail: "",
			confirmEmail: "",
			password: "",
		},
	}),
	computed: {},
	methods: {
		changeEmail() {
			console.log(this.form);
			// todo
			// validation
			// user bootstrap util
			if (this.form.newEmail !== this.form.confirmEmail) {
				console.log("email validation error");
				return;
			}
			this.$store
				.dispatch("auth/setEmail", {
					new_email: this.form.newEmail,
					re_new_email: this.form.confirmEmail,
					current_password: this.form.password,
				})
				.then(() => {
					console.log("email changed!");
					// message
					this.$store.dispatch("message/setInfoMessage", {
						message: "メールアドレスを変更しました",
					});

					// Clear input data
					this.form = {
						newEmail: "",
						confirmEmail: "",
						password: "",
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
<style scoped>
html,
body {
	height: 100%;
}

body {
	display: -ms-flexbox;
	display: flex;
	-ms-flex-align: center;
	align-items: center;
	padding-top: 40px;
	padding-bottom: 40px;
	background-color: #f5f5f5;
}

.form-signin {
	width: 100%;
	max-width: 330px;
	padding: 15px;
	margin: auto;
}

.form-signin .checkbox {
	font-weight: 400;
}

.form-signin .form-floating:focus-within {
	z-index: 2;
}

.form-signin input[type="text"] {
	margin-bottom: -1px;
	border-bottom-right-radius: 0;
	border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
	margin-bottom: 10px;
	border-top-left-radius: 0;
	border-top-right-radius: 0;
}
</style>
