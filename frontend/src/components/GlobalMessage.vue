<template>
	<!--メッセージエリア -->
	<div id="messages">
		<b-alert
			variant="danger"
			:show="message.dismissCountDown"
			v-show="message.error"
			dismissible
			@dismissed="message.dismissCountDown = 0"
			@dismiss-count-down="countDownChanged"
			fade
			style="z-index: 2000;"
			class="mb-0 position-fixed fixed-top"
		>
			{{ message.error }}
			<b-progress
				variant="danger"
				:max="message.dismissSecs"
				:value="message.dismissCountDown"
				height="4px"
			></b-progress>
		</b-alert>

		<b-alert
			variant="warning"
			:show="message.dismissCountDown"
			v-show="message.warnings.length"
			dismissible
			@dismissed="message.dismissCountDown = 0"
			@dismiss-count-down="countDownChanged"
			fade
			style="z-index: 2000;"
			class="mb-0 position-fixed fixed-top"
		>
			<p v-for="warning in message.warnings" :key="warning" class="mb-0">
				{{ warning }}
			</p>
			<b-progress
				variant="warning"
				:max="message.dismissSecs"
				:value="message.dismissCountDown"
				height="4px"
			></b-progress>
		</b-alert>

		<b-alert
			variant="info"
			:show="message.dismissCountDown"
			v-show="message.info"
			dismissible
			@dismissed="message.dismissCountDown = 0"
			@dismiss-count-down="countDownChanged"
			fade
			style="z-index: 2000;"
			class="mb-0 position-fixed fixed-top"
		>
			{{ message.info }}
			<b-progress
				variant="info"
				:max="message.dismissSecs"
				:value="message.dismissCountDown"
				height="4px"
			></b-progress>
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
	methods: {
		countDownChanged(dismissCountDown) {
			this.$store.commit("message/countDownChanged", dismissCountDown);
		},
	},
	mounted() {},
};
</script>
