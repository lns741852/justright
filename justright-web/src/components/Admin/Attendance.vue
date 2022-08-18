<template>
  <div class="Attendance">
    <div class="top">
      <div class="left">
        <div class="leftBar">
          <button @click="inputWindowswitch()" class="btnAdd">
            自檔案匯入班表
          </button>
          <button @click="timeSwitch()" class="btnAdd">編輯時段</button>
        </div>
      </div>
      <div class="right">
        <div class="rightBar">
          <label>歡迎使用本系統，{{ username }}</label>
          <a href="/#/Download">表格下載</a>
          <!-- <a href="">最新消息</a> -->
          <button @click="logout()">帳號登出</button>
          <a href>
            <img src="../../assets/img/Logo.png" alt />
          </a>
        </div>
      </div>
    </div>
    <h1>
      <small>{{ year }}年{{ month }}月{{ day }}日</small>出勤管理
    </h1>
    <div class="attendanceMain">
      <div class="attendanceTable">
        <div class="bar">
          <div class="left">
            <input
              type="text"
              class="textSearch form-control"
              placeholder="以員編或姓名(中文)搜尋"
              v-model="searchText"
            />
          </div>
          <div class="right">
            <div class="selectSearch">
              <select v-model="selectGroup">
                <option value="none">所屬組別</option>
                <option
                  v-for="group in data_Group"
                  :key="group.group_no"
                  :value="group.group_no"
                >
                  {{ group.group_name }}
                </option>
              </select>
            </div>
            <button type="button" class="btnSearch" @click="search()">
              <span>搜尋</span>
            </button>
          </div>
        </div>
        <div class="tableBorder">
          <div class="table">
            <div class="attendanceTable_bg"></div>
            <v-client-table
              ref="attendanceTable"
              id="attendanceTable"
              v-model="data_Table"
              :columns="table_Columns"
              :options="table_Options"
            ></v-client-table>
          </div>
        </div>
      </div>
    </div>
    <transition name="inputWintran">
      <div class="inputWindow" v-show="importWindow.importDataswitch">
        <div class="inputWindow_content">
          <div>
            <div class="right">
              <div class="selectSearch">
                <select v-model="importWindow.selectImportEMP">
                  <option value="none">員工編號</option>
                  <option
                    v-for="importEMP in importWindow.importEMPlist"
                    :key="importEMP"
                    :value="importEMP"
                  >
                    {{ importEMP }}
                  </option>
                </select>
              </div>
              <label class="btnUpload" for="importData">瀏覽上傳</label>
              <button class="btn close_window_btn" @click="inputWindowswitch()">
                &times;
              </button>
            </div>
            <input
              type="file"
              id="importData"
              class="inputUpload"
              ref="files"
              multiple
              @change="importData()"
            />
          </div>
          <div class="importlistborder">
            <div class="table_bg"></div>
            <div class="table inporttable">
              <v-client-table
                ref="importData"
                id="scheduleTable"
                v-model="input_Data"
                :columns="input_Columns"
                :options="Input_Options"
              ></v-client-table>
            </div>
            <div class="submitlocation">
              <div class="submit" v-show="importWindow.submit">
                <button class="btn" @click="insertData()">
                  {{ importWindow.submitText }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
    <transition name="timeWintran">
      <div class="timeWindow" v-show="timeWindow.timeWindowswitch">
        <div class="timeWindow_content">
          <div class="title_box">
            <span>時段總覽</span>
            <button class="btn left_window_btn" @click="addTimedata()">
              新增
            </button>
            <button class="btn close_window_btn" @click="timeSwitch()">
              &times;
            </button>
          </div>
          <div class="table timetable">
            <div class="timetable_bg"></div>
            <v-client-table
              ref="timeTable"
              id="timeTable"
              v-model="time_Data"
              :columns="time_Columns"
              :options="time_Options"
            ></v-client-table>
          </div>
        </div>
      </div>
    </transition>
    <transition name="timeEditwintran">
      <div class="timeEditwindow" v-show="timeEditwindow.timeEditwindowswitch">
        <div class="timeEditwindow_content">
          <div class="title_box">
            <span>{{ timeEditwindow.title }}</span>
            <button class="btn close_window_btn" @click="editTimeswitch()">
              &times;
            </button>
          </div>
          <div>
            <form @submit.prevent="saveTimedata">
              <div class="addForm_box">
                <div class="addForm_row">
                  <div class="addForm_lable">時段代號</div>
                  <div class="addForm_input">
                    <input
                      type="text"
                      v-model="timeData.id"
                      maxlength="1"
                      onkeyup="value=value.replace(/[^a-zA-Z]/g,'')"
                      placeholder="請輸入時段代碼(單碼英文)"
                      :readonly="timeEditwindow.readonly"
                    />
                  </div>
                </div>

                <div class="addForm_row">
                  <div class="addForm_lable">出勤時間</div>
                  <div class="addForm_input">
                    <input type="time" v-model="timeData.startTime" />
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">下班時間</div>
                  <div class="addForm_input">
                    <input type="time" v-model="timeData.endTime" />
                    <div class="addForm_lable_error">
                      {{ timeDataerror.endTime }}
                    </div>
                  </div>
                </div>
                <div class="addForm_row">
                  <div class="addForm_lable">是否跨日</div>
                  <div class="addForm_input">
                    <input
                      type="checkbox"
                      id="tomorrow"
                      class="checkbox_checkbox"
                      v-model="timeData.crossDay"
                    />
                    <label for="tomorrow" class="checkbox_btn"> </label>
                  </div>
                </div>
              </div>
              <button type="submit" class="btn timeEditwindow_submit">
                儲存
              </button>
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

import userService from "../../services/user.services";
import authService from "../../services/auth.service";
import VTattendanceAction from "../VT/VTattendanceAction.vue";
import VTtimeAction from "../VT/VTtimeAction.vue";
import userData from "../../js/userData";
import schedule from "../../models/newSchedule";

let temp;
let defdate = new Date();
let selectEMP = "";
let selectTime = "";
let fileName = "";
let importData = [];
const ckDate =
  /^(?:(?:1[6-9]|[2-9][0-9])[0-9]{2}([-/.]?)(?:(?:0?[1-9]|1[0-2])\1(?:0?[1-9]|1[0-9]|2[0-8])|(?:0?[13-9]|1[0-2])\1(?:29|30)|(?:0?[13578]|1[02])\1(?:31))|(?:(?:1[6-9]|[2-9][0-9])(?:0[48]|[2468][048]|[13579][26])|(?:16|[2468][048]|[3579][26])00)([-/.]?)0?2\2(?:29))$/;
const ckEMPno = /^[a-zA-Z0-9]/;
const map_API = "AIzaSyDrLBuWokOGkLzT1loeY-2ZufP9jAVTeqc";

Vue.use(ClientTable);

export default {
  data() {
    const vm = this;
    return {
      username: "",
      year: "",
      month: "",
      day: "",
      data_Group: [],
      data_WP: [],
      selectGroup: "none",
      searchText: "",
      importWindow: {
        importDataswitch: false,
        importEMPlist: [],
        selectImportEMP: "none",
        submit: false,
        submitText: "送出",
      },
      timeWindow: {
        timeWindowswitch: false,
      },
      timeEditwindow: {
        title: "",
        readonly: true,
        timeEditwindowswitch: false,
      },
      timeData: {
        id: "",
        startTime: "",
        endTime: "",
        crossDay: 0,
      },
      data_Table: [],
      table_Columns: [
        "emp_no",
        "emp_name",
        "work_position",
        "group_no",
        "attendance",
        "latetime",
        "action",
      ],
      table_Options: {
        headings: {
          emp_no: "員工編號",
          emp_name: "姓名",
          work_position: "職位",
          group_no: "組別",
          attendance: "出勤狀態",
          latetime: "遲到狀況",
          action: "操作",
        },
        texts: {
          noResults: "無出勤狀況資料",
        },
        orderBy: { column: "attend_no" },
        sortable: [
          "attend_no",
          "emp_name",
          "group_no",
          "work_position",
          "attendance",
          "latetime",
        ],
        templates: {
          work_position: function (h, row, index) {
            let wp = row.work_position;

            wp = vm.dataTransform(wp, "wp_code", vm.data_WP);
            return wp["wp_name"];
          },
          group_no: function (h, row, index) {
            let groupNo = row.group_no;

            groupNo = vm.dataTransform(groupNo, "group_no", vm.data_Group);
            return groupNo["group_name"];
          },
          latetime: function (h, row, index) {
            let lateStuts = "無";

            if (row.latetime != 0 && row.latetime != null) {
              lateStuts = "遲到 " + row.latetime + "分";
            }

            return lateStuts;
          },
          attendance: function (h, row, index) {
            let stutsColor = "#48ddff";
            let stutsStyle;

            if (row.shift_no && !row.attend_no) {
              stutsColor = "#FF0000";
            } else if (row.out_position) {
              stutsColor = "#fff42e";
            } else if (row.in_position) {
              stutsColor = "#9be872";
            }

            stutsStyle = "border-radius:50%; background-color:" + stutsColor;

            return (
              <div class="VTattendanceStuts">
                <div style={stutsStyle} class="attendanceStutsColor"></div>
                <div>{row.attendance}</div>
              </div>
            );
          },
          action: VTattendanceAction,
        },
        childRow: function (h, row) {
          let local_Position = "";
          let mapSrc = "";
          if (row.out_in_position) {
            local_Position = row.out_position;
          } else if (row.in_position) {
            local_Position = row.in_position;
          } else {
            local_Position = "25.0618582336187, 121.53754518418633";
          }

          mapSrc =
            "https://www.google.com/maps/embed/v1/place?key=" +
            map_API +
            "&q=" +
            local_Position +
            "&language=zh-TW";

          return (
            <div class="childRow">
              <iframe
                src={mapSrc}
                width="100%"
                height="400"
                frameborder="0"
                allowfullscreen
              ></iframe>
            </div>
          );
        },
        uniqueKey: "emp_no",
        perPage: 9999999,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: true,
        filterable: false,
        resizableColumns: false,
        destroyEventBus: true,
        customFilters: [
          {
            name: "customFilter",
            callback: function (row, query) {
              if (ckEMPno.test(query)) {
                return row.emp_no.toLowerCase().includes(query.toLowerCase());
              } else {
                return row.emp_name.toLowerCase().includes(query.toLowerCase());
              }
            },
          },
          {
            name: "groupFilter",
            callback: function (row, query) {
              if (query == "none") {
                return row.group_no !== query;
              }
              return row.group_no == query;
            },
          },
        ],
      },
      input_Data: [],
      input_Columns: [
        "emp_no",
        "date",
        "punch_in",
        "punch_out",
        "hours",
        "text",
      ],
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
        perPage: 9999999,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: true,
        filterable: false,
        resizableColumns: false,
        customFilters: [
          {
            name: "empFilter",
            callback: function (row, query) {
              if (query == "none") {
                return row.emp_no !== query;
              }
              return row.emp_no == query;
            },
          },
        ],
      },
      time_Data: [],
      time_Columns: ["id", "startTime", "endTime", "crossDay", "action"],
      time_Options: {
        headings: {
          id: "時段代號",
          startTime: "出勤時間",
          endTime: "下班時間",
          crossDay: "跨日與否",
          action: "操作",
        },
        texts: {
          noResults: "無時段資料",
        },
        templates: {
          crossDay: function (h, row, index) {
            let status = row.crossDay == 1 ? "是" : "否";
            return status;
          },
          action: VTtimeAction,
        },
        orderBy: { column: "id" },
        sortable: [],
        perPage: 9999999,
        perPageValues: [],
        pagination: false,
        showChildRowToggler: true,
        filterable: false,
        resizableColumns: false,
        destroyEventBus: true,
      },
      timeDataerror: {
        endTime: "",
      },
    };
  },
  watch: {
    searchText: function () {
      this.search();
    },
    selectGroup: function () {
      this.queryGroup();
    },
    "importWindow.selectImportEMP": function () {
      this.queryEMP();
    },
    "timeData.startTime": function () {
      let ck = this.timeDatacheck();
      this.timeDataerror.endTime = ck ? "" : "請確認選擇的時間";
    },
    "timeData.endTime": function () {
      let ck = this.timeDatacheck();
      this.timeDataerror.endTime = ck ? "" : "請確認選擇的時間";
    },
    "timeData.crossDay": function () {
      let ck = this.timeDatacheck();
      this.timeDataerror.endTime = ck ? "" : "請確認選擇的時間";
    },
  },
  async mounted() {
    //token驗證
    this.tokenCheck();
    //權限確認
    this.Auth();
    let vm = this;
    this.$refs.attendanceTable.setLoadingState(true);
    //取得資料
    this.getAttendancedata();
    this.getSettingdata();
    //接收編輯事件
    Event.$on("vue-tables.checkDetails", function (data) {
      temp = vm.data_Table.find((x) => x.emp_no === data.emp_no);
      selectEMP = temp;
      vm.checkEMP(selectEMP);
    });
    //接收取消打卡事件
    Event.$on("vue-tables.dlATTdata", function (data) {
      temp = vm.data_Table.find((x) => x.emp_no === data.emp_no);
      selectEMP = temp;
      vm.deleteAttendPunch(selectEMP);
    });
    //接收時段編輯事件
    Event.$on("vue-tables.editDetails", function (data) {
      temp = vm.time_Data.find((x) => x.id === data.id);
      selectTime = temp;
      vm.editTimedata(selectTime);
    });
    //監控enter
    window.addEventListener("keyup", this.enter);
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
    /** 刷新頁面 */
    reload() {
      window.location.reload();
    },
    /** 匯入視窗開關 */
    async inputWindowswitch() {
      await this.getTimePerioddata();
      this.importWindow.importDataswitch = !this.importWindow.importDataswitch;
      this.importWindow.submit = false;
      this.importWindow.submitText = "送出";
      this.input_Data = [];
      importData = [];
      this.$refs.files.value = "";
    },
    /** 時段視窗開關 */
    async timeSwitch() {
      await this.getTimePerioddata();
      this.timeWindow.timeWindowswitch = !this.timeWindow.timeWindowswitch;
    },
    /** 時段編輯視窗開關 */
    async editTimeswitch() {
      this.timeEditwindow.timeEditwindowswitch =
        !this.timeEditwindow.timeEditwindowswitch;
    },
    /**搜尋*/
    search() {
      if (this.searchText != undefined) {
        Event.$emit("vue-tables.filter::customFilter", this.searchText);
      }
    },
    /** 群組篩選 */
    queryGroup() {
      Event.$emit("vue-tables.filter::groupFilter", this.selectGroup);
    },
    /** 匯入班表員工編號篩選 */
    queryEMP() {
      Event.$emit(
        "vue-tables.filter::empFilter",
        this.importWindow.selectImportEMP
      );
    },
    /**enter事件*/
    enter(event) {
      if (event.keyCode === 13) {
        this.search();
      }
    },
    /** 進入員工排班表 */
    checkEMP(emp) {
      this.getEMPInfo(emp.emp_no);
      if (confirm("選取員工為:" + emp.emp_name + "\n請問要確認排班資料嗎?")) {
        this.$router.push("/Schedule");
      }
    },
    /** 導入時段資料 */
    editTimedata(time) {
      this.timeEditwindow.title = "編輯時段資料";
      this.timeEditwindow.readonly = true;
      this.timeData = time;
      this.editTimeswitch();
    },
    /** 新增時段資料 */
    addTimedata() {
      this.timeEditwindow.title = "新增時段資料";
      this.timeEditwindow.readonly = false;
      this.timeData = {
        id: "",
        startTime: "",
        endTime: "",
        crossDay: 0,
      };
      this.editTimeswitch();
    },
    //取得特定使用者資料
    getEMPInfo(emp_no) {
      const tempJSON = this.data_Table;
      for (const key in tempJSON) {
        if (tempJSON.hasOwnProperty.call(tempJSON, key)) {
          const el = tempJSON[key];
          const el_emp_no = tempJSON[key].emp_no;
          if (el_emp_no === emp_no) {
            localStorage.setItem("selectEMPinfo", JSON.stringify(el));
          }
        }
      }
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
    /** 取得班表時段資料 */
    async getTimePerioddata() {
      let tempData = await userService.getTimePerioddata();
      tempData = tempData["Response"]["data"];
      this.time_Data = tempData;
    },
    /** 取得出勤資料 */
    async getAttendancedata() {
      this.year = moment(defdate).format("YYYY");
      this.month = moment(defdate).format("MM");
      this.day = moment(defdate).format("DD");

      let tempDate =
        "?year=" + this.year + "&month=" + this.month + "&day=" + this.day;

      let resData = await userService.getAttendancedata("");

      let tempData = resData["Response"]["data"];
      this.data_Table = [];

      tempData.forEach((row) => {
        console.log(row)
        let attendanceStuts = "休假";

        if (row.shift_no && !row.attend_no) {
          attendanceStuts = "未打卡";
        } else if (row.out_position) {
          attendanceStuts = "下班";
        } else if (row.in_position) {
          attendanceStuts = "出勤";
        }

        this.data_Table.push({
          emp_no: row.emp_no,
          emp_name: row.emp_name,
          work_position: row.work_position,
          group_no: row.group_no,
          attendance: attendanceStuts,
          latetime: row.latetime,
          punch_in: row.punch_in,
          in_position: row.in_position,
          punch_out: row.punch_out,
          out_position: row.out_position,
          shift_no: row.shift_no,
          attend_no: row.attend_no,
        });
      });

      this.$refs.attendanceTable.setLoadingState(false);
    },
    /** 打卡取消 */
    async deleteAttendPunch(attend_Data) {
      const delMSG = attend_Data.punch_out
        ? "請問是否要刪除下班打卡紀錄?\n"
        : attend_Data.punch_in
        ? "請問是否要刪除上班打卡紀錄?\n"
        : "";
      if (attend_Data.attend_no) {
        if (attend_Data.punch_out || attend_Data.punch_in) {
          if (confirm(delMSG + "員工姓名：" + attend_Data.emp_name)) {
            let resData = await userService.deleteAttendPunch(
              attend_Data.attend_no
            );
            if (
              resData.Response == "Update Succeed" ||
              resData.Response == "Delete Succeed"
            ) {
              alert("刪除成功!");
              this.getAttendancedata();
            } else {
              alert("刪除失敗!");
            }
          }
        }
      } else {
        if (attend_Data.shift_no == null) {
          alert("此員工本日未排班!");
        } else {
          alert("此員工尚未有打卡紀錄");
        }
      }
    },
    /** 自檔案讀取資料 */
    async importData() {
      let uploadedFiles = this.$refs.files.files;
      let file = uploadedFiles[0];
      let reader = new FileReader();

      importData = [];

      reader.onload = async (e) => {
        let data = e.target.result;
        data = new Uint8Array(data);
        let workbook = XLSX.read(data, {
          type: "array",
          cellDates: true,
        });

        fileName = workbook.SheetNames[0];
        let worksheet = workbook.Sheets[fileName];
        data = await XLSX.utils.sheet_to_json(worksheet, {
          header: 1,
        });
        this.selectFile = fileName;
        // console.log(data);
        this.formatJSONdata(data);
      };
      await reader.readAsArrayBuffer(file);
    },
    /** JSON再處理 */
    async formatJSONdata(jsonData) {
      let tempData = [];
      let dateData = [];
      let rowMaxlength = 0;

      this.importWindow.importEMPlist = [];

      for (const key in jsonData) {
        if (Object.hasOwnProperty.call(jsonData, key)) {
          const row = jsonData[key];
          let tempRowdata = [];
          let rowEmpno = "";
          let rowText = " ";

          if (key == 0) {
            rowMaxlength = row.length;
            row.forEach((el) => {
              if (typeof el == "object" || ckDate.test(el)) {
                dateData.push(moment(el).format("YYYY-MM-DD"));
              }
            });
          } else {
            rowEmpno = row[1];
            rowText =
              row[rowMaxlength - 1] != null &&
              row[rowMaxlength - 1] != undefined
                ? row[rowMaxlength - 1]
                : " ";
            if (String(rowEmpno).trim().length != 0 && rowEmpno != undefined) {
              this.importWindow.importEMPlist.push(rowEmpno);
            }
            row.forEach((code, index) => {
              if (
                code != undefined &&
                code.length == 1 &&
                index != rowMaxlength - 1
              ) {
                tempRowdata.push({ code, index });
              }
            });
            tempRowdata.forEach((rowTime) => {
              let rowDate = dateData[rowTime.index - 3];
              let rowShiftno =
                "SH" + rowEmpno + moment(rowDate).format("YYYYMMDD");
              let crossDate = rowDate;
              rowTime = this.dataTransform(rowTime.code, "id", this.time_Data);
              let rowClockin = "";
              let rowClockout = "";
              let tempDate = new Date(rowDate);
              let hoursData = "";
              if (rowTime.startTime != undefined) {
                rowClockin = rowDate + " " + rowTime.startTime;
                crossDate = tempDate.getTime();
                tempDate.setTime(crossDate + 1000 * 60 * 60 * 24);
                crossDate = moment(tempDate).format("YYYY-MM-DD");
                rowClockout =
                  rowTime.crossDay == 1
                    ? crossDate + " " + rowTime.endTime
                    : rowDate + " " + rowTime.endTime;
                hoursData = moment(rowClockout).diff(
                  moment(rowClockin),
                  "hours"
                );
                const shiftData = new schedule(
                  rowShiftno,
                  rowEmpno,
                  rowDate,
                  rowClockin,
                  rowClockout,
                  rowText
                );
                importData.push(shiftData);
                tempData.push({
                  shift_no: rowShiftno,
                  emp_no: rowEmpno,
                  date: rowDate,
                  punch_in: moment(rowClockin).format("MM-DD HH:mm"),
                  punch_out: moment(rowClockout).format("MM-DD HH:mm"),
                  hours: hoursData + "小時",
                  text: rowText,
                });
              } else {
                tempData.push({
                  shift_no: rowShiftno,
                  emp_no: rowEmpno,
                  date: rowDate,
                  punch_in: "時段代碼未定義",
                  punch_out: "時段代碼未定義",
                  hours: "",
                  text: rowText,
                });
              }
            });
          }
        }
      }

      this.input_Data = tempData;
      if (this.input_Data.length != 0) {
        this.importWindow.submit = true;
      }
    },


    /** 上傳資料 */
    async insertData() {
      let count = 0;
      let msgList = [];
      let msgText = "";
      let i = 0;
      this.importWindow.submitText = "上傳中";
      let date =""
      for(let i =0 ; i<importData.length; i+=1){
        if(date=="" || date != importData[i].date){
          importData[i].del=true
        }else{
          importData[i].del=false
        }
        let MSG = await userService.addScheduledata(JSON.stringify(importData[i]));  
        count++;
        if (MSG["code"] == 200) {
          if (MSG["msg"] !== "Succeed") {
            msgList.push({ schedule, MSG });
          }
        }
         // console.log(count == importData.length, importData.length);
        if (count == importData.length) {
          let errCount = 0;
          // console.log("msgList.length != 0 ", msgList.length != 0);
          if (msgList.length != 0) {
            msgList.forEach((err) => {
              errCount++;
              if (err.MSG.msg.indexOf("此編號已有資料") != -1) {
                msgText +=
                  "員工編號:" +
                  err.schedule.emp_no +
                  " 該員工在此日:" +
                  err.schedule.date +
                  "已有排班\n";
              } else {
                msgText +=
                  err.schedule.shift_no +
                  "此編號發生錯誤 " +
                  err.MSG.msg +
                  "\n";
              }
            });
          }
          alert("上傳完成!");
          this.getAttendancedata();
          if (errCount != 0) {
            alert("錯誤列表:\n" + msgText);
          }
          this.inputWindowswitch();
        }
      date = importData[i].date
      }
    // await  importData.forEach(async (schedule) => {
    //     let MSG = await userService.addScheduledata(JSON.stringify(schedule));      
    //     count++;
    //     if (MSG["code"] == 200) {
    //       if (MSG["msg"] !== "Succeed") {
    //         msgList.push({ schedule, MSG });
    //       }
    //     }
    //     // console.log(count == importData.length, importData.length);
    //     if (count == importData.length) {
    //       let errCount = 0;
    //       // console.log("msgList.length != 0 ", msgList.length != 0);
    //       if (msgList.length != 0) {
    //         msgList.forEach((err) => {
    //           errCount++;
    //           if (err.MSG.msg.indexOf("此編號已有資料") != -1) {
    //             msgText +=
    //               "員工編號:" +
    //               err.schedule.emp_no +
    //               " 該員工在此日:" +
    //               err.schedule.date +
    //               "已有排班\n";
    //           } else {
    //             msgText +=
    //               err.schedule.shift_no +
    //               "此編號發生錯誤 " +
    //               err.MSG.msg +
    //               "\n";
    //           }
    //         });
    //       }
    //       alert("上傳完成!");
    //       this.getAttendancedata();
    //       if (errCount != 0) {
    //         alert("錯誤列表:\n" + msgText);
    //       }
    //       this.inputWindowswitch();
    //     }

    //   });

      this.$refs.files.value = "";
    },
    /** 儲存時段資料 */
    async saveTimedata() {
      const check = this.timeDatacheck();
      if (check) {
        if (this.timeEditwindow.readonly) {
          let MSG = await userService.editTimePerioddata(this.timeData);
          if (MSG.status == "Succeed") {
            alert("修改完成");
          } else {
            alert("錯誤訊息", MSG.status);
          }
        } else {
          let MSG = await userService.addTimePerioddata(this.timeData);
          if (MSG.status == "Succeed") {
            alert("新增完成");
          } else {
            alert("錯誤訊息", MSG.status);
          }
        }
        this.getTimePerioddata();
        this.editTimeswitch();
      } else {
        alert("資料填寫有誤，請再次檢查");
      }
    },
    /** 時段資料檢查 */
    timeDatacheck() {
      let check = true;
      let start_Time = moment(
        moment(defdate).format("YYYY-MM-DD") + " " + this.timeData.startTime
      );
      let end_Time = moment(
        moment(defdate).format("YYYY-MM-DD") + " " + this.timeData.endTime
      );
      let diff_Time = end_Time.diff(start_Time, "hours");

      check =
        this.timeData.crossDay == 1 || this.timeData.crossDay == true
          ? true
          : diff_Time > 0
          ? true
          : false;

      this.timeData.crossDay =
        this.timeData.crossDay == 1 || this.timeData.crossDay == true ? 1 : 0;

      return check;
    },
    /** 計算遲到時間 */
    lateTimecount(latetime) {
      let lateStuts = "無";

      if (latetime != 0 && latetime != null) {
        lateStuts = "遲到 " + latetime + "分";
      }

      return lateStuts;
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
    window.removeEventListener("keyup", this.handleMessage);
  },
};
</script>

<style scoped>
@import "../../assets/css/attendance.css";
</style>
