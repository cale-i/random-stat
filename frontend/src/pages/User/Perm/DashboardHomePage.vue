<template>
	<div>
		<b-row>
			<b-col md="4">
			<h1>ダッシュボード ほめ</h1>
            aaa
			</b-col>
		</b-row>
		<b-row>
		</b-row>
	</div>
</template>

<script>
export default {
	props: {

	},
	data: () => ({
		user: {

		},
	}),
	computed: {},
	methods: {
		logout () {
			this.$store.dispatch('auth/logout')
				.then(() => {
					console.log('success logout')
					// クエリ文字列に「next」がなければホーム画面へ
					const next = this.$route.query.next || '/'
					this.$router.replace(next)
				})
		},
	},
	watch: {
	},
	mounted() {

	},
	// updated() {
	//   this.makeSelected();
	// },
};
</script>
<style scoped>

</style>
