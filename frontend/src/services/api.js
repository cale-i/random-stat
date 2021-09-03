import axios from "axios";
import store from "@/store";

export const api = axios.create({
	baseURL: process.env.VUE_APP_ROOT_API,
	timeout: 5000,
	withCredentials: true,
	headers: {
		"Content-Type": "application/json",
		"X-Requested-With": "XMLHttpRequest",
	},
});
// 共通前処理
api.interceptors.request.use(
	async function(config) {
		// メッセージをクリア
		// ログアウト時のメッセージが表示されないため
		// エラー時にのみクリアするよう変更
		// store.dispatch("message/clearAllMessages");
		// 認証用トークンがあればリクエストヘッダに乗せる
		let token = localStorage.getItem("access");

		if (token === "undefined") return config;
		if (!token) return config;

		// 認証用トークンの有効期限を確認し､有効期限切れの場合はリフレッシュトークンを発行
		if (isExpired(token)) {
			// 認証用トークンが有効期限切れの場合の処理
			await store.dispatch("auth/refresh");
			token = localStorage.getItem("access");
		}

		config.headers.Authorization = `JWT ${token}`;
		return config;
	},
	function(error) {
		return Promise.reject(error);
	}
);

// 共通エラー処理
api.interceptors.response.use(
	function(response) {
		return response;
	},
	function(error) {
		// console.log("error.response", error.response);
		const status = error.response ? error.response.status : 500;

		// メッセージをクリア
		store.dispatch("message/clearAllMessages");

		// エラーの内容に応じてstoreのメッセージを更新
		let message;
		if (status === 400 || status === 415) {
			// バリデーション警告
			message = [].concat.apply([], Object.values(error.response.data));
			store.dispatch("message/setWarningMessage", { message });
		} else if (status === 401) {
			// 認証エラー
			const token = localStorage.getItem("access");
			if (token != null) {
				message = "ログイン有効期限切れ";
			} else {
				message = "認証エラー";
			}
			// ログアウト処理
			store.dispatch("auth/logout");
			// エラーメッセージ表示
			store.dispatch("message/setErrorMessage", {
				message,
			});

			// 現在のページが"/"でない場合"/"に移動
			if (window.location.pathname !== "/") {
				this.$router.replace("/");
			}
		} else if (status === 403) {
			// 権限エラー
			message = "権限エラー";
			store.dispatch("message/setErrorMessage", { message });
		} else {
			// その他のエラー
			message = "想定外のエラー";
			store.dispatch("message/setErrorMessage", { message });
		}
		return Promise.reject(error);
	}
);

export const refreshApi = axios.create({
	baseURL: process.env.VUE_APP_ROOT_API,
	timeout: 5000,
	withCredentials: true,
	headers: {
		"Content-Type": "application/json",
		"X-Requested-With": "XMLHttpRequest",
	},
});

const isExpired = (token) => {
	// tokenをデコード
	const base64Url = token.split(".")[1];
	const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
	token = JSON.parse(decodeURIComponent(escape(window.atob(base64))));

	const expirationTime = token.exp;
	// getTime関数はミリ秒で取得するため､秒に揃えるため1000で除す
	const nowTime = Math.floor(new Date().getTime() / 1000);

	return expirationTime <= nowTime;
};

export const socialApi = axios.create({
	baseURL: process.env.VUE_APP_ROOT_API,
	timeout: 5000,
	withCredentials: true,
	headers: {
		"Content-Type": "application/x-www-form-urlencoded",
	},
});
