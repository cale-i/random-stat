<template>
	<!--メッセージエリア -->
	<div id="messages">
		<b-alert
			:show="message.dismissCountDown"
			v-show="message.error"
			dismissible
			@dismissed="message.dismissCountDown = 0"
			@dismiss-count-down="countDownChanged"
			fade
			style="z-index: 2000;"
			class="mb-0 position-fixed fixed-top alert error"
		>
			{{ message.error }}
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
			class="mb-0 position-fixed fixed-top alert warning"
		>
			<p v-for="warning in message.warnings" :key="warning" class="mb-0">
				{{ warning }}
			</p>
		</b-alert>

		<b-alert
			:show="message.dismissCountDown"
			v-show="message.info"
			dismissible
			@dismissed="message.dismissCountDown = 0"
			@dismiss-count-down="countDownChanged"
			fade
			style="z-index: 2000;"
			class="mb-0  position-fixed fixed-top alert info"
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
	methods: {
		countDownChanged(dismissCountDown) {
			this.$store.commit("message/countDownChanged", dismissCountDown);
		},
	},
	mounted() {},
};
</script>
<style scoped>
.alert {
	left: unset;
	color: white;
	border: 0;
	margin-top: 62px;
	max-width: 300px;
	user-select: none;
	font-weight: bold;
	overflow-wrap: break-word;
	text-align: left;
}
.error {
	background: #bd3f4c;
}
.warning {
	background: #ffc107;
	color: black;
	max-width: 600px;
}
.info {
	background: #00a040;
}
</style>
