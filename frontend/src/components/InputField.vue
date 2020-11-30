<template>
    <div id="input-field">

        <b-container>
            <b-form @submit="onSubmit" @reset="onReset" v-if="show">
                <b-row>

                    <b-form-group id="input-group-1" label="ID:" label-for="input-id">
                        <b-form-input
                        id="input-id"
                        v-model="form.id"
                        :disabled="true"
                        >{{ form.id }}</b-form-input>
                    </b-form-group>

                    <b-form-group id="input-group-2" label="Title:" label-for="input-title">
                        <b-form-input
                        id="input-title"
                        v-model="form.title"
                        required
                        placeholder="Enter Title"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="input-group-3" label="Price:" label-for="input-price">
                        <b-form-input
                        id="input-price"
                        v-model="form.price"
                        required
                        placeholder="Enter Price"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="input-group-4" label="Created at:" label-for="input-created-at">
                        <b-form-input
                        id="input-created-at"
                        v-model="form.created_at"
                        :disabled="true"
                        >{{ form.created_at }}</b-form-input>
                    </b-form-group>



                    <b-button type="submit" variant="primary">Submit</b-button>
                    <b-button type="reset" variant="danger">Reset</b-button>
                </b-row>
            </b-form>
        </b-container>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                form: {
                    id: '',
                    title: '',
                    price: '',
                    created_at: ''
                },
                show: true
            }
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()
                // alert(JSON.stringify(this.form))
                this.$store.dispatch(
                    'item/create',
                    {
                        title: this.form.title,
                        price: this.form.price
                    }
                )
                .then(response => {
                    this.form.id = response.id
                    this.form.created_at = response.created_at
                })
            },
            onReset(evt) {
                evt.preventDefault()
                // Reset our form values
                this.form.id = ''
                this.form.title = ''
                this.form.price = ''
                this.form.created_at = ''
                // Trick to reset/clear native browser form validation state
                this.show = false
                this.$nextTick(() => {
                this.show = true
                })
            }
        },
        computed: {

        }

    }
</script>

<style scoped>


</style>