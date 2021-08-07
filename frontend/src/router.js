import Vue from "vue";
import VueRouter from "vue-router";

import store from "@/store";

// import HomePage from "@/pages/HomePage";

// import LoginPage from "@/pages/User/LoginPage";
// import CreateAccountPage from "@/pages/User/CreateAccountPage";

import DashboardBasePage from "@/pages/User/Perm/DashboardBasePage";
import DashboardHomePage from "@/pages/User/Perm/DashboardHomePage";

import AccountPage from "@/pages/User/Perm/AccountPage";

Vue.use(VueRouter);

const router = new VueRouter({
	mode: "history",
	routes: [
		{
			path: "/",
			component: () =>
				import("@/pages/HomePage" /* webpackChunkName: "Home" */),
			name: "home",
		},
		// { path: "/login", component: LoginPage, name: "login" },
		// {path: "/create-account",component: CreateAccountPage,name: "create-account",},

		{
			path: "/dashboard",
			component: DashboardBasePage,
			meta: { requiresAuth: true },
			children: [
				{ path: "", component: DashboardHomePage },
				{ path: "account", component: AccountPage },
			],
		},
		{ path: "*", redirect: "/" },
	],
});

// 画面遷移の度に認証を確認
router.beforeEach((to, from, next) => {
	const isLoggedIn = store.getters["auth/isLoggedIn"];
	const token = localStorage.getItem("access");
	console.log("to.path=", to.path);
	console.log("isLoggedIn=", isLoggedIn);

	// ログインが必要な画面に遷移しようとした場合
	if (to.matched.some((record) => record.meta.requiresAuth)) {
		if (isLoggedIn) {
			// ログインしている場合
			console.log("already logged in");
			next();
		} else {
			// ログインしていない場合

			// 認証用トークンが残っていれば、ユーザー情報を再取得
			if (token != null) {
				console.log("not logged in, now trying to reload again");

				store
					.dispatch("auth/reload")
					.then(() => {
						// 再取得できた場合そのまま画面遷移
						console.log("success!");
						next();
					})
					.catch(() => {
						// 再取得できない場合ホーム画面へ
						forceToHome(to, from, next);
					});
			} else {
				// 認証用トークンがない場合は、ホーム画面へ
				forceToHome(to, from, next);
			}
		}
	} else {
		// ログインが不要な画面であればそのまま次へ
		next();
	}
});

// ホーム画面へ強制移動
function forceToHome(to, from, next) {
	console.log("force user to login page");
	next({
		path: "/",
		// 遷移先のURLはクエリ文字列として付加
		query: { next: to.fullPath },
	});
}

export default router;
