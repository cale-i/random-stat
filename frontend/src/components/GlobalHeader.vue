<template>
	<div id="header">
		<b-navbar type="dark" variant="dark" fixed="top">
			<b-navbar-brand href="/" class="navbar-brand">
				<b-icon icon="bar-chart-line" aria-hidden="true"></b-icon>
				Random Stat
			</b-navbar-brand>

			<b-navbar-nav class="ml-auto">
				<b-nav-item to="/login" active-class="active">
					<b-icon icon="person-fill" aria-hidden="true"></b-icon>
					Login
				</b-nav-item>

				<b-nav-item-dropdown no-caret right>
					<template #button-content>
						<b-icon icon="list" aria-hidden="true"></b-icon>
					</template>
					<b-dropdown-item-button to="/account">
						<b-icon icon="person-fill" aria-hidden="true"></b-icon>
						Account
					</b-dropdown-item-button>

					<b-dropdown-item-button @click="logout" variant="info">
						<b-icon icon="power" aria-hidden="true"></b-icon>
						Logout
					</b-dropdown-item-button>
				</b-nav-item-dropdown>
			</b-navbar-nav>
		</b-navbar>
	</div>
</template>

<script>
export default {
	components: {},
	props: {},
	data: () => ({}),
	computed: {},
	methods: {
		logout() {
			this.$store.dispatch("auth/logout");
			this.$store.dispatch("message/setInfoMessage", {
				message: "ログアウトしました。",
			});

			console.log("success logout");

			// クエリ文字列に「next」がなければホーム画面へ
			// const next = this.$route.query.next || "/";
			this.$router.replace("/login");
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
</style>
