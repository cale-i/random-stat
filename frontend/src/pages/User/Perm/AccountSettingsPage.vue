<template>
	<div>
		<h1 class="my-5">アカウント管理</h1>
		<AvatarUpload />
		<b-form-row class="my-3">
			<b-col md="3">
				<label class="m-2" for="inputUsername">Username:</label>
			</b-col>
			<b-col md="6">
				<b-form-input
					id="inputUsername"
					v-model="user.username"
					type="text"
					required
					class=""
				></b-form-input>
			</b-col>
			<b-col md="3">
				<b-button
					size="md"
					variant="success"
					@click="changeUsername"
					class="w-100"
				>
					ユーザー名変更
				</b-button>
			</b-col>
		</b-form-row>

		<b-overlay :show="sendingConfirmationEmail" rounded="sm">
			<b-form-row class="my-3">
				<b-col md="3">
					<label class="m-2" for="inputEmail">Email:</label>
				</b-col>
				<b-col md="6">
					<b-form-input
						id="inputEmail"
						:placeholder="user.email"
						type="email"
						required
						class=""
						disabled
					></b-form-input>
				</b-col>
				<b-col md="3">
					<div @click="sendEmailChangeRequest" class="btn btn-success w-100">
						Email変更
					</div>
				</b-col>
			</b-form-row>
		</b-overlay>

		<b-form-row class="my-3">
			<b-col md="3"> </b-col>
			<b-col md="6"> </b-col>
			<b-col md="3">
				<div v-b-modal.changePasswordModal class="btn btn-success w-100">
					パスワード変更
				</div>
			</b-col>
		</b-form-row>

		<b-form-row class="my-3">
			<b-col md="3"> </b-col>
			<b-col md="6"> </b-col>
			<b-col md="3">
				<div v-b-modal.deleteAccountModal class="btn btn-danger w-100 mt-5">
					アカウント削除
				</div>
			</b-col>
		</b-form-row>
		<ChangePasswordModal />
		<DeleteAccountModal />
	</div>
</template>

<script>
import ChangePasswordModal from "@/components/account/auth/ChangePasswordModal.vue";
import DeleteAccountModal from "@/components/account/auth/DeleteAccountModal.vue";
import AvatarUpload from "@/components/account/AvatarUpload.vue";

export default {
	components: {
		ChangePasswordModal,
		DeleteAccountModal,
		AvatarUpload,
	},
	props: {},
	data: () => ({
		sendingConfirmationEmail: false,
	}),
	computed: {
		user: function() {
			return this.$store.state.auth;
		},
	},
	methods: {
		changeUsername() {
			console.log(this.user.username);

			this.$store
				.dispatch("auth/setUsername", {
					username: this.user.username,
				})
				.then(() => {
					console.log("username changed!");
					this.$store.dispatch("message/setInfoMessage", {
						message: "ユーザー名を変更しました",
					});
				});
		},
		sendEmailChangeRequest() {
			const confirmMsg =
				"メールアドレス変更リクエストを送信します｡よろしいですか?";
			if (confirm(confirmMsg) === false) {
				return;
			}

			// 変更リクエスト送信
			// 送信先メールアドレスは登録済みメールアドレスに限定する
			this.$store
				.dispatch("resetEmail/sendEmail")
				.then(() => {
					this.isResettingEmail = true;
					this.$store.dispatch("message/setInfoMessage", {
						message:
							"メールアドレス変更リクエストを送信しました｡届いたメールから変更手続きを行って下さい｡",
					});
					this.sendingConfirmationEmail = false;
				})
				.catch();
			this.sendingConfirmationEmail = true;
		},
	},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped></style>
