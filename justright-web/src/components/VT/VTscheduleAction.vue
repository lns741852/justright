<template>
  <div class="VTscheduleAction">
    <button @click.prevent="checkDetails" title="編輯此排班資料" v-show="Admin">
      <img src="../../assets/img/setting.png" alt="" style="height: 2rem" />
    </button>
    <button @click.prevent="deleteData" title="刪除此排班資料" v-show="Admin">
      <img src="../../assets/img/delete.png" alt="" style="height: 2rem" />
    </button>
    <label v-if="tip">不可操作</label>
  </div>
</template>

<script>
import { Event } from "vue-tables-2";
import userData from "../../js/userData";

export default {
  name: "VTscheduleAction",
  props: ["data", "index", "column"],
  data() {
    return {
      Admin: false,
      tip: false,
    };
  },
  created() {},
  mounted() {
    if (userData().auth === "A") {
      this.Admin = true;
    } else {
      this.tip = true;
    }
  },
  methods: {
    checkDetails() {
      // console.log("checkDetails");
      Event.$emit("vue-tables.checkDetails", this.data);
    },
    deleteData() {
      // console.log("deleteData");
      Event.$emit("vue-tables.deleteData", this.data);
    },
  },
};
</script>
