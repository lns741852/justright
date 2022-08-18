import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const router = new Router({
  // mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Default',
      component: () => import('../components/piblic/Login.vue')
    },
    {
      path: '/LoginV2',
      name: 'LoginV2',
      component: () => import('../components/piblic/LoginV2.vue')
    },
    {
      path: '/Login',
      name: 'Login',
      component: () => import('../components/piblic/Login.vue')
    },
    {
      path: '/Forgetpw',
      name: 'Forgetpw',
      component: () => import('../components/piblic/Forgetpw.vue')
    },
    {
      path: '/Resetpw/:token',
      name: 'Resetpw',
      component: () => import('../components/piblic/Resetpw.vue')
    },
    {
      path: '/Download',
      name: 'Download',
      component: () => import('../components/User/Download.vue')
    },
    {
      path: '/Attendance',
      name: 'Attendance',
      component: () => import('../components/Admin/Attendance.vue')
    },
    {
      path: '/AttendanceQuery',
      name: 'AttendanceQuery',
      component: () => import('../components/Admin/AttendanceQuery.vue')
    },
    {
      path: '/Schedule',
      name: 'Schedule',
      component: () => import('../components/Admin/Schedule.vue')
    },
    {
      path: '/userSchedule',
      name: 'userSchedule',
      component: () => import('../components/User/Schedule.vue')
    },
    {
      path: '/OvertimeQuery',
      name: 'OvertimeQuery',
      component: () => import('../components/Admin/OvertimeQuery.vue')
    },
    {
      path: '/EmpManage',
      name: 'EmpManage',
      component: () => import('../components/Admin/EmpManage.vue')
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('../components/test.vue')
    },
  ]
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/Attendance', '/Schedule', '/OvertimeQuery', '/EmpManage', '/Download'];
  const authRequired = publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  // trying to access a restricted page + not logged in
  // redirect to login page
  if (authRequired && !loggedIn) {
    next('/Login');
  } else {
    next();
  }
});

export default router
