import axios from "axios";
export default {
  name: "HelloWorld",
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
          rows: res.accel
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