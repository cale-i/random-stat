<template>
  <div>
    <b-row>
      <b-col md="4">
        地域
      </b-col>
      <b-col md="8">
        <b-form-select
          v-model="selectedArea"
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
          :value="selectedSubCategory[item.id]"
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
    show: false,
    selectedArea: null,
    selectedSubCategory: {},
  }),
  computed: {},
  methods: {
    makeSelectedSubCategory() {
      this.subCategory.map((e) => {
        this.selectedSubCategory[e.category.id] = e.id;
      });
    },
    changeSubCategory(target, event) {
      this.selectedSubCategory[target] = event;
    },
  },
  mounted() {
    // 初期 area IDを格納
    this.selectedArea = this.areaId;
    this.makeSelectedSubCategory();
  },
};
</script>

<style scoped></style>
