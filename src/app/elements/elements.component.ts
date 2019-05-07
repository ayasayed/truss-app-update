import { Component, OnInit } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import{ImageService}from "../image.service"


@Component({
  selector: 'app-elements',
  templateUrl: './elements.component.html',
  styleUrls: ['./elements.component.scss']
})
export class ElementsComponent implements OnInit {
  members=[];
  loads=[];
  obs =new Observable;
  public flag=false;
  constructor(private http:HttpClient,private ImageService: ImageService) { }

ms:any;
ns:any;
nodeLocation:any=[];
loadvalue:any=[];
 public list_ml(n:Number,m:any[]){
  m.length=0;


  this.nodeLocation.length=0;
  this.loadvalue.length=0;
  for( let i=0;i<n;i++){
    m[i]=i;
  }
 }

 onEntern(value: string,i) {
   this.nodeLocation[i] =value;
}
onEnterl(value: string,i) {
  this.loadvalue[i] = value;

}
to_object(n:Number,arr:[]){
  let body=new Object;
  for(let i=0;i<n;i++){

   body[i]=arr[i];
  }
  return body;
}

onsubmit(){
if(this.nodeLocation.length== this.members.length&&this.loadvalue.length== this.loads.length){
  console.log("submitted");
  let body =this.to_object(this.ms,this.nodeLocation);// {0:"6,9",1:"5,9"}
  let body2 =this.to_object(this.ns,this.loadvalue);
  this.http.post("http://localhost:3000", body).subscribe(res =>console.log("done"));
  this.http.post("http://localhost:3000/api", body2).subscribe(res =>console.log("done"));
  this.flag=true;
  }else{alert("please input all missing fields");}

}


    ngOnInit() {


     this.ImageService.getListener().subscribe(loggedIn => {
      if(loggedIn==true){
          this.ms=this.ImageService.test.m;
          this.list_ml(this.ms,this.members);
          this.ns=this.ImageService.test.n;
          this.list_ml(this.ns,this.loads);
         }
      });
     }
}
//////////////////////////////////////////
