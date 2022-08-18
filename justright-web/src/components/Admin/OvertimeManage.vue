<template>
  <div class="OvertimeManage">
    <div class="top">
      <div class="left">
        <div class="leftBar"></div>
      </div>
      <div class="right">
        <div class="rightBar">
          <a href="/#/Download">表格下載</a>
          <a href="">最新消息</a>
          <button @click="logout()">帳號登出</button>
          <a href=""> <img src="../../assets/img/Logo.png" alt="" /></a>
        </div>
      </div>
    </div>
    <h1>加班管理</h1>
    <div class="filterBar">
      <button>全部申請<span>25筆</span></button>
    </div>
    <div class="tableSearch">
      <div class="selectSearch">
        <select>
          <option>加班審核</option>
        </select>
      </div>
      <button class="btnSearch"><span>Search</span></button>
      <input class="textSearch" type="text" placeholder="姓名搜尋" />
    </div>
    <div class="tableWrapper">
      <table>
        <thead>
          <tr>
            <th><input type="checkbox" /></th>
            <th>姓名</th>
            <th>職位</th>
            <th>加班日期</th>
            <th>加班打卡</th>
            <th>加班結束</th>
            <th>加班時數</th>
            <th>申請狀態</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><input type="checkbox" /></td>
            <td>王大明</td>
            <td>司機</td>
            <td>2021.07.07</td>
            <td>21:00:00</td>
            <td>23:00:00</td>
            <td>2</td>
            <td><i class="pass"></i>通過</td>
            <td>
              <a href=""><span>操作</span></a>
            </td>
          </tr>
          <tr>
            <td><input type="checkbox" /></td>
            <td>王大明</td>
            <td>司機</td>
            <td>2021.07.07</td>
            <td>21:00:00</td>
            <td>23:00:00</td>
            <td>2</td>
            <td><i class="fail"></i>不通過</td>
            <td>
              <a href=""><span>操作</span></a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import { ClientTable, Event } from "vue-tables-2";
import moment from "moment";
import UserService from "../../services/user.services";
import authService from "../../services/auth.service";

let defdate = new Date();

Vue.use(ClientTable);

export default {
  name: "Overtime",
  data() {
    return {
      isActive: null,
      list: 5,
    };
  },
  mounted() {},
  methods: {
    /** 登出 */
    async logout() {
      await authService.logout();
      this.$router.push("/");
      window.location.reload()
    },
    clickFunc(index) {
      this.isActive = index;
    },
  },
  destroyed() {},
};
</script>
<style>
@import "../../assets/css/overtimeManage.css";
</style>
