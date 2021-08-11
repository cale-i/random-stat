import Vue from "vue";
import Vuex from "vuex";
import api from "@/services/api";

Vue.use(Vuex);

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
		username: "",
		isLoggedIn: false,
	},
	getters: {
		email: (state) => state.email,
		username: (state) => state.username,
		isLoggedIn: (state) => state.isLoggedIn,
	},
	mutations: {
		setUserData(state, payload) {
			state.email = payload.user.email;
			state.username = payload.user.username;
			state.isLoggedIn = true;
		},
		clearUserData(state) {
			state.email = "";
			state.username = "";
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
				// storeのユーザー情報を更新
				const user = response.data;
				context.commit("setUserData", { user });

				// ユーザーアバターの読み込み
				store.dispatch("avatar/reload");

				console.log(user);
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
					data: {
						current_password: payload.current_password,
					},
				})
				.then((response) => {
					console.log("deleted");
					console.log(response);
					context.dispatch("logout");
				});
			// .catch((response) => {
			// console.log("response", response);
			// });
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
		dismissSecs: 5,
		dismissCountDown: 0,
	},

	getters: {
		error: (state) => state.error,
		warnings: (state) => state.warnings,
		info: (state) => state.info,
		dismissSecs: (state) => state.dismissSecs,
		dismissCountDown: (state) => state.dismissCountDown,
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
			state.dismissCountDown = 0;
		},
		setAlertTimer(state) {
			// Alertのタイマーを設定
			state.dismissCountDown = state.dismissSecs;
		},
		countDownChanged(state, dismissCountDown) {
			// Alertのカウントダウンを制御
			state.dismissCountDown = dismissCountDown;
		},
	},

	actions: {
		// Errorメッセージ表示
		setErrorMessage(context, payload) {
			context.commit("clearMessages");
			context.commit("setMessage", { error: payload.message });
			context.commit("setAlertTimer");
		},

		// Warningメッセージ(複数)表示
		setWarningMessage(context, payload) {
			context.commit("clearMessages");
			context.commit("setMessage", { warnings: payload.message });
			context.commit("setAlertTimer");
		},

		// Infoメッセージ表示
		setInfoMessage(context, payload) {
			context.commit("clearMessages");
			context.commit("setMessage", { info: payload.message });
			context.commit("setAlertTimer");
		},
		clearAllMessages(content) {
			content.commit("clearMessages");
		},
	},
};

// アバター関連
const avatarModule = {
	strict: process.env.NODE_ENV !== "production",
	namespaced: true,
	state: {
		isDefaultImage: true,
		imageURL: null,
	},
	getters: {
		imageURL: (state) => state.imageURL,
		isDefaultImage: (state) => state.isDefaultImage,
	},
	mutations: {
		setImageURL(state, response) {
			state.imageURL =
				process.env.NODE_ENV === "production"
					? response.data.image_url
					: `http://localhost:8000${response.data.image_url}`;
		},
		setIsDefaultImage(state, response) {
			state.isDefaultImage = response.data.is_default_image;
		},
	},
	actions: {
		uploadImage(context, payload) {
			return api.post("/user-profile/avatar/", payload.formData).then(() => {
				context.dispatch("reload");
			});
		},
		deleteImage(context) {
			return api.delete("/user-profile/avatar/").then(() => {
				context.dispatch("reload");
			});
		},
		reload(context) {
			return api.get("/user-profile/avatar/").then((response) => {
				context.commit("setImageURL", response);
				context.commit("setIsDefaultImage", response);

				return response;
			});
		},
	},
};

const store = new Vuex.Store({
	modules: {
		chart: chartModule,
		auth: authModule,
		message: messageModule,
		avatar: avatarModule,
	},
});

export default store;
