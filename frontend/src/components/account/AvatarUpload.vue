<template>
	<div class="container my-5">
		<b-form @submit.prevent="uploadImage">
			<div>
				<img
					v-show="avatarImage"
					:src="avatarImage"
					class="avatar-image"
					alt="アバターイメージ"
				/>
			</div>
			<b-form-file
				v-model="form.image"
				accept="image/png, image/jpeg, image/gif"
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
			<div
				v-else-if="avatar.isDefaultImage === false"
				class="position-relative"
			>
				<!-- Delete -->
				<b-button
					type="button"
					variant="danger"
					class="position-absolute"
					style="left: 0;top: 0;"
					@click="deleteImage"
				>
					Delete
				</b-button>
			</div>
			<b-button v-if="this.form.image" type="submit" variant="success"
				>Upload
			</b-button>
			<b-button v-else type="submit" disabled>
				Upload
			</b-button>
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
	}),
	computed: {
		avatar: function() {
			return this.$store.state.avatar;
		},
		avatarImage() {
			return (
				this.previewSrc || this.avatar.imageURL || this.avatar.socialImageURL
			);
		},
	},
	methods: {
		onInputImage() {
			// ファイルを選択時にプレビューを表示する
			// ファイルを選択しなかった場合form.imageがNULLになるため､
			// プレビュー画面もNULLとなる
			this.previewSrc = this.form.image
				? URL.createObjectURL(this.form.image)
				: null;
		},
		removeImage() {
			this.form.image = null;
			this.previewSrc = null;
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
					this.$store.dispatch("message/setInfoMessage", {
						message: "アバターを変更しました｡",
					});
				});
			this.removeImage();
		},
		deleteImage() {
			// 登録されたアバターをDBから削除する
			if (confirm("アバターを削除します｡") === false) return;
			this.$store.dispatch("avatar/deleteImage").then(() => {
				this.$store.dispatch("message/setInfoMessage", {
					message: "アバターを削除しました｡",
				});
			});
		},
	},
	watch: {},
	mounted() {},
	updated() {},
};
</script>
<style scoped>
.avatar-image {
	min-width: 200px;
	max-width: 200px;
	min-height: 200px;
	max-height: 200px;
	border-radius: 50%;
}
</style>
