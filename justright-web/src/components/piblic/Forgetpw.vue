<template>
  <div class="Forgetpw">
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
    <div class="forgetpwMain">
      <img src="../../assets/img/FWBG.png" class="fgbgImg" alt="" />
      <div class="fgpwForm">
        <div class="fgpwForm_box">
          <div>
            <label class="fgpwFormtitle">{{ fgpwTitle }}</label
            ><br />
            <label class="fgpwtext">{{ fgText1 }}</label
            ><br />
            <label class="fgpwtext">{{ fgText2 }}</label>
          </div>
          <div>
            <input type="text" placeholder="帳號(員工編號)" v-model="inp1" required />
          </div>
          <div>
            <input type="email" placeholder="電子信箱" v-model="inp2" required />
          </div>
          <div class="fgpwSubmit">
            <input
              type="button"
              @click="sendResetcode()"
              value="確認"
              :disabled="subBTN"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
import authService from "../../services/auth.service";

const ckEMPno = /^[a-zA-Z0-9]\w+$/;
let url = "";

export default {
  data() {
    return {
      fgpwTitle: "忘記密碼",
      fgText1: "讓我們來協助您，請新驗證您的身分",
      fgText2: "我們會將密碼重新設定的相關說明寄至您的電子信箱",
      pl1: "帳號(員工編號)",
      pl2: "電子信箱",
      inp1: "",
      inp2: "",
      subBTN: false,
    };
  },
  mounted() {
    url = window.location.href;
    url = url.replace("Forgetpw", "Resetpw/");
  },
  methods: {
    /** 根據訊息寄出重置代碼 */
    async sendResetcode() {
      if (ckEMPno.test(this.inp1)) {
        let nowTime = new Date();
        let deadLine = nowTime.getTime();
        nowTime.setTime(deadLine + 1000 * 60 * 30);
        deadLine = moment(nowTime).format("YYYY-MM-DD HH:mm:ss");
        // console.log(nowTime);
        this.subBTN = false;
        let resetMail = await authService.resetCode(this.inp1, this.inp2, deadLine, url);
        if (resetMail.status == "Succeed") {
          alert("已寄出重置密碼信件，麻煩確認信箱是否有收到");
        } else {
          alert(resetMail.status);
          this.subBTN = true;
        }
      } else {
        alert("輸入員工編號不符規則，請確認是否輸入正確");
        this.inp1 = "";
      }
    },
  },
};
</script>

<style>
@import url("../../assets/css/forgetpw.css");
</style>
