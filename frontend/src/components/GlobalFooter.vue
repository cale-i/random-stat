<template>
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
				<b-col class="footer-left">
					<b-row class="pr-5">
						<b-col>
							<router-link to="/account/">このサイトについて</router-link>
						</b-col>
						<a href="https://github.com/cale-i/random-stat" class="text-white">
							<b-icon icon="github"></b-icon>
						</a>
					</b-row>
				</b-col>
			</b-row>
		</b-navbar>
	</footer>
</template>
<style scoped>
.footer {
	color: white;
}
.footer-left {
	display: grid;
	justify-content: end;
}
.footer-left a {
	color: white;
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
