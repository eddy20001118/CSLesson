<template>
  <div class="hello">
    <el-container>
      <el-header>Pendulum Simulator</el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="grid-content" style="background-color: rgb(88,202,154)">
              <div class="grid-data">100</div>
              <div class="grid-title">Angle</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content" style="background-color: rgb(238,112,109)">
              <div class="grid-data">100</div>
              <div class="grid-title">Distance</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content" style="background-color: rgb(247,218,71)">
              <div class="grid-data">100</div>
              <div class="grid-title">Velocity</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content" style="background-color: rgb(68,126,255)">
              <div class="grid-data">100</div>
              <div class="grid-title">Acceleration</div>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="16">
            <div id="canvasContainer" class="canvas-container">
              <canvas id="canvas" :width="400" :height="300"/>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="params-container">
              <el-row type="flex" align="middle">
                <el-col :span="5">
                  <div class="label">Mass (Kg)</div>
                </el-col>
                <el-col :span="19">
                  <el-input-number
                    style="width: 100%;"
                    controls-position="right"
                    v-model="params.mass"
                    :min="0"
                    :step="0.5"
                  ></el-input-number>
                </el-col>
              </el-row>
              <el-row type="flex" align="middle">
                <el-col :span="5">
                  <div class="label">Length (m)</div>
                </el-col>
                <el-col :span="19">
                  <el-input-number
                    style="width: 100%;"
                    controls-position="right"
                    v-model="params.length"
                    :min="0"
                    :step="0.5"
                  ></el-input-number>
                </el-col>
              </el-row>
              <el-row type="flex" align="middle">
                <el-col :span="5">
                  <div class="label">
                    K
                    <sub>drag</sub>
                  </div>
                </el-col>
                <el-col :span="19">
                  <el-input-number
                    style="width: 100%;"
                    controls-position="right"
                    v-model="params.dg"
                    :min="0.1"
                    :step="0.1"
                  ></el-input-number>
                </el-col>
              </el-row>
              <el-row type="flex" align="middle">
                <el-col :span="5">
                  <div class="label">
                    θ
                    <sub>0</sub> (°)
                  </div>
                </el-col>
                <el-col :span="19">
                  <el-input-number
                    style="width: 100%;"
                    controls-position="right"
                    v-model="params.initAngle"
                    :min="-90"
                    :max="90"
                    :step="1"
                  ></el-input-number>
                </el-col>
              </el-row>
              <el-row type="flex" align="middle">
                <el-col :span="5">
                  <div class="label">Step (s)</div>
                </el-col>
                <el-col :span="19">
                  <el-input-number
                    style="width: 100%;"
                    controls-position="right"
                    v-model="params.timeStep"
                    :min="0.02"
                    :max="1"
                    :step="0.02"
                  ></el-input-number>
                </el-col>
              </el-row>
              <el-row type="flex" align="middle">
                <el-col :span="5">
                  <div class="label">Time (s)</div>
                </el-col>
                <el-col :span="19">
                  <el-input-number
                    style="width: 100%;"
                    controls-position="right"
                    v-model="params.totalTime"
                    :min="0"
                    :step="0.5"
                  ></el-input-number>
                </el-col>
              </el-row>
              <el-row type="flex" align="middle">
                <el-col :span="5">
                  <div class="label">Real Time</div>
                </el-col>
                <el-col :span="19" style="text-align: left; line-height: 40px;">
                  <el-switch
                    v-model="params.realTime"
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                  ></el-switch>
                </el-col>
              </el-row>
              <el-row style="height: 80px; margin-bottom: 0px;" type="flex" align="middle">
                <el-col :span="12">
                  <img class="button shadow" src="../res/play.png">
                </el-col>
                <el-col :span="12">
                  <img class="button shadow" src="../res/refresh.png">
                </el-col>
              </el-row>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <div class="chart-container">
              <el-tabs
                v-model="tabs.active"
                :tab-position="'left'"
                style="height: 360px; padding: 20px 0 20px 0;"
              >
                <el-tab-pane label="Angle" name="ang">
                  <ve-line :data="chartData" judge-width :colors="['#447eff']"></ve-line>
                </el-tab-pane>
                <el-tab-pane label="Distance" name="dis">配置管理</el-tab-pane>
                <el-tab-pane label="Velocity" name="vel">角色管理</el-tab-pane>
                <el-tab-pane label="Acceration" name="acc">定时任务补偿</el-tab-pane>
              </el-tabs>
            </div>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "MainPage",
  data() {
    return {
      params: {
        mass: 1,
        length: 1,
        dg: 0.1,
        initAngle: 30,
        timeStep: 0.02,
        totalTime: 10,
        realTime: false
      },
      tabs: {
        active: "ang"
      },
      chartData: {}
    };
  },
  created() {
    var that = this;
    axios
      .get("http://127.0.0.1:9000/data")
      .then(response => {
        var res = response.data.data;
        that.chartData = {
          columns: ["x", "y"],
          rows: res.angle
        };
      })
      .catch(error => {
        console.log(error);
      });
  },
  mounted() {},
  updated() {
    var canvasContainer = document.getElementById("canvasContainer");
    var height = canvasContainer.clientHeight - 60;
    var width = canvasContainer.clientWidth - 60;
    var canvas = document.getElementById("canvas");
    canvas.setAttribute("height", height);
    canvas.setAttribute("width", width);
    var ctx = canvas.getContext("2d");
    var lineLength = this.params.length * 100;
    var startX = width / 2;
    var radius = this.params.mass * 15;

    //line
    ctx.beginPath();
    ctx.lineWidth = 2;
    ctx.moveTo(startX, 0);
    ctx.lineTo(startX, lineLength);
    ctx.closePath();
    ctx.strokeStyle = "#a29376";
    ctx.stroke();

    //circle 01
    ctx.beginPath();
    ctx.arc(startX, lineLength + radius, radius, 0, Math.PI);
    ctx.fillStyle = "#828386";
    ctx.fill();
    //circle 02
    ctx.beginPath();
    ctx.arc(startX, lineLength + radius, radius, Math.PI, 0);
    ctx.fillStyle = "#939598";
    ctx.fill();
  }
};
</script>
<style scoped>
.el-main {
  min-height: 500px;
  width: 100%;
  background-color: #f2f2f2;
}

.el-header {
  display: flex;
  flex-direction: row;
  align-items: center;
  background-color: #447eff;
  font-size: 30px;
  font-weight: bold;
  color: #ffffff;
}

.el-row {
  margin-bottom: 20px;
  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}

.canvas-container {
  padding: 30px;
  height: 500px;
  background-color: #d3dce6;
  border-radius: 4px;
}

.params-container {
  padding: 30px;
  height: 500px;
  background-color: #ffffff;
  border-radius: 4px;
}

.chart-container {
  height: 400px;
  background-color: #ffffff;
  border-radius: 4px;
}

.grid-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  min-height: 100px;
}

.grid-title {
  font-size: 15px;
  color: #ffffff;
}

.grid-data {
  font-size: 36px;
  font-weight: bold;
  color: #ffffff;
}

.label {
  font-size: 14px;
  text-align: right;
  padding-right: 12px;
}

.button {
  height: 60px;
  width: 60px;
  border-radius: 50%;
  border: solid 1px #ebebeb;
  transition: 0.2s;
  padding: 15px;
  background-color: #ffffff;
}

.button:hover {
  height: 60px;
  width: 60px;
  border-radius: 50%;
  border: solid 1px #ebebeb;
  transition: 0.2s;
  padding: 15px;
  cursor: pointer;
}

.button:active {
  height: 60px;
  width: 60px;
  border-radius: 50%;
  border: solid 1px #ebebeb;
  transition: 0.2s;
  padding: 15px;
  cursor: pointer;
  background-color: #eeeeee;
}

.shadow {
  box-shadow: 0 3px 5px rgba(26, 26, 26, 0.1);
  box-sizing: border-box;
}

</style>
