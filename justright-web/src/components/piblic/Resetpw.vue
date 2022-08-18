<template>
  <div class="Resetpw">
    <div class="top">
      <div class="left">
        <div class="leftBar"></div>
      </div>
      <div class="right">
        <div class="rightBar">
          <!-- <a href="/#/Download">表格下載</a>
          <a href="">最新消息</a> -->
          <!-- <button>帳號登出</button> -->
          <a href=""> <img src="../../assets/img/Logo.png" alt="" /></a>
        </div>
      </div>
    </div>
    <div class="resetpwMain">
      <img src="../../assets/img/FWBG.png" class="rsbgImg" alt="" />
      <div class="rspwForm">
        <div>
          <label class="rspwFormtitle">重置密碼</label><br />
          <label class="rspwtext">請在下方的輸入框輸入新的密碼</label><br />
          <!-- <label class="rspwtext">{{}}</label> -->
        </div>
        <div>
          <input
            type="text"
            placeholder="帳號(員工編號)"
            v-model="data.emp_no"
            disabled
          />
        </div>
        <div>
          <input type="password" placeholder="新密碼" v-model="data.password" required />
        </div>
        <div>
          <input type="password" placeholder="確認密碼" v-model="repw" required />
        </div>
        <div class="rspwSubmit">
          <input type="button" @click="resetPW()" value="確認" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from "../../services/auth.service";

let restToken;

export default {
  name: "Resetpw",
  data() {
    return {
      data: {
        emp_no: "",
        password: "",
        token: "",
      },
      repw: "",
    };
  },
  async mounted() {
    //取得token
    restToken = this.$route.params.token;
    //驗證token
    if (restToken !== null && restToken != undefined) {
      await this.checkToken();
    } else {
      this.toLogin();
    }
  },
  methods: {
    /** 返回首頁 */
    toLogin() {
      this.$router.push("/");
    },
    /** 驗證Token */
    async checkToken() {
      let check = await authService.checkResttoken(restToken);
      // console.log(check);
      if (check.Response.status === "Succeed") {
        this.data.emp_no = check.Response.emp_no;
        this.data.token = restToken;
      } else {
        alert(check.Response.msg);
        this.toLogin();
      }
    },
    /** 重設密碼 */
    async resetPW() {
      let check = await this.formCheck(this.data);

      if (check.ck) {
        let resetPW = await authService.resetPW(this.data);
        if (resetPW.status === "Succeed") {
          alert("修改密碼成功，請回到首頁登入");
          this.toLogin();
        } else {
          alert("修改密碼失敗");
        }
      } else {
        alert(check.msg);
      }
    },
    /** 表單檢查 */
    async formCheck(data) {
      let check = { ck: true, msg: "" };

      if (data.password == null || data.password.trim().length == 0) {
        check.ck = false;
        check.msg = "未輸入密碼或有效的密碼，請重新輸入";

        return check;
      }

      if (data.password !== this.repw) {
        check.ck = false;
        check.msg = "密碼確認輸入的密碼與密碼不符，請確認";

        return check;
      }

      return check;
    },
  },
  beforeDestroy() {},
};
</script>

<style>
@import url("../../assets/css/resetPW.css");
</style>
