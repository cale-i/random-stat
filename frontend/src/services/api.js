import axios from "axios";
import store from "@/store";

const api = axios.create({
	baseURL: process.env.VUE_APP_ROOT_API,
	timeout: 5000,
	headers: {
		"Content-Type": "application/json",
		"X-Requested-With": "XMLHttpRequest",
	},
});

// 共通前処理
const commonPreProcessFulfill = function(config) {
	// メッセージをクリア
	// ログアウト時のメッセージが表示されないため
	// エラー時にのみクリアするよう変更
	// store.dispatch("message/clearAllMessages");
	// 認証用トークンがあればリクエストヘッダに乗せる
	const token = localStorage.getItem("access");
	if (token) {
		config.headers.Authorization = `JWT ${token}`;
		return config;
	}
	return config;
};
const commonPreProcessReject = function(error) {
	return Promise.reject(error);
};
api.interceptors.request.use(commonPreProcessFulfill, commonPreProcessReject);

// 共通エラー処理
const commonResponseProcessFulfill = function(response) {
	return response;
};
const commonResponseProcessReject = function(error) {
	// console.log("error.response", error.response);
	const status = error.response ? error.response.status : 500;
	console.log(status);

	// メッセージをクリア
	store.dispatch("message/clearAllMessages");

	// エラーの内容に応じてstoreのメッセージを更新
	let message;
	if (status === 400) {
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
		store.dispatch("auth/logout");
		store.dispatch("message/setErrorMessage", {
			message,
		});

		// rootへ戻る
		const next = "/";
		this.$router.replace(next);
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
};
api.interceptors.response.use(
	commonResponseProcessFulfill,
	commonResponseProcessReject
);

export default api;
