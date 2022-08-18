<template>
  <div class="VTattendanceAction">
    <button @click.prevent="dlATTdata" title="取消打卡紀錄">
      <img src="../../assets/img/delete.png" alt="" style="height: 2rem" />
    </button>
    <button @click.prevent="checkDetails" title="檢視班表">
      <img src="../../assets/img/listbtn.png" alt="" style="height: 2rem" />
    </button>
  </div>
</template>

<script>
import { Event } from "vue-tables-2";

export default {
  name: "VTattendanceAction",
  props: ["data", "index", "column"],
  data() {
    return {};
  },
  created() {},
  mounted() {},
  methods: {
    dlATTdata() {
      Event.$emit("vue-tables.dlATTdata", this.data);
    },
    checkDetails() {
      Event.$emit("vue-tables.checkDetails", this.data);
    },
    /* test() {
      Event.$emit("vue-tables.test", this.data);
    }, */
  },
};
</script>
