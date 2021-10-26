<template>
	<div>
		<h1 class="my-5">アカウント管理</h1>
		<AvatarUpload />
		<b-overlay spinner-variant="success" :show="changingUsername" rounded="sm">
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
					<div
						size="md"
						@click="changeUsername"
						class="btn w-100 button rsbg-green"
					>
						ユーザー名変更
					</div>
				</b-col>
			</b-form-row>
		</b-overlay>
		<b-overlay
			spinner-variant="success"
			:show="sendingConfirmationEmail"
			rounded="sm"
		>
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
					<div
						@click="sendEmailChangeRequest"
						class="btn button rsbg-green w-100"
					>
						Email変更
					</div>
				</b-col>
			</b-form-row>
		</b-overlay>
		<template v-if="this.validPassword">
			<b-form-row class="my-3">
				<b-col md="3"> </b-col>
				<b-col md="6"> </b-col>
				<b-col md="3">
					<div
						v-b-modal.changePasswordModal
						class="btn button rsbg-green w-100"
					>
						パスワード変更
					</div>
				</b-col>
			</b-form-row>
		</template>
		<template v-else>
			<b-overlay spinner-variant="success" :show="sendingEmail" rounded="sm">
				<b-form-row class="my-3">
					<b-col md="3"> </b-col>
					<b-col md="6"> </b-col>
					<b-col md="3">
						<div @click="setPassword" class="btn button rsbg-green w-100">
							パスワード設定
						</div>
					</b-col>
				</b-form-row>
			</b-overlay>
		</template>

		<b-form-row class="my-3">
			<b-col md="3"> </b-col>
			<b-col md="6"> </b-col>
			<b-col md="3">
				<div
					v-b-modal.deleteAccountModal
					class="btn rsbg-red button w-100 mt-5"
				>
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
		changingUsername: false,
		sendingConfirmationEmail: false,
		sendingEmail: false,
	}),
	computed: {
		user: function() {
			return this.$store.state.auth;
		},
		validPassword() {
			return this.$store.getters["auth/validPassword"];
		},
		isGuestUser() {
			return this.$store.getters["auth/isGuestUser"];
		},
	},
	methods: {
		async changeUsername() {
			// ユーザー名変更結果が返るまでSpinner動かす
			this.changingUsername = true;

			await this.$store
				.dispatch("auth/setUsername", {
					username: this.user.username,
				})
				.then(() => {
					console.log("username changed!");
					this.$store.dispatch("message/setInfoMessage", {
						message: "ユーザー名を変更しました",
					});
				})
				.finally(() => {
					// Spinner停止
					this.changingUsername = false;
				});
		},
		async sendEmailChangeRequest() {
			// ゲストユーザーの場合処理なし
			if (this.isGuestUser) {
				alert("ゲストユーザーのメールアドレスは変更できません｡");
				return;
			}

			// パスワード未設定の場合は処理なし
			if (!this.validPassword) {
				alert("パスワードが未設定の場合､メールアドレスの変更はできません｡");
				return;
			}

			const confirmMsg =
				"メールアドレス変更リクエストを送信します｡よろしいですか?";
			if (confirm(confirmMsg) === false) {
				return;
			}

			// 確認メール送信完了までSpinner動かす
			this.sendingConfirmationEmail = true;

			// 変更リクエスト送信
			// 送信先メールアドレスは登録済みメールアドレスに限定する
			await this.$store
				.dispatch("resetEmail/sendEmail")
				.then(() => {
					this.isResettingEmail = true;
					this.$store.dispatch("message/setInfoMessage", {
						message:
							"メールアドレス変更リクエストを送信しました｡届いたメールから変更手続きを行って下さい｡",
					});
				})
				.finally(() => {
					// Spinner停止
					this.sendingConfirmationEmail = false;
				});
		},

		async setPassword() {
			// ゲストユーザーの場合処理なし
			if (this.isGuestUser) {
				alert("ゲストユーザーのパスワードは変更できません｡");
				return;
			}

			// 確認メール送信完了までSpinner動かす
			this.sendingEmail = true;

			const email = this.$store.getters["auth/email"];
			await this.$store
				.dispatch("socialAuth/setPasswordSendEmail", { email })
				.then(() => {
					console.log("success");
					this.$store.dispatch("message/setInfoMessage", {
						message: "確認メールを送信しました｡",
					});
				})
				.finally(() => {
					// Spinner停止
					this.sendingEmail = false;
				});
		},
	},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped>
.button {
	color: white;
	user-select: none;
}
.button:hover {
	opacity: 0.8;
}
.rsbg-green {
	background: #00a040;
}
.rsbg-red {
	background: #bd3f4c;
}
</style>
