<template>
	<div>
		<b-modal
			:id="mordalId"
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
					<b-icon
						icon="bar-chart-line"
						aria-hidden="true"
						class="mr-2"
					></b-icon>
					<div>
						<span class="rs-green">R</span>andom
						<span class="rs-red">S</span>tat
					</div>
				</div>
			</template>
			<template #default="{}">
				<div class="p-0">
					<h4 class="text-center my-2 font-weight-bold">アカウント登録</h4>

					<hr />

					<div class="button google-signup" @click="signup('google-oauth2')">
						<b-icon icon="google" aria-hidden="true"></b-icon>
						<div>Google</div>
					</div>
					<div class="button github-signup" @click="signup('github')">
						<b-icon icon="github" aria-hidden="true"></b-icon>
						<div>GitHub</div>
					</div>
					<div class="button facebook-signup" @click="signup('facebook')">
						<b-icon icon="facebook" aria-hidden="true"></b-icon>
						<div>Facebook</div>
					</div>

					<hr />

					<div v-b-modal.emailSignUpModal class="button email-signup">
						<b-icon icon="envelope-fill" aria-hidden="true"></b-icon>
						<div>メールアドレス</div>
					</div>

					<hr />

					<div v-b-modal.loginModal class="button login">
						<b-icon icon="pencil-square" aria-hidden="true"></b-icon>
						<div>アカウントをお持ちの方</div>
					</div>
				</div>
			</template>
			<template #modal-footer="{}">
				<div class="d-flex justify-content-center flex-grow-1 text-muted small">
					Random Stat 2021
				</div>
			</template>
		</b-modal>
		<EmailSignUpModal />
	</div>
</template>

<script>
import EmailSignUpModal from "@/components/account/auth/EmailSignUpModal.vue";
export default {
	components: {
		EmailSignUpModal,
	},
	props: {},
	data: () => ({
		mordalId: "signUpModal",
	}),
	computed: {},
	methods: {
		signup(provider) {
			this.$store.dispatch("socialAuth/authenticate", {
				provider,
			});
		},
		guestLogin() {
			this.$store.dispatch("auth/guestLogin").then(() => {
				// クエリ文字列に「next」がなければホーム画面へ
				const next = this.$route.query.next || "/";
				if (next === "/") {
					// モーダルウィンドウを閉じる
					this.$bvModal.hide(this.modalId);
				} else {
					// window.location.href = next;
					this.$router.replace(next);
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
.google-signup {
	background: #db4437;
}
.github-signup {
	background: #333;
}
.facebook-signup {
	background: #1877f2;
}
.twitter-signup {
	background: #1da1f2;
}
.email-signup {
	background: #00a040;
}
.login {
	background: #bd3f4c;
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
