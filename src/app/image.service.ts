import { HttpClient} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable,Subject } from 'rxjs';
import { TestBed } from '@angular/core/testing';
@Injectable({
  providedIn: 'root'
})
export class ImageService {
 public test:any;
 public  is_done= new Subject<boolean>();
 private Listener = new Subject<boolean>();
  constructor(private http: HttpClient) {}


  public uploadImage(image: File): Observable<any> {
    const formData = new FormData();

    formData.append('image', image);

    return this.http.post('http://localhost:3000/api/upload', formData);

  }
public  reqcom() {
fetch('http://localhost:3000/api/upload')
.then(response => response.json())
.then(data => {console.log(this.test=data);
console.log(this.test.m,this.test.n);
 this.Listener.next(true);
 console.log(this.Listener);
} );
}

public  reqdone() {
  fetch('http://localhost:3000/api/upload2')
  .then(response => response.json())
  .then(data => {

    console.log(data.d)
   this.is_done.next(true);

    });
  }

getListener(): Observable<boolean> {
  return this.Listener.asObservable();
}
getListener2(): Observable<boolean> {
  return this.is_done.asObservable();
}
}
