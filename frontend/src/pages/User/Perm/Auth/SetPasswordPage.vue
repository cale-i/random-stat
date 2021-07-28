<template>
	<div class="container">
		<b-row>
			<b-col md=12>
				ユーザー名: {{ user.username }}
			</b-col>
		</b-row>

		<main class="form-signin">
			<b-form @submit.prevent="submitSetUsername">
				<h1 class="h3 mb-3 fw-normal">パスワード変更</h1>
				<label for="inputCurrentPassword" class="sr-only"></label>
				<input type="password" 
					id="inputCurrentPassword"
					class="form-control"
					v-model="form.currentPassword"
					placeholder="現在のパスワード"
					required
					autofocus
				>
				<label for="inputRePassword" class="sr-only"></label>
				<input type="password"
					id="inputRePassword"
					class="form-control"
					v-model="form.newPassword"
					placeholder="新しいパスワード"
					required
				>
				<label for="inputReNewPassword" class="sr-only"></label>
				<input type="password"
					id="inputReNewPassword"
					class="form-control"
					v-model="form.reNewPassword"
					placeholder="新しいパスワード"
					required
				>
				<b-button class="mt-3 btn btn-md " variant="warning" type="submit">
					変更
				</b-button>

				<p class="mt-5 mb-3 text-muted">&copy; 2021</p>
			</b-form>
		</main>
	</div>
</template>

<script>
export default {
	props: {

	},
	data: () => ({
		user: {
			username: '',
		},
		form: {
			newPassword: '',
			reNewPassword: '',
			currentPassword: '',

		},
	}),
	computed: {},
	methods: {
		submitSetUsername () {
			this.$store.dispatch('auth/setPassword', {
				new_password: this.form.newPassword,
				re_new_password: this.form.reNewPassword,
				current_password: this.form.currentPassword,
			})
				.then(() => {
					console.log('password changed!')
					// クエリ文字列に「next」がなければホーム画面へ
					const next = this.$route.query.next || '/dashboard/user'
					this.$router.replace(next)
				})
		},
		async getUserData() {
			const user = await this.$store.dispatch('auth/getUserData')
			this.user = user
		},
	},
	watch: {
	},
	mounted() {
		this.getUserData()
	},
	// updated() {
	//   this.makeSelected();
	// },
};
</script>
<style scoped>
html,
body {
  height: 100%;
}

body {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signin .checkbox {
  font-weight: 400;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="text"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
