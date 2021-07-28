<template>
	<div>
		<GlobalHeader />
		<GlobalMessage />
		<GlobalSidebar />
		<div>
			<div class="row">
				<div class="col-md-3"></div>
				<div class="main col-md-9">
					<b-row>
						<b-col md="4">
							<h1>ダッシュボード</h1>
							<b-button variant="primary" @click="logout">logout</b-button>
						</b-col>
						<b-col md="4">
							<router-link to="/dashboard">root</router-link>
						</b-col>
						<b-col md="4">
							<router-link to="/dashboard/user">user</router-link>
						</b-col>
					</b-row>

					<b-row>
						<router-view />
					</b-row>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import GlobalMessage from "@/components/GlobalMessage.vue";
import GlobalHeader from "@/components/GlobalHeader.vue";
import GlobalSidebar from "@/components/GlobalSidebar.vue";

export default {
	components: {
		GlobalMessage,
		GlobalHeader,
		GlobalSidebar,
	},
	props: {},
	data: () => ({
		user: {},
	}),
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
	// updated() {
	//   this.makeSelected();
	// },
};
</script>
<style scoped></style>
