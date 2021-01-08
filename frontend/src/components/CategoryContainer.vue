<template>
  <div>
    <b-row>
      <b-col md="3">
        地域
      </b-col>
      <b-col md="9">
        <b-form-select
          v-model="selectedArea"
          :options="areaList"
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
  },
  data: () => ({
    selectedArea: null,
  }),
  computed: {},
  methods: {},
  mounted() {
    // 初期 area IDを格納
    this.selectedArea = this.areaId;
  },
};
</script>

<style scoped></style>
