const w = 800;
const h = 400;
const white = 255;
const metal = 180;

let upperCog, lowerCog, upperComb;
let speed = 0.2;
let toothSoften = 5;

class Cog {
  constructor(xPos,yPos, rotDir) {
    this.xCenter = xPos;
    this.yCenter = yPos;
    this.rotDir = rotDir;
    
    this.angle = 0;
    this.xBody = 0;
    this.yBody = 0;
    this.diamBody = 100;
    this.teethNum = 7
    this.wTooth = 20;
    this.hTooth = 125;
    this.toothDist = 2*PI*(this.diamBody/2) / this.teethNum;
  }
  
  drawCog(){
    push();
    translate(this.xCenter,this.yCenter);
    noStroke();
    
    // spin cog
    this.angle += speed * this.rotDir; //speed of rotation
    rotate(this.angle); 

    // update cog teeth positions
    for (let i=0; i<this.teethNum/2; i+=1){
      fill(color(metal));
      rect(this.xBody - this.wTooth/2, 
           this.yBody - this.hTooth/2, 
           this.wTooth, 
           this.hTooth,
           toothSoften
          );
      rotate(this.toothDist);
    }

    // draw cog body
    circle(this.xBody,this.yBody,this.diamBody); 
    fill(color(white));
    circle(this.xBody,this.yBody,this.diamBody/2.5); 
    
    pop();
    
  }
}

class Comb {
  constructor(xPos,yPos){
    this.xCoord = xPos;
    this.yCoord = yPos;
    
    this.step = 0;
    this.xLeft = 90;
    this.yTop = 270;
    this.wComb = 400;
    this.hComb = 40;
    
    this.teethNum = 10;
    this.wTooth = 20;
    this.hTooth = 35;
  
  }
  drawComb(){
    push();
    
    this.step += speed;
    translate(this.step, 0);
    
    noStroke();
    fill(color(metal));
    
    for (let i=0; i < this.teethNum; i+=1){
      rect(
        this.xLeft + i * (this.wComb/(this.teethNum-0.5)), 
        this.yTop - this.hTooth/2, 
        this.wTooth,
        this.hTooth,
        toothSoften
      );
    }
    
    rect(this.xLeft, this.yTop, this.wComb, this.hComb);
    
    pop();
    
  }
}

function setup() {
  angleMode(DEGREES);
  createCanvas(w, h);
  
  upperCog = new Cog(600,140,1); 
  lowerCog = new Cog(504,205,-1); 
  
  upperComb = new Comb(0,0);
}

function draw() {
  background(color(white));
  upperCog.drawCog();
  lowerCog.drawCog();
  upperComb.drawComb();
}