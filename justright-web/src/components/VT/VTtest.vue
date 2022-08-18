<template>
  <div class="VTattendanceAction">
    <button @click.prevent="dlEMPdata">
      <img src="../../assets/img/dl.png" alt="" style="height: 2rem" />
    </button>
    <button @click.prevent="checkDetails">
      <img src="../../assets/img/setting.png" alt="" style="height: 2rem" />
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
    dlEMPdata() {
      Event.$emit("vue-tables.dlEMPdata", this.data);
    },
    checkDetails() {
      Event.$emit("vue-tables.checkDetails", this.data);
    },
    test() {
      Event.$emit("vue-tables.test", this.data);
    },
  },
};
</script>
