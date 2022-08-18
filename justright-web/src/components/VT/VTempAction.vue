<template>
  <div class="VTempAction">
    <button @click.prevent="checkDetails" title="編輯員工資料">
      <img src="../../assets/img/setting_emp.png" alt="" style="height: 2rem" />
    </button>
    <!-- <button @click.prevent="exportDetails" title="月報表匯出">
      <img src="../../assets/img/listbtn.png" alt="" style="height: 2rem" />
    </button> -->
    <!-- <button @click.prevent="deleteData">
      <img src="../../assets/img/delete.png" alt="" style="height: 2rem" />
    </button> -->
  </div>
</template>

<script>
import { Event } from "vue-tables-2";

export default {
  name: "VTempAction",
  props: ["data", "index", "column"],
  data() {
    return {};
  },
  created() {},
  mounted() {},
  methods: {
    checkDetails() {
      // console.log("checkDetails");
      Event.$emit("vue-tables.checkDetails", this.data);
    },
    exportDetails() {
      // console.log("checkDetails");
      Event.$emit("vue-tables.reportDetails", this.data);
    },
    deleteData() {
      // console.log("deleteData");
      Event.$emit("vue-tables.deleteData", this.data);
    },
  },
};
</script>
