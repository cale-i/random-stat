import Vue from "vue";
import Vuex from "vuex";
import { api, refreshApi } from "@/services/api";

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
		validPassword: true,
		lastLoginType: {
			"google-oauth2": false,
			github: false,
			twitter: false,
			email: false,
		},
	},
	getters: {
		email: (state) => state.email,
		username: (state) => state.username,
		isLoggedIn: (state) => state.isLoggedIn,
		validPassword: (state) => state.validPassword,
		lastLoginType: (state) => state.lastLoginType,
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
		setValidPassword(state, payload) {
			// payload === response.data
			state.validPassword = payload.valid_password;
		},
		setLastLoginType(state) {
			const lastLoginType = localStorage.getItem("lastLoginType");
			if (lastLoginType) state.lastLoginType[lastLoginType] = true;
		},
		resetLastLoginType(state) {
			state.lastLoginType = {
				"google-oauth2": false,
				github: false,
				twitter: false,
				email: false,
			};
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
					// 有効なパスワードが設定されているかを判別
					context.commit("setValidPassword", response.data);
					//ユーザー情報を取得してstoreのユーザー情報を更新
					const user = context.dispatch("reload");
					// 前回のログイン情報を保存
					context.commit("resetLastLoginType");
					localStorage.setItem("lastLoginType", "email");

					return user;
				});
		},
		guestLogin(context) {
			return api.post("/auth/jwt/create/guest/").then((response) => {
				// 認証用トークンをlocalStorageに保存
				localStorage.setItem("access", response.data.access);
				// 有効なパスワードが設定されているかを判別
				context.commit("setValidPassword", response.data);
				//ユーザー情報を取得してstoreのユーザー情報を更新
				store.dispatch("auth/reload");

				// メッセージ表示
				store.dispatch("message/setInfoMessage", {
					message: "ログインしました。",
				});
			});
		},
		// logout/
		logout(context) {
			// server side ログアウト処理
			refreshApi.post("/auth/jwt/logout/");
			// 認証用トークンをlocalStorageから削除
			localStorage.removeItem("access");
			// storeのユーザー情報をクリア
			context.commit("clearUserData");
		},
		// Refresh Token
		refresh(context) {
			return refreshApi
				.post("/auth/jwt/refresh/")
				.then((response) => {
					// 認証用トークンをlocalStorageに保存
					localStorage.setItem("access", response.data.access);
					// 有効なパスワードが設定されているか
					context.commit("setValidPassword", response.data);
				})
				.catch(() => {
					// localStorageに保存されている認証用トークンを削除
					localStorage.removeItem("access");
					// storeのユーザー情報をクリア
					context.commit("clearUserData");
				});
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
				.then(() => {
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
				.then(() => {
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

				return user;
			});
		},
		// アカウント作成
		createAccount(context, payload) {
			return api
				.post("/auth/users/", {
					username: payload.username,
					email: payload.email,
					password: payload.password,
					re_password: payload.rePassword,
				})
				.then((response) => {
					const user = response.data;
					return user;
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
				.then(() => {
					context.dispatch("logout");
				});
			// .catch((response) => {
			// console.log("response", response);
			// });
		},
		updateField(context, payload) {
			// patch操作は同一URIに対し、
			// { User.FIELDS_TO_UPDATE: VALUE } 形式のparamを送るため抽象化
			return api.patch("/auth/users/me/", payload).then(() => {
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
		socialImageURL: null,
	},
	getters: {
		imageURL: (state) => state.imageURL,
		socialImageURL: (state) => state.socialImageURL,
		isDefaultImage: (state) => state.isDefaultImage,
	},
	mutations: {
		setImageURL(state, response) {
			state.imageURL = response.data.image_url;
		},
		setSocialImageURL(state, response) {
			state.socialImageURL = response.data.social_image_url;
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
				context.commit("setSocialImageURL", response);
				context.commit("setIsDefaultImage", response);

				return response;
			});
		},
	},
};
// ログイン履歴
const loginRecordModule = {
	strict: process.env.NODE_ENV !== "production",
	namespaced: true,
	state: {
		records: [],
	},
	getters: {
		records: (state) => state.records,
	},
	mutations: {
		setRecord(state, payload) {
			state.records = payload.data;
		},
	},
	actions: {
		getRecord(context) {
			api.get("/auth/record/login/").then((response) => {
				context.commit("setRecord", response);
			});
		},
	},
};

const activationModule = {
	strict: process.env.NODE_ENV !== "production",
	namespaced: true,
	state: {},
	getters: {},
	mutations: {},
	actions: {
		activate(context, payload) {
			return api.post("/auth/users/activation/", {
				uid: payload.uid,
				token: payload.token,
			});
		},
	},
};
// パスワード再設定
const resetPasswordModule = {
	strict: process.env.NODE_ENV !== "production",
	namespaced: true,
	state: {},
	getters: {},
	mutations: {},
	actions: {
		sendEmail(context, payload) {
			return api.post("/auth/users/reset_password/", { email: payload.email });
		},
		confirmation(context, payload) {
			return api
				.post("/auth/users/reset_password_confirm/", {
					uid: payload.uid,
					token: payload.token,
					new_password: payload.new_password,
					re_new_password: payload.re_new_password,
				})
				.then(() => {
					store.dispatch("auth/logout");
				});
		},
	},
};
// メールアドレス再設定
const resetEmailModule = {
	strict: process.env.NODE_ENV !== "production",
	namespaced: true,
	state: {},
	getters: {},
	mutations: {},
	actions: {
		sendEmail() {
			const email = store.getters["auth/email"];
			return api.post("/auth/users/reset_email/", { email });
		},
		confirmation(context, payload) {
			return api
				.post("/auth/users/reset_email_confirm/", {
					uid: payload.uid,
					token: payload.token,
					new_email: payload.new_email,
					re_new_email: payload.re_new_email,
				})
				.catch();
		},
	},
};
// ソーシャル認証
const socialAuthModule = {
	strict: process.env.NODE_ENV !== "production",
	namespaced: true,
	state: {
		providers: {
			"google-oauth2": false,
			github: false,
		},
	},
	getters: {
		providers: (state) => state.providers,
	},
	mutations: {
		setProviders(state, payload) {
			const providers = payload.providers;
			if (providers === undefined) return;

			providers.map((arr) => {
				state.providers[arr.provider] = true;
			});
		},
		initProviders(state) {
			state.providers["google-oauth2"] = false;
			state.providers["github"] = false;
		},
	},
	actions: {
		authenticate(context, payload) {
			const pathname = `/social/o/${payload.provider}/`;
			const url = `/auth/social/o/${payload.provider}/`;

			const redirect_uri = `${window.location.origin}${pathname}`;
			return api
				.get(url, {
					params: {
						redirect_uri,
					},
				})
				.then((response) => {
					window.location.href = response.data.authorization_url;
				});
		},
		authComplete(context, payload) {
			const formData = new URLSearchParams();
			formData.append("code", payload.code);
			formData.append("state", payload.state);

			return api
				.post(`/auth/social/o/${payload.provider}/`, formData, {
					headers: {
						"Content-Type": "application/x-www-form-urlencoded",
						"X-Requested-With": "XMLHttpRequest",
					},
				})
				.then((response) => {
					console.log("in authComplete");
					if (response.data.access) {
						// アカウント登録
						console.log("in register in authComplete");

						// 認証用トークンをlocalStorageに保存
						localStorage.setItem("access", response.data.access);
						// 有効なパスワードが設定されているか
						store.commit("auth/setValidPassword", response.data);
						//ユーザー情報を取得してstoreのユーザー情報を更新
						store.dispatch("auth/reload");
						// 前回のログイン情報を保存
						store.commit("auth/resetLastLoginType");
						localStorage.setItem("lastLoginType", payload.provider);

						return { next: "/dashboard", message: "ログインしました｡" };
					} else {
						// アカウント連携
						console.log("in connect in authComplete");

						context.dispatch("getProviders");
						return {
							next: "/account/social",
							message: "アカウントを連携しました｡",
						};
					}
				});
		},
		disconnect(context, payload) {
			api
				.post(`/auth/social/disconnect/${payload.provider}/`)
				.then((response) => {
					context.commit("initProviders");
					context.commit("setProviders", response.data);
				});
		},
		getProviders(context) {
			// 連携済みサービス一覧を取得
			api.get("/auth/social/services/").then((response) => {
				context.commit("initProviders");
				context.commit("setProviders", response.data);
				store.commit("auth/setValidPassword", response.data);
			});
		},
		setPasswordSendEmail(context, payload) {
			return api.post("/auth/social/users/set_password/", {
				email: payload.email,
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
		loginRecord: loginRecordModule,
		activation: activationModule,
		resetPassword: resetPasswordModule,
		resetEmail: resetEmailModule,
		socialAuth: socialAuthModule,
	},
});

export default store;
