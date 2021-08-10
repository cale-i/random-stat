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
				class="mb-3"
				plain
			></b-form-file>
			<div v-if="previewSrc" class="position-relative">
				<!-- Cancel -->
				<b-button
					type="button"
					variant="warning"
					class="position-absolute"
					style="left: 0;top: 0;"
					@click="removeImage"
				>
					Cancel
				</b-button>
			</div>
			<b-button type="submit" variant="success">Upload</b-button>
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
		removeImage() {
			this.form.image = null;
			this.previewSrc = null;
		},
		show() {
			// TODO: remove
			console.log(this.form.image);
		},
		uploadImage() {
			// 選択したファイルをフォームにしてアップロードする
			const formData = new FormData();
			formData.append("image", this.form.image);

			this.$store
				.dispatch("avatar/uploadImage", {
					formData,
				})

				.then(() => {
					console.log("success");
					this.$store.dispatch("message/setInfoMessage", {
						message: "アバターを変更しました｡",
					});
					// アバターsrcを変更
				});
		},
	},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped></style>
