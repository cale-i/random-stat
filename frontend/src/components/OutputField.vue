<template>
    <div id="output-field">
        <b-container fluid>

            <b-button @click="reloadTable" variant="danger">reload</b-button>
            <b-table 
                sticky-header
                striped
                hover
                :items="items"
                :fields="fields"
            >
                <template #cell(edit)="row">
                    <b-button size="sm" @click="row.toggleDetails">
                        {{ row.detailsShowing ? 'CANCEL': 'EDIT'}}
                    </b-button>
                </template>
                <template #cell(delete)="row">
                    <b-button size="sm" @click="deleteItem(row.item)">
                        DELETE
                    </b-button>
                </template>
                <template #row-details="row">
                    <b-card>
                        <b-form>
                            <b-row>

                                <b-form-group id="edit-group-1" label="ID:" label-for="edit-id">
                                    <b-form-input
                                    id="edit-id"
                                    v-model="row.item.id"
                                    :disabled="true"
                                    >{{ row.item.id }}</b-form-input>
                                </b-form-group>

                                <b-form-group id="edit-group-2" label="Title:" label-for="edit-title">
                                    <b-form-input
                                    id="edit-title"
                                    v-model="row.item.title"
                                    required
                                    placeholder="Enter Title"
                                    ></b-form-input>
                                </b-form-group>

                                <b-form-group id="edit-group-3" label="Price:" label-for="edit-price">
                                    <b-form-input
                                    id="edit-price"
                                    v-model="row.item.price"
                                    required
                                    placeholder="Enter Price"
                                    ></b-form-input>
                                </b-form-group>

                                <b-form-group id="edit-group-4" label="Created at:" label-for="edit-created-at">
                                    <b-form-input
                                    id="edit-created-at"
                                    v-model="row.item.created_at"
                                    :disabled="true"
                                    >{{ row.item.created_at }}</b-form-input>
                                </b-form-group>
                        

                                <b-button @click="onSubmit(row.item)" variant="primary">Submit</b-button>
                            </b-row>
                        </b-form>
                    </b-card>
                </template>
            </b-table>
        </b-container>

   </div>
</template>

<script>
    export default {
        data() {
            return {
                items: [{
                }],
                fields: [
                    {key: 'id', label:'ID',},
                    {key: 'title', label:'Title'},
                    {key: 'price', label:'Price'},
                    {key: 'created_at', label:'date'},
                    {key: 'edit', label:'Edit'},
                    {key: 'delete', label: 'Delete'}
                ]
            }
        },
        methods: {
            reloadTable() {
                this.$store.dispatch(
                    'item/retlieve'
                )
                .then(response => {
                    this.items = response.results
                })
            },
            deleteItem(item) {
                this.$store.dispatch(
                    'item/delete',
                    {item: item}
                )
                .then(() =>{
                    this.reloadTable()
                }
                )
            },
            onSubmit(obj) {
                console.log(obj)
                this.$store.dispatch(
                    'item/put',
                    {
                        id: obj.id,
                        title: obj.title,
                        price: obj.price,
                        created_at: obj.created_at,
                    }
                )
                .then(response => {
                    console.log(response)
                })
            },
        },
        created() {
            this.reloadTable()
        }
    }
</script>

<style scoped>

</style>