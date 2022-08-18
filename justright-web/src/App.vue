<template>
  <div id="app">
    <div class="main">
      <div class="menu">
        <table>
          <tbody>
            <tr>
              <td>
                <button id="menu" @click="menuSwitch">
                  <label><img src="././assets/img/menu.png" alt="Menu" /></label>
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <label for=""> 捷利合人力資源管理顧問平台 </label>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="functionList" v-show="functionList">

        <li :class="{ active: empSetting.toggle }">
          <span @click="empActive">人事管理</span>
          <div ref="EMP" :class="{ in: empSetting.toggle }">
            <li @click="toAttendance" v-show="auth">出勤狀況管理</li>
            <li @click="toAttendanceQuery" v-show="auth">出勤狀況查詢</li>
            <li @click="toSchedule" v-show="!auth">員工排班</li>
            <li @click="toEmpManage" v-show="auth">人員管理</li>
          </div>
        </li>
        <!-- <li class="">薪資管理
            <div class="">
              <li>薪資查詢</li>
              <li class="">薪資專區</li>
            </div>
        </li> -->
        <!-- <li>出差管理
            <div class="">
              <li>出差申請</li>
              <li>出差查詢</li>
            </div>
        </li> -->
        <li :class="{ active: overtimeSetting.toggle }">
          <span @click="overtimeActive"> 加班管理</span>
          <div ref="Overtime" :class="{ in: overtimeSetting.toggle }">
            <!-- <li>加班申請</li> -->
            <li @click="toOvertimeQuery">加班時數查詢</li>
          </div>
        </li>

        <!-- <li>公告管理
            <div class="">
              <li>公告取消</li>
              <li>公告查詢</li>
              <li>公告申請</li>
            </div>
        </li> -->
        <!-- <li>請假管理
            <div class="">
              <li>請假申請</li>
              <li>請假查詢</li>
            </div>
        </li> -->
        <!-- <li>勞檢專區
            <div class="">
              <li>勞檢專區</li>
            </div>
        </li> -->
        <!-- <li>帳號登出</li> -->
      </div>
      <router-view />
      <div class="bottomText">
        <div style="">
          <p>
            公司名稱: 捷利合人力資源管理股份有限公司 |<br />
            地址: 104台北市中山區建國北路二段147號6樓之4 (604室) |<br />
            電話:(02)2562-3058 | 傳真:(02)2507-9055 | E-mail: jeilihe@justright.com
          </p>
        </div>
        <div>
          <p>© 2021 Greatest Idea Strategy Co.,Ltd All rights reserved.</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      functionList: true,
      empSetting: {
        toggle: false,
      },
      overtimeSetting: {
        toggle: false,
      },
      auth: false,
      DialogVisible: false,
    };
  },
  watch: {},
  async mounted() {},
  methods: {
    /** 登入提示 */
    loginAlert() {
      alert("請先登入再使用功能");
      this.reload();
    },
    /** 刷新頁面 */
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(() => {
        this.isRouterAlive = true;
      });
    },
    /** 選單開關 */
    menuSwitch() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          this.functionList = !this.functionList;
          if (ck.auth == "A") {
            this.auth = true;
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 人事管理開關 */
    empActive() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        this.empSetting.toggle = !this.empSetting.toggle;
        this.overtimeSetting.toggle = false;
        if (ck.auth == "A") {
          this.auth = true;
        }
        this.Admin = true;
      } else {
        this.loginAlert();
      }
    },
    /** 加班管理開關 */
    overtimeActive() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        this.overtimeSetting.toggle = !this.overtimeSetting.toggle;
        this.empSetting.toggle = false;
        if (ck.auth == "A") {
          this.auth = true;
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至出勤頁面 */
    toAttendance() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/Attendance") {
            this.$router.push("/Attendance");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至出勤查詢頁面 */
    toAttendanceQuery() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/AttendanceQuery") {
            this.$router.push("/AttendanceQuery");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至排班頁面 */
    toSchedule() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/userSchedule") {
            this.$router.push("/userSchedule");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至人員管理頁面 */
    toEmpManage() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/EmpManage") {
            this.$router.push("/EmpManage");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
    /** 移至加班查詢頁面 */
    toOvertimeQuery() {
      const ck = JSON.parse(localStorage.getItem("user"));
      if (ck != null) {
        if (ck.token != undefined) {
          if (this.$route.path != "/OvertimeQuery") {
            this.$router.push("/OvertimeQuery");
          } else {
            location.reload();
          }
        }
      } else {
        this.loginAlert();
      }
    },
  },
};
</script>

<style>
@import "assets/css/base.css";
</style>
