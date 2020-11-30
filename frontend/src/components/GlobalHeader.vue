<template>
    <div id="header">
        <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
            <b-navbar-brand href="https://random-stat.work">Random Stat</b-navbar-brand>
            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        
            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav lass="ml-auto">
                    <b-nav-item to="/" active-class="active" exact>Home</b-nav-item>
                    <!-- <b-nav-item to="/login" active-class="active" >ログイン</b-nav-item> -->
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
    export default {
    }
</script>

<style scoped>
    #header {
        margin-bottom: 60px;
    }
</style>