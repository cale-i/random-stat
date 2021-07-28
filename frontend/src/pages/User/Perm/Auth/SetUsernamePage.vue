<template>
	<div class="container">
		<b-row>
			<b-col md=12>
				ユーザー名: {{ user.username }}
			</b-col>
		</b-row>

		<main class="form-signin">
			<b-form @submit.prevent="submitSetUsername">
				<h1 class="h3 mb-3 fw-normal">ユーザー名変更</h1>
				<label for="inputUsername" class="sr-only"></label>
				<input type="text" 
					id="inputUsername"
					class="form-control"
					v-model="form.newUsername"
					placeholder="新しいユーザー名"
					required
					autofocus
				>
				<b-button class="mt-3 w-100 btn btn-lg " variant="primary" type="submit">
					ユーザー名変更
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
			newUsername: '',
		},
	}),
	computed: {},
	methods: {
		async getUserData() {
			const user = await this.$store.dispatch('auth/getUserData')
			this.user = user
		},
		submitSetUsername() {
			this.$store.dispatch('auth/setUsername', {
				username: this.form.newUsername,
			})
				.then(() => {
					console.log('username changed!')
					const next = this.$route.query.next || '/dashboard/user'
					this.$router.replace(next)
				})
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
