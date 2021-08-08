<template>
	<div class="container">
		<b-form @submit.prevent="uploadImage">
			<div>
				<img
					:src="previewSrc || imageURL"
					style="max-width: 200px;max-height: 200px;"
				/>
			</div>
			<b-form-file
				v-model="form.image"
				accept="image/png, .png"
				@input="onInputImage"
				plain
			></b-form-file>
			<b-button @click="show">表示</b-button>
			<b-button type="submit">Upload</b-button>
		</b-form>
	</div>
</template>

<script>
export default {
	props: {},
	data: () => ({
		form: {
			image: null,
		},
		previewSrc: null,
		imageURL:
			"https://www.minervastrategies.com/wp-content/uploads/2016/03/default-avatar.jpg",
	}),
	computed: {
		user: function() {
			return this.$store.state.avatar;
		},
	},
	methods: {
		onInputImage() {
			// ファイルを選択時にプレビューを表示する
			// if (this.form.image) {
			// 	const reader = new FileReader();
			// 	reader.addEventListener("load", () => {
			// 		this.previewSrc = reader.result;
			// 	});
			// 	reader.readAsDataURL(this.form.image);
			// } else {
			// 	console.log("null:", this.previewSrc);
			// this.form.image = new File([""], "");
			// }

			// ファイルを選択しなかった場合form.imageがNULLになる
			this.previewSrc = this.form.image
				? URL.createObjectURL(this.form.image)
				: null;
		},
		show() {
			// TODO: remove
			console.log(this.form.image);
		},
		uploadImage() {
			// 選択したファイルをフォームにしてアップロードする
			const formData = new FormData();
			formData.append("image", this.form.image);
			this.$store.dispatch("avatar/uploadImage", {
				formData,
			});
			// .then(() => {
			// 	console.log("success");
			// 	this.$store.dispatch("message/setInfoMessage", {
			// 		message: "アバターを変更しました｡",
			// 	});
			// 	// アバターsrcを変更
			// });
		},
	},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped></style>
