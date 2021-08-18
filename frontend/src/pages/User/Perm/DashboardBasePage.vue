<template>
	<div>
		<GlobalHeader />
		<GlobalMessage />

		<router-view />
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
<style scoped></style>
