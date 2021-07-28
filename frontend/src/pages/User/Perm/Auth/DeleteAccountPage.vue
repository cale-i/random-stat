<template>
	<div id="delete-account-page" class="container">
		<main class="form-signin">
			<b-form @submit.prevent="deleteAccount">
				<h1 class="h3 mb-3 fw-normal">アカウント削除</h1>

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
					placeholder="再入力"
					required
				>
				<b-button class="mt-3 w-100 btn btn-lg " variant="warning" type="submit">
					削除
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
			currentPassword: '',
			reCurrentPassword: '',
		},
	}),
	computed: {},
	methods: {
		deleteAccount() {
			if (this.form.currentPassword !== this.form.reCurrentPassword) {
				console.log('パスワード不一致')
				return
			}
			const res = confirm('削除します。よろしいですか')
			console.log(res)
			if (res === false) {
				return
			}

			this.$store.dispatch('auth/deleteAccount', {
				current_password : this.form.currentPassword
				})
				.then(()=> {
					console.log('アカウントを削除しました')
					// クエリ文字列に「next」がなければホーム画面へ
					const next = this.$route.query.next || '/'
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
