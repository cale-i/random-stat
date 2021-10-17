<template>
	<div id="favorites">
		<div
			v-if="isFavorites"
			class="btn btn-secondary btn-sm mt-2"
			@click="deleteFavorites"
		>
			お気に入りから削除
		</div>
		<div v-else class="btn btn-success btn-sm mt-2" @click="addFavorites">
			お気に入りに追加
		</div>
	</div>
</template>
<script>
export default {
	props: {
		statsCodeID: {
			type: String,
			default: null,
		},
		areaId: {
			type: String,
			default: null,
		},
		subCategory: {
			type: Array,
			default: null,
		},
	},
	data() {
		return {
			isFavorites: false,
		};
	},
	computed: {
		params() {
			return {
				stats_code: this.statsCodeID,
				area: this.areaId,
				sub_category: this.subCategory.map((el) => el.id),
			};
		},
	},
	methods: {
		checkIsFavorites() {
			this.$store
				.dispatch("chart/checkIsFavorites", this.params)
				.then((response) => {
					this.isFavorites = response.data.is_favorites;
				});
		},
		async addFavorites() {
			await this.$store.dispatch("chart/addFavorites", this.params);
			this.$store.dispatch("message/setInfoMessage", {
				message: "お気に入りに追加しました｡",
			});
			this.checkIsFavorites();
		},
		async deleteFavorites() {
			await this.$store.dispatch("chart/deleteFavorites", this.params);
			this.$store.dispatch("message/setInfoMessage", {
				message: "お気に入から削除しました｡",
			});
			this.checkIsFavorites();
		},
	},
	watch: {
		params: {
			handler: function() {
				this.checkIsFavorites();
			},
		},
	},
};
</script>
