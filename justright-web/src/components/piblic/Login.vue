<template>
  <div class="login">
    <div class="top">
      <div class="left">
        <div class="leftBar"></div>
      </div>
      <div class="right">
        <div class="rightBar">
          <!-- <a href="/#/Download">表格下載</a>
          <a href="">最新消息</a> -->
          <a href=""> <img src="../../assets/img/Logo.png" alt="" /></a>
        </div>
      </div>
    </div>
    <div class="loginMain">
      <img src="../../assets/img/loginBG.png" class="loginImg" alt="" />
      <form class="loginForm" @submit.prevent="login()">
        <div>
          <label for="" class="loginFormtitle">捷利合人員管理系統</label>
        </div>
        <div>
          <input type="text" placeholder="帳號" v-model="user.username" required />
        </div>
        <div>
          <input type="password" placeholder="密碼" v-model="user.password" required />
        </div>
        <div>
          <div>
            <a href="/#/LoginV2" class="fp">員工入口</a>
            <span class="separate_marks">｜</span>
            <a href="/#/Forgetpw" class="fp">忘記密碼?</a>
          </div>
        </div>
        <div class="loginSubmit">
          <input type="submit" value="登入" />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import authService from "../../services/auth.service";
import userServices from "../../services/user.services";

const ckEMPno = /^[a-zA-Z0-9]\w+$/;

export default {
  data() {
    return {
      user: {
        username: "",
        password: "",
      },
    };
  },
  async mounted() {
    // 驗證既有token是否有效
    await this.tokenCheck();
  },
  methods: {
    /** 移至出勤頁面 */
    toAttendance() {
      this.$router.push("/Attendance");
    },
    /** token驗證 */
    async tokenCheck() {
      let tc = await userServices.tokenCheck();
      let user = JSON.parse(localStorage.getItem("user"));

      if (tc.Response === "Succeed") {
        if (user.auth == "A") {
          this.toAttendance();
        } else {
          alert("一般員工無法登入本系統，請洽管理部管理人員");
          localStorage.clear();
        }
      }
    },
    /** 登入 */
    async login() {
      const ck = await this.formCheck(this.user);

      if (ck.ck) {
        let loginMSG = await authService.login(this.user);
        // console.log(loginMSG);
        if (loginMSG) {
          if (loginMSG.token != undefined && loginMSG.auth == "A") {
            alert("登入成功");
            this.toAttendance();
          } else if (loginMSG.token != undefined && loginMSG.auth != "A") {
            alert("一般員工無法登入本系統，請洽管理部管理人員");
            localStorage.clear();
          } else {
            alert(loginMSG);
          }
        }
      }
    },
    /** 表單驗證 */
    async formCheck(data) {
      let check = { ck: true, msg: "" };

      if (!ckEMPno.test(data.username)) {
        check.ck = false;
        check.msg = "員工編號錯誤";

        return check;
      }

      if (data.password == null || data.password.trim().length == 0) {
        check.ck = false;
        check.msg = "請輸入密碼";

        return check;
      }

      return check;
    },
  },
  beforeDestroy() {},
};
</script>

<style scoped>
@import "../../assets/css/login.css";
</style>
