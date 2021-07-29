<template>
	<div class="container">
		<h1>アカウント管理</h1>
		<b-row>
			<b-col></b-col>
			<b-col> ユーザー名: {{ user.username }} </b-col>
			<b-col>
				<router-link to="set-username" class="btn btn-primary"
					>ユーザー名変更</router-link
				>
			</b-col>
		</b-row>
		<b-row>
			<b-col></b-col>
			<b-col> email: {{ user.email }} </b-col>
			<b-col>
				<router-link to="set-email" class="btn btn-primary"
					>メールアドレス変更</router-link
				>
			</b-col>
		</b-row>
		<b-row>
			<b-col></b-col>
			<b-col>
				<input type="text" :placeholder="user.first_name" />
			</b-col>
			<b-col>
				<router-link to="set-email" class="btn btn-primary"
					>firstname変更</router-link
				>
			</b-col>
		</b-row>
		<b-row>
			<b-col></b-col>
			<b-col>
				<input type="text" :placeholder="user.last_name" />
			</b-col>
			<b-col>
				<router-link to="set-email" class="btn btn-primary"
					>lastname変更</router-link
				>
			</b-col>
		</b-row>
		<b-row>
			<b-col></b-col>
			<b-col> </b-col>
			<b-col>
				<router-link to="set-password" class="btn btn-primary"
					>パスワード変更</router-link
				>
			</b-col>
		</b-row>

		<b-row>
			<b-col md="8"></b-col>
			<b-col>
				<router-link to="delete-account" class="btn btn-warning"
					>アカウント削除</router-link
				>
			</b-col>
		</b-row>

		<b-button @click="getUser()">GetUser</b-button>
	</div>
</template>

<script>
export default {
	props: {},
	data: () => ({
		user: {
			username: "",
			first_name: "",
			last_name: "",
			email: "",
		},
	}),
	computed: {},
	methods: {
		async getUserData() {
			const user = await this.$store.dispatch("auth/getUserData");
			this.user = user;
		},
	},
	watch: {},
	mounted() {
		this.getUserData();
	},
	// updated() {
	//   this.makeSelected();
	// },
};
</script>
<style scoped></style>
