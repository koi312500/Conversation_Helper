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
    text("음성 입력을 기다리는 중에 있습니다...",0, 40);
    text("입력된 음성 : ",0, 20);
    text("-----------------------------------",0, 30);
    text("-----------------------------------",0, 70);
    text("-----------------------------------",0, 120);
    text("변경된 텍스트 : ",0, 110);
    text("학습할 단어 : ",400, 20);
    text("-----------------------------------",400, 30);
    text("-----------------------------------",400, 70);
    text("-----------------------------------",400, 120);
    text("단어의 뜻 : ",400, 110);
}

void draw(){
    if (myClient.active() == false){
        println("Client died.");
        myClient.stop();
        exit();
    }
    if (myClient.available() > 0) {
        String dataIn = myClient.readString();
        myClient.clear();
        background(0);
        text("입력된 음성 : ",0, 20);
        text("-----------------------------------",0, 30);
        text("-----------------------------------",0, 70);
        text("-----------------------------------",0, 120);
        text("변경된 텍스트 : ",0, 110);
        text("학습할 단어 : ",400, 20);
        text("-----------------------------------",400, 30);
        text("-----------------------------------",400, 70);
        text("-----------------------------------",400, 120);
        text("단어의 뜻 : ",400, 110);
        if(dataIn.charAt(0) == '0'){
            dataIn = dataIn.split(" ", 2)[1];
            text(dataIn, 0, 40);
            while(myClient.available() <= 0){
                delay(100);
            }  
            dataIn = myClient.readString();
            myClient.clear();
            if(dataIn.charAt(0) != '1'){
                println("Error occured. >ㅅ<");
                exit();
            }
            else
                dataIn = dataIn.split(" ", 2)[1];
            text(dataIn, 0, 130);

        }
        else if(dataIn.charAt(0) == '2'){
            dataIn = dataIn.split(" ", 2)[1];
            text(dataIn, 400, 40);
            while(myClient.available() <= 0){
                delay(100);
            }  
            dataIn = myClient.readString();
            myClient.clear();
            if(dataIn.charAt(0) != '3'){
                println("Error occured. >ㅅ<");
                exit();
            }
            else
                dataIn = dataIn.split(" ", 2)[1];
            text(dataIn, 400, 130);
        }
        else{
            println("Error occured. >ㅅ<");
            exit();
        }
    }
}