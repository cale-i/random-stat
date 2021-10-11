<template>
	<div>
		<GlobalHeader />
		<GlobalMessage />
		<ResetPasswordConfirmationModal />
		<ResetEmailConfirmationModal />
		{{ resultMessage }}
		<GlobalFooter />
	</div>
</template>

<script>
import GlobalMessage from "@/components/GlobalMessage.vue";
import GlobalHeader from "@/components/GlobalHeader.vue";

import ResetPasswordConfirmationModal from "@/components/account/auth/ResetPasswordConfirmationModal.vue";
import ResetEmailConfirmationModal from "@/components/account/auth/ResetEmailConfirmationModal.vue";
import GlobalFooter from "@/components/GlobalFooter.vue";

export default {
	components: {
		GlobalMessage,
		GlobalHeader,
		ResetPasswordConfirmationModal,
		ResetEmailConfirmationModal,
		GlobalFooter,
	},
	props: {},
	data: () => ({
		resultMessage: "確認中",
		actions: {
			userActivation: "activate",
			resetPasswordConfirmation: "password",
			resetEmailConfirmation: "email",
		},
	}),
	computed: {},
	methods: {
		getAction() {
			// URLから処理を分岐
			// 次の3つの候補がある
			// 1, '/activate/{uid}/{token}'
			// 2, '/password/reset/confirm/{uid}/{token}'
			// 3, '/email/reset/confirm/{uid}/{token}'

			// [
			// 	"",
			// 	"password", <= ここの文字列で処理を決定する
			// 	"reset",
			// 	"confirm",
			// 	uid,
			// 	token,
			// ];
			let pathname = window.location.pathname.split("/");
			if (pathname.length < 2) {
				return null;
			}
			return pathname[1];
		},
		userActivation() {
			this.$store
				.dispatch("activation/activate", {
					uid: this.$route.params.uid,
					token: this.$route.params.token,
				})
				.then((response) => {
					console.log(response);
					this.resultMessage = "アクティベーションを完了しました｡";
					this.$store.dispatch("message/setInfoMessage", {
						message: "アクティベーション完了",
					});
					// 現在のページが"/"でない場合"/"に移動
					if (window.location.pathname !== "/") {
						this.$router.replace("/");
					}
				})
				.catch((response) => {
					console.log(response);
					this.resultMessage = "アクティベーションに失敗しました｡";
				});
		},
		resetPasswordConfirmation() {
			// モーダル表示
			this.$bvModal.show("resetPasswordConfirmationModal");
		},
		resetEmailConfirmation() {
			// モーダル表示
			this.$bvModal.show("resetEmailConfirmationModal");
		},
	},
	watch: {},
	mounted() {
		// 処理を分岐
		const action = this.getAction();
		if (action === this.actions.userActivation) {
			// ユーザーアクティベーション処理
			this.userActivation();
		}
		if (action === this.actions.resetPasswordConfirmation) {
			// パスワード再設定処理
			this.resetPasswordConfirmation();
		}
		if (action === this.actions.resetEmailConfirmation) {
			this.resetEmailConfirmation();
		}
	},
	updated() {},
};
</script>
<style scoped></style>
