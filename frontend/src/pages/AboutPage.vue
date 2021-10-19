<template functional>
	<div class="about">
		<b-jumbotron
			bg-variant="dark"
			text-variant="white"
			bordar-variant="dark"
			class="hero"
		>
			<template #header>
				<div class="hero-title">
					Enjoy the <span class="rs-green">R</span>andomnes<span class="rs-red"
						>S</span
					>!
				</div>
			</template>
			<template #lead>
				<div class="hero-text">
					Random Statは､2つの統計表をランダムに表示するサービスです｡
				</div>
			</template>
		</b-jumbotron>
		<br />
		<p>
			※
			このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。
		</p>
	</div>
</template>
<script>
export default {
	components: {},
};
</script>
<style strict>
.about {
	margin-bottom: 60px;
	border-top: solid 0.3rem green;
}
.hero {
	color: #fff;
	border-bottom: solid 0.3rem green;
}
.hero-title {
	font-size: 5rem;
	margin-bottom: 2rem;
}
.hero-text {
	font-size: 1.4rem;
}
.rs-green {
	color: #00a040;
}
.rs-red {
	color: #bd3f4c;
}
</style>
