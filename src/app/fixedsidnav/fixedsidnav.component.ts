import { Component, OnInit } from '@angular/core';
import{ImageService}from "../image.service";
import { Observable ,Subscriber} from 'rxjs';
@Component({
  selector: 'app-fixedsidnav',
  templateUrl: './fixedsidnav.component.html',
  styleUrls: ['./fixedsidnav.component.scss']
})
export class FixedsidnavComponent implements OnInit {

  is_done1:boolean=false;


  constructor(private ImageService: ImageService) { }



  ngOnInit() {

    this.ImageService.getListener2().subscribe(loggedIn => {
        this.is_done1=loggedIn;
         }
      );
     }
}
