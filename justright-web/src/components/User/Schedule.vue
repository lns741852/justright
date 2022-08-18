<template>
  <div class="Schedule">
    <div class="top">
      <div class="left">
        <div class="leftBar" v-show="Admin">
          <button @click="dlShifttable()" class="btnAdd">匯出目前班表</button>
        </div>
      </div>
      <div class="right">
        <div class="rightBar">
          <label>歡迎使用本系統，{{ username }}</label>
          <a href="/#/Download">表格下載</a>
          <!-- <a href="">最新消息</a> -->
          <button @click="logout()">帳號登出</button>
          <a href=""> <img src="../../assets/img/Logo.png" alt="" /></a>
        </div>
      </div>
    </div>
    <h1>人員排班</h1>
    <div class="scheduleMain">
      <div class="calendar">
        <div class="user">
          <label class="name">{{ emp_Name }}</label>
          <label class="emp">員工編號:{{ emp_No }}</label>
        </div>
        <div class="colorKey">
          <img src="../../assets/img/Vacation.png" alt="" />
          <label for="">無排班</label>
        </div>
        <vc-calendar
          :attributes="calendarAttrs"
          is-expanded
          @update:from-page="dateChange"
        ></vc-calendar>
      </div>
      <div></div>

      <div class="scheduleTable">
        <div class="bar">
          <input
            type="text"
            class="textSearch form-control"
            placeholder="以日期搜尋"
            v-model="searchText"
          />
          <button type="button" class="btnSearch" @click="search()">
            <span>搜尋</span>
          </button>
        </div>
        <div class="tableBorder">
          <div class="table Schedule_notadmin">
            <v-client-table
              ref="scheduleTable"
              id="scheduleTable"
              v-model="table_Data"
              :columns="table_Columns"
              :options="table_Options"
            >
            </v-client-table>
          </div>
        </div>
      </div>
    </div>
    <transition name="editWintran">
      <div class="editWindow" v-show="editWindow">
        <div class="editWindow_content">
          <div>
            <button class="btn" @click="editWindowswitch">關閉</button>
          </div>
          <div>
            <div ref="editForm">
              <table>
                <tr>
                  <td>排班表編號:</td>
                  <td>{{ editData.shift_no }}</td>
                </tr>
                <tr>
                  <td>排班日期:</td>
                  <td>
                    <input type="date" id="editData.date" v-model="editData.date" />
                  </td>
                </tr>
                <tr>
                  <td>出勤時間:</td>
                  <td>
                    <input
                      type="datetime-local"
                      id="editData.punch_in"
                      v-model="editData.punch_in"
                    />
                  </td>
                </tr>
                <tr>
                  <td>下班時間:</td>
                  <td>
                    <input
                      type="datetime-local"
                      id="editData.punch_out"
                      v-model="editData.punch_out"
                    />
                  </td>
                </tr>
                <tr>
                  <td>備註:</td>
                  <td>
                    <textarea
                      name=""
                      id=""
                      cols="30"
                      rows="10"
                      v-model="editData.text"
                    ></textarea>
                  </td>
                </tr>
              </table>
              <input
                type="button"
                class="btn"
                value="確認"
                @click="updataScheduledata()"
              />
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import Vue from "vue";
import { ClientTable, Event } from "vue-tables-2";
import VCalendar from "v-calendar";
import moment from "moment";
import XLSX from "xlsx";

import authService from "../../services/auth.service";
import userService from "../../services/user.services";
import VTscheduleAction from "../VT/VTscheduleAction.vue";

let emp_info = "";
let fileName = "";
let defdate = new Date();
let year;
let month;
let temp;
let selectData = "";

Vue.use(ClientTable);
Vue.use(VCalendar, {
  componentPrefix: "vc",
});

export default {
  components: {},
  computed: {},
  data() {
    return {
      emp_Name: "",
      emp_No: "",
      calendarAttrs: [],
      searchText: "",
      Admin: false,
      username: "",
      table_Data: [],
      table_Columns: ["date", "punch_in", "punch_out", "hours", "action"],
      table_Options: {
        headings: {
          date: "日期",
          punch_in: "上班",
          punch_out: "下班",
          hours: "時數",
          action: "操作",
        },
        texts: {
          noResults: "無排班資料",
        },
        orderBy: { column: "date" },
        sortable: ["date", "punch_in", "punch_out", "hours"],
        templates: {
          punch_in: function (h, row, index) {
            let date_in = moment(row.punch_in).format("HH:mm");
            return date_in;
          },
          punch_out: function (h, row, index) {
            let date_out = moment(row.punch_out).format("HH:mm");
            return date_out;
          },
          hours: function (h, row, index) {
            let tempTime = "";
            let date_in = moment(row.punch_in);
            let date_out = moment(row.punch_out);

            tempTime = date_out.diff(date_in, "hours");

            return tempTime + "小時";
          },
          action: VTscheduleAction,
        },
        childRow: function (h, row) {
          return (
            <div class="childRow">
              <div class="remarktext">備註: {row.text}</div>
            </div>
          );
        },
        uniqueKey: "shift_no",
        perPage: 31,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: true,
        filterable: false,
        destroyEventBus: true,
        customFilters: [
          {
            name: "customFilter",
            callback: function (row, query) {
              // console.log(query);
              return row.date.toLowerCase().includes(query.toLowerCase());
            },
          },
        ],
      },
      selectFile: fileName,
      input_Data: [],
      input_Columns: ["emp_no", "date", "punch_in", "punch_out", "hours", "text"],
      Input_Options: {
        headings: {
          emp_no: "員工編號",
          date: "日期",
          punch_in: "上班",
          punch_out: "下班",
          hours: "時數",
          text: "備註",
        },
        texts: {
          noResults: "無排班資料",
        },
        orderBy: { column: "date" },
        sortable: ["emp_no", "date", "punch_in", "punch_out", "hours"],
        perPage: 31,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: true,
        filterable: false,
        destroyEventBus: true,
        resizableColumns: false,
      },
      windowSwitch: false,
      importDataswitch: false,
      submit: false,
      editWindow: false,
      editData: {
        shift_no: "",
        date: "",
        punch_in: "",
        punch_out: "",
        text: "",
      },
    };
  },
  created() {
    emp_info = JSON.parse(localStorage.getItem("user"));
    this.username = emp_info.emp_name;
    this.emp_Name = emp_info.emp_name;
    this.emp_No = emp_info.emp_no;
    // console.log("created ", emp_info, this.emp_Name, this.emp_No);
  },
  watch: {
    searchText: function () {
      this.search();
    },
  },
  async mounted() {
    //token驗證
    this.tokenCheck();
    let vm = this;
    this.$refs.scheduleTable.setLoadingState(true);
    //接收編輯事件
    Event.$on("vue-tables.checkDetails", function (data) {
      // console.log("vue-tables.checkDetails", data);
      temp = vm.table_Data.find((x) => x.shift_no === data.shift_no);
      selectData = temp;
      vm.setEditdata(selectData);
    });
    //接收刪除事件
    Event.$on("vue-tables.deleteData", function (data) {
      // console.log("vue-tables.deleteData", data);
      temp = vm.table_Data.find((x) => x.shift_no === data.shift_no);
      selectData = temp;
      vm.deleteScheduledata(selectData.shift_no);
    });
    //監控enter
    window.addEventListener("keyup", this.enter);
    this.$refs.scheduleTable.setLoadingState(false);
  },
  methods: {
    /** token驗證 */
    async tokenCheck() {
      let tc = await userService.tokenCheck();

      if (tc.Response != "Succeed") {
        alert("登入已逾期，請重新登入");
        localStorage.clear();
        this.$router.push("/");
      }
    },
    /** 登出 */
    async logout() {
      await authService.logout();
      this.$router.push("/LoginV2");
      window.location.reload();
    },
    /** 編輯視窗開關 */
    editWindowswitch() {
      this.editWindow = false;
      this.editData = {
        shift_no: "",
        date: "",
        punch_in: "",
        punch_out: "",
        text: "",
      };
    },
    /**搜尋*/
    search() {
      if (this.searchText != undefined) {
        Event.$emit("vue-tables.filter::customFilter", this.searchText);
      }
    },
    /**enter事件*/
    enter(event) {
      if (event.keyCode === 13) {
        this.search();
      }
    },
    /** 取得資料 */
    async getScheduledata(date) {
      // console.log("getScheduledata", date);
      year = moment(date).format("YYYY");
      month = moment(date).format("MM");

      this.table_Data = [];

      let tempData = await userService.getShiftdata(
        "?emp_no=" + this.emp_No + "&year=" + year + "&month=" + month
      );

      tempData = tempData["Response"];

      if (tempData["status"] === "Succeed") {
        let monthDaycount = this.getDaysOfMonth(year, month) + 1;
        let Daycount = [];
        let highLightdates = [];
        tempData = tempData["data"];

        this.calendarAttrs.splice(0);

        for (let i = 1; i < monthDaycount; i++) {
          Daycount.push(i);
        }

        for (const key in tempData) {
          if (Object.hasOwnProperty.call(tempData, key)) {
            const data = tempData[key];
            const dataDate = data["date"];

            this.removeItem(moment(dataDate).format("D"), Daycount);
          }
        }

        for (let i = 0; i < Daycount.length; i++) {
          highLightdates.push(new Date(year, month - 1, Daycount[i]));
        }

        this.calendarAttrs.push({
          highlight: {
            color: "orange",
            fillMode: "light",
          },
          dates: highLightdates,
          popover: {
            label: "休假日",
          },
        });
        this.table_Data = tempData;
      } else {
        this.table_Data = [];
        alert("所選月份無資料\n所選年月:" + moment(date).format("YYYY-MM"));
      }
    },
    /** 時間修改事件 */
    dateChange(date) {
      let newDate;

      date.month = date.month - 1;
      newDate = moment(date).format("YYYY-MM-DD");

      this.getScheduledata(newDate);
    },
    /** 下載目前畫面上班表 */
    dlShifttable() {
      const fileName =
        this.emp_Name + this.emp_No + " " + year + "-" + month + " 班表.xlsx";
      let wbHraed = ["emp_no", "date", "punch_in", "punch_out", "text"];
      let wbData = [
        {
          emp_no: "員工編號",
          date: "日期",
          punch_in: "上班時間",
          punch_out: "下班時間",
          text: "備註",
        },
      ];
      let wb = XLSX.utils.book_new();
      let ws;

      if (this.table_Data.length != 0) {
        for (const key in this.table_Data) {
          if (Object.hasOwnProperty.call(this.table_Data, key)) {
            const data = this.table_Data[key];
            wbData.push({
              date: data.date,
              emp_no: data.emp_no,
              punch_in: moment(data.punch_in).format("HH:mm"),
              punch_out: moment(data.punch_out).format("HH:mm"),
              text: data.text,
            });
          }
        }
        ws = XLSX.utils.json_to_sheet(wbData, { header: wbHraed, skipHeader: true });

        XLSX.utils.book_append_sheet(wb, ws, year + "-" + month + " 班表");
        XLSX.writeFile(wb, fileName);
      } else {
        alert("無資料可供輸出");
      }
    },
    /** 編輯排班資料 */
    setEditdata(data) {
      // console.log("setEditdata");
      this.editWindow = true;

      this.editData.shift_no = data.shift_no;
      this.editData.date = data.date;
      this.editData.punch_in = data.date + "T" + moment(data.punch_in).format("HH:mm:ss");
      this.editData.punch_out =
        data.date + "T" + moment(data.punch_out).format("HH:mm:ss");
      this.editData.text = data.text;
      // console.log("setEditdata ", this.editData);
    },
    /** 更新排班資料 */
    async updataScheduledata() {
      // console.log("updataScheduledata ", this.editData);
      await userService.modShiftdata(this.editData);
      setTimeout(async () => {
        let MSG = JSON.parse(localStorage.getItem("MSG"));
        // console.log("MSG ", MSG);
        if (MSG["code"] == 200) {
          if (MSG["msg"] !== "Succeed") {
            alert(MSG["msg"]);
            this.getScheduledata(defdate);
          } else {
            alert("成功修改");
            this.getScheduledata(defdate);
          }
        }
        localStorage.removeItem("MSG");
        this.editWindowswitch();
      }, 100);
    },
    /**移除排班資料 */
    async deleteScheduledata(shiftNo) {
      // console.log("deleteScheduledata ", shiftNo);
      if (confirm("請問是否要移除該排班資料")) {
        await userService.delShiftdata(shiftNo);
        setTimeout(async () => {
          let MSG = JSON.parse(localStorage.getItem("MSG"));
          // console.log("MSG ", MSG);
          if (MSG["code"] == 200) {
            if (MSG["msg"] !== "Succeed") {
              alert(MSG["msg"]);
              this.getScheduledata(defdate);
            } else {
              alert("成功移除");
              this.getScheduledata(defdate);
            }
          }
          localStorage.removeItem("MSG");
        }, 100);
      }
    },
    /** 取得該月最大天數 */
    getDaysOfMonth(year, month) {
      let date = new Date(year, month, 0);
      let days = date.getDate();
      return days;
    },
    /** 從陣列移除特定物件 */
    removeItem(item, list) {
      let index = this.itemIndex(item, list);
      // console.log("removeItem ",item,list,index);
      if (index != -1) {
        list.splice(index, 1);
      }
    },
    /** 取得特定物件在陣列的位置 */
    itemIndex(item, list) {
      let index = -1;
      for (const key in list) {
        if (Object.hasOwnProperty.call(list, key)) {
          const list_item = list[key];
          if (item == list_item) {
            index = key;
            return index;
          }
        }
      }
      return index;
    },
  },
  beforeDestroy() {
    window.removeEventListener("keyup", this.handleMessage);
    localStorage.removeItem("MSG");
  },
};
</script>

<style scoped>
@import "../../assets/css/schedule.css";
</style>
