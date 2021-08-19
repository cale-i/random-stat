<template>
	<b-container>
		<GlobalHeader />
		<GlobalMessage />
		<div class="container">
			<b-row align-v="baseline">
				<b-col md="3" class="bg-white mt-5">
					<aside class="mt-5 mb-3 sidebar">
						<b-row>
							<router-link to="settings" class="sidebar-item">
								アカウント管理
							</router-link>
						</b-row>
						<hr />
						<b-row>
							<router-link to="login-record" class="sidebar-item">
								ログイン履歴
							</router-link>
						</b-row>
					</aside>
				</b-col>
				<b-col></b-col>
				<b-col md="8" class="bg-white">
					<router-view />
				</b-col>
			</b-row>
		</div>
	</b-container>
</template>

<script>
import GlobalMessage from "@/components/GlobalMessage.vue";
import GlobalHeader from "@/components/GlobalHeader.vue";
export default {
	components: {
		GlobalMessage,
		GlobalHeader,
	},
	props: {},
	data: () => ({}),
	computed: {},
	methods: {},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped>
.sidebar-item {
	font-size: 1.6rem;
	color: black;
	padding-left: 1rem;
}
</style>
