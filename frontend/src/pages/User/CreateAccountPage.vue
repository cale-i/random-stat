<template>
	<div id="create-account-page">
		<main class="form-signin">
			<b-form @submit.prevent="submitCreateAccount">
				<h1 class="h3 mb-3 fw-normal">ユーザー登録</h1>

				<label for="inputUsername" class="sr-only"></label>
				<input type="text" 
					id="inputUsername"
					class="form-control"
					v-model="form.username"
					placeholder="ユーザー名"
					autofocus
				>
				<label for="inputEmail" class="sr-only"></label>
				<input type="email" 
					id="inputEmail"
					class="form-control"
					v-model="form.email"
					placeholder="Email"
					required
					autofocus
				>
				<label for="inputPassword" class="sr-only"></label>
				<input type="password"
					id="inputPassword"
					class="form-control"
					v-model="form.password"
					placeholder="パスワード"
					required
				>
				<label for="inputRePassword" class="sr-only"></label>
				<input type="password"
					id="inputRePassword"
					class="form-control"
					v-model="form.rePassword"
					placeholder="パスワード再入力"
					required
				>
				<b-button class="mt-3 w-100 btn btn-lg " variant="primary" type="submit">
					登録
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
		form: {
			username: '',
			email: '',
			password: '',
			rePassword: '',
		},
	}),
	computed: {},
	methods: {
		submitCreateAccount() {
			// ログイン
			this.$store.dispatch('auth/createAccount', {
				username: this.form.username,
				email: this.form.email,
				password: this.form.password,
				rePassword: this.form.rePassword,
			})
				.then(response => {
					if (response) {
						console.log('success')
						// クエリ文字列に「next」がなければログイン画面へ
						const next = this.$route.query.next || '/login'
						this.$router.replace(next)

					}
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
  margin-bottom: 10px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="email"] {
  margin-bottom: 10px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
