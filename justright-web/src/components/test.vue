<template>
  <div class="Attendance">
    <div class="listborder">
      <input type="text" ref="keyword" class="form-control" placeholder="以姓名搜尋" />
      <button type="button" @click="search($refs.keyword.value)">搜尋</button>
      <div class="list">
        <v-client-table
          ref="attendanceTable"
          id="attendanceTable"
          v-model="data_Table"
          :columns="table_Columns"
          :options="table_Options"
        >
        </v-client-table>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { ClientTable, Event } from "vue-tables-2";
import moment from "moment";
import UserService from "../services/user.services";
import VTtest from "./VT/VTtest.vue";

let temp;
let defdate = new Date();
let selectEMP = "";
let year;
let month;
let day;
let workFlag = true;

Vue.use(ClientTable); //Client table

export default {
  components: {},
  computed: {},
  data() {
    return {
      data_Table: [],
      table_Columns: [],
      table_Options: {
        headings: {},
        texts: {
          noResults: "",
        },
        templates: {},
        childRow: function (h, row) {
          return <div class="childRow"></div>;
        },
        orderBy: { column: "" },
        sortable: [],
        uniqueKey: "",
        perPage: 9999999,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: true,
        filterable: false,
        destroyEventBus: true,
        customFilters: [
          {
            name: "filterBySide",
            callback: function (row, query) {
              return row.data.toLowerCase().includes(query.toLowerCase());
            },
          },
        ],
      },
    };
  },
  created() {},
  async mounted() {
    this.$refs.attendanceTable.setLoadingState(true);
    //接收測試
    Event.$on("vue-tables.test", function (data) {
      console.log("vue-tables.test", data);
    });
  },
  methods: {},
  //離開此頁面執行的動作
  beforeDestroy() {},
};
</script>

<style></style>

<style scoped>
@import "../assets/css/attendance.css";
</style>
