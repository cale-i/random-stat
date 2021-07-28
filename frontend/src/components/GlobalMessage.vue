<template>
	<!--メッセージエリア -->
	<div id="messages">
		<b-alert
			variant="danger"
			show="3"
			dismissible
			fade
			v-show="message.error"
			class="mb-0"
		>
			{{ message.error }}
		</b-alert>

		<b-alert
			variant="warning"
			show
			dismissible
			fade
			v-show="message.warnings.length > 0"
			class="mb-0"
		>
			<p v-for="warning in message.warnings" :key="warning" class="mb-0">
				{{ warning }}
			</p>
		</b-alert>

		<b-alert
			variant="info"
			show
			v-show="message.info"
			dismissible
			fade
			class="mb-0"
		>
			{{ message.info }}
		</b-alert>
	</div>
</template>

<script>
export default {
	data() {
		return {};
	},
	computed: {
		message: function() {
			return this.$store.state.message;
		},
	},
	methods: {},
};
</script>
