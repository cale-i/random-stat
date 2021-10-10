<template>
	<div id="home-page" class="homepage">
		<GlobalHeader />

		<GlobalMessage />

		<router-view />

		<GlobalFooter />
	</div>
</template>

<script>
import GlobalHeader from "@/components/GlobalHeader.vue";
import GlobalMessage from "@/components/GlobalMessage.vue";
import GlobalFooter from "@/components/GlobalFooter.vue";

// import { mapGetters } from 'vuex'

export default {
	components: {
		GlobalHeader,
		GlobalMessage,
		GlobalFooter,
	},
};
</script>

<style scoped>
.homepage {
	height: 100vh;
	background-color: #f8f9fa;
}
</style>
