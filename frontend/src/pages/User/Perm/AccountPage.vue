<template>
	<div>
		<GlobalHeader />
		<GlobalMessage />
		<div class="container">
			<b-row>
				<b-col md="4">
					<aside class="mt-5">
						<b-row>
							<router-link to="settings" class="sidebar-item">
								アカウント管理
							</router-link>
						</b-row>
						<b-row>
							<router-link to="login-record" class="sidebar-item">
								ログイン履歴
							</router-link>
						</b-row>
					</aside>
				</b-col>
				<b-col md="8">
					<router-view />
				</b-col>
			</b-row>
		</div>
	</div>
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
	font-size: 2rem;
	color: black;
}
</style>
