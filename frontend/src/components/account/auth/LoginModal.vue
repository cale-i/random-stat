<template>
	<div>
		<b-modal
			id="loginModal"
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
					<b-icon icon="bar-chart-line" aria-hidden="true"></b-icon>
					<div class="ml-2">Random Stat</div>
				</div>
			</template>
			<template #default="{}">
				<div class="p-0">
					<h4 class="text-center my-2 font-weight-bold">ログイン</h4>

					<hr />

					<div class="button google-login" @click="googleLogin">
						<b-icon icon="google" aria-hidden="true"></b-icon>
						<div>Google</div>
					</div>
					<div class="button github-login">
						<b-icon icon="github" aria-hidden="true"></b-icon>
						<div>GitHub</div>
					</div>
					<div class="button twitter-login">
						<b-icon icon="twitter" aria-hidden="true"></b-icon>
						<div>Twitter</div>
					</div>

					<hr />

					<div v-b-modal.emailLoginModal class="button email-login">
						<b-icon icon="envelope-fill" aria-hidden="true"></b-icon>
						<div>メールアドレス</div>
					</div>
					<div class="button guest-login" @click="guestLogin">
						<b-icon icon="person-circle" aria-hidden="true"></b-icon>
						<div>ゲストログイン</div>
					</div>
					<hr />

					<div v-b-modal.signUpModal class="button sign-up">
						<b-icon icon="pencil-square" aria-hidden="true"></b-icon>
						<div>アカウント登録</div>
					</div>
				</div>
			</template>
			<template #modal-footer="{}">
				<div class="d-flex justify-content-center flex-grow-1 text-muted small">
					Random Stat 2021
				</div>
			</template>
		</b-modal>
		<EmailLoginModal />
	</div>
</template>

<script>
import EmailLoginModal from "@/components/account/auth/EmailLoginModal.vue";
export default {
	components: {
		EmailLoginModal,
	},
	props: {},
	data: () => ({}),
	computed: {},
	methods: {
		googleLogin() {
			this.$store.dispatch("socialAuth/googleLogin");
		},
		guestLogin() {
			this.$store.dispatch("auth/guestLogin").then(() => {
				// クエリ文字列に「next」がなければダッシュボード画面へ
				const next = this.$route.query.next || "/dashboard";
				this.$router.replace(next);
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
.button {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 3rem;
	font-size: 1.2rem;
	color: white;
	margin: 0.5rem 2rem;
	user-select: none;
}
.button:hover {
	opacity: 0.8;
}
.button > svg {
	margin-right: 0.5rem;
}
.google-login {
	background: #db4437;
}
.github-login {
	background: #333;
}
.twitter-login {
	background: #1da1f2;
}
.email-login {
	background: #00a040;
}
.guest-login {
	background: gray;
}
.sign-up {
	background: #bd3f4c;
}
</style>
