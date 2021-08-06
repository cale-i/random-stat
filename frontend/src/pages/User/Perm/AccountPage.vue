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
				<h1>アカウント管理</h1>
				<b-form-row class="username my-3">
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
						<b-button size="md" variant="success" @click="changeUsername">
							変更
						</b-button>
					</b-col>
				</b-form-row>

				<b-form-row class="email my-3">
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
						<div v-b-modal.changeEmailModal class="btn btn-success">
							変更
						</div>
					</b-col>
				</b-form-row>

				<b-row>
					<b-col></b-col>
					<b-col> </b-col>
					<b-col>
						<div v-b-modal.changePasswordModal class="btn btn-primary">
							パスワード変更
						</div>
					</b-col>
				</b-row>

				<b-row>
					<b-col md="8"></b-col>
					<b-col>
						<router-link to="delete-account" class="btn btn-warning"
							>アカウント削除</router-link
						>
					</b-col>
				</b-row>
			</b-col>
		</b-row>
		<ChangeEmailModal />
		<ChangePasswordModal />
	</div>
</template>

<script>
import ChangeEmailModal from "@/components/auth/ChangeEmailModal.vue";
import ChangePasswordModal from "@/components/auth/ChangePasswordModal.vue";

// import { mapGetters } from "vuex";

export default {
	components: {
		ChangeEmailModal,
		ChangePasswordModal,
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
	mounted() {
		// this.getUserData();
	},
	updated() {},
};
</script>
<style scoped></style>
