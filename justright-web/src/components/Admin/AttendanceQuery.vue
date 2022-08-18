<template>
  <div class="AttendanceQuery">
    <div class="top">
      <div class="left">
        <div class="leftBar">
          <button @click="addEMPtoggle()" class="btnAdd">員工補打卡</button>
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
    <h1>出勤狀況查詢</h1>
    <h2><span>員工出勤狀況查詢</span></h2>
    <div id="contentA" class="contentBody">
      <div>
        <div class="inputGroup">
          <label for="" style="vertical-align: middle">員工編號：</label>
          <input
            type="text"
            class="textSearch"
            placeholder="請輸入員工編號"
            v-model="queryData.emp_no"
          />
          <div class="right">
            <label for="" style="vertical-align: middle">所屬組別：</label>
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
        </div>
        <div class="inputGroup dateWrapper">
          查詢日期：
          <input
            type="date"
            class="dateSearch"
            v-model="queryData.date_start"
          />至
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
            出勤狀況
          </button>
          <button
            style="margin-left:1rem"
            class="btnExport"
            @click="empReport"
          >
            員工報表
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
    <transition name="addWintran">
      <div class="addwindow" v-show="addwindow">
        <div class="addwindow_content">
          <div class="closeParent">
            <button class="btn btnClose" @click="addEMPtoggle()">X</button>
          </div>
          <div>
            <form ref="addForm" @submit.prevent="subAddAttendance">
              <h3>補打卡</h3>
              <div class="addForm_box">
                <div class="addForm_row">
                  <div class="addForm_lable">員工編號:</div>
                  <div class="addForm_input">
                    <input
                      type="text"
                      v-model="addAttendance.emp_no"
                      required
                    />
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">日期</div>
                  <div class="addForm_input">
                    <input
                      type="date"
                      class="dateSearch"
                      v-model="addAttendance.attend_date"
                    />
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">補打整天卡:</div>
                  <div class="addForm_input">
                    <input
                      id="workingnow_edit"
                      class="checkbox_checkbox"
                      type="checkbox"
                      v-model="addAttendance.time"
                    />
                    <label for="workingnow_edit" class="checkbox_btn"> </label>
                  </div>
                </div>
              </div>
              <br />
              <input type="submit" class="btn" value="確認" />
            </form>
          </div>
        </div>
      </div>
    </transition>
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
    const vm = this;
    return {
      queryData: {
        emp_no: "",
        group_no: "",
        date_start: "",
        date_end: "",
      },
      addAttendance: {
        emp_no: "",
        attend_date: moment(defdate).format("yyyy-MM-DD"),
        time:false
      },
      addwindow: false,
      Admin: false,
      username: "",
      data_Group: [],
      data_WP: [],
      data_Table: [],
      table_Columns: [
        "emp_no",
        "emp_name",
        "group_no",
        "attend_date",
        "punch_in",
        "punch_out",
        "err",
        "total_time",
      ],
      //表單中文
      table_Options: {
        headings: {
          emp_no: "員工編號",
          emp_name: "員工姓名",
          group_no: "組別",
          attend_date: "日期",
          punch_in: "出勤打卡(排班時間)",
          punch_out: "下班打卡(排班時間)",
          err: "異常",
          total_time: "時數",
        },
        texts: {
          noResults: "目前無查詢",
        },
        //處理v-model回傳值
        templates: {
          group_no: function (h, row, index) {
            let groupNo = vm.dataTransform(
              row.group_no,
              "group_no",
              vm.data_Group
            );

            return groupNo["group_name"];
          },
          date: function (h, row, index) {
            let date_dd = vm.dateTransform(row.punch_in);

            return date_dd;
          },
          err: function (h, row, index) {       
            let err_r = "";

            if (row.punch_in == null && new Date(row.s_punch_in).valueOf() < new Date()) {
              err_r += "上班未打卡,";
            } else if (row.punch_in > row.s_punch_in) {
              err_r += "遲到,";
            }

            if (row.punch_out < row.s_punch_out) {
              err_r += "提早下班,";
            } else if (
              new Date(row.s_punch_out).valueOf() + 1800000 <
              new Date(row.punch_out).valueOf()
            ) {
              err_r += "超時打卡,";
            } else if (
              row.punch_out == null &&
              new Date() > new Date(row.s_punch_out).valueOf() + 1800000
            ) {
              err_r += "下班未打卡,";
            }

            err_r = err_r.substring(0, err_r.length - 1);

            return err_r;
          },
          punch_in: function (h, row, index) {
            let date_in =
              vm.dateTransform(row.punch_in) +
              "(" +
              vm.dateTransform(row.s_punch_in) +
              ")";
            return date_in;
          },
          punch_out: function (h, row, index) {
            let date_out =
              vm.dateTransform(row.punch_out) +
              "(" +
              vm.dateTransform(row.s_punch_out) +
              ")";

            return date_out;
          },
          total_time: function (h, row, index) {
            let totalTime = vm.totalTimetransform(row.total_time);

            return totalTime;
          },
        },
        orderBy: { column: "attend_no" },
        sortable: [],
        uniqueKey: "attend_no",
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
  watch: {},
  mounted() {
    //token驗證
    this.tokenCheck();
    //權限驗證
    this.Auth();
    //取得設定資料
    this.getSettingdata();
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
    /** 補打卡視窗開關 */
    addEMPtoggle() {
      this.addwindow = !this.addwindow;
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
    /** 取得設定資料 */
    async getSettingdata() {
      let tempGroupdata = await userService.getGroupdata();
      let tempWPdata = await userService.getWPdata();
      tempGroupdata = tempGroupdata["Response"]["data"];
      tempWPdata = tempWPdata["Response"]["data"];
      this.data_Group = tempGroupdata;
      this.data_WP = tempWPdata;
    },
    /** 取得組別資料 */
    async getGroupdata() {
      let tempGroupdata = await userService.getGroupdata();
      tempGroupdata = tempGroupdata["Response"]["data"];
      this.data_Group = tempGroupdata;
    },
    /** 補打卡 */
    async subAddAttendance() {
      if (this.addAttendance.emp_no === "") {
        return;
      }
      await userService.addAttendanceData(this.addAttendance);
      setTimeout(() => {
        let MSG = JSON.parse(localStorage.getItem("MSG"));
        if (MSG["code"] == 200) {
          if (MSG["msg"] != "Succeed") {
            alert(MSG["msg"]);
          } else {
            alert("成功新增");
          }
        }
      }, 100);
      this.addAttendance= {
        emp_no: "",
        attend_date: moment(defdate).format("yyyy-MM-DD"),
        time:false
      },
      this.addEMPtoggle();
    },
    /** 檢查表單資料並執行查詢 */
    async queryOvertimedata() {
      let tempData = [];

      //判斷內容是否有問題
      const dataCheck = this.checkFormdata();

      if (dataCheck) {
        tempData = await userService.getShiftsAttendanceEmpViewQuery(
          "?emp_no=" +
            this.queryData.emp_no +
            "&group_no=" +
            this.queryData.group_no +
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
    // 員工報表
    async empReport(){
      if(this.queryData.emp_no==""){
        alert("請輸入員工編號")
        return
      }
      let req="?emp_no="+this.queryData.emp_no
      
      if(this.queryData.date_start !="" && this.queryData.date_end !=""){
        if(this.queryData.date_end <= this.queryData.date_start){
          alert("結束日期須大於開始日期")
          return
        }
        req=req+"&date_start="+this.queryData.date_start+"&date_end="+this.queryData.date_end
      }
      await userService.exportRMPdata(req);
    },

    /** 匯出查詢結果 */
    async dlQuerydata() {
      let fileName;
      let wbHraed = [
        "emp_no",
        "emp_name",
        "work_position",
        "group_no",
        "attend_date",
        "attendance",
        "punch_in",
        "in_addr",
        "in_position",
        "punch_out",
        "out_addr",
        "out_position",
        "latetime",
        "total_time",
        "err",
      ];
      let wbData = [
        {
          emp_no: "員工編號",
          emp_name: "員工姓名",
          work_position: "職位",
          group_no: "組別",
          attend_date: "出勤日期",
          attendance: "當日出勤狀態",
          punch_in: "出勤時間(排班時間)",
          in_addr: "出勤打卡位置",
          in_position: "出勤打卡位置連結",
          punch_out: "下班時間(排班時間)",
          out_addr: "下班打卡位置",
          out_position: "下班打卡位置連結",
          latetime: "遲到狀況",
          total_time: "時數",
          err: "異常",
        },
      ];
      let wb = XLSX.utils.book_new();
      let ws;

      if (this.data_Table.length != 0) {
        fileName =
          this.queryData.emp_no +
          "[" +
          this.queryData.date_start +
          "至" +
          this.queryData.date_end +
          "]出勤查詢結果.xlsx";
        for (const key in this.data_Table) {
          if (Object.hasOwnProperty.call(this.data_Table, key)) {
            const data = this.data_Table[key];
            let group_no = await this.dataTransform(
              data["group_no"],
              "group_no",
              this.data_Group
            );
            let work_position = await this.dataTransform(
              data["work_position"],
              "wp_code",
              this.data_WP
            );
            let attendanceStuts = await this.attendanceStuts(
              data["in_position"],
              data["out_position"]
            );
            let lateTime = await this.lateTimecount(data["latetime"]);
            let date_in =
              this.dateTransform(data.punch_in) +
              " (" +
              this.dateTransform(data.s_punch_in) +
              ")";
            let date_out =
              this.dateTransform(data.punch_out) +
              " (" +
              this.dateTransform(data.s_punch_out) +
              ")";
            let totalTime = this.totalTimetransform(data.total_time);
            let in_position_url =
              date_in != "無紀錄"
                ? "https://www.google.com.tw/maps/place/" + data.in_position
                : "";
            let out_position_url =
              date_out != "無紀錄"
                ? "https://www.google.com.tw/maps/place/" + data.out_position
                : "";

            let err_r = "";

            if (data.punch_in == null && new Date(data.s_punch_in).valueOf() < new Date()) {
              err_r += "上班未打卡,";
            } else if (data.punch_in > data.s_punch_in) {
              err_r += "遲到,";
            }
            if (data.punch_out < data.s_punch_out) {
              err_r += "提早下班,";
            } else if (
              new Date(data.s_punch_out).valueOf() + 1800000 <
              new Date(data.punch_out).valueOf()
            ) {
              err_r += "超時打卡,";
            } else if (
              data.punch_out == null &&
              new Date() > new Date(data.s_punch_out).valueOf() + 1800000
            ) {
              err_r += "下班未打卡,";
            }

            err_r = err_r.substring(0, err_r.length - 1);

            wbData.push({
              emp_no: data.emp_no,
              emp_name: data.emp_name,
              work_position: work_position.wp_name,
              group_no: group_no["group_name"],
              attend_date: data.attend_date,
              attendance: attendanceStuts,
              punch_in: date_in,
              in_addr: data.in_addr,
              in_position: in_position_url,
              punch_out: date_out,
              out_addr: data.out_addr,
              out_position: out_position_url,
              latetime: lateTime,
              total_time: totalTime,
              err: err_r,
            });
          }
        }
        ws = XLSX.utils.json_to_sheet(wbData, {
          header: wbHraed,
          skipHeader: true,
        });

        ws["!cols"] = [
          { wpx: 80 },
          { wpx: 80 },
          { wpx: 50 },
          { wpx: 50 },
          { wpx: 80 },
          { wpx: 120 },
          { wpx: 130 },
          { wpx: 120 },
          { wpx: 200 },
          { wpx: 120 },
          { wpx: 120 },
          { wpx: 200 },
          { wpx: 80 },
          { wpx: 50 },
          { wpx: 200 },
        ];

        for (let i = 0; i < wbData.length; i++) {
          if (wbData[i].in_position) {
            ws[
              XLSX.utils.encode_cell({
                c: 8,
                r: i,
              })
            ].l = { Target: wbData[i].in_position, Tooltip: "GoogleMap" };
          }
          if (wbData[i].out_position) {
            ws[
              XLSX.utils.encode_cell({
                c: 11,
                r: i,
              })
            ].l = { Target: wbData[i].out_position, Tooltip: "GoogleMap" };
          }
        }

        XLSX.utils.book_append_sheet(wb, ws, "出勤紀錄查詢結果");
        XLSX.writeFile(wb, fileName);
      } else {
        alert("無資料可供輸出");
      }
    },
    /** 轉換上下班時間狀態 */
    dateTransform(date) {
      if (date == null) {
        date = "無紀錄";
      } else {
        date = moment(date).format("HH:mm");
      }

      return date;
    },
    /** 轉換出勤狀態 */
    attendanceStuts(in_position, out_position) {
      let attendanceStuts = "";

      if (out_position) {
        attendanceStuts = "正常";
      } else if (in_position) {
        attendanceStuts = "下班未打卡";
      }

      return attendanceStuts;
    },
    /** 計算遲到時間 */
    lateTimecount(latetime) {
      let lateStuts = "無";

      if (latetime != 0 && latetime != null) {
        lateStuts = "遲到 " + latetime + "分";
      }

      return lateStuts;
    },
    /** 時數轉換 */
    totalTimetransform(totalTime) {
      if (totalTime != null) {
        totalTime = Math.round(totalTime / 60);
        totalTime += "小時";
      } else {
        totalTime = "無";
      }

      return totalTime;
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
@import "../../assets/css/attendanceQuery.css";
</style>
