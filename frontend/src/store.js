import Vue from "vue";
import Vuex from "vuex";
import api from "@/services/api";

Vue.use(Vuex);

const itemModule = {
	namespaced: true,
	state: {
		getURL: "list/books/",
		postURL: "post/books/",
		updateURL: "update/books/",
		deleteURL: "delete/books/",
	},
	getters: {
		getURL: (state) => state.getURL,
		postURL: (state) => state.postURL,
		updateURL: (state) => state.updateURL,
		deleteURL: (state) => state.deleteURL,
	},
	mutations: {},
	actions: {
		retlieve(context) {
			return api({
				method: "get",
				url: context.getters.getURL,
			}).then((response) => {
				return response.data;
			});
		},
		create(context, payload) {
			return api({
				method: "post",
				url: context.getters.postURL,
				data: {
					title: payload.title,
					price: payload.price,
				},
			}).then((response) => {
				return response.data;
			});
		},
		put(context, payload) {
			return api({
				method: "put",
				url: context.getters.updateURL + payload.id + "/",
				data: {
					id: payload.id,
					title: payload.title,
					price: payload.price,
					created_at: payload.created_at,
				},
			});
		},
		delete(context, payload) {
			return api({
				method: "delete",
				url: context.getters.deleteURL + payload.item.id + "/",
			}).then((response) => {
				return response;
			});
		},
	},
};
const chartModule = {
	namespaced: true,
	state: {
		chartURL: "timeseries/",
		searchURL: "search/",
		searchStatsCodeURL: "search/statscode/",
	},
	getters: {
		chartURL: (state) => state.chartURL,
		searchURL: (state) => state.searchURL,
		searchStatsCodeURL: (state) => state.searchStatsCodeURL,
	},
	mutations: {},
	actions: {
		getChart(context) {
			return api({
				method: "get",
				url: context.getters.chartURL,
			}).then((response) => {
				return response.data;
			});
		},
		searchChart(context, data) {
			return api({
				method: "post",
				url: context.getters.searchURL,
				data,
			}).then((response) => {
				return response.data;
			});
		},
		searchStatsCodeChart(context, data) {
			return api({
				method: "post",
				url: context.getters.searchStatsCodeURL,
				data,
			}).then((response) => {
				return response.data;
			});
		},
	},
};
// 認証
const authModule = {
	strict: process.env.NODE_ENV !== "production",
	namespaced: true,
	state: {
		email: "",
		isLoggedIn: false,
	},
	getters: {
		email: (state) => state.email,
		isLoggedIn: (state) => state.isLoggedIn,
	},
	mutations: {
		setUserData(state, payload) {
			state.email = payload.user.email;
			state.isLoggedIn = true;
		},
		clearUserData(state) {
			state.email = "";
			state.isLoggedIn = false;
		},
	},
	actions: {
		// login
		login(context, payload) {
			return api
				.post("/auth/jwt/create/", {
					email: payload.email,
					password: payload.password,
				})
				.then((response) => {
					// 認証用トークンをlocalStorageに保存
					localStorage.setItem("access", response.data.access);
					//ユーザー情報を取得してstoreのユーザー情報を更新
					const user = context.dispatch("reload");
					return user;
				});
		},
		// logout/
		logout(context) {
			// 認証用トークンをlocalStorageから削除
			localStorage.removeItem("access");
			// storeのユーザー情報をクリア
			context.commit("clearUserData");
			console.log("logouted");
		},
		setEmail(context, payload) {
			// ユーザー名変更
			console.log(payload);
			return api
				.post("/auth/users/set_email/", {
					new_email: payload.new_email,
					re_new_email: payload.re_new_email,
					current_password: payload.current_password,
				})
				.then((response) => {
					console.log(response);
					return context.dispatch("reload");
				});
		},
		setUsername(context, payload) {
			// console.log(payload)
			const response = context.dispatch("updateField", {
				username: payload.username,
			});
			// console.log(response)
			return response;
		},
		setPassword(context, payload) {
			// パスワード変更
			return api
				.post("/auth/users/set_password/", {
					new_password: payload.new_password,
					re_new_password: payload.re_new_password,
					current_password: payload.current_password,
				})
				.then((response) => {
					console.log(response);
					return context.dispatch("reload");
				});
		},
		// ユーザー情報更新
		reload(context) {
			return api.get("/auth/users/me/").then((response) => {
				const user = response.data;
				// storeのユーザー情報を更新
				context.commit("setUserData", { user });
				console.log(user);
				return user;
			});
		},
		// ユーザー情報取得
		getUserData() {
			return api.get("/auth/users/me/").then((response) => {
				const user = response.data;
				// storeのユーザー情報を更新
				return user;
			});
		},
		// アカウント作成
		createAccount(context, payload) {
			console.log(payload);
			return api
				.post("/auth/users/", {
					username: payload.username,
					email: payload.email,
					password: payload.password,
					re_password: payload.rePassword,
				})
				.then((response) => {
					const user = response.data;
					console.log(user);
					return user;
				})
				.catch((response) => {
					console.log(response);
					return undefined;
				});
		},
		// アカウント削除
		deleteAccount(context, payload) {
			return api
				.delete("/auth/users/me/", {
					current_password: payload.current_password,
				})
				.then((response) => {
					console.log("deleted");
					console.log(response);
					context.dispatch("logout");
				})
				.catch((response) => {
					console.log(response);
				});
		},
		updateField(context, payload) {
			// patch操作は同一URIに対し、
			// { User.FIELDS_TO_UPDATE: VALUE } 形式のparamを送るため抽象化
			return api.patch("/auth/users/me/", payload).then((response) => {
				console.log("updated!");
				console.log(response);
				return context.dispatch("reload");
			});
		},
		getUser() {
			return api.get("/get-user/me/").then((response) => {
				return response;
			});
		},
	},
};

// グローバルメッセージ
const messageModule = {
	strict: process.env.NODE_ENV !== "production",
	namespaced: true,

	state: {
		error: "",
		warnings: [],
		info: "",
	},

	getters: {
		error: (state) => state.error,
		warnings: (state) => state.warnings,
		info: (state) => state.info,
	},

	mutations: {
		setMessage(state, payload) {
			if (payload.error) {
				state.error = payload.error;
			}
			if (payload.warnings) {
				state.warnings = payload.warnings;
			}
			if (payload.info) {
				state.info = payload.info;
			}
		},
		clearMessages(state) {
			state.error = "";
			state.warnings = [];
			state.info = "";
		},
	},

	actions: {
		// Errorメッセージ表示
		setErrorMessage(context, payload) {
			context.commit("clearMessages");
			context.commit("setMessage", { error: payload.message });
		},

		// Warningメッセージ(複数)表示
		setWarningMessage(context, payload) {
			context.commit("clearMessages");
			context.commit("setMessage", { warnings: payload.message });
		},

		// Infoメッセージ表示
		setInfoMessage(context, payload) {
			context.commit("clearMessages");
			context.commit("setMessage", { info: payload.message });
		},
		clearAllMessages(content) {
			content.commit("clearMessages");
		},
	},
};

const store = new Vuex.Store({
	modules: {
		item: itemModule,
		chart: chartModule,
		auth: authModule,
		message: messageModule,
	},
});

export default store;
