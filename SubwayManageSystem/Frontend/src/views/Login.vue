<template>
    <div id="background">
        <div id="logo">SUBWAYMANAGESYSTEM</div>
        <div id="login">
            <el-card class="box-card" >
                <el-form :model='loginForm' rules='rules' ref='loginForm'>
                    <el-input v-model="loginForm.username" placeholder="请输入账号"></el-input>
                    <el-input placeholder="请输入密码" v-model="loginForm.password" show-password></el-input>
                    <el-button type="primary">登录</el-button>
                </el-form>
            </el-card>
        </div>
        <div id="clock">
            <div id="time">{{ time }}</div>
            <div id="date">{{ date }}</div>
        </div>
        <div id="copyright">Copyright © 2023 HuyOh . all rights reserved.</div>

    </div>
</template>

<style scoped>
#background {
    position: fixed;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
    background-image: linear-gradient(90deg,
            cyan,
            purple);
    background-size: 400%;
    animation: myanimation 10s infinite;
}

@keyframes myanimation {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

#logo {
    color: aliceblue;
    font-size: 25px;
    font-weight: 800;
    text-transform: uppercase;
    position: absolute;
    top: 10%;
    left: 10%;
}

#login {
    position: absolute;
    top: 30%;
    left: 38%;
}

.box-card {
    width: 373px;
    height: 210px;
    background-color: rgba(255, 255, 255, 0.4);

    line-height: 60px;
    padding-left: 15px;
    padding-right: 15px;

    border-radius: 15px;
}

#clock {
    color: aliceblue;
    position: absolute;
    top: 80%;
    left: 10%;
    text-align: left;
}

#time {
    font-size: 60px;
}

#date {
    font-size: 35px;
}

#copyright {
    color: aliceblue;
    position: absolute;
    top: 95%;
    left: 40%;
}
</style>

<script>
export default {
    data() {
        return {
            loginForm:{
                username: '',
                password: ''
            },
            rules:{
                username:[{
                    required:true,
                    message:'用户账号必须输入',
                    trigger:'blur'
                }],
                password:[{
                    required:true,
                    message:'用户密码必须输入',
                    trigger:'blur'
                }],
            },
            time: '',
            date: '',
        }
    },
    mounted() {
        this.$nextTick(() => {
            setInterval(this.update_clock, 1000)
        })
    },
    methods: {
        update_clock: function (e) {
            var d = new Date();
            var year = d.getFullYear();
            if (year < 10) {
                year = "0" + year;
            }
            var month = d.getMonth();
            if (month < 10) {
                month = "0" + month;
            }
            var day = d.getDay();
            if (day < 10) {
                day = "0" + day;
            }
            var hour = d.getHours();
            if (hour < 10) {
                hour = "0" + hour;
            }
            var minute = d.getMinutes();
            if (minute < 10) {
                minute = "0" + minute;
            }
            this.time = hour + ":" + minute;
            this.date = year + "/" + month + "/" + day;
        }
    }
}

</script>
