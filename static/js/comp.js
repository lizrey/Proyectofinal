var candado=document.getElementById("AbrirC"),
Shora=document.getElementById("HORAI"),
Fhora=document.getElementById("HORAF"),
imagenInd=document.getElementById("led"),
imagenAla=document.getElementById("Alarma"),
imagenCan=document.getElementById("candado");

var activar=0,Mensaje,Datos,CntAc=0,abrir=0,cerrar=0,desactivar=0;

///////conexion al servidor////
client = new Paho.MQTT.Client("maqiatto.com", 8883, "web_" + parseInt(Math.random() * 100, 10));

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;
var options = {
  useSSL: false,
  userName: "licha_05reyes@outlook.com",
  password: "Galapagos1001",
  onSuccess:onConnect,
  onFailure:doFail
}
// connect the client
client.connect(options);
   
// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("Conectado...");
  client.subscribe("licha_05reyes@outlook.com/IoT");
  enviarInfo("00:00/00:00/0/0/0/0")
  
}

function doFail(e){
  console.log(e);
 
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}

// called when a message arrives
function onMessageArrived(message) {
  Mensaje=message.payloadString;
  console.log(Mensaje);
  Datos=Mensaje.split("/");

  if(CntAc==0 || Datos[0]=="0"){
    ActuHoras();
  }
  if(Datos[3]=="1"){
    location.reload();
  }
  if(Datos[0]=="2"){
    AcAlarm();
  }
  if(Datos[0]=="3"){
    DsAlarm();
  }
}

/////////////////////////////
function ActuHoras(){
  Shora.value=Datos[1];
  Fhora.value=Datos[2];
  MensajeA=Datos[1]+"/"+Datos[2];
  enviarInfo(MensajeA);
  CntAc=1;
}

function Aceptar(){
  MensajeA=Shora.value+"/"+Fhora.value+"/"+String(activar)+"/"+String(desactivar)+"/"+String(abrir)+"/"+String(cerrar);
  enviarInfo(MensajeA);
  location.reload();
}


function AcAlarm(){
  imagenInd.src="/static/images/led.gif";
  activar=1;
  desactivar=0;
  abrir=0
  cerrar=0
  imagenCan.src="/static/images/close.png"
  candado.innerText='Abrir';
  MensajeA=Shora.value+"/"+Fhora.value+"/"+String(activar)+"/"+String(desactivar)+"/"+String(abrir)+"/"+String(cerrar);
  console.log(MensajeA);
  enviarInfo(MensajeA);
  enviarInfo(Shora.value+"/"+Fhora.value+"/"+"0/0/0/0")
}

function DsAlarm(){
  imagenInd.src="/static/images/off.png";
  imagenCan.src="/static/images/Open.png"
  activar=0;
  desactivar=1
  abrir=0
  cerrar=0
  imagenAla.src="/static/images/alarma.png";
  candado.innerText='Cerrar';
  MensajeA=Shora.value+"/"+Fhora.value+"/"+String(activar)+"/"+String(desactivar)+"/"+String(abrir)+"/"+String(cerrar);
  enviarInfo(MensajeA);
  enviarInfo(Shora.value+"/"+Fhora.value+"/"+"0/0/0/0")
  console.log(MensajeA);
}


function AcCerradura(){
   if(candado.innerText=='Cerrar'){
      candado.innerText='Abrir';
      abrir=0
      cerrar=1
      imagenCan.src="/static/images/close.png"
      if(activar==1){
         imagenAla.src="/static/images/alarma.png";
      }
      MensajeA=Shora.value+"/"+Fhora.value+"/"+String(activar)+"/"+String(desactivar)+"/"+String(abrir)+"/"+String(cerrar);
      enviarInfo(MensajeA);
      enviarInfo(Shora.value+"/"+Fhora.value+"/"+"0/0/0/0")
      console.log(MensajeA);
      
	}else
	{
      
    candado.innerText='Cerrar';
      abrir=1
      cerrar=0
      imagenCan.src="/static/images/open.png";
      imagenAla.src="/static/images/alarma.png";
      if(activar==1){
         imagenAla.src="/static/images/alaAc.gif";
      }
      MensajeA=Shora.value+"/"+Fhora.value+"/"+String(activar)+"/"+String(desactivar)+"/"+String(abrir)+"/"+String(cerrar);
      enviarInfo(MensajeA);
      enviarInfo(Shora.value+"/"+Fhora.value+"/"+"0/0/0/0")
      console.log(MensajeA);
	}
}

function enviarInfo(Men){
  message = new Paho.MQTT.Message(Men);
    message.destinationName = "licha_05reyes@outlook.com/IoT1";
    client.send(message);
}

function ObtenerHora(){
    Tiempo=new Date();
    Hora=Tiempo.getHours()+":"+Tiempo.getMinutes()+":"+Tiempo.getSeconds();
    Hora1=Shora.value+":0"
    Hora2=Fhora.value+":0"
    if(Hora==Hora1){
      AcAlarm();
    }
    if(Hora==Hora2){
      DsAlarm();
    }
}

window.onload=function(){
  setInterval(ObtenerHora, 1000);
}
