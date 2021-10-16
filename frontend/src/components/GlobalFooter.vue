<template>
	<div>
		<footer id="footer" class="footer">
			<b-navbar class="d-block" type="dark" variant="dark" fixed="bottom">
				<b-row>
					<b-col class="footer-right"> </b-col>
					<b-col class="footer-middle">
						<div class="footer-copyright">
							<b-icon
								icon="bar-chart-line"
								aria-hidden="true"
								class="mr-2"
							></b-icon>
							<span class="rs-green">R</span>andom
							<span class="rs-red">S</span>tat
						</div>
					</b-col>
					<b-col class="footer-right">
						<b-row class="pr-5">
							<b-col class="about-link">
								<template v-if="isMobile">
									<router-link to="/about">about</router-link>
								</template>
								<template v-else>
									<router-link to="/about">このサイトについて</router-link>
								</template>
							</b-col>
							<a
								href="https://github.com/cale-i/random-stat"
								class="text-white"
							>
								<b-icon icon="github"></b-icon>
							</a>
						</b-row>
					</b-col>
				</b-row>
			</b-navbar>
		</footer>
	</div>
</template>
<script>
export default {
	computed: {
		isMobile() {
			return document.body.clientWidth <= 400;
		},
	},
};
</script>
<style scoped>
.footer {
	color: white;
	margin-top: 600px;
}
.footer-right {
	display: grid;
	justify-content: end;
}
.footer-right a {
	color: white;
}

@media screen and (max-width: 640px) {
	.footer {
		font-size: 0.5rem;
	}
	.about-link {
		font-size: 0.1rem;
	}
	.footer-right a {
		font-size: 0.5rem;
	}
}
@media screen and (max-width: 340px) {
	.footer {
		font-size: 0.5rem;
	}
	.about-link {
		font-size: 0.1rem;
	}
	.footer-right a {
		font-size: 0.5rem;
	}
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
