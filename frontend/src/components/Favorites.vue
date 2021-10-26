<template>
	<div id="favorites">
		<template v-if="isFavorites">
			<div
				:id="deleteFavoritesId"
				class="btn delete-favorites-icon"
				@click="deleteFavorites"
			>
				<b-icon icon="heart-fill"></b-icon>
			</div>
			<b-popover
				:target="deleteFavoritesId"
				placement="topright"
				triggers="hover focus"
				content="お気に入りから削除"
			></b-popover>
		</template>
		<template v-else>
			<div
				:id="addFavoritesId"
				class="btn add-favorites-icon"
				@click="addFavorites"
			>
				<b-icon icon="heart-fill"></b-icon>
			</div>
			<b-popover
				:target="addFavoritesId"
				placement="topright"
				triggers="hover focus"
				content="お気に入りに追加"
			></b-popover>
		</template>
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
		idSuffix: {
			type: String,
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
		addFavoritesId() {
			return `addFavoritesBtn-${this.idSuffix}`;
		},
		deleteFavoritesId() {
			return `deleteFavoritesBtn-${this.idSuffix}`;
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
<style scoped>
.add-favorites-icon {
	color: gray;
}
.add-favorites-icon:hover {
	color: red;
}
.delete-favorites-icon {
	color: red;
}
.delete-favorites-icon:hover {
	color: gray;
}
</style>
