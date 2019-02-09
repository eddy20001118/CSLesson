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

<script src="./MainPage.js"></script>
<style scoped>
    @import "MainPage.css";
</style>
