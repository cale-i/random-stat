<template>
	<div id="header">
		<b-navbar type="dark" variant="dark" fixed="top">
			<b-navbar-brand href="/" class="navbar-brand">
				<b-icon icon="bar-chart-line" aria-hidden="true" class="mr-2"></b-icon>
				<span class="rs-green">R</span>andom <span class="rs-red">S</span>tat
			</b-navbar-brand>

			<b-navbar-nav class="ml-auto navbar-nav">
				<template v-if="isLoggedIn">
					<b-nav-item-dropdown no-caret right>
						<template #button-content>
							<img :src="avatar" class="avatar-image" alt="アバターイメージ" />
						</template>

						<b-dropdown-item to="/account/settings" class="account mb-3">
							<b-row>
								<b-col md="2">
									<img
										:src="avatar"
										class="avatar-image-md"
										alt="アバターイメージ"
									/>
								</b-col>
								<b-col md="10" class="pl-4">
									<div class="username text-truncate">{{ username }}</div>
									<span class="rs-green">アカウント設定</span>
								</b-col>
							</b-row>
						</b-dropdown-item>
						<hr />
						<b-dropdown-item-button @click="logout">
							<b-icon
								icon="power"
								aria-hidden="true"
								class="rs-red mr-1"
							></b-icon>
							<span class="rs-red">ログアウト</span>
						</b-dropdown-item-button>
					</b-nav-item-dropdown>
				</template>
				<template v-else>
					<b-nav-item v-b-modal.signUpModal class="signup">
						<b-icon icon="pen" aria-hidden="true" class="rs-red"></b-icon>
						アカウント作成
					</b-nav-item>
					<b-nav-item v-b-modal.loginModal class="login">
						<b-icon icon="person" aria-hidden="true" class="rs-green"></b-icon>
						ログイン
					</b-nav-item>
				</template>
			</b-navbar-nav>
		</b-navbar>

		<LoginModal />
		<SignUpModal />
		<ResetPasswordModal />
		<ResendActivationEmailModal />
	</div>
</template>

<script>
import SignUpModal from "@/components/account/auth/SignUpModal";
import LoginModal from "@/components/account/auth/LoginModal.vue";
import ResetPasswordModal from "@/components/account/auth/ResetPasswordModal.vue";
import ResendActivationEmailModal from "@/components/account/auth/ResendActivationEmailModal.vue";
export default {
	components: {
		SignUpModal,
		LoginModal,
		ResetPasswordModal,
		ResendActivationEmailModal,
	},
	props: {},
	data: () => ({}),
	computed: {
		isLoggedIn: function() {
			return this.$store.getters["auth/isLoggedIn"];
		},
		avatar() {
			return (
				this.$store.getters["avatar/imageURL"] ||
				this.$store.getters["avatar/socialImageURL"]
			);
		},
		username() {
			// 一定文字数で省略する
			return this.$store.getters["auth/username"];
		},
	},
	methods: {
		logout() {
			this.$store.dispatch("auth/logout");
			this.$store.dispatch("message/setInfoMessage", {
				message: "ログアウトしました。",
			});

			// 現在のページが"/"でない場合"/"に移動
			if (window.location.pathname !== "/") {
				this.$router.replace("/");
			}
		},
	},
	watch: {},
	mounted() {},
};
</script>

<style scoped>
#header {
	margin-bottom: 60px;
}
.navbar-brand {
	font-size: 1.5em;
}
.navbar-nav {
	font-size: 1.2em;
}
.avatar-image {
	width: 32px;
	height: 32px;
	border-radius: 50%;
}
.login,
.signup {
	font-weight: bold;
	user-select: none;
}
.account {
	width: 348px;
	user-select: none;
	font-size: 1.2rem;
}
.avatar-image-md {
	width: 50px;
	height: 50px;
	border-radius: 50%;
	padding: 0;
}
.account-text {
	padding: 0;
	margin: 0;
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
@media screen and (max-width: 640px) {
	.navbar-brand {
		font-size: 1rem;
	}
	.signup,
	.login {
		font-size: 0.5rem;
	}
}
@media screen and (max-width: 340px) {
	.navbar-brand {
		font-size: 0.9rem;
	}
	.signup,
	.login {
		font-size: 0.45rem;
	}
}
</style>
