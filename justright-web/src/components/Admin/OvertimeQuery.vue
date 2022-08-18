<template>
  <div class="OvertimeQuery">
    <div class="top">
      <div class="left">
        <div class="leftBar"></div>
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
    <h1>加班時數查詢</h1>
    <h2><span>員工加班時數查詢</span></h2>
    <div id="contentA" class="contentBody">
      <div>

        <div class="right">
               <label for="" style="vertical-align: middle">員工編號：</label>
          <input
            type="text"
            class="textSearch"
            placeholder="請輸入員工編號"
            v-model="queryData.emp_no"
          />
          <label for="" style="vertical-align: middle;    margin-left: 10px;">所屬組別：</label>
          <div class="selectSearch">
            <select v-model="queryData.group_no">
              <option value="">請選擇</option>
              <option
                v-for="group in data_Group"
                :key="group.group_no"
                :value="group.group_no"
              >
                {{ group.group_name }}
              </option>
            </select>
          </div>
        </div>
        <div class="inputGroup dateWrapper">
          查詢日期：
          <input type="date" class="dateSearch" v-model="queryData.date_start" />至
          <input type="date" class="dateSearch" v-model="queryData.date_end" />
          <button class="btnSearch" @click="queryOvertimedata" title="搜尋">
            <span>Search</span>
          </button>
          <button
            class="btnExport"
            @click="dlQuerydata"
            v-show="Admin"
            title="匯出查詢結果"
          >
            匯出
          </button>
        </div>
      </div>
      <hr />
      <div class="result">
        <div class="resultTitle">查詢結果：</div>
        <v-client-table
          ref="attendanceTable"
          id="attendanceTable"
          v-model="data_Table"
          :columns="table_Columns"
          :options="table_Options"
        >
        </v-client-table>
        <div class="clear"></div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { ClientTable, Event } from "vue-tables-2";
import moment from "moment";
import XLSX from "xlsx";
import authService from "../../services/auth.service";
import userService from "../../services/user.services";
import userData from "../../js/userData";

const inputDatacheck = /[A-Za-z0-9]+$/;
const defdate = new Date();

Vue.use(ClientTable);

export default {
  data() {
    let vm = this;
    return {
      queryData: {
        emp_no: "",
        depno: "",
        work_position: "",
        date_start: "",
        date_end: "",
        group_no: "",
      },
      Admin: false,
      username: "",
      data_Group: [],
      data_Table: [],
      table_Columns: [
        "emp_no",
        "emp_name",
        "group_no",
        "overtime_date",
        "punch_in",
        "punch_out",
        "overtime_hours",
      ],
      table_Options: {
        headings: {
          emp_no: "員工編號",
          emp_name: "員工姓名",
          group_no: "組別",
          overtime_date: "加班日期",
          punch_in: "出勤時間",
          punch_out: "加班結束時間",
          overtime_hours: "加班時間",
        },
        texts: {
          noResults: "目前無查詢",
        },
        templates: {
          group_no: function (h, row, index) {
            let groupNo = vm.dataTransform(row.group_no, "group_no", vm.data_Group);

            return groupNo["group_name"];
          },
          punch_in: function (h, row) {
            let date_in = vm.dateTransform(row.punch_in);

            return date_in;
          },
          punch_out: function (h, row) {
            let date_out = vm.dateTransform(row.punch_out);

            return date_out;
          },
          overtime_hours: function (h, row) {
            let overTime = parseInt(row.overtime_hours);
            let ot_hours = parseInt(overTime / 60);
            let ot_min = parseInt(overTime % 60);

            return (
              <div>
                {ot_hours}小時{ot_min}分
              </div>
            );
          },
        },
        orderBy: { column: "overtime_date" },
        sortable: [],
        uniqueKey: "overtime_no",
        perPage: 9999999,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: false,
        filterable: false,
        resizableColumns: false,
        destroyEventBus: true,
      },
    };
  },
  mounted() {
    //token驗證
    this.tokenCheck();
    //權限驗證
    this.Auth();
    //取得組別資料
    this.getGroupdata();
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
    /** 權限判別 */
    Auth() {
      this.username = userData().emp_name;
      if (userData().auth == "A") {
        this.Admin = true;
      }
    },
    /** 登出 */
    async logout() {
      await authService.logout();
      this.$router.push("/");
      window.location.reload();
    },
    /** 取得組別資料 */
    async getGroupdata() {
      let tempGroupdata = await userService.getGroupdata();
      tempGroupdata = tempGroupdata["Response"]["data"];
      this.data_Group = tempGroupdata;
    },
    /** 檢查表單資料並執行查詢 */
    async queryOvertimedata() {
      let tempData = [];

      //判斷內容是否有問題
      const dataCheck = this.checkFormdata();

      if (dataCheck) {
        tempData = await userService.getWorkOvertimeQuery(
          "?emp_no=" +
            this.queryData.emp_no +
            "&dep_no=" +
            this.queryData.depno +
            "&group_no=" +
            this.queryData.group_no +
            "&work_position=" +
            this.queryData.work_position +
            "&start_date=" +
            this.queryData.date_start +
            "&end_date=" +
            this.queryData.date_end
        );
        tempData = tempData["Response"]["data"];

        if (tempData.length !== 0) {
          this.data_Table = tempData;
        } else {
          this.data_Table = [];
          this.table_Options.texts.noResults = "無查詢結果";
        }
      }
    },
    /** 確認表單內容 */
    checkFormdata() {
      const form_empNo = this.queryData.emp_no;

      if (this.queryData.date_start == "" || this.queryData.date_end == "") {
        this.queryData.date_start = moment(defdate).format("yyyy-MM-DD");
        this.queryData.date_end = moment(defdate).format("yyyy-MM-DD");
      }

      if (this.queryData.emp_no !== "") {
        if (!inputDatacheck.test(form_empNo)) {
          alert("請檢查員工編號");

          return false;
        }
      }

      return true;
    },
    /** 匯出查詢結果 */
    dlQuerydata() {
      const fileName =
        this.queryData.emp_no +
        "[" +
        this.queryData.date_start +
        "至" +
        this.queryData.date_end +
        "]加班查詢結果.xlsx";
      let wbHraed = [
        "emp_no",
        "overtime_date",
        "punch_in",
        "punch_out",
        "overtime_hours",
      ];
      let wbData = [
        {
          emp_no: "員工編號",
          overtime_date: "加班日期",
          punch_in: "加班開始時間",
          punch_out: "加班結束時間",
          overtime_hours: "加班時間",
        },
      ];
      let wb = XLSX.utils.book_new();
      let ws;

      if (this.data_Table.length != 0) {
        for (const key in this.data_Table) {
          if (Object.hasOwnProperty.call(this.data_Table, key)) {
            const data = this.data_Table[key];
            let overTime = data.overtime_hours;
            let date_in = this.dateTransform(data.punch_in);
            let date_out = this.dateTransform(data.punch_out);
            let ot_hours = parseInt(overTime / 60);
            let ot_min = parseInt(overTime % 60);

            overTime = ot_hours + "小時" + ot_min + "分";

            wbData.push({
              emp_no: data.emp_no,
              overtime_date: data.overtime_date,
              punch_in: date_in,
              punch_out: date_out,
              overtime_hours: overTime,
            });
          }
        }
        ws = XLSX.utils.json_to_sheet(wbData, { header: wbHraed, skipHeader: true });

        ws["!cols"] = [
          { wpx: 80 },
          { wpx: 80 },
          { wpx: 120 },
          { wpx: 120 },
          { wpx: 80 },
        ];

        XLSX.utils.book_append_sheet(wb, ws, "加班紀錄查詢結果");
        XLSX.writeFile(wb, fileName);
      } else {
        alert("無資料可供輸出");
      }
    },
    /** 轉換上下班時間狀態 */
    dateTransform(date) {
      if (date == "Null") {
        date = "無紀錄";
      } else {
        date = moment(date).format("MM-DD HH:mm");
      }

      return date;
    },
    /** 資料轉換 */
    dataTransform(item, attr, listData) {
      let getData = item;
      listData.forEach((data) => {
        if (item == data[attr]) {
          getData = data;
        }
      });
      return getData;
    },
  },
  destroyed() {
    localStorage.removeItem("MSG");
  },
};
</script>

<style scope>
@import "../../assets/css/overtimeQuery.css";
</style>
