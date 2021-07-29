<template>
	<div>
		<b-row>
			<b-col md="4">
				<GlobalSidebar />
			</b-col>

			<b-col md="8">
				<h1>ダッシュボード ほめ</h1>
				aaa
			</b-col>
		</b-row>
		<b-row> </b-row>
	</div>
</template>

<script>
import GlobalSidebar from "@/components/GlobalSidebar.vue";

export default {
	components: {
		GlobalSidebar,
	},
	props: {},
	data: () => ({
		user: {},
	}),
	computed: {},
	methods: {},
	watch: {},
	mounted() {},
};
</script>
<style scoped></style>
