<template>
	<div id="header">
		<b-navbar type="dark" variant="dark" fixed="top">
			<b-navbar-brand href="/" class="navbar-brand">
				<b-icon icon="bar-chart-line" aria-hidden="true"></b-icon>
				Random Stat
			</b-navbar-brand>

			<b-navbar-nav class="ml-auto navbar-nav">
				<template v-if="isLoggedIn">
					<b-nav-item @click="logout" active-class="active">
						<b-icon icon="power" aria-hidden="true"></b-icon>
						Logout
					</b-nav-item>
				</template>

				<template v-else>
					<b-nav-item v-b-modal.loginModal>
						<b-icon icon="person" aria-hidden="true"></b-icon>
						Login
					</b-nav-item>
					<LoginModal />
				</template>

				<b-nav-item-dropdown no-caret right>
					<template #button-content>
						<b-icon icon="list" aria-hidden="true"></b-icon>
					</template>

					<template v-if="isLoggedIn">
						<b-dropdown-item to="/dashboard">
							<b-icon icon="house-door" aria-hidden="true"></b-icon>
							Dashboard
						</b-dropdown-item>

						<b-dropdown-item to="/dashboard/account">
							<b-icon icon="gear" aria-hidden="true"></b-icon>
							Account
						</b-dropdown-item>

						<b-dropdown-divider></b-dropdown-divider>

						<b-dropdown-item-button @click="logout" variant="info">
							<b-icon icon="power" aria-hidden="true"></b-icon>
							Logout
						</b-dropdown-item-button>
					</template>

					<template v-else>
						<b-dropdown-item v-b-modal.loginModal variant="success">
							<b-icon icon="person" aria-hidden="true"></b-icon>
							Login
						</b-dropdown-item>
						<LoginModal />
					</template>
				</b-nav-item-dropdown>
			</b-navbar-nav>
		</b-navbar>
	</div>
</template>

<script>
import LoginModal from "@/components/auth/LoginModal.vue";

export default {
	components: {
		LoginModal,
	},
	props: {},
	data: () => ({}),
	computed: {
		isLoggedIn: function() {
			return this.$store.getters["auth/isLoggedIn"];
		},
	},
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
