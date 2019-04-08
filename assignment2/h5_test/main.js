let data = new Array()

//生成随机数个数
num = 10
//时间间隔 = 1000ms
t = 1000

for(let i=0;i<num;i++){
    data[data.length] = Math.floor(Math.random() * 1000)
}

index = 0

a = setInterval(()=>{
    if(index<num){
        console.log(data[index])
        index++
    }else{
        clearInterval(a)
    }
},t)