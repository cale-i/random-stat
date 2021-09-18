<template>
	<b-container>
		<b-row>
			<b-col md="4">
				<GlobalSidebar />
			</b-col>
			<b-button @click="refresh">refresh</b-button>
		</b-row>
		<StatHistoryPage />
	</b-container>
</template>

<script>
import GlobalSidebar from "@/components/GlobalSidebar.vue";
import StatHistoryPage from "@/pages/User/Perm/StatHistoryPage.vue";

export default {
	components: {
		GlobalSidebar,
		StatHistoryPage,
	},
	props: {},
	data: () => ({
		user: {},
	}),
	computed: {},
	methods: {
		refresh() {
			this.$store.dispatch("auth/refresh");
		},
	},
	watch: {},
	mounted() {},
};
</script>
<style scoped></style>
