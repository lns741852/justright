<template>
  <div class="Download">
    <div class="top">
      <div class="left">
        <div class="leftBar">
          <!-- <label for="">出勤狀況管理</label> -->
        </div>
      </div>
      <div class="right">
        <div class="rightBar">
          <label>歡迎使用本系統，{{ username }}</label>
          <!-- <a href="/#/Download">表格下載</a> -->
          <!-- <a href="">最新消息</a> -->
          <button @click="logout()">帳號登出</button>
          <a href>
            <img src="../../assets/img/Logo.png" alt />
          </a>
        </div>
      </div>
    </div>
    <h1>表格下載</h1>
    <div class="Download_content">
      <div class="Download_box">
        <table class="Download_table" RULES="COLS">
          <thead>
            <th>下載項目</th>
            <th>說明</th>
            <th>下載</th>
          </thead>
          <tbody>
            <tr>
              <td>排班表格範例</td>
              <td>排班表頁面匯入用的表格格式</td>
              <td><button @click="dlShifttable()">下載</button></td>
            </tr>

            <!-- <tr>
              <td> </td>
              <td> </td>
              <td><a href=""> 連結</a></td>
            </tr>

            <tr>
              <td> </td>
              <td> </td>
              <td><a href=""> 連結</a></td>
            </tr> -->
          </tbody>
        </table>
        <div class="Download_table"></div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import XLSX from "xlsx";
import authService from "../../services/auth.service";
import userServices from "../../services/user.services";
import userData from "../../js/userData";

let defdate = new Date();

export default {
  data() {
    return {
      username: "",
    };
  },
  async mounted() {
    //token驗證
    this.tokenCheck();
    this.username = userData().emp_name;
  },
  methods: {
    /** token驗證 */
    async tokenCheck() {
      let tc = await userServices.tokenCheck();

      if (tc.Response != "Succeed") {
        alert("登入已逾期，請重新登入");
        localStorage.clear();
        this.$router.push("/");
      }
    },
    /** 登出 */
    async logout() {
      await authService.logout();
      this.$router.push("/");
      window.location.reload();
    },
    /** 下載目前畫面上班表 */
    dlShifttable() {
      const fileName = "員工排班表範例.xlsx";
      let year = moment(defdate).format("YYYY");
      let month = moment(defdate).format("MM");
      let wbHraed = ["no", "emp_no", "emp_name"];
      let wbHraedtext = {
        no: "編號",
        emp_no: "員工編號",
        emp_name: "員工姓名",
        text: "備註",
      };
      let wbData = [];
      let testData = {
        no: 1,
        emp_no: "L0000",
        emp_name: "司機姓名",
        text: "備註欄位",
      };
      let wb = XLSX.utils.book_new();
      let ws;
      let monthDaycount = this.getDaysOfMonth(year, month) + 1;

      for (let i = 1; i < monthDaycount; i++) {
        let day = i > 9 ? i : "0" + i;
        let date = year + "/" + month + "/" + day;
        wbHraed.push(date);
        wbHraedtext[date] = date;
        testData[date] = "A";
      }

      wbHraed.push("text");
      wbData.push(wbHraedtext);
      wbData.push(testData);

      ws = XLSX.utils.json_to_sheet(wbData, {
        header: wbHraed,
        skipHeader: true,
        raw: false,
        dateNF: "yyyy-mm-dd",
      });

      XLSX.utils.book_append_sheet(wb, ws, "班表範例");
      XLSX.writeFile(wb, fileName);
    },
    /** 取得該月最大天數 */
    getDaysOfMonth(year, month) {
      let date = new Date(year, month, 0);
      let days = date.getDate();
      return days;
    },
  },
  beforeDestroy() {},
};
</script>

<style>
@import "../../assets/css/download.css";
</style>
