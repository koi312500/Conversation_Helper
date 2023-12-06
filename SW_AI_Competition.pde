import processing.net.*; 

Client myClient;
PFont mainFont;

void setup() { 
    size(1600, 200); 
    myClient = new Client(this, "127.0.0.1", 15625);
    myClient.write("Client Hello");
    mainFont = createFont("D2Coding", 16);
    textFont(mainFont);
    background(0);
    text("입력된 음성 : ",0, 20);
    text("음성 입력을 기다리는 중에 있습니다...",0, 40);
    text("-----------------------------------",0, 30);
    text("-----------------------------------",0, 60);
    text("변경된 텍스트 : ",0, 70);
}

void draw(){
    if (myClient.active() == false){
        println("Client died.");
        myClient.stop();
        exit();
    }
    if (myClient.available() > 0) {
        String dataIn = myClient.readString();
        myClient.write("Data Sent detected."); // send whatever you need to send here
        background(0);
        if(dataIn.charAt(0) != '0'){
            println("Error occured. >ㅅ<");
            exit();
        }
        else
            dataIn = dataIn.split(" ")[1];
        
        text(dataIn, 0, 40);
        text("입력된 음성 : ",0, 20);
        text("-----------------------------------",0, 30);
        text("-----------------------------------",0, 90);
        text("변경된 텍스트 : ",0, 100);
        while(myClient.available() <= 0){
            delay(100);
        }  
        dataIn = myClient.readString();
        if(dataIn.charAt(0) != '1'){
            println("Error occured. >ㅅ<");
            exit();
        }
        else
            dataIn = dataIn.split(" ")[1];
        text(dataIn, 0, 110);
    }
}