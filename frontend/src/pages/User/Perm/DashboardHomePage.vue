<template>
	<b-container>
		<b-row>
			<b-col md="4">
				<GlobalSidebar />
			</b-col>

			<b-col md="8">
				<h1>ダッシュボード ほめ</h1>
				<p v-b-modal.modal-login>Launch centered modal</p>

				<b-modal id="modal-login" centered title="BootstrapVue">
					<p class="my-4">Vertically centered modal!</p>
				</b-modal>

				<b-button v-b-modal.modal-login>
					<b-icon icon="person" aria-hidden="true"></b-icon>
					Login
				</b-button>
				<b-modal id="modal-login">
					test
				</b-modal>
			</b-col>
		</b-row>
		<b-row> </b-row>
	</b-container>
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
