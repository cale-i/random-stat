<template>
	<div class="container">
		<b-row>
			<b-col md="4">
				<aside style="background-color:gray;">
					<h2>アカウント</h2>
					<h2>ログイン履歴</h2>
				</aside>
			</b-col>
			<b-col md="8">
				<h1 class="mb-5">アカウント管理</h1>
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
						<div v-b-modal.changeEmailModal class="btn btn-success w-100">
							Email変更
						</div>
					</b-col>
				</b-form-row>

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
			</b-col>
		</b-row>
		<ChangeEmailModal />
		<ChangePasswordModal />
		<DeleteAccountModal />
	</div>
</template>

<script>
import ChangeEmailModal from "@/components/account/auth/ChangeEmailModal.vue";
import ChangePasswordModal from "@/components/account/auth/ChangePasswordModal.vue";
import DeleteAccountModal from "@/components/account/auth/DeleteAccountModal.vue";

import AvatarUpload from "@/components/account/AvatarUpload.vue";

// import { mapGetters } from "vuex";

export default {
	components: {
		ChangeEmailModal,
		ChangePasswordModal,
		DeleteAccountModal,
		AvatarUpload,
	},
	props: {},
	data: () => ({}),
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
	},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped></style>
