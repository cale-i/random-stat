<template>
	<div>
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
					<h4 class="text-center my-2 font-weight-bold">ログイン</h4>

					<hr />
					<template v-if="lastLoginType['google-oauth2']">
						<div class="last-login-box">
							<b-row>
								<p class="last-login-caption">
									前回のログイン
								</p>
							</b-row>
							<b-row
								class="last-login-button google-login"
								@click="login('google-oauth2')"
							>
								<b-icon icon="google" aria-hidden="true"></b-icon>
								<div>Google</div>
							</b-row>
							<b-row>
								<p class="last-login-reset" @click="resetLastLoginType">
									前回のログイン情報をリセット
								</p>
							</b-row>
						</div>
					</template>
					<template v-else>
						<div class="button google-login" @click="login('google-oauth2')">
							<b-icon icon="google" aria-hidden="true"></b-icon>
							<div>Google</div>
						</div>
					</template>

					<template v-if="lastLoginType['github']">
						<div class="last-login-box">
							<b-row>
								<p class="last-login-caption">
									前回のログイン
								</p>
							</b-row>
							<b-row
								class="last-login-button github-login"
								@click="login('github')"
							>
								<b-icon icon="github" aria-hidden="true"></b-icon>
								<div>GitHub</div>
							</b-row>
							<b-row>
								<p class="last-login-reset" @click="resetLastLoginType">
									前回のログイン情報をリセット
								</p>
							</b-row>
						</div>
					</template>
					<template v-else>
						<div class="button github-login" @click="login('github')">
							<b-icon icon="github" aria-hidden="true"></b-icon>
							<div>GitHub</div>
						</div>
					</template>

					<template v-if="lastLoginType['facebook']">
						<div class="last-login-box">
							<b-row>
								<p class="last-login-caption">
									前回のログイン
								</p>
							</b-row>
							<b-row
								class="last-login-button facebook-login"
								@click="login('facebook')"
							>
								<b-icon icon="facebook" aria-hidden="true"></b-icon>
								<div>Facebook</div>
							</b-row>
							<b-row>
								<p class="last-login-reset" @click="resetLastLoginType">
									前回のログイン情報をリセット
								</p>
							</b-row>
						</div>
					</template>
					<template v-else>
						<div class="button facebook-login" @click="login('facebook')">
							<b-icon icon="facebook" aria-hidden="true"></b-icon>
							<div>Facebook</div>
						</div>
					</template>

					<hr />

					<template v-if="lastLoginType.email">
						<div class="last-login-box">
							<b-row>
								<p class="last-login-caption">
									前回のログイン
								</p>
							</b-row>
							<b-row
								class="last-login-button email-login"
								v-b-modal.emailLoginModal
							>
								<b-icon icon="envelope-fill" aria-hidden="true"></b-icon>
								<div>メールアドレス</div>
							</b-row>
							<b-row>
								<p class="last-login-reset" @click.stop="resetLastLoginType">
									前回のログイン情報をリセット
								</p>
							</b-row>
						</div>
					</template>
					<template v-else>
						<div v-b-modal.emailLoginModal class="button email-login">
							<b-icon icon="envelope-fill" aria-hidden="true"></b-icon>
							<div>メールアドレス</div>
						</div>
					</template>

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
	data: () => ({
		modalId: "loginModal",
	}),
	computed: {
		lastLoginType() {
			return this.$store.getters["auth/lastLoginType"];
		},
	},
	methods: {
		login(provider) {
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
		resetLastLoginType() {
			if (confirm("前回のログイン情報をリセットします｡よろしいですか?")) {
				localStorage.removeItem("lastLoginType");
				this.$store.commit("auth/resetLastLoginType");
			}
		},
	},
	watch: {},
	mounted() {
		this.$store.commit("auth/setLastLoginType");
	},
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

.last-login-box {
	position: relative;

	justify-content: center;
	align-items: center;
	height: 7rem;
	margin: 2rem 2rem;
	margin-bottom: 1rem;
	user-select: none;
	border: 1px solid #dbdbdb;
}
.last-login-caption {
	position: absolute;
	top: 0;
	left: 50%;
	transform: translateY(-50%) translateX(-50%);

	background: #f8f9fa;
	font-size: 0.8rem;
	margin: 0;
	font-weight: bold;
}
.last-login-button {
	justify-content: center;
	color: white;
	align-items: center;
	font-size: 1rem;
	margin: 1.2rem auto 1rem auto;
	align-items: center;
	height: 2.8rem;
	width: 90%;
}
.last-login-reset {
	font-size: 0.5rem;
	margin: auto;
	color: #666;
	border-bottom: 1px solid #666;
}
.last-login-reset:hover {
	color: black;
	font-weight: bold;
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
.button:hover,
.last-login-button:hover {
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
.facebook-login {
	background: #1877f2;
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
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
