<template>
  <div>
    <b-row>
      <b-col md="4">
        地域
      </b-col>
      <b-col md="8">
        <b-form-select
          v-model="selected.area"
          :options="areaList"
          class="mb-3"
          value-field="id"
          text-field="name"
        ></b-form-select>
      </b-col>
    </b-row>

    <b-row v-for="item in categoryList" :key="item.id">
      <b-col md="4">
        {{ item.name }}
      </b-col>
      <b-col md="8">
        <b-form-select
          @change="changeSubCategory(item.id, $event)"
          :value="selected.subCategory[item.id]"
          :options="item.sub_category_list"
          class="mb-3"
          value-field="id"
          text-field="name"
        ></b-form-select>
      </b-col>
    </b-row>
  </div>
</template>

<script>
export default {
  props: {
    areaId: {
      type: String,
      default: null,
    },
    areaList: {
      type: Array,
      default: null,
    },
    categoryList: {
      type: Array,
      default: null,
    },
    subCategory: {
      type: Array,
      default: null,
    },
  },
  data: () => ({
    selected: {
      area: null,
      subCategory: {},
    },
  }),
  computed: {},
  methods: {
    makeSelected() {
      // area
      // 初期 area IDを格納
      this.selected.area = this.areaId;

      // subcategory
      // this.selected.subCategory = {
      //    category: "sub_category",
      //    category2: "sub_category2",
      // }
      this.subCategory.map((e) => {
        this.selected.subCategory[e.category.id] = e.id;
      });
      console.log(this.selected);
    },
    changeSubCategory(target, event) {
      this.selected.subCategory[target] = event;
      console.log(this.selected);
    },
  },
  mounted() {
    this.makeSelected();
  },
};
</script>

<style scoped></style>
