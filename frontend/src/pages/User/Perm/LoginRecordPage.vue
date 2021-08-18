<template>
	<div>
		<b-row class="record-title my-5">
			<b-col>IPアドレス </b-col>
			<b-col>ログイン時刻 </b-col>
			<b-col>ログアウト時刻 </b-col>
		</b-row>
		<hr />
		<div v-for="record in records" :key="record.login_time">
			<b-row class="record-item my-4">
				<b-col>
					{{ record.ip_address }}
				</b-col>
				<b-col>
					{{ record.login_time | formatDateTime }}
				</b-col>
				<b-col>
					<template v-if="record.logout_time">
						{{ record.logout_time | formatDateTime }}
					</template>
					<template v-else>
						ログイン中
					</template>
				</b-col>
			</b-row>
			<hr />
		</div>
	</div>
</template>

<script>
export default {
	components: {},
	props: {},
	data: () => ({}),
	computed: {
		records() {
			return this.$store.getters["loginRecord/records"];
		},
	},
	methods: {},
	watch: {},
	mounted() {
		this.$store.dispatch("loginRecord/getRecord");
	},
	updated() {},
};
</script>
<style scoped>
.record-title {
	font-size: 1.6em;
}
.record-item {
	font-size: 1.4em;
}
</style>
