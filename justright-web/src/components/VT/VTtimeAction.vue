<template>
  <div class="VTattendanceAction">
    <button @click.prevent="editDetails" title="編輯時段資料">
      <img src="../../assets/img/setting.png" alt="" style="height: 2rem" />
    </button>
  </div>
</template>

<script>
import { Event } from "vue-tables-2";

export default {
  name: "VTtimeAction",
  props: ["data", "index", "column"],
  data() {
    return {
      Admin: false,
    };
  },
  created() {},
  mounted() {},
  methods: {
    editDetails() {
      Event.$emit("vue-tables.editDetails", this.data);
    },
  },
};
</script>
