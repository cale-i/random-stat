<template>
	<div>
		<h1 class="my-5">アカウント連携</h1>

		<div>
			<template v-if="this.providers['google-oauth2']">
				<div class="button google" @click="disconnect('google-oauth2')">
					<b-icon icon="google" aria-hidden="true"></b-icon>
					<div>Google連携解除</div>
				</div>
				<p v-if="!this.allowedToDisconnect">
					連携を解除をするには他のサービスと連携するか､パスワードを設定して下さい｡
				</p>
			</template>
			<template v-else>
				<div
					class="button google disconnected"
					@click="connect('google-oauth2')"
				>
					<b-icon icon="google" aria-hidden="true"></b-icon>
					<div>Google連携</div>
				</div>
			</template>

			<template v-if="this.providers['github']">
				<div class="button github" @click="disconnect('github')">
					<b-icon icon="github" aria-hidden="true"></b-icon>
					<div>Github連携解除</div>
				</div>
				<p v-if="!this.allowedToDisconnect">
					連携を解除をするには他のサービスと連携するか､パスワードを設定して下さい｡
				</p>
			</template>
			<template v-else>
				<div class="button github disconnected" @click="connect('github')">
					<b-icon icon="github" aria-hidden="true"></b-icon>
					<div>Github連携</div>
				</div>
			</template>

			<template v-if="this.providers['twitter']">
				<div class="button twitter" @click="disconnect('twitter')">
					<b-icon icon="twitter" aria-hidden="true"></b-icon>
					<div>Twitter連携解除</div>
				</div>
				<p v-if="!this.allowedToDisconnect">
					連携を解除をするには他のサービスと連携するか､パスワードを設定して下さい｡
				</p>
			</template>
			<template v-else>
				<div class="button twitter disconnected" @click="connect('twitter')">
					<b-icon icon="twitter" aria-hidden="true"></b-icon>
					<div>Twitter連携</div>
				</div>
			</template>
		</div>
	</div>
</template>

<script>
export default {
	components: {},
	props: {},
	data: () => ({}),
	computed: {
		providers() {
			return this.$store.getters["socialAuth/providers"];
		},
		allowedToDisconnect() {
			// パスワード設定済み OR 連携サービス数2以上 => true
			const validPassword = this.$store.getters["auth/validPassword"];
			const numAssociatedService = Object.keys(this.providers).length;

			return validPassword || numAssociatedService > 1;
		},
	},
	methods: {
		connect(provider) {
			// アカウント連携
			this.$store.dispatch("socialAuth/authenticate", {
				provider,
				action: "connect",
			});
		},
		disconnect(provider) {
			// 連携解除可能か判別
			if (!this.allowedToDisconnect) return;

			this.$store
				.dispatch("socialAuth/disconnect", {
					provider,
				})
				.then(() => {
					this.$store.dispatch("message/setInfoMessage", {
						message: "アカウント連携を解除しました｡",
					});
				});
		},
		complete() {
			// アカウント連携
			// 認証後のリダイレクトを処理する
			console.log("in comp");
			const regex = /account\/social\/connect\//;
			const pathname = window.location.pathname;
			if (!pathname.match(regex)) {
				return;
			}

			this.$store
				.dispatch("socialAuth/connectComplete", {
					code: this.$route.query.code,
					state: this.$route.query.state,
					provider: this.$route.params.provider,
				})
				.then(() => {
					this.$store.dispatch("message/setInfoMessage", {
						message: "アカウント連携が完了しました｡",
					});

					// 元のページに移動
					this.$router.replace("/account/social/");
				});
		},
	},
	watch: {},
	async mounted() {
		await this.complete();
		this.$store.dispatch("socialAuth/getProviders");
	},
	updated() {},
};
</script>
<style scoped>
.button {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 4rem;
	font-size: 1.2rem;
	color: white;
	margin: 0.7rem auto;
	user-select: none;
	border-style: solid;
	width: 70%;
}

.button > svg {
	margin-right: 0.5rem;
}

.button:hover {
	background: white;
	color: black;
}

.google {
	background: #db4437;
	border-color: #db4437;
}
.google.disconnected > svg {
	color: #db4437;
}

.github {
	background: #333;
	border-color: #333;
}
.google.disconnected > svg {
	color: #db4437;
}

.twitter {
	background: #1da1f2;
	border-color: #1da1f2;
}
.twitter.disconnected > svg {
	color: #1da1f2;
}

.disconnected {
	background: white;
	color: black;
}

.google.disconnected:hover,
.google.disconnected:hover > svg {
	background: #db4437;
	color: white;
}

.github.disconnected:hover,
.github.disconnected:hover > svg {
	background: #333;
	color: white;
}
.twitter.disconnected:hover,
.twitter.disconnected:hover > svg {
	background: #1da1f2;
	color: white;
}
</style>
