<template>
	<div>
		<h1 class="my-5">アカウント連携</h1>

		<div>
			<template v-if="this.providers['google-oauth2']">
				<div @click="disconnect" class="btn btn-warning">
					Google連携解除
				</div>
				<p v-if="!this.allowedToDisconnect">
					連携を解除をするには他のサービスと連携するか､パスワードを設定して下さい｡
				</p>
			</template>
			<template v-else>
				<div class="btn btn-success">
					Google連携
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
		disconnect() {
			// 連携解除可能か判別
			if (!this.allowedToDisconnect) return;

			this.$store.dispatch("socialAuth/disconnect", {
				provider: "google-oauth2",
			});
		},
	},
	watch: {},
	mounted() {
		this.$store.dispatch("socialAuth/getAssociatedServices");
	},
	updated() {},
};
</script>
<style scoped></style>
